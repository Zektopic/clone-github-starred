
# GitHub Repository Cloner

This Python script automates the process of cloning repositories from GitHub. It can clone all repositories starred by a user or all repositories from all members of a GitHub organization.

## Features
- Clone all starred repositories for a user.
- Clone all public repositories from all members of an organization.
- Interactive CLI for selecting the cloning action.
- Handles GitHub API rate limits to avoid being blocked.
- Fetches all pages of repositories using pagination.
- Skips already cloned repositories to avoid duplication.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)
- `GitPython` library (`pip install gitpython`)
- A GitHub Personal Access Token (PAT) with `repo` and `read:org` scopes.

## Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/manupawickramasinghe/clone-github-starred.git
cd clone-github-starred
```

### 2. Install Dependencies
```bash
pip install requests gitpython
```

### 3. Run the Script
Execute the script with the required arguments.

**To clone your starred repositories:**
```bash
python github-clone.py <your-username> <your-token> --starred
```

**To clone repositories from an organization:**
```bash
python github-clone.py <your-username> <your-token> --org <organization-name>
```

Replace `<your-username>`, `<your-token>`, and `<organization-name>` with your actual GitHub username, Personal Access Token, and the name of the organization.

## Troubleshooting
- Ensure your PAT has the necessary permissions (`repo` and `read:org`).
- Verify your network connection if cloning fails.
- If repositories already exist, the script will skip them.

## Contributing
Feel free to submit issues or pull requests to enhance the functionality.

## License
This project is licensed under the MIT License.
```
```
