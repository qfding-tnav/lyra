import os
import sys
import re
from github import Github, Auth
from openai import OpenAI


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    pr_number = os.getenv("PR_NUMBER")
    api_key = os.getenv("LLM_API_KEY")
    feedback = os.getenv("COMMENT_BODY")

    if not all([token, repo_name, pr_number, api_key, feedback]):
        print("Error: Missing required environment variables!")
        sys.exit(1)
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    client = OpenAI(api_key=api_key)

    # 1. Get the current code changes from the PR
    files = pr.get_files()
    diff_text = ""
    for file in files:
        if file.patch:
            diff_text += f"--- {file.filename}\n+++ {file.filename}\n{file.patch}\n\n"

    print(f"Applying fixes to PR #{pr_number}")

    # 2. Ask the LLM to rewrite the code based on the feedback
    system_prompt = """You are an expert Python Developer fixing failing code.
    Review the Git diff and the Reviewer's feedback. 
    Rewrite the necessary files to fix the issues.

    You MUST output the code using the following strict format:
    ===FILE: path/to/your/file.py===
    <your python code here>
    ===ENDFILE===
    """

    user_prompt = f"Code Diff:\n{diff_text}\n\nReviewer Feedback:\n{feedback}\n\nPlease generate the corrected code."

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    llm_output = response.choices[0].message.content

    # 3. Parse and save the fixed files locally
    pattern = r'===FILE: (.*?)===\n(.*?)===ENDFILE==='
    files_to_write = re.findall(pattern, llm_output, re.DOTALL)

    if not files_to_write:
        print("Could not parse any files. LLM might not have generated fixes.")
        sys.exit(1)

    for filepath, content in files_to_write:
        filepath = filepath.strip()
        print(f"Applying fix to {filepath}...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')

    # Acknowledge the fix in the PR comments
    pr.create_issue_comment(
        "🔧 **Healer Agent:** I have read the feedback and applied the necessary code fixes. Pushing new commit now!")


if __name__ == "__main__":
    main()
