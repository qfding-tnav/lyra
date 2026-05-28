import os
import sys
import re
from github import Github, Auth
from openai import OpenAI


def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    issue_number = os.getenv("ISSUE_NUMBER")
    api_key = os.getenv("OPENAI_API_KEY")

    if not all([token, repo_name, issue_number, api_key]):
        print("Error: Missing required environment variables!")
        sys.exit(1)
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(number=int(issue_number))
    client = OpenAI(api_key=api_key)

    # 1. Find the first unchecked task
    body = issue.body
    tasks = re.findall(r'- \[ \] (.*)', body)

    if not tasks:
        print("No pending tasks found. Exiting.")
        sys.exit(0)

    current_task = tasks[0]
    print(f"Working on task: {current_task}")

    # 2. Ask the LLM to write the code
    system_prompt = """You are an expert Python Developer.
    Your job is to write code based on the given task.
    You MUST output the code using the following strict format so my script can parse it:

    ===FILE: path/to/your/file.py===
    <your python code here>
    ===ENDFILE===

    Do not output markdown code blocks outside of this format.
    """

    user_prompt = f"Issue Context: {issue.title}\nTask to implement: {current_task}\nPlease write the necessary code."

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    llm_output = response.choices[0].message.content

    # 3. Parse the LLM output and save the files locally
    pattern = r'===FILE: (.*?)===\n(.*?)===ENDFILE==='
    files_to_write = re.findall(pattern, llm_output, re.DOTALL)

    if not files_to_write:
        print("Could not parse any files from the LLM output.")
        print("Raw output:", llm_output)
        sys.exit(1)

    for filepath, content in files_to_write:
        filepath = filepath.strip()
        print(f"Writing to {filepath}...")

        # Ensure the directory exists (e.g., src/ or tests/)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')

    # 4. Remove the label so it doesn't trigger repeatedly (Evaluator will re-add if needed)
    try:
        issue.remove_from_labels("status:planned")
    except:
        pass

    print("✅ Code generation complete. Files saved locally.")


if __name__ == "__main__":
    main()
