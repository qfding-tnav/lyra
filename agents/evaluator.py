import json
import os
import re
import sys
from pathlib import Path

from github import Github, Auth

ROOT_DIR = str(Path(__file__).resolve().parents[1])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agents.constants import agent_constants, label_constants, section_constants
from agents.tools.open_ai_client import OpenAiClient
from agents.tools.utils import github_utils, skill_utils


class Evaluator:
    ROLE = "evaluator"

    def __init__(self):
        # 1. Load Environment Variables
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_token_pat = os.getenv("GITHUB_TOKEN_PAT")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.repo_name = os.getenv("REPO_NAME")
        self.issue_number = os.getenv("ISSUE_NUMBER")

        if not all([self.github_token_pat, self.llm_api_key, self.repo_name, self.issue_number]):
            print("Error: Missing required environment variables.")
            sys.exit(1)
        # Use PAT so the label change can trigger the downstream Generator workflow on reject
        auth = Auth.Token(self.github_token_pat)
        self.gh = Github(auth=auth)
        self.repo = self.gh.get_repo(self.repo_name)
        self.issue = self.repo.get_issue(number=int(self.issue_number))
        self.llm_client = OpenAiClient(self.llm_api_key)

    def execute(self):
        print(f"Starting Evaluator Agent for Issue #{self.issue_number}")
        approved_plan = github_utils.get_approved_plan(self.issue)
        generator_summary = github_utils.get_latest_generator_summary(self.issue)
        test_runner_result = github_utils.get_latest_test_runner_result(self.issue)

        role_instructions = skill_utils.load_agent_role_skill(self.ROLE)
        if not role_instructions:
            print("No role instructions found. Exiting.")
            return
        # Load Available Skills
        skills_context = skill_utils.load_skills(["constraints/artifacts.md"])
        if skills_context:
            skills_context = f"### AVAILABLE FRAMEWORK SKILLS\n\n{skills_context}\n\n"

        system_prompt = f"""{role_instructions}\n\n{skills_context}\n\n"""
        user_prompt = f"""
### ORIGINAL PLAN (What the code SHOULD do)
{approved_plan}

### GENERATOR'S IMPLEMENTATION SUMMARY (What the code DOES)
{generator_summary}

### TEST RUNNER EXECUTION RESULT (Raw test logs)
{test_runner_result}
"""
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)
        if response:
            final_summary = response.output_text.strip()
            verdict = self._parse_verdict(final_summary)
            if verdict is True:
                self._handle_pass()
            elif verdict is False:
                self._handle_fail(self._format_feedback(final_summary))
            else:
                # Output matched neither the JSON schema nor the keywords
                self._handle_fail(
                    "⚠️ The evaluator did not return a clear verdict, so the change "
                    "is being treated as failed. Please re-check the implementation "
                    "against the approved plan.")
        else:
            print(msg)
            self.issue.create_comment(msg)

    @staticmethod
    def _parse_verdict(summary):
        """Parses the evaluator verdict. Returns True (pass), False (fail), or None (unknown).

        Primary protocol: the JSON evaluation object defined in skills/evaluator.md.
        Legacy fallback: the TEST-APPROVED / TEST-REJECTED keywords.
        """
        match = re.search(r"\{.*\}", summary, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group(0))
                if (result.get("recommended_action") == "approve"
                        or result.get("root_cause") == "none"
                        or result.get("status") in ("passed", "approved", "success")):
                    return True
                if result.get("status") or result.get("root_cause"):
                    return False
            except json.JSONDecodeError:
                print("Failed to parse evaluator JSON output. Falling back to keywords.")
        if section_constants.TEST_APPROVED in summary:
            return True
        if section_constants.TEST_REJECTED in summary:
            return False
        return None

    @staticmethod
    def _format_feedback(summary):
        """Renders the evaluator's JSON verdict as a human-readable markdown list,
        so the raw JSON object never leaks into the issue. Falls back to the raw
        text only if it is not the expected JSON object."""
        match = re.search(r"\{.*\}", summary, re.DOTALL)
        if not match:
            return summary
        try:
            result = json.loads(match.group(0))
        except json.JSONDecodeError:
            return summary
        lines = []
        for item in result.get("feedback") or []:
            tags = " · ".join(filter(None, [
                f"**[{item['priority']}]**" if item.get("priority") else "",
                item.get("category", ""),
                f"`{item['file']}`" if item.get("file") else "",
            ]))
            message = item.get("message", "").strip()
            lines.append(f"- {tags}\n  {message}".rstrip() if tags else f"- {message}")
        return "\n".join(lines) if lines else (result.get("message") or "No detailed feedback provided.")

    def _handle_pass(self):
        github_utils.switch_status_label(self.issue, label_constants.READY_FOR_PR)
        self.issue.create_comment(
            f"{agent_constants.EVALUATOR_SIGNATURE}: {section_constants.EVALUATOR_EXEC_COMPLETE}: "
            f"✅ {section_constants.TEST_APPROVED}\n\n"
            f"All tests passed and the implementation satisfies the approved plan.")

    def _handle_fail(self, details):
        github_utils.switch_status_label(self.issue, label_constants.EVALUATION_FAILED)
        self.issue.create_comment(
            f"{agent_constants.EVALUATOR_SIGNATURE}: {section_constants.EVALUATOR_EXEC_COMPLETE}: "
            f"❌ {section_constants.TEST_REJECTED}\n\n"
            f"The code failed the QA testing phase. Generator, please review the feedback and fix the bugs.\n\n"
            f"{details}")


if __name__ == "__main__":
    agent = Evaluator()
    agent.execute()
