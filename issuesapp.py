import requests
import json

creds=''

response = requests.get(f'https://{creds}api.github.com/users/devopshq/repos')
if response.status_code == 200:
    repos = (ind['name'] for ind in json.loads(response.content))
    for rep in repos:
        response1 = requests.get(f'https://{creds}api.github.com/repos/devopshq/{rep}/issues')
        print (f'{rep}:')
        iss = json.loads(response1.content)
        for issue in iss:
            print (issue['number'])
            print (issue['title'])
