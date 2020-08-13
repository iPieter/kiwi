import os
import logging
import subprocess

from mlflow.tracking.context.abstract_context import RunContextProvider
from mlflow.tracking.context.default_context import _get_main_file
from mlflow.utils.mlflow_tags import MLFLOW_GIT_COMMIT, MLFLOW_GIT_DIFF

_logger = logging.getLogger(__name__)


def _get_git_commit(path):
    try:
        import git
    except ImportError as e:
        _logger.warning(
            "Failed to import Git (the Git executable is probably not on your PATH),"
            " so Git SHA is not available. Error: %s", e)
        return None
    try:
        if os.path.isfile(path):
            path = os.path.dirname(path)
        repo = git.Repo(path, search_parent_directories=True)
        commit = repo.head.commit.hexsha
        return commit
    except (git.InvalidGitRepositoryError, git.GitCommandNotFound, ValueError, git.NoSuchPathError):
        return None


def _get_source_version():
    main_file = _get_main_file()
    if main_file is not None:
        return _get_git_commit(main_file)
    return None


def _get_git_diff(path):
    try:
        import git
        if os.path.isfile(path):
            path = os.path.dirname(path)
        repo = git.Repo(path, search_parent_directories=True) # try to confirm this is a git repository
        # GitPython doesn't seem to provide a handy way get the actual diff, thus the system call is used
        diff = subprocess.check_output(["git", "diff"]).decode("utf-8")
        return diff
    except (ImportError, git.InvalidGitRepositoryError, git.GitCommandNotFound, ValueError, git.NoSuchPathError):
        return None

def _get_git_diff_nopath():
    main_file = _get_main_file()
    if main_file is not None:
        return _get_git_diff(main_file)
    return None



class GitRunContext(RunContextProvider):

    def __init__(self):
        self._cache = {}

    @property
    def _source_version(self):
        if "source_version" not in self._cache:
            self._cache["source_version"] = _get_source_version()
        return self._cache["source_version"]

    @property
    def _git_diff(self):
        if "git_diff" not in self._cache:
            self._cache["git_diff"] = _get_git_diff_nopath()
        return self._cache["git_diff"]

    def in_context(self):
        return self._source_version is not None

    def tags(self):
        return {
            MLFLOW_GIT_COMMIT: self._source_version,
            MLFLOW_GIT_DIFF: self._git_diff
        }
