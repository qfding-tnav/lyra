import os
import sys
from pathlib import Path

from github import Github, Auth

ROOT_DIR = str(Path(__file__).resolve().parents[1])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agents.constants import agent_constants, section_constants, label_constants
from agents.tools.open_ai_client import OpenAiClient
from agents.tools.utils import skill_utils, github_utils


class Planner:
    """This class is responsible for interacting with the GitHub API."""
    ROLE = "planner"

    def __init__(self):
        """Initializes the Planner Agent, loading configuration, clients, and skills."""
        # 1. Load Environment Variables
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_token_pat = os.getenv("GITHUB_TOKEN_PAT")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.repo_name = os.getenv("REPO_NAME")
        self.issue_number = os.getenv("ISSUE_NUMBER")
        self.event_name = os.getenv("EVENT_NAME", "issues")
        self.comment_body = os.getenv("COMMENT_BODY", "").strip()

        if not all([self.github_token, self.llm_api_key, self.repo_name, self.issue_number]):
            print("Error: Missing required environment variables.")
            sys.exit(1)

        # 2. Initialize Clients
        auth = Auth.Token(self.github_token)
        self.gh = Github(auth=auth)
        self.repo = self.gh.get_repo(self.repo_name)
        self.issue = self.repo.get_issue(number=int(self.issue_number))
        self.llm_client = OpenAiClient(self.llm_api_key)

    def _generate_plan(self, issue_title, issue_body, feedback=None, previous_plan=None):
        """Core logic to communicate with the LLM and generate a Markdown plan."""
        role_instructions = skill_utils.load_agent_role_skill(self.ROLE)

        system_prompt = f"{role_instructions}"

        user_prompt = f"Objective: {issue_title}\nDetails: {issue_body}\n\n"

        if feedback and previous_plan:
            feedback = feedback.replace(section_constants.CMD_PLAN, "").strip()
            user_prompt += (
                f"Here is the previous plan we created:\n{previous_plan}\n\n"
                f"The human reviewer provided this feedback: \n'{feedback}'\n\n"
                "Please revise the plan based strictly on this feedback."
            )
        else:
            user_prompt += "Please generate the initial step-by-step implementation plan."

        print("Calling LLM to generate plan...")
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)
        return response.output_text.strip()

    def handle_initial_plan(self):
        """Handles the creation of a brand-new issue."""
        print("Scenario: New Issue Opened. Generating initial plan.")
        plan = self._generate_plan(self.issue.title, self.issue.body)

        comment_text = (
            f"{agent_constants.PLANNER_SIGNATURE} Initial {section_constants.PLAN_DRAFT}\n\n"
            f"{plan}\n\n"
            f"---\n*Reply with `{section_constants.CMD_PLAN}` to update the plan, "
            f"or reply with `{section_constants.CMD_APPROVE}` to send it to the Generator Agent.*"
        )
        self.issue.create_comment(comment_text)
        print("Initial plan posted to GitHub.")

    def handle_approval(self):
        """Handles the human trigger to approve the plan and hand off to the Generator."""
        print("Approval detected. Adding label...")
        # use PAT token to trigger next step automatically.
        auth = Auth.Token(self.github_token_pat)
        gh = Github(auth=auth)
        repo = gh.get_repo(self.repo_name)
        issue = repo.get_issue(number=int(self.issue_number))

        issue.add_to_labels(label_constants.PLAN_APPROVED)
        issue.create_comment(
            f"{agent_constants.PLANNER_SIGNATURE}: "
            "✅ **Plan Approved!** The `plan-approved` label has been added. The Generator Agent will now take over."
        )
        print("Issue labeled as approved.")

    def handle_feedback(self):
        """Handles human feedback by fetching the previous plan and rewriting it."""
        print("Feedback detected. Fetching previous plan to update...")
        previous_plan = github_utils.get_previous_plan(self.issue)

        if not previous_plan:
            print("Could not find a previous plan to update. Treating as a new plan request.")

        updated_plan = self._generate_plan(
            issue_title=self.issue.title,
            issue_body=self.issue.body,
            feedback=self.comment_body,
            previous_plan=previous_plan
        )

        comment_text = (
            f"{agent_constants.PLANNER_SIGNATURE} Updated {section_constants.PLAN_DRAFT}\n\n"
            f"{updated_plan}\n\n"
            f"---\n*Reply with `{section_constants.CMD_PLAN}` to update the plan, "
            f"or reply with `{section_constants.CMD_APPROVE}` to begin coding.*"
        )
        self.issue.create_comment(comment_text)
        print("Updated plan posted to GitHub.")

    def execute(self):
        """Main routing function based on GitHub workflow events."""
        print(f"Running Planner Agent for Issue #{self.issue_number} triggered by {self.event_name}")

        if self.event_name == "issues":
            self.handle_initial_plan()

        elif self.event_name == "issue_comment":
            print(f"Scenario: New Comment detected: {self.comment_body}")
            if section_constants.CMD_APPROVE in self.comment_body.lower():
                self.handle_approval()
            elif section_constants.CMD_PLAN in self.comment_body.lower():
                self.handle_feedback()
        else:
            print(f"Unhandled event type: {self.event_name}")


if __name__ == "__main__":
    agent = Planner()
    agent.execute()
