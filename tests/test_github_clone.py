import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import argparse
import git

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from github_clone import get_paged_data, get_starred_repos, get_org_repos, clone_repo, main

class TestGitHubClone(unittest.TestCase):

    @patch('github_clone.requests.get')
    def test_get_paged_data_single_page(self, mock_get):
        # Mock the API response for a single page
        mock_response = MagicMock()
        mock_response.json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
        mock_response.raise_for_status = MagicMock()
        mock_response.links = {}
        mock_response.headers = {'X-RateLimit-Remaining': '5000', 'X-RateLimit-Reset': '1678886400'}
        mock_get.return_value = mock_response

        repos = get_paged_data('http://example.com/repos', {'Authorization': 'token test'})
        self.assertEqual(len(repos), 2)
        mock_get.assert_called_once_with('http://example.com/repos', headers={'Authorization': 'token test'})

    @patch('github_clone.requests.get')
    def test_get_paged_data_multiple_pages(self, mock_get):
        # Mock the API response for multiple pages
        mock_response1 = MagicMock()
        mock_response1.json.return_value = [{'name': 'repo1'}]
        mock_response1.raise_for_status = MagicMock()
        mock_response1.links = {'next': {'url': 'http://example.com/repos?page=2'}}
        mock_response1.headers = {'X-RateLimit-Remaining': '5000', 'X-RateLimit-Reset': '1678886400'}

        mock_response2 = MagicMock()
        mock_response2.json.return_value = [{'name': 'repo2'}]
        mock_response2.raise_for_status = MagicMock()
        mock_response2.links = {}
        mock_response2.headers = {'X-RateLimit-Remaining': '4999', 'X-RateLimit-Reset': '1678886400'}

        mock_get.side_effect = [mock_response1, mock_response2]

        repos = get_paged_data('http://example.com/repos', {'Authorization': 'token test'})
        self.assertEqual(len(repos), 2)
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_has_calls([
            call('http://example.com/repos', headers={'Authorization': 'token test'}),
            call('http://example.com/repos?page=2', headers={'Authorization': 'token test'})
        ])

    @patch('github_clone.time.sleep')
    @patch('github_clone.requests.get')
    def test_get_paged_data_rate_limiting(self, mock_get, mock_sleep):
        # Mock the API response for rate limiting
        # The time.time() call will be mocked to a fixed value.
        current_time = 1678886390.0
        reset_time = current_time + 10

        mock_response1 = MagicMock()
        mock_response1.json.return_value = [{'name': 'repo1'}]
        mock_response1.raise_for_status = MagicMock()
        mock_response1.links = {'next': {'url': 'http://example.com/repos?page=2'}}
        mock_response1.headers = {'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(int(reset_time))}

        mock_response2 = MagicMock()
        mock_response2.json.return_value = [{'name': 'repo2'}]
        mock_response2.raise_for_status = MagicMock()
        mock_response2.links = {}
        mock_response2.headers = {'X-RateLimit-Remaining': '5000', 'X-RateLimit-Reset': str(int(reset_time) + 3600)}

        mock_get.side_effect = [mock_response1, mock_response2]

        with patch('time.time', return_value=current_time):
            get_paged_data('http://example.com/repos', {'Authorization': 'token test'})

        mock_sleep.assert_called_once()
        # The sleep duration should be slightly more than 10 seconds
        self.assertAlmostEqual(mock_sleep.call_args[0][0], 10, delta=1)

    @patch('github_clone.get_paged_data')
    def test_get_starred_repos(self, mock_get_paged_data):
        get_starred_repos('testuser', 'testtoken')
        mock_get_paged_data.assert_called_with(
            'https://api.github.com/users/testuser/starred',
            {'Authorization': 'token testtoken'}
        )

    @patch('github_clone.get_paged_data')
    def test_get_org_repos(self, mock_get_paged_data):
        get_org_repos('testorg', 'testtoken')
        mock_get_paged_data.assert_called_with(
            'https://api.github.com/orgs/testorg/repos',
            {'Authorization': 'token testtoken'}
        )

    @patch('github_clone.git.Repo.clone_from')
    @patch('github_clone.os.path.exists')
    def test_clone_repo_new(self, mock_exists, mock_clone_from):
        mock_exists.return_value = False
        repo_info = {'name': 'new_repo', 'clone_url': 'http://example.com/new_repo.git'}
        clone_repo(repo_info, 'test_dir')
        mock_clone_from.assert_called_with('http://example.com/new_repo.git', os.path.join('test_dir', 'new_repo'))

    @patch('github_clone.git.Repo.clone_from')
    @patch('github_clone.os.path.exists')
    def test_clone_repo_exists(self, mock_exists, mock_clone_from):
        mock_exists.return_value = True
        repo_info = {'name': 'existing_repo', 'clone_url': 'http://example.com/existing_repo.git'}
        clone_repo(repo_info, 'test_dir')
        mock_clone_from.assert_not_called()

    @patch('github_clone.git.Repo.clone_from')
    @patch('github_clone.os.path.exists')
    def test_clone_repo_error(self, mock_exists, mock_clone_from):
        mock_exists.return_value = False
        mock_clone_from.side_effect = git.exc.GitCommandError('clone', 'error')
        repo_info = {'name': 'error_repo', 'clone_url': 'http://example.com/error_repo.git'}
        with patch('builtins.print') as mock_print:
            clone_repo(repo_info, 'test_dir')
            self.assertIn("Error cloning error_repo", mock_print.call_args_list[1][0][0])

    @patch('github_clone.argparse.ArgumentParser.parse_args')
    @patch('github_clone.get_starred_repos')
    @patch('github_clone.clone_repo')
    @patch('github_clone.os.makedirs')
    @patch('github_clone.os.path.exists', return_value=False)
    def test_main_starred(self, mock_exists, mock_makedirs, mock_clone_repo, mock_get_starred_repos, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            token='testtoken',
            starred='testuser',
            org=None,
            clone_dir='test_clone_dir'
        )
        mock_get_starred_repos.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]

        main()

        mock_get_starred_repos.assert_called_with('testuser', 'testtoken')
        self.assertEqual(mock_clone_repo.call_count, 2)
        mock_makedirs.assert_called_with('test_clone_dir')

    @patch('github_clone.argparse.ArgumentParser.parse_args')
    @patch('github_clone.get_org_repos')
    @patch('github_clone.clone_repo')
    @patch('github_clone.os.makedirs')
    @patch('github_clone.os.path.exists', return_value=False)
    def test_main_org(self, mock_exists, mock_makedirs, mock_clone_repo, mock_get_org_repos, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            token='testtoken',
            starred=None,
            org='testorg',
            clone_dir='test_clone_dir'
        )
        mock_get_org_repos.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]

        main()

        mock_get_org_repos.assert_called_with('testorg', 'testtoken')
        self.assertEqual(mock_clone_repo.call_count, 2)
        mock_makedirs.assert_called_with('test_clone_dir')

if __name__ == '__main__':
    unittest.main()
