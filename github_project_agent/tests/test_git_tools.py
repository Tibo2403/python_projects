from pathlib import Path

import pytest

from github_project_agent.git_tools import RepoContext, parse_repo_slug


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/openai/codex.git", ("openai", "codex")),
        ("https://github.com/openai/codex", ("openai", "codex")),
        ("git@github.com:openai/codex.git", ("openai", "codex")),
    ],
)
def test_parse_repo_slug_accepts_common_github_urls(url, expected):
    assert parse_repo_slug(url) == expected


def test_parse_repo_slug_rejects_invalid_url():
    with pytest.raises(ValueError):
        parse_repo_slug("not-a-github-url")


def test_repo_path_is_stable_under_workspace(tmp_path: Path):
    context = RepoContext(workspace=tmp_path)
    assert context.repo_path("https://github.com/openai/codex") == tmp_path / "openai" / "codex"
