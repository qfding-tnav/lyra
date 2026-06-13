import os
import subprocess
import sys

from github import Github, Auth

from constants import agent_constants, label_constants, path_constants, section_constants

MAX_COMMENT_OUTPUT_CHARS = 6000
PYTEST_TIMEOUT_SECONDS = 300


class TestRunner:
    def __init__(self):
        # Use PAT so the label change can trigger the downstream Evaluator workflow
        self.github_token_pat = os.getenv("GITHUB_TOKEN_PAT")
        self.repo_name = os.getenv("REPO_NAME")
        self.issue_number = os.getenv("ISSUE_NUMBER")

        if not all([self.github_token_pat, self.repo_name, self.issue_number]):
            print("Error: Missing required environment variables.")
            sys.exit(1)
        auth = Auth.Token(self.github_token_pat)
        self.gh = Github(auth=auth)
        self.repo = self.gh.get_repo(self.repo_name)
        self.issue = self.repo.get_issue(number=int(self.issue_number))

    def _find_project_dir(self):
        """Locate the artifacts/{project_name} directory that contains a tests/ folder."""
        artifacts_dir = path_constants.ARTIFACTS_DIR
        if not os.path.isdir(artifacts_dir):
            return None
        for name in sorted(os.listdir(artifacts_dir)):
            project_dir = os.path.join(artifacts_dir, name)
            if os.path.isdir(os.path.join(project_dir, "tests")):
                return project_dir
        return None

    def _run_pytest(self, project_dir):
        """Run pytest inside the project sandbox and return (exit_code, output)."""
        command = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]
        print(f"Running: {' '.join(command)} (cwd={project_dir})")
        try:
            result = subprocess.run(
                command,
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=PYTEST_TIMEOUT_SECONDS,
            )
            output = f"{result.stdout}\n{result.stderr}".strip()
            return result.returncode, output
        except subprocess.TimeoutExpired:
            return 1, f"pytest timed out after {PYTEST_TIMEOUT_SECONDS} seconds."

    def _save_report(self, project_dir, output):
        """Persist the test output to tests_report/ so the workflow commits it to the branch."""
        report_dir = os.path.join(project_dir, "tests_report")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "pytest_report.txt")
        with open(report_path, "w") as f:
            f.write(output)
        print(f"Test report saved to {report_path}")

    def _switch_labels(self, new_label):
        if label_constants.TEST_GENERATION_COMPLETE in [l.name for l in self.issue.labels]:
            self.issue.remove_from_labels(label_constants.TEST_GENERATION_COMPLETE)
        self.issue.add_to_labels(new_label)

    def execute(self):
        print(f"Starting Test Runner Agent for Issue #{self.issue_number}")

        project_dir = self._find_project_dir()
        if not project_dir:
            self.issue.create_comment(
                f"🛠️ {agent_constants.TEST_RUNNER_SIGNATURE}: {section_constants.TEST_RUNNER_EXEC_ERROR}\n\n"
                f"No project with a `tests/` directory found under `{path_constants.ARTIFACTS_DIR}/`."
            )
            self._switch_labels(label_constants.TEST_RUNNER_FAILED)
            return

        exit_code, output = self._run_pytest(project_dir)
        self._save_report(project_dir, output)

        if len(output) > MAX_COMMENT_OUTPUT_CHARS:
            output = "... (truncated) ...\n" + output[-MAX_COMMENT_OUTPUT_CHARS:]

        if exit_code == 0:
            self.issue.create_comment(
                f"🛠️ {agent_constants.TEST_RUNNER_SIGNATURE}: {section_constants.TEST_RUNNER_EXEC_COMPLETE}\n\n"
                f"All tests passed in `{project_dir}`.\n\n"
                f"```text\n{output}\n```"
            )
            self._switch_labels(label_constants.TEST_RUNNER_COMPLETE)
            print("Tests passed. Issue labeled for the Evaluator.")
        else:
            self.issue.create_comment(
                f"🛠️ {agent_constants.TEST_RUNNER_SIGNATURE}: {section_constants.TEST_RUNNER_EXEC_ERROR}\n\n"
                f"Tests failed in `{project_dir}` (exit code {exit_code}).\n\n"
                f"```text\n{output}\n```"
            )
            self._switch_labels(label_constants.TEST_RUNNER_FAILED)
            print("Tests failed. Issue labeled as test-runner-failed.")


if __name__ == "__main__":
    agent = TestRunner()
    agent.execute()
