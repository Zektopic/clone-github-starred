import os
import requests
import git

def get_starred_repos(username, token):
    """
    Fetches the list of starred repositories for a given user.
    """
    url = f'https://api.github.com/users/{username}/starred'
    response = requests.get(url, auth=(username, token))
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def clone_repo(repo_info, clone_dir):
    """
    Clones a single repository into the specified directory.
    """
    repo_name = repo_info['name']
    repo_url = repo_info['clone_url']
    repo_dir = os.path.join(clone_dir, repo_name)

    if not os.path.exists(repo_dir):
        print(f'Cloning {repo_name}...')
        git.Repo.clone_from(repo_url, repo_dir)
        print(f'Finished cloning {repo_name}')
    else:
        print(f'{repo_name} already exists, skipping...')

def main():
    """
    Main function to clone starred GitHub repositories.
    """
    # Your GitHub username
    username = 'Enter Your Username'
    # Example username = 'manupawickramasinghe'

    # Your GitHub personal access token
    token = 'Enter Your PAT'
    # Example token = '123123123133'

    # Directory to clone repos into
    clone_dir = 'starred_repos'

    # Create the directory if it doesn't exist
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    try:
        repos = get_starred_repos(username, token)
        for repo in repos:
            clone_repo(repo, clone_dir)
        print('All repositories have been cloned.')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")

if __name__ == "__main__":
    main()
