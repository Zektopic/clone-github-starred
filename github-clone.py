import requests
import git
import os
import argparse
import time

def get_paginated_data(url, headers):
    """
    Fetches all pages of data from a paginated API endpoint.
    """
    results = []
    while url:
        response = requests.get(url, headers=headers)

        # Check rate limit
        if response.status_code == 403 and 'rate limit exceeded' in response.text.lower():
            rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = max(rate_limit_reset - time.time(), 0) + 10 # wait 10 seconds buffer
            print(f"Rate limit exceeded. Waiting for {sleep_time:.0f} seconds...")
            time.sleep(sleep_time)
            continue

        response.raise_for_status()
        results.extend(response.json())

        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None

    return results

def clone_repo(repo_url, repo_dir):
    """
    Clones a repository from a given URL into a specified directory.
    """
    if not os.path.exists(repo_dir):
        print(f"Cloning {repo_dir}...")
        git.Repo.clone_from(repo_url, repo_dir)
        print(f"Finished cloning {repo_dir}")
    else:
        print(f"{repo_dir} already exists, skipping...")

def get_starred_repos(username, token):
    """
    Fetches all starred repositories for a given user.
    """
    url = f"https://api.github.com/users/{username}/starred"
    headers = {'Authorization': f'token {token}'}
    return get_paginated_data(url, headers)

def get_org_members(org_name, token):
    """
    Fetches all members of a given organization.
    """
    url = f"https://api.github.com/orgs/{org_name}/members"
    headers = {'Authorization': f'token {token}'}
    members = get_paginated_data(url, headers)
    return [member['login'] for member in members]

def get_user_repos(username, token):
    """
    Fetches all public repositories for a given user.
    """
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'Authorization': f'token {token}'}
    return get_paginated_data(url, headers)

def main():
    parser = argparse.ArgumentParser(description="Clone GitHub repositories.")
    parser.add_argument("username", help="Your GitHub username")
    parser.add_argument("token", help="Your GitHub Personal Access Token")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--starred", action="store_true", help="Clone your starred repositories.")
    group.add_argument("--org", help="Clone repositories from all members of an organization.")

    args = parser.parse_args()

    if args.starred:
        print("Fetching your starred repositories...")
        repos = get_starred_repos(args.username, args.token)
        clone_dir = 'starred_repos'
    elif args.org:
        print(f"Fetching members of organization '{args.org}'...")
        members = get_org_members(args.org, args.token)
        print(f"Found {len(members)} members.")

        repos = []
        for member in members:
            print(f"Fetching repositories for member '{member}'...")
            repos.extend(get_user_repos(member, args.token))
        clone_dir = f'{args.org}_repos'

    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    for repo in repos:
        repo_name = repo['name']
        repo_url = repo['clone_url']
        repo_dir = os.path.join(clone_dir, repo_name)
        clone_repo(repo_url, repo_dir)

    print("All repositories have been cloned.")

if __name__ == "__main__":
    main()
