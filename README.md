# GitHub Repository Cloner

![Python CI](.github/workflows/ci.yml/badge.svg)

This Python script automates the process of cloning repositories from GitHub. It can clone all repositories starred by a user or all repositories from a specific organization.

## Features
- Clone all starred repositories for a user.
- Clone all repositories from a GitHub organization.
- Command-line interface to specify what to clone.
- Handles GitHub API pagination to fetch all repositories.
- Includes rate limiting handling to avoid API request failures.
- Skips already cloned repositories to avoid duplication.

## Requirements
- Python 3.x
- `requests` library
- `GitPython` library
- A GitHub Personal Access Token (PAT)

## Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/manupawickramasinghe/clone-github-starred.git
cd clone-github-starred
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Script
Execute the script using the command-line interface. You must provide a GitHub Personal Access Token (PAT) with the `--token` argument.

#### To clone starred repositories:
Use the `--starred` argument with your GitHub username.
```bash
python github_clone.py --token YOUR_PAT --starred YOUR_USERNAME
```

#### To clone repositories from an organization:
Use the `--org` argument with the organization name.
```bash
python github_clone.py --token YOUR_PAT --org ORGANIZATION_NAME
```

#### Optional Arguments:
- `--clone-dir`: Specify a directory to clone the repositories into. Defaults to `repos`.
  ```bash
  python github_clone.py --token YOUR_PAT --starred YOUR_USERNAME --clone-dir my_starred_repos
  ```

## Troubleshooting
- Ensure your PAT has the necessary permissions to read repository data.
- Verify your network connection if cloning fails.
- If repositories already exist, the script will skip them.

## Contributing
Feel free to submit issues or pull requests to enhance the functionality.

## License
This project is licensed under the MIT License.
