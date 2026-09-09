"""GitHub repository discovery client.

Contract:
    Single self-contained module that queries the GitHub search API for
    recently created repositories and renders them to standard output.
"""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass(frozen=True)
class BotConfig:
    """Centralized configuration for GitHub discovery."""

    token: str = ""
    search_url: str = "https://api.github.com/search/repositories"
    output_filename: str = "output.txt"
    default_language: str = "python"
    default_days: int = 1
    default_count: int = 30
    max_per_page: int = 100
    seconds_per_day: int = 86400
    date_format: str = "%Y-%m-%dT%H:%M:%SZ"
    format_command: tuple[str, ...] = ("gum", "format")
    format_timeout_seconds: int = 30


CONFIG = BotConfig()

HEADERS = (
    {
        "Authorization": f"token {CONFIG.token}",
        "Accept": "application/vnd.github.v3+json",
    }
    if CONFIG.token
    else {}
)


def find_new_repos(
    language: str = CONFIG.default_language,
    days: int = CONFIG.default_days,
    count: int = CONFIG.max_per_page,
    order: str = "desc",
    config: BotConfig = CONFIG,
) -> list[dict[str, object]]:
    """Search GitHub for recently created repositories.

    Args:
        language: Programming language filter.
        days: Look-back window in days.
        count: Maximum repositories to request.
        order: Sort order for creation date.
        config: Module configuration.

    Returns:
        Normalized repository summaries.
    """
    since = time.strftime(
        config.date_format,
        time.gmtime(time.time() - days * config.seconds_per_day),
    )
    query = f"created:>={since} language:{language}"
    params = {
        "q": query,
        "sort": "created",
        "order": order,
        "per_page": min(count, config.max_per_page),
    }
    response = requests.get(config.search_url, headers=HEADERS, params=params, timeout=30)
    if response.status_code != 200:
        print("GitHub API error:", response.status_code, response.json())
        return []
    repos = response.json().get("items", [])
    results: list[dict[str, object]] = []
    for repo in repos:
        results.append(
            {
                "name": repo["name"],
                "owner": repo["owner"]["login"],
                "url": repo["html_url"],
                "description": repo["description"] or "No description",
                "language": repo["language"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "created": repo["created_at"],
                "size_kb": f"{repo['size']} KB",
                "license": repo["license"]["name"] if repo["license"] else "No license",
            }
        )
    return results


def render_repos(repos: list[dict[str, object]], config: BotConfig = CONFIG) -> str:
    """Render repository summaries to text and persist them to disk.

    Args:
        repos: Normalized repository summaries.
        config: Module configuration.

    Returns:
        Rendered text written to the output file.
    """
    lines: list[str] = []
    for index, repo in enumerate(repos, 1):
        created = str(repo["created"])[:10]
        lines.append(f"{index}. {repo['name']} (@{repo['owner']})")
        lines.append(f"   URL: {repo['url']}")
        lines.append(f"   Description: {repo['description']}")
        lines.append(f"   Language: {repo['language']}")
        lines.append(f"   Stars: {repo['stars']} | Forks: {repo['forks']}")
        lines.append(f"   Created: {created} | Size: {repo['size_kb']}")
        lines.append(f"   License: {repo['license']}")
        lines.append("-" * 60)
    content = "\n".join(lines)
    Path(config.output_filename).write_text(content, encoding="utf-8")
    return content


def format_output(content: str, config: BotConfig = CONFIG) -> None:
    """Pipe rendered content through the external formatter when available.

    Args:
        content: Text to format.
        config: Module configuration.
    """
    try:
        subprocess.run(
            list(config.format_command),
            input=content,
            capture_output=True,
            text=True,
            timeout=config.format_timeout_seconds,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        print(f"Format error: {exc}")


def main(config: BotConfig = CONFIG) -> None:
    """Discover recent repositories and render them.

    Args:
        config: Module configuration.
    """
    language = sys.argv[1] if len(sys.argv) > 1 else config.default_language
    print("Searching new repos...\n")
    repos = find_new_repos(
        language=language,
        days=config.default_days,
        count=config.default_count,
        config=config,
    )
    content = render_repos(repos, config)
    print(content)
    format_output(content, config)


buscar_repos_nuevos = find_new_repos


if __name__ == "__main__":
    main()
