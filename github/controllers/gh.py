from cement import Controller, ex
import os
import sys
import json
import pprint
import requests


BASE_URL = "https://api.github.com"


class Github:
    def __init__(self):
        OAUTH_TOKEN = os.getenv("GITAUTH_TOKEN")
        self.GH_UNAME = os.getenv("GH_UNAME")
        if OAUTH_TOKEN == None or self.GH_UNAME == None:
            print(
                'To use this tool follow these setup instructions\n   1. set environment varible GITAUTH_TOKEN as authentication token\nFollow link for more details: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token\n   2. set environment varible GH_UNAME as username for Github\n(Set as: export GITAUTH_TOKEN="<Token>")'
            )
            sys.exit()
        self.headers = {"Authorization": f"token {OAUTH_TOKEN}"}

    def list_repos(self):
        data = requests.get(f"{BASE_URL}/user/repos", headers=self.headers)
        user_repos = data.json()
        for seq_no, repo in enumerate(user_repos):
            if repo["private"] == True:
                print(f'{seq_no+1}.  {repo["name"]} (Pri.)')
            else:
                print(f'{seq_no+1}.  {repo["name"]}')

    def new_repo(self, repo, repo_type="private"):
        print(f"Creating Repo => {repo}")
        if repo_type == "private":
            params = {"name": repo, "auto_init": True, "private": True}
        else:
            params = {"name": repo, "auto_init": True, "private": False}

        req = requests.post(
            f"{BASE_URL}/user/repos", data=json.dumps(params), headers=self.headers
        )
        pprint.pprint(req.json())

    def rm_repo(self, repo):
        print(f"Deleting Repo => {repo}")
        req = requests.delete(
            f"{BASE_URL}/repos/{self.GH_UNAME}/{repo}", headers=self.headers
        )
        pprint.pprint(req.content)

    def list_branch(self, repo):
        req = requests.get(
            f"{BASE_URL}/repos/{self.GH_UNAME}/{repo}/branches", headers=self.headers
        )
        branches = [val["name"] for val in req.json()]
        print(f"Branches in {repo}")
        for seq, branch in enumerate(branches):
            print(f"{seq+1}.  {branch}")

    def new_branch(self, repo, branch_name):
        req = requests.get(
            f"https://api.github.com/repos/{self.GH_UNAME}/{repo}/git/refs/heads",
            headers=self.headers,
        )
        sha = req.json()[0]["object"]["sha"]
        print(sha)
        params = {"ref": f"refs/heads/{branch_name}", "sha": sha}
        req = requests.post(
            f"https://api.github.com/repos/{self.GH_UNAME}/{repo}/git/refs",
            data=json.dumps(params),
            headers=self.headers,
        )
        pprint.pprint(req.json())

    def rm_branch(self, repo, branch_name):
        req = requests.delete(
            f"https://api.github.com/repos/{self.GH_UNAME}/{repo}/git/refs/heads/{branch_name}",
            headers=self.headers,
        )
        pprint.pprint(json.loads(req.content))



class Gh(Controller):
    class Meta:
        label = "github"

    @ex(
        help="Create Repos or Branches",
        arguments=[(["entity"], {"help": "repo or branch"})],
    )
    def create(self):
        gh = Github()
        entity = self.app.pargs.entity
        if entity.lower() == "repo":
            repo_name = input("\n Repo Name :")
            private = input("Private Repo (Y/n):")
            if private[0].lower() == "y":
                gh.new_repo(repo_name, "private")
            elif private[0].lower() == "n":
                gh.new_repo(repo_name, "public")
            self.app.log.info(f"Created {entity} {repo_name}")
        elif entity.lower() == "branch":
            repo_name = input("\n Repo Name :")
            branch_name = input("Branch Name :")
            gh.new_branch(repo_name, branch_name)
            self.app.log.info(f"Created {entity} {branch_name} in {repo_name}")

    @ex(
        help="List Repos or Branches",
        arguments=[(["entity"], {"help": "repo or branch"})],
    )
    def list(self):
        gh = Github()
        entity = self.app.pargs.entity
        if entity.lower() == "repo":
            self.app.log.info(f"Repository List")
            gh.list_repos()
        elif entity.lower() == "branch":
            repo_name = input('Enter repo name: ')
            self.app.log.info(f"Branches in {repo_name}:-")
            gh.list_branch(repo_name)
        

    @ex(
        help="Delete Repo or Branches",
        arguments=[(["entity"], {"help": "repo or branch"})],
    )
    def delete(self):
        gh = Github()
        entity = self.app.pargs.entity
        if entity.lower() == "repo":
            repo_name = input('Enter repo name: ')
            self.app.log.warning(f"Deleting repo {repo_name}")
            if(input(f"\nAbout to delete {repo_name}. Confirm by typing repo name : ").lower() == repo_name.lower()):
                gh.rm_repo(repo_name)
            else:
                print('You entered incorrect name. ABORT')
            
        elif entity.lower() == "branch":
            repo_name = input("\n Repo Name :")
            branch_name = input("Branch Name :")
            self.app.log.warning(f"Deleting branch {branch_name} in repo {repo_name}")
            if(input(f"\nAbout to delete {branch_name}. Confirm by typing branch name : ").lower() == branch_name.lower()):
                gh.rm_branch(repo_name, branch_name)
            else:
                print('You entered incorrect name. ABORT')
            
            
        
