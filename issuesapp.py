# -*- coding: utf-8 -*-

import requests
import json
from sys import stderr

creds = ''

def GitHubAPIRequest (url,creds=''):
    response = requests.get(f'https://{creds}api.github.com/{url}')
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        message = json.loads(response.content)['message']
        raise Exception (f"{message} (GET /{url} HTTP response code: {response.status_code})")

def GetReposByUser (user,creds=''):
    repos = GitHubAPIRequest (f'users/{user}/repos', creds)
    for repo in repos:
        yield repo['name']

def GetIssuesByUserRepo (user, repo, creds=''):
    issues = GitHubAPIRequest(f"repos/{user}/{repo}/issues", creds)
    for iss in issues:
        yield (iss['number'],iss['title'])

def main ():
    try:
        for repo in GetReposByUser ('devopshq', creds):
            print (f'{repo}:\n')
            for (inumber,ititle) in GetIssuesByUserRepo ('devopshq',repo):
                print (f'#{inumber} {ititle}')
            print ('')
    except Exception as e:
        print('Query failed: {}'.format(str(e)), file = stderr)

if __name__== "__main__":
    main()
