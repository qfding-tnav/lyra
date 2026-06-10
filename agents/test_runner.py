import os
import sys

from github import Github, Auth

from tools.open_ai_client import OpenAiClient


class TestRunner:
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

    def execute(self):
        print(f"Starting Test runner Agent for Issue #{self.issue_number}")


if __name__ == "__main__":
    agent = TestRunner()
    agent.execute()
