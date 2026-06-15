import os
import sys
from pathlib import Path

from github import Github, Auth

ROOT_DIR = str(Path(__file__).resolve().parents[1])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agents.constants import agent_constants, section_constants, label_constants
from agents.tools.open_ai_client import OpenAiClient
from agents.tools.utils import github_utils, skill_utils


class TestGenerator:
    ROLE = "test_generator"

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN_PAT")
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

    def execute(self):
        print(f"Starting Test Generator Agent for Issue #{self.issue_number}")
        current_try_count = github_utils.get_evaluator_reject_number_after_approved(self.issue)
        if current_try_count >= agent_constants.AGENT_RETRY_LIMIT:
            print("Max retry limit reached. Exiting.")
            self.issue.create_comment(
                f"🛠️ {agent_constants.TEST_GENERATOR_SIGNATURE}: {section_constants.TEST_GENERATOR_EXEC_ERROR}\n\n"
                f"Max retry limit {agent_constants.AGENT_RETRY_LIMIT} reached. Exiting."
            )
            return
        approved_plan = github_utils.get_approved_plan(self.issue)
        generator_summary = github_utils.get_latest_generator_summary(self.issue)

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
        """
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)
        if response:
            final_summary = response.output_text.strip()
            comment_text = (
                f"🛠️ {agent_constants.TEST_GENERATOR_SIGNATURE}: "
                f"{section_constants.TEST_GENERATOR_EXEC_COMPLETE}-{current_try_count + 1}\n\n"
                "I have finished writing the test code based on the approved plan and generate code.\n"
                f"Here is the summary:\n\n{final_summary}"
            )
            self.issue.create_comment(comment_text)
            # Clean up trigger labels
            self.issue.set_labels()
            self.issue.add_to_labels(label_constants.TEST_GENERATION_COMPLETE)
            print("Posted completion comment to GitHub.")
        else:
            comment_text = (
                f"🛠️ {agent_constants.TEST_GENERATOR_SIGNATURE}: {section_constants.TEST_GENERATOR_EXEC_ERROR}\n\n"
                f"test code generator failed. Here is the error message:\n{msg}"
            )
            print(comment_text)
            self.issue.create_comment(comment_text)


if __name__ == "__main__":
    agent = TestGenerator()
    agent.execute()
