import os
import sys

from github import Github, Auth, GithubException

from constants import agent_constants, label_constants, section_constants
from tools.utils import github_utils


class PrCreator:
    """Opens a pull request once the Evaluator has approved the generated code.

    Triggered by the `status:ready-for-pr` label. The mechanical work (branch
    push) was already done by the upstream agents, so this agent only has to:
      1. Open a PR from the issue's feature branch into the default branch.
      2. Link the PR back on the issue.
      3. Hand off to a human by switching the label to `status:needs-human-review`.
    """

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_token_pat = os.getenv("GITHUB_TOKEN_PAT")
        self.repo_name = os.getenv("REPO_NAME")
        self.issue_number = os.getenv("ISSUE_NUMBER")

        if not all([self.github_token_pat, self.repo_name, self.issue_number]):
            print("Error: Missing required environment variables.")
            sys.exit(1)
        # Use the PAT so the PR (and the label change) are attributed to the bot
        # account and can wake downstream workflows on review events.
        auth = Auth.Token(self.github_token_pat)
        self.gh = Github(auth=auth)
        self.repo = self.gh.get_repo(self.repo_name)
        self.issue = self.repo.get_issue(number=int(self.issue_number))

    @property
    def branch_name(self):
        return f"feature/agent-task-{self.issue_number}"

    def execute(self):
        print(f"Starting PR Creator Agent for Issue #{self.issue_number}")
        base = self.repo.default_branch
        head = self.branch_name
        owner = self.repo.owner.login

        try:
            existing = list(self.repo.get_pulls(state="open", head=f"{owner}:{head}"))
            if existing:
                pr = existing[0]
                print(f"PR already open for {head}: #{pr.number}")
                self._handle_existing(pr)
                return

            pr = self.repo.create_pull(
                title=f"[Agent] {self.issue.title} (#{self.issue_number})",
                body=self._build_body(),
                head=head,
                base=base,
            )
            print(f"Opened PR #{pr.number}: {pr.html_url}")
            self._handle_success(pr)
        except GithubException as exc:
            print(f"Failed to create PR: {exc}")
            self._handle_error(exc)

    def _build_body(self):
        generator_summary = github_utils.get_latest_generator_summary(self.issue)
        body = (
            f"Automated pull request opened by the agent pipeline after the "
            f"Evaluator approved the generated code.\n\n"
            f"Closes #{self.issue_number}\n\n"
            f"---\n\n"
            f"### Generator Implementation Summary\n\n"
            f"{generator_summary or '_No generator summary found on the issue._'}\n"
        )
        return body

    def _handle_success(self, pr):
        github_utils.switch_status_label(self.issue, label_constants.NEEDS_HUMAN_REVIEW)
        self.issue.create_comment(
            f"{agent_constants.PR_CREATOR_SIGNATURE}: {section_constants.PR_CREATOR_EXEC_COMPLETE}: "
            f"🚀 [PR #{pr.number}]({pr.html_url}) is open from `{self.branch_name}` "
            f"into `{self.repo.default_branch}`.\n\n"
            f"Awaiting human review. Once a reviewer approves, the PR can be merged.")

    def _handle_existing(self, pr):
        github_utils.switch_status_label(self.issue, label_constants.NEEDS_HUMAN_REVIEW)
        self.issue.create_comment(
            f"{agent_constants.PR_CREATOR_SIGNATURE}: {section_constants.PR_CREATOR_EXEC_COMPLETE}: "
            f"ℹ️ An open PR already exists for this issue: [PR #{pr.number}]({pr.html_url}). "
            f"No new PR was created.\n\nAwaiting human review.")

    def _handle_error(self, exc):
        self.issue.create_comment(
            f"{agent_constants.PR_CREATOR_SIGNATURE}: {section_constants.PR_CREATOR_EXEC_ERROR}: "
            f"❌ Failed to open a pull request from `{self.branch_name}`.\n\n"
            f"```\n{exc}\n```")


if __name__ == "__main__":
    agent = PrCreator()
    agent.execute()