import os
import sys
from github import Github, Auth
from openai import OpenAI


def main():
    # 1. Fetch environment variables passed from GitHub Actions
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    issue_number = os.getenv("ISSUE_NUMBER")
    api_key = os.getenv("LLM_API_KEY")

    if not all([token, repo_name, issue_number, api_key]):
        print("Error: Missing required environment variables!")
        sys.exit(1)

    # 2. Initialize GitHub and OpenAI clients
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(number=int(issue_number))
    client = OpenAI(api_key=api_key)

    print(f"Processing Issue #{issue_number}: {issue.title}")

    # 3. Construct the prompt for the LLM
    system_prompt = """You are an expert Python Software Architect.
    Your task is to break down the user's request into a concrete checklist of development tasks.
    Output ONLY a Markdown formatted task list using checkboxes. Do not include extra conversational text.

    Example format:
    - [ ] Task 1: Write core logic in src/converter.py
    - [ ] Task 2: Write tests in tests/test_converter.py
    """

    user_prompt = f"Issue Title: {issue.title}\nIssue Description: {issue.body}"

    # 4. Call the LLM to generate the plan
    response = client.chat.completions.create(
        model="gpt-5.4",  # Feel free to change this if using a different model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    plan = response.choices[0].message.content

    # 5. Append the plan to the GitHub Issue and label it
    new_body = f"{issue.body if issue.body else ''}\n\n### Agent Task Breakdown 🤖\n\n{plan}"
    issue.edit(body=new_body)

    # Try to add a label, create it if it doesn't exist
    try:
        issue.add_to_labels("status:planned")
    except:
        repo.create_label(name="status:planned", color="0e8a16")
        issue.add_to_labels("status:planned")

    print("✅ Planning complete! Issue updated successfully.")


if __name__ == "__main__":
    main()
