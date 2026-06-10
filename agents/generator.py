import os
import sys

from github import Github, Auth

from constants import agent_constants, section_constants, label_constants
from tools.open_ai_client import OpenAiClient
from tools.utils import github_utils, skill_utils


class Generator:
    def __init__(self):
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
        # A standard signature so the bot can easily find its own past comments
        self.bot_signature = agent_constants.PLANNER_SIGNATURE

    def execute(self):
        print(f"Starting Generator Agent for Issue #{self.issue_number}")
        current_try_count = 0
        role_instructions = skill_utils.load_skills(["generator.md"])
        if not role_instructions:
            print("No role instructions found. Exiting.")
            return
        # Load Available Skills
        skills_context = skill_utils.load_skills(["artifacts.md"])
        if skills_context:
            skills_context = f"### AVAILABLE FRAMEWORK SKILLS\n\n{skills_context}\n\n"

        # Prepare the Agent's identity
        system_prompt = (
            f"{role_instructions}\n\n{skills_context}\n\n"
        )

        # get current label
        labels = [l.name for l in self.issue.labels]
        is_approved_plan = label_constants.PLAN_APPROVED in labels
        is_evaluator_reject = label_constants.EVALUATION_FAILED in labels
        print(labels)
        if is_approved_plan:
            """Get approved plan and generate code"""
            plan = github_utils.get_approved_plan(self.issue)
            if not plan:
                print("No plan found to execute. Exiting.")
                return
            user_prompt = f"Here is the plan to execute:\n\n{plan}"
        elif is_evaluator_reject:
            # get loop limits
            current_try_count = github_utils.get_evaluator_reject_number_after_approved(self.issue)
            if current_try_count >= agent_constants.AGENT_RETRY_LIMIT:
                print("Max retry limit reached. Exiting.")
                self.issue.create_comment(
                    f"🛠️ {agent_constants.GENERATOR_SIGNATURE}: {section_constants.GENERATOR_EXEC_ERROR}\n\n"
                    f"Max retry limit {agent_constants.AGENT_RETRY_LIMIT} reached. Exiting."
                )
                return
            # Get latest evaluation reject information and generate code
            error_info = github_utils.get_evaluator_reject_content(self.issue)
            plan = github_utils.get_approved_plan(self.issue)
            user_prompt = f"""### ORIGINAL PLAN (What the code SHOULD do)
{plan}

### Evaluator Reject Content:
{error_info}\n\n"""
        else:
            user_prompt = ""

        if not user_prompt:
            print("user prompt not found. Exiting.")
            return

        print("Entering autonomous coding loop...")
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)
        if response:
            final_summary = response.output_text.strip()
            comment_text = (
                f"🛠️ {agent_constants.GENERATOR_SIGNATURE}: "
                f"{section_constants.GENERATOR_EXEC_COMPLETE}-{current_try_count + 1}\n\n"
                "I have finished writing the code based on the approved plan"
                f"{is_evaluator_reject and 'and the evaluator rejection error log.' or '.'}"
                f"Here is the summary:\n\n{final_summary}"
            )
            self.issue.create_comment(comment_text)
            # Clean up trigger labels
            if label_constants.PLAN_APPROVED in [l.name for l in self.issue.labels]:
                self.issue.remove_from_labels(label_constants.PLAN_APPROVED)
            if label_constants.EVALUATION_FAILED in [l.name for l in self.issue.labels]:
                self.issue.remove_from_labels(label_constants.EVALUATION_FAILED)
            self.issue.add_to_labels(label_constants.GENERATION_COMPLETE)
            print("Posted completion comment to GitHub.")
        else:
            comment_text = (
                f"🛠️ {agent_constants.GENERATOR_SIGNATURE}: {section_constants.GENERATOR_EXEC_ERROR}\n\n"
                f"code generator failed. Here is the error message:\n{msg}"
            )
            print(comment_text)
            self.issue.create_comment(comment_text)


if __name__ == "__main__":
    agent = Generator()
    agent.execute()
