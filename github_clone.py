import os
import requests
import git
import argparse
import time

def get_paged_data(url, headers):
    """
    Fetches all pages of data from a paginated GitHub API endpoint.
    """
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())

        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None

        # Handle rate limiting
        if int(response.headers.get('X-RateLimit-Remaining', 1)) == 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_duration = max(0, reset_time - time.time())
            print(f"Rate limit exceeded. Waiting for {sleep_duration:.0f} seconds.")
            time.sleep(sleep_duration)

    return repos

def get_starred_repos(username, token):
    """
    Fetches the list of starred repositories for a given user.
    """
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    return get_paged_data(url, headers)

def get_org_repos(org, token):
    """
    Fetches the list of repositories for a given organization.
    """
    url = f'https://api.github.com/orgs/{org}/repos'
    headers = {'Authorization': f'token {token}'}
    return get_paged_data(url, headers)

def clone_repo(repo_info, clone_dir):
    """
    Clones a single repository into the specified directory.
    """
    repo_name = repo_info['name']
    repo_url = repo_info['clone_url']
    repo_dir = os.path.join(clone_dir, repo_name)

    if not os.path.exists(repo_dir):
        print(f'Cloning {repo_name}...')
        try:
            git.Repo.clone_from(repo_url, repo_dir)
            print(f'Finished cloning {repo_name}')
        except git.exc.GitCommandError as e:
            print(f"Error cloning {repo_name}: {e}")
    else:
        print(f'{repo_name} already exists, skipping...')

def main():
    """
    Main function to clone starred GitHub repositories.
    """
    parser = argparse.ArgumentParser(description='Clone GitHub repositories.')
    parser.add_argument('--token', required=True, help='GitHub Personal Access Token.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--starred', metavar='USERNAME', help='Clone starred repositories for a user.')
    group.add_argument('--org', metavar='ORG_NAME', help='Clone repositories from an organization.')

    parser.add_argument('--clone-dir', default='repos', help='Directory to clone repositories into.')

    args = parser.parse_args()

    # Create the directory if it doesn't exist
    if not os.path.exists(args.clone_dir):
        os.makedirs(args.clone_dir)

    try:
        if args.starred:
            print(f"Fetching starred repositories for {args.starred}...")
            repos = get_starred_repos(args.starred, args.token)
        elif args.org:
            print(f"Fetching repositories for organization {args.org}...")
            repos = get_org_repos(args.org, args.token)

        print(f"Found {len(repos)} repositories to clone.")

        for repo in repos:
            clone_repo(repo, args.clone_dir)

        print('All repositories have been processed.')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")

if __name__ == "__main__":
    main()
