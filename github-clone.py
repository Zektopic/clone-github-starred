import requests
import git
import os

# Your GitHub username
username = 'Enter Your Username'
# Example username = 'manupawickramasinghe'

# Your GitHub personal access token
token = 'enter your PAT'

# Example token = '123123123133'

# GitHub API URL for starred repos
url = f'https://api.github.com/users/{username}/starred'

# Directory to clone repos into
clone_dir = 'starred_repos'

# Create the directory if it doesn't exist
if not os.path.exists(clone_dir):
    os.makedirs(clone_dir)

# Fetch starred repos
response = requests.get(url, auth=(username, token))
repos = response.json()

# Clone each repo
for repo in repos:
    repo_name = repo['name']
    repo_url = repo['clone_url']
    repo_dir = os.path.join(clone_dir, repo_name)
    
    if not os.path.exists(repo_dir):
        print(f'Cloning {repo_name}...')
        git.Repo.clone_from(repo_url, repo_dir)
        print(f'Finished cloning {repo_name}')
    else:
        print(f'{repo_name} already exists, skipping...')

print('All repositories have been cloned.')
