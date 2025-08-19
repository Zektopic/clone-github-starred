
# GitHub Starred Repository Cloner

![Python CI](.github/workflows/ci.yml/badge.svg)

This Python script automates the process of cloning all repositories starred by a GitHub user. Simply provide your GitHub username and Personal Access Token (PAT), and it will fetch and clone the repositories into a local directory.

## Features
- Automatically fetches starred repositories.
- Clones each repository locally.
- Skips already cloned repositories to avoid duplication.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)
- `GitPython` library (`pip install gitpython`)
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

### 3. Configure Your Credentials
Edit `github_clone.py` and set your GitHub username and PAT:
```python
username = 'Enter Your Username'
token = 'Enter Your PAT'
```

### 4. Run the Script
Execute the script to clone starred repositories:
```bash
python github_clone.py
```

## Troubleshooting
- Ensure your PAT has the necessary permissions to read repository data.
- Verify your network connection if cloning fails.
- If repositories already exist, the script will skip them.

## Contributing
Feel free to submit issues or pull requests to enhance the functionality.

## License
This project is licensed under the MIT License.

```
```
