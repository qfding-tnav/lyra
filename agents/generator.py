import os
import sys

from github import Github, Auth

from constants import agent_constants, section_constants
from tools.open_ai_client import OpenAiClient


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

        # Load Available Skills
        self.skills_context = self._load_skills()

        # A standard signature so the bot can easily find its own past comments
        self.bot_signature = agent_constants.PLANNER_SIGNATURE

    def _load_skills(self):
        """Reads the skill file to understand the agent's capabilities."""
        skills = ["artifacts.md"]
        for skill in skills:
            current_dir = os.path.dirname(__file__)
            skills_path = os.path.join(current_dir, "skills", skill)
            try:
                with open(skills_path, "r", encoding="utf-8") as f:
                    print(f"Successfully loaded skills from {skills_path}")
                    return f.read()
            except FileNotFoundError:
                print(f"Warning: Skills file not found at {skills_path}. Proceeding without skill context.")
                return "No specific framework skills documented."
        return "No specific framework skills documented."

    def _get_approved_plan(self):
        """Scans the issue to find the final approved plan from the Planner Agent."""
        comments = list(self.issue.get_comments())
        for comment in reversed(comments):
            if (agent_constants.PLANNER_SIGNATURE in comment.body and
                    section_constants.PLAN_DRAFT_HEADER in comment.body):
                return comment.body
        return None

    def execute(self):
        print(f"Starting Generator Agent for Issue #{self.issue_number}")

        plan = self._get_approved_plan()
        if not plan:
            print("No plan found to execute. Exiting.")
            return

        # Prepare the Agent's identity
        system_prompt = (
            "You are an expert Autonomous Software Engineer (The Generator Agent). "
            "Your job is to execute the provided technical plan step-by-step. "
            "### AVAILABLE FRAMEWORK SKILLS\n"
            f"{self.skills_context}\n\n"
            "### INSTRUCTIONS\n"
            "You must use your available tools (create_file, read_file) to write the actual code. "
            "When you have finished implementing all steps, return a final message summarizing what you built."
        )

        user_prompt = f"Here is the plan to execute:\n\n{plan}"

        print("Entering autonomous coding loop...")
        response, msg = self.llm_client.call(user_prompt, [system_prompt], agent_constants.AGENT_GENERATOR)
        if response:
            final_summary = response.output_text.strip()
            comment_text = (f"🛠️ {agent_constants.AGENT_GENERATOR}: Execution Complete\n\n"
                            f"I have finished writing the code based on the approved plan. "
                            f"Here is the summary:\n\n{final_summary}")
            self.issue.create_comment(comment_text)
            print("Posted completion comment to GitHub.")
        else:
            print(msg)
            self.issue.create_comment(msg)


if __name__ == "__main__":
    agent = Generator()
    agent.execute()
