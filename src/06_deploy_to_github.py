import os
import sys
import json
import base64
import urllib.request
import urllib.error

TOKEN = os.environ.get("GITHUB_TOKEN")

def load_env_file():
    global TOKEN
    env_path = os.path.expanduser("~/.env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITHUB_TOKEN="):
                    TOKEN = line.split("=", 1)[1].strip('"\'')
                    break

def gh_request(url, method="GET", data=None):
    load_env_file()
    if not TOKEN:
        raise ValueError("GITHUB_TOKEN not found in environment or ~/.env")
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "JobShield-Deployer"
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        if e.code in [200, 201, 204]:
            return {}
        print(f"HTTP Error {e.code}: {err_msg}")
        raise e

def deploy_repository(repo_name="fake-job-posting-detection"):
    load_env_file()
    if not TOKEN:
        print("[!] GITHUB_TOKEN is missing.")
        return False
        
    print("[*] Authenticating with GitHub API...")
    user_info = gh_request("https://api.github.com/user")
    username = user_info["login"]
    print(f"[+] Authenticated as GitHub user: {username}")
    
    repo_url = f"https://api.github.com/user/repos"
    try:
        gh_request(repo_url, method="POST", data={
            "name": repo_name,
            "description": "Fake Job Posting Detection System - NLP & Machine Learning Application",
            "private": False,
            "has_pages": True
        })
        print(f"[+] Created GitHub repository: {username}/{repo_name}")
    except Exception:
        print(f"[*] Repository {username}/{repo_name} already exists. Updating contents...")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    files_to_upload = [
        "README.md",
        "index.html",
        "style.css",
        "app.js",
        "requirements.txt",
        "generate_notebook.py",
        "data/01_fake_job_postings.csv",
        "src/01_data_loader.py",
        "src/02_text_processor.py",
        "src/03_model_trainer.py",
        "src/04_evaluation.py",
        "src/05_predict.py",
        "src/06_deploy_to_github.py",
        "notebooks/Fake_Job_Posting_Detection.ipynb"
    ]

    for rel_path in files_to_upload:
        full_path = os.path.join(root_dir, rel_path)
        if not os.path.exists(full_path):
            continue
            
        with open(full_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("utf-8")
            
        api_path = f"https://api.github.com/repos/{username}/{repo_name}/contents/{rel_path}"
        
        sha = None
        try:
            existing = gh_request(api_path)
            sha = existing.get("sha")
        except Exception:
            pass

        payload = {
            "message": f"Upload {rel_path}",
            "content": content_b64
        }
        if sha:
            payload["sha"] = sha
            
        gh_request(api_path, method="PUT", data=payload)
        print(f"  [+] Uploaded {rel_path}")

    try:
        pages_url = f"https://api.github.com/repos/{username}/{repo_name}/pages"
        gh_request(pages_url, method="POST", data={
            "source": {"branch": "main", "path": "/"}
        })
        print("[+] GitHub Pages enabled on main branch!")
    except Exception:
        print("[*] GitHub Pages already configured.")

    live_url = f"https://{username}.github.io/{repo_name}/"
    repo_github_url = f"https://github.com/{username}/{repo_name}"
    
    print("\n========================================================")
    print("[+] PROJECT SUCCESSFULLY DEPLOYED TO GITHUB!")
    print(f"[*] Repository URL : {repo_github_url}")
    print(f"[*] Live Working Link : {live_url}")
    print("========================================================\n")
    return live_url

if __name__ == "__main__":
    deploy_repository()
