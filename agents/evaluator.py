import os
import sys
from github import Github, Auth
from openai import OpenAI


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    pr_number = os.getenv("PR_NUMBER")
    api_key = os.getenv("OPENAI_API_KEY")

    if not all([token, repo_name, pr_number, api_key]):
        print("Error: Missing required environment variables!")
        sys.exit(1)
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    client = OpenAI(api_key=api_key)

    # 1. Extract the code changes (the Diff) from the PR
    files = pr.get_files()
    diff_text = ""
    for file in files:
        if file.patch:
            diff_text += f"--- {file.filename}\n+++ {file.filename}\n{file.patch}\n\n"

    if not diff_text:
        print("No code changes found in PR.")
        sys.exit(0)

    print(f"Evaluating PR #{pr_number}: {pr.title}")

    # 2. Ask the LLM to review the code
    system_prompt = """You are a strict, expert Python Code Reviewer.
    Review the provided Git diff for a length converter application.
    Look for logical errors, missing edge cases (e.g., negative lengths), and syntax issues.

    If the code is flawless, output EXACTLY the word: PASS
    If the code has issues, output the word FAIL followed by a detailed explanation of what needs to be fixed.
    Format: FAIL: <your specific feedback>
    """

    user_prompt = f"PR Title: {pr.title}\n\nCode Changes (Diff):\n{diff_text}"

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    evaluation = response.choices[0].message.content.strip()

    # 3. Take action based on the LLM's decision
    if evaluation.startswith("PASS"):
        print("✅ Code passed evaluation. Approving and Merging...")
        pr.create_issue_comment("✅ **Evaluator Agent:** The code looks excellent. Merging automatically!")
        pr.merge(merge_method='squash')
    else:
        print("❌ Code failed evaluation. Requesting changes...")
        feedback = evaluation.replace("FAIL:", "").strip()
        pr.create_issue_comment(
            f"❌ **Evaluator Agent found issues:**\n\n{feedback}\n\n*Please fix these issues and push the changes.*")


if __name__ == "__main__":
    main()
