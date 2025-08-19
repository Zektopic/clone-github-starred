import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from github_clone import get_starred_repos, clone_repo

class TestGitHubClone(unittest.TestCase):

    @patch('github_clone.requests.get')
    def test_get_starred_repos_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        repos = get_starred_repos('testuser', 'testtoken')
        self.assertEqual(len(repos), 2)
        self.assertEqual(repos[0]['name'], 'repo1')
        mock_get.assert_called_with('https://api.github.com/users/testuser/starred', auth=('testuser', 'testtoken'))

    @patch('github_clone.requests.get')
    def test_get_starred_repos_failure(self, mock_get):
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_starred_repos('testuser', 'testtoken')

    @patch('github_clone.git.Repo.clone_from')
    @patch('github_clone.os.path.exists')
    def test_clone_repo_new(self, mock_exists, mock_clone_from):
        # Mock that the repo does not exist
        mock_exists.return_value = False

        repo_info = {'name': 'new_repo', 'clone_url': 'http://example.com/new_repo.git'}
        clone_dir = 'test_dir'

        clone_repo(repo_info, clone_dir)

        repo_dir = os.path.join(clone_dir, repo_info['name'])
        mock_exists.assert_called_with(repo_dir)
        mock_clone_from.assert_called_with(repo_info['clone_url'], repo_dir)

    @patch('github_clone.git.Repo.clone_from')
    @patch('github_clone.os.path.exists')
    def test_clone_repo_exists(self, mock_exists, mock_clone_from):
        # Mock that the repo already exists
        mock_exists.return_value = True

        repo_info = {'name': 'existing_repo', 'clone_url': 'http://example.com/existing_repo.git'}
        clone_dir = 'test_dir'

        clone_repo(repo_info, clone_dir)

        repo_dir = os.path.join(clone_dir, repo_info['name'])
        mock_exists.assert_called_with(repo_dir)
        mock_clone_from.assert_not_called()

if __name__ == '__main__':
    unittest.main()
