import os
import sys

from github import Github, Auth

from constants import agent_constants
from tools.open_ai_client import OpenAiClient
from tools.utils import github_utils, skill_utils


class Evaluator:
    def __init__(self):
        # 1. Load Environment Variables
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.repo_name = os.getenv("REPO_NAME")
        self.issue_number = os.getenv("ISSUE_NUMBER")

        if not all([self.github_token, self.llm_api_key, self.repo_name, self.issue_number]):
            print("Error: Missing required environment variables.")
            sys.exit(1)
        auth = Auth.Token(self.github_token)
        self.gh = Github(auth=auth)
        self.repo = self.gh.get_repo(self.repo_name)
        self.issue = self.repo.get_issue(number=int(self.issue_number))
        self.llm_client = OpenAiClient(self.llm_api_key)

    def execute_evaluation(self):
        print(f"Starting Evaluator Agent for Issue #{self.issue_number}")
        approved_plan = github_utils.get_approved_plan(self.issue)
        generator_summary = github_utils.get_latest_generator_summary(self.issue)

        role_instructions = skill_utils.load_skills(["evaluator.md"])
        if not role_instructions:
            print("No role instructions found. Exiting.")
            return
        # Load Available Skills
        skills_context = skill_utils.load_skills(["artifacts.md"])
        if skills_context:
            skills_context = f"### AVAILABLE FRAMEWORK SKILLS\n\n{skills_context}\n\n"

        system_prompt = f"""{role_instructions}\n\n{skills_context}\n\n"""
        user_prompt = f"""
### ORIGINAL PLAN (What the code SHOULD do)
{approved_plan}

### GENERATOR'S IMPLEMENTATION SUMMARY (What the code DOES)
{generator_summary}
"""
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)

    def _handle_pass(self, summary):
        self.issue.remove_from_labels("status:code-generated")
        self.issue.add_to_labels("status:ready-for-review")
        self.issue.create_comment(f"✅ **Agent Evaluator: APPROVED**\n\nAll tests passed successfully.\n\n{summary}")

    def _handle_fail(self, summary):
        self.issue.remove_from_labels("status:code-generated")
        self.issue.add_to_labels("status:test-failed")
        self.issue.create_comment(
            f"❌ **Agent Evaluator: REJECTED**\n\nThe code failed the QA testing phase. Generator, please review the logs and fix the bugs.\n\n{summary}")


if __name__ == "__main__":
    Evaluator().execute_evaluation()
