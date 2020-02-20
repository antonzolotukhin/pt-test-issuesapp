#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import argparse
import re
from sys import stderr


class HTTPGeneralException(Exception):
    pass


def GitHubAPIRequest(url, creds=''):
    response = requests.get(f'https://{creds}api.github.com/{url}')
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        message = json.loads(response.content)['message']
        raise HTTPGeneralException(
                "(GET /{url} HTTP response code: {response.status_code})\n" +
                message)


def GetReposByUser(user, creds=''):
    repos = GitHubAPIRequest(f'users/{user}/repos', creds)
    for repo in repos:
        yield repo['name']


def GetIssuesByUserRepo(user, repo, creds=''):
    issues = GitHubAPIRequest(f"repos/{user}/{repo}/issues", creds)
    for iss in issues:
        yield (iss['number'], iss['title'])


def GithubCredsType(arg_value,
                    pat=re.compile(r"^[a-zA-Z0-9\-]{0,39}\:[a-f0-9]{40}$")):
    if not pat.match(arg_value) and arg_value != '':
        raise argparse.ArgumentTypeError
    return arg_value


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, default='devopshq', help='''
                        You can define github account instead of "devopshq".
                        ''')
    parser.add_argument("-r", "--repo", type=str, default='all',
                        help='Also you can specify repository.')
    parser.add_argument("-c", "--creds", type=GithubCredsType, default='',
                        help='Access credentials in format "login:token".')

    args = parser.parse_args()

    if args.creds != '':
        creds = args.creds + '@'
    else:
        creds = ''
    try:
        if args.repo == 'all':
            reps = GetReposByUser(args.user, creds)
        else:
            reps = [args.repo]
        for repo in reps:
            print(f'{repo}:\n')
            for (inumber, ititle) in GetIssuesByUserRepo(args.user,
                                                         repo, creds):
                print(f'#{inumber} {ititle}')
            print('')
    except HTTPGeneralException as e:
        print('Query failed: {}'.format(str(e)), file=stderr)
        return 2
    else:
        return 0


if __name__ == "__main__":
    main()
