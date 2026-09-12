#!/usr/bin/env python3
"""Read-before-you-write journal over GitHub Discussions.

I keep a durable engineering journal in a GitHub Discussion category. Every
unit of work appends one entry with the reasoning that a stateless agent
cannot recover from the code alone. ``read_journal`` prints the recent
entries, and the ``read-before-write`` workflow forces the next change to
cite the journal before it lands.

The module never opens a shell. It drives ``gh api graphql`` with an argument
list, and the runner is injectable so the tests never touch the network.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CATEGORY = "Show and tell"
DEFAULT_LIMIT = 5
GIT_TIMEOUT_SECONDS = 10
GH_TIMEOUT_SECONDS = 60

REPO_QUERY = "query($owner:String!,$name:String!){repository(owner:$owner,name:$name){id}}"
CATEGORY_QUERY = (
    "query($owner:String!,$name:String!){"
    "repository(owner:$owner,name:$name){"
    "discussionCategories(first:50){nodes{id name}}}}"
)
CREATE_MUTATION = (
    "mutation($repoId:ID!,$catId:ID!,$title:String!,$body:String!){"
    "createDiscussion(input:{repositoryId:$repoId,categoryId:$catId,title:$title,body:$body}){"
    "discussion{number url title}}}"
)
ENTRIES_QUERY = (
    "query($owner:String!,$name:String!,$limit:Int!){"
    "repository(owner:$owner,name:$name){"
    "discussions(first:$limit,orderBy:{field:UPDATED_AT,direction:DESC}){"
    "nodes{number title body url updatedAt}}}}"
)


class JournalError(RuntimeError):
    """Raised when the GitHub API call fails or the category is missing."""


@dataclass
class JournalConfig:
    """Configuration for the engineering journal.

    Attributes:
        owner: GitHub account or organization that owns the repository.
        name: Repository name.
        category: Discussion category that holds the journal entries.
        limit: Default number of entries ``read`` returns.
        marker: Token the read-before-write workflow looks for in a PR body.
    """

    owner: str
    name: str
    category: str = DEFAULT_CATEGORY
    limit: int = DEFAULT_LIMIT
    marker: str = "Journal"

    @classmethod
    def from_git_remote(cls, remote: str | None = None, category: str = DEFAULT_CATEGORY) -> JournalConfig:
        """Build a config from the ``origin`` remote of the current checkout.

        Args:
            remote: Optional repository slug ``owner/name``. When omitted, the
                slug is read from ``git config --get remote.origin.url``.
            category: Discussion category that holds the journal entries.
        Returns:
            The resolved configuration.
        Raises:
            JournalError: When the remote cannot be resolved to a slug.
        """
        slug = remote or _git_remote_slug()
        if "/" not in slug:
            raise JournalError(f"cannot derive owner/name from {slug!r}")
        owner, name = slug.split("/", 1)
        return cls(owner=owner, name=name.rstrip(".git"), category=category)


def _run_git(args: list[str]) -> str:
    """Run a git command and return its standard output.

    Args:
        args: Arguments passed to git, without the leading ``git``.
    Returns:
        The stripped standard output.
    Raises:
        JournalError: When git exits non-zero or is unavailable.
    """
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise JournalError(f"git invocation failed: {error}") from error
    if result.returncode != 0:
        raise JournalError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def _git_remote_slug() -> str:
    """Return the ``owner/name`` slug of the ``origin`` remote."""
    url = _run_git(["config", "--get", "remote.origin.url"])
    if url.startswith("git@"):
        _, _, path = url.partition(":")
        return path.removesuffix(".git")
    path = url.split("github.com/", 1)[-1]
    return Path(path).with_suffix("").as_posix() if path.endswith(".git") else path


def _default_runner(args: list[str]) -> str:
    """Run ``gh`` with an argument list and return its standard output.

    Args:
        args: Arguments passed to ``gh``.
    Returns:
        The standard output of the command.
    Raises:
        JournalError: When ``gh`` is missing or exits non-zero.
    """
    try:
        result = subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise JournalError(f"gh invocation failed: {error}") from error
    if result.returncode != 0:
        raise JournalError(result.stderr.strip() or "gh command failed")
    return result.stdout


@dataclass
class Journal:
    """GitHub Discussions backed journal.

    Attributes:
        config: Active journal configuration.
        runner: Callable that executes ``gh`` and returns its output. The
            default shells out through an argument list; tests inject a stub.
    """

    config: JournalConfig
    runner: Callable[[list[str]], str] = _default_runner
    _repo_id: str | None = field(default=None, init=False, repr=False)
    _category_id: str | None = field(default=None, init=False, repr=False)

    def _graphql(self, query: str, variables: dict[str, object]) -> dict:
        """Run a GraphQL query through ``gh`` and return the ``data`` payload.

        Args:
            query: GraphQL document.
            variables: Variables passed to ``gh`` with ``-f``.
        Returns:
            The ``data`` object of the response.
        Raises:
            JournalError: When the response contains GraphQL errors.
        """
        args = ["api", "graphql", "-f", f"query={query}"]
        for key, value in variables.items():
            flag = "-F" if isinstance(value, int) and not isinstance(value, bool) else "-f"
            args.extend([flag, f"{key}={value}"])
        payload = json.loads(self.runner(args))
        if payload.get("errors"):
            raise JournalError("; ".join(error.get("message", "") for error in payload["errors"]))
        return payload.get("data", {})

    @property
    def repo_id(self) -> str:
        """The GraphQL node id of the repository."""
        if self._repo_id is None:
            data = self._graphql(REPO_QUERY, {"owner": self.config.owner, "name": self.config.name})
            self._repo_id = str(data["repository"]["id"])
        return self._repo_id

    @property
    def category_id(self) -> str:
        """The GraphQL node id of the journal category."""
        if self._category_id is None:
            data = self._graphql(
                CATEGORY_QUERY,
                {"owner": self.config.owner, "name": self.config.name},
            )
            nodes = data["repository"]["discussionCategories"]["nodes"]
            match = next((node for node in nodes if node["name"] == self.config.category), None)
            if match is None:
                raise JournalError(f"discussion category not found: {self.config.category}")
            self._category_id = str(match["id"])
        return self._category_id

    def post(self, title: str, body: str) -> dict:
        """Create a journal entry and return its number, url, and title.

        Args:
            title: Entry title.
            body: Entry body in markdown.
        Returns:
            A dict with ``number``, ``url`` and ``title``.
        Raises:
            JournalError: When the mutation fails.
        """
        data = self._graphql(
            CREATE_MUTATION,
            {"repoId": self.repo_id, "catId": self.category_id, "title": title, "body": body},
        )
        return data["createDiscussion"]["discussion"]

    def entries(self, limit: int | None = None) -> list[dict]:
        """Return the most recently updated journal entries.

        Args:
            limit: Maximum number of entries. Defaults to the config limit.
        Returns:
            A list of dicts with ``number``, ``title``, ``body``, ``url`` and
            ``updatedAt``.
        Raises:
            JournalError: When the query fails.
        """
        data = self._graphql(
            ENTRIES_QUERY,
            {
                "owner": self.config.owner,
                "name": self.config.name,
                "limit": limit if limit is not None else self.config.limit,
            },
        )
        return list(data["repository"]["discussions"]["nodes"])


def _build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(prog="journal")
    parser.add_argument("--repo", help="repository slug owner/name (default: origin remote)")
    parser.add_argument("--category", default=DEFAULT_CATEGORY, help="discussion category")
    sub = parser.add_subparsers(dest="command", required=True)

    post = sub.add_parser("post", help="append a journal entry")
    post.add_argument("--title", required=True)
    body_group = post.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--body")
    body_group.add_argument("--body-file")

    read = sub.add_parser("read", help="print recent journal entries")
    read.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    read.add_argument("--json", action="store_true", help="emit raw JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the journal CLI and return the process exit code.

    Args:
        argv: Optional argument vector. Defaults to ``sys.argv``.
    Returns:
        0 on success, 1 on a journal error.
    """
    args = _build_parser().parse_args(argv)
    try:
        config = JournalConfig.from_git_remote(remote=args.repo, category=args.category)
        journal = Journal(config)
        if args.command == "post":
            body = args.body
            if args.body_file:
                body = Path(args.body_file).read_text(encoding="utf-8")
            entry = journal.post(args.title, body or "")
            print(f"posted journal entry #{entry['number']}: {entry['url']}")
            return 0
        entries = journal.entries(args.limit)
        if args.json:
            print(json.dumps(entries, indent=2))
            return 0
        for entry in entries:
            print(f"# {entry['number']} {entry['title']} ({entry['updatedAt']})")
            print(entry["body"].strip())
            print()
        return 0
    except JournalError as error:
        print(f"[journal] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
