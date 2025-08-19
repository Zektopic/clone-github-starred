# Unit Tests

This directory contains the unit tests for the GitHub Starred Repository Cloner.

## Framework

The tests are written using Python's built-in `unittest` framework. The `unittest.mock` library is used to simulate external dependencies like API calls and file system operations.

## Running the Tests

To run the tests, navigate to the root directory of the project and run the following command:

```bash
python -m unittest discover tests
```

This will automatically discover and run all the tests in this directory.

## Test Coverage

The tests cover the following functionality:

- **`get_starred_repos`**:
  - Verifies that the function correctly parses a successful API response.
  - Ensures that the function handles API errors gracefully.
- **`clone_repo`**:
  - Checks that a new repository is cloned if it doesn't already exist.
  - Confirms that an existing repository is skipped.
