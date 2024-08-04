import requests

# Replace with your repository details
repo_owner = 'Gland0rf'
repo_name = 'CustomCommandLine'
api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'

response = requests.get(api_url)
commit_count = len(response.json())

badge_url = f'https://img.shields.io/badge/commits-{commit_count}-blue'
print(badge_url)