#!/usr/bin/env python3
"""Generate PR changelog and Next release-draft notes from Conventional Commits.

Commands:
  pr       Update the changelog markers on the current pull request body.
  release  Create or update the draft GitHub Release tagged ``next``.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

CHANGELOG_START_MARKER = "<!-- changelog:start -->"
CHANGELOG_END_MARKER = "<!-- changelog:end -->"
CHANGELOG_HEADING = "### Changelog"
CHECKLIST_HEADING = "## Checklist do revisor"
EMPTY_CHANGELOG = "N/A"

MERGE_COMMIT_PATTERN = re.compile(
    r"^(Merge pull request|Merge branch|Merge remote-tracking branch)\b"
)
CONVENTIONAL_HEADER_PATTERN = re.compile(
    r"^(?P<type>[A-Za-z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<subject>.+)$"
)
BREAKING_CHANGE_PATTERN = re.compile(r"^BREAKING[ -]CHANGE:", re.MULTILINE)
GITHUB_NOREPLY_PATTERN = re.compile(
    r"^(?:\d+\+)?(?P<login>[^@]+)@users\.noreply\.github\.com$", re.IGNORECASE
)
NEXT_LINK_PATTERN = re.compile(r'<([^>]+)>;\s*rel="next"')
SCOPE_SEGMENT_PATTERN = re.compile(r"[-_/]+")
GIT_LOG_FORMAT = "%H%x1f%an%x1f%ae%x1f%B%x1e"
BOT_LOGIN_SUFFIX = "[bot]"
DRAFT_TAG = "next"
COMPARE_COMMIT_LIMIT = 250
API_VERSION = "2022-11-28"

TYPE_TO_CATEGORY = {
    "feat": "feat",
    "feature": "feat",
    "fix": "fix",
    "bug": "fix",
    "bugfix": "fix",
    "perf": "perf",
    "refactor": "refactor",
    "docs": "docs",
    "doc": "docs",
    "test": "test",
    "tests": "test",
    "dep": "deps",
    "deps": "deps",
    "build": "build",
    "ci": "ci",
    "chore": "chore",
    "revert": "revert",
}

DEPENDENCY_SCOPES = {"dep", "deps", "dependencies"}

CATEGORIES = [
    ("breaking", "### 💥 Breaking Changes"),
    ("feat", "### ✨ Features"),
    ("fix", "### 🐛 Bug Fixes"),
    ("perf", "### ⚡️ Performance"),
    ("refactor", "### ♻️ Refactors"),
    ("docs", "### 📝 Documentation"),
    ("test", "### ✅ Tests"),
    ("deps", "### 📦 Dependencies"),
    ("build", "### 🏗️ Build"),
    ("ci", "### 👷 CI"),
    ("chore", "### 🔧 Chores"),
    ("revert", "### ⏪ Reverts"),
    ("other", "### 🔹 Other"),
]


def parse_commit(message: str) -> dict[str, Any]:
    lines = message.split("\n")
    header = lines[0] if lines else ""
    body = "\n".join(lines[1:])
    match = CONVENTIONAL_HEADER_PATTERN.match(header.strip())
    breaking_in_body = bool(BREAKING_CHANGE_PATTERN.search(body))
    if not match:
        return {
            "type": None,
            "scope": None,
            "subject": header.strip(),
            "breaking": breaking_in_body,
        }
    groups = match.groupdict()
    return {
        "type": groups["type"].lower(),
        "scope": groups["scope"],
        "subject": groups["subject"],
        "breaking": groups["breaking"] == "!" or breaking_in_body,
    }


def category_of(parsed: dict[str, Any]) -> str:
    if parsed["breaking"]:
        return "breaking"
    category = TYPE_TO_CATEGORY.get(parsed["type"] or "", "other")
    scope = (parsed["scope"] or "").lower()
    if category == "chore" and scope in DEPENDENCY_SCOPES:
        return "deps"
    return category


def is_skipped_commit(commit: dict[str, Any]) -> bool:
    parents = commit.get("parents") or []
    if len(parents) > 1:
        return True
    return bool(MERGE_COMMIT_PATTERN.match(commit["message"]))


def login_from_email(email: str | None) -> str | None:
    if not email:
        return None
    match = GITHUB_NOREPLY_PATTERN.match(email)
    return match.group("login") if match else None


def capitalize_segment(segment: str) -> str:
    return f"{segment[:1].upper()}{segment[1:].lower()}"


def to_camel_case(scope: str) -> str:
    parts = [part for part in SCOPE_SEGMENT_PATTERN.split(scope) if part]
    if not parts:
        return scope
    first, *rest = parts
    return first.lower() + "".join(capitalize_segment(part) for part in rest)


def author_markdown(commit: dict[str, Any]) -> str:
    handle = commit.get("login") or login_from_email(commit.get("email"))
    if handle and handle.endswith(BOT_LOGIN_SUFFIX):
        app = handle[: -len(BOT_LOGIN_SUFFIX)]
        return f"[{app}](https://github.com/apps/{app})"
    if handle:
        return f"[{handle}](https://github.com/{handle})"
    return commit.get("name") or "unknown"


def format_entry(parsed: dict[str, Any], commit: dict[str, Any], repository: str) -> str:
    if parsed["scope"]:
        subject = f"**{to_camel_case(parsed['scope'])}**: {parsed['subject']}"
    else:
        subject = parsed["subject"]
    sha = commit["sha"][:7]
    sha_url = f"https://github.com/{repository}/commit/{commit['sha']}"
    return f"- {subject} — {author_markdown(commit)} · [`{sha}`]({sha_url})"


def format_changelog(commits: list[dict[str, Any]], repository: str) -> str:
    grouped: dict[str, list[str]] = {category_id: [] for category_id, _ in CATEGORIES}
    for commit in commits:
        if is_skipped_commit(commit):
            continue
        parsed = parse_commit(commit["message"])
        grouped[category_of(parsed)].append(format_entry(parsed, commit, repository))
    sections: list[str] = []
    for category_id, title in CATEGORIES:
        entries = grouped[category_id]
        if not entries:
            continue
        sections.append(f"{title}\n" + "\n".join(entries))
    if not sections:
        return EMPTY_CHANGELOG
    return "\n\n".join(sections)


def format_release_notes(commits: list[dict[str, Any]], repository: str) -> str:
    return f"## Changelog\n\n{format_changelog(commits, repository)}"


def marked_section(markdown: str) -> str:
    return f"{CHANGELOG_START_MARKER}\n{markdown}\n{CHANGELOG_END_MARKER}"


def section_with_heading(markdown: str) -> str:
    return f"{CHANGELOG_HEADING}\n\n{marked_section(markdown)}"


def replace_marked_section(current: str, section: str) -> str | None:
    start = current.find(CHANGELOG_START_MARKER)
    end = current.find(CHANGELOG_END_MARKER)
    if start == -1 or end <= start:
        return None
    return (
        current[:start]
        + section
        + current[end + len(CHANGELOG_END_MARKER) :]
    )


def insert_before_checklist(current: str, block: str) -> str:
    index = current.find(CHECKLIST_HEADING)
    if index == -1:
        return current.rstrip() + f"\n\n{block}"
    prefix = current[:index].rstrip()
    return f"{prefix}\n\n{block}\n\n{current[index:]}"


def inject_changelog(body: str | None, markdown: str) -> str:
    current = body or ""
    replaced = replace_marked_section(current, marked_section(markdown))
    if replaced is not None:
        return replaced
    if current.strip() == "":
        return section_with_heading(markdown)
    return insert_before_checklist(current, section_with_heading(markdown))


def parse_git_log_output(output: str) -> list[dict[str, Any]]:
    commits: list[dict[str, Any]] = []
    for record in output.split("\x1e"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("\x1f")
        sha = parts[0] if len(parts) > 0 else ""
        name = parts[1] if len(parts) > 1 else ""
        email = parts[2] if len(parts) > 2 else ""
        message = parts[3] if len(parts) > 3 else ""
        if message.startswith("\n"):
            message = message[1:]
        commits.append(
            {
                "sha": sha,
                "name": name,
                "email": email,
                "message": message,
                "login": login_from_email(email),
                "parents": [],
            }
        )
    return commits


def commits_from_git_log(from_ref: str | None, to_ref: str) -> list[dict[str, Any]]:
    range_spec = f"{from_ref}..{to_ref}" if from_ref else to_ref
    output = subprocess.check_output(
        ["git", "log", "--reverse", f"--format={GIT_LOG_FORMAT}", range_spec],
        text=True,
    )
    return parse_git_log_output(output)


def normalize_api_commit(item: dict[str, Any]) -> dict[str, Any]:
    commit = item.get("commit") or {}
    author = commit.get("author") or {}
    return {
        "sha": item.get("sha") or "",
        "message": commit.get("message") or "",
        "login": (item.get("author") or {}).get("login"),
        "name": author.get("name") or "",
        "email": author.get("email") or "",
        "parents": item.get("parents") or [],
    }


def github_headers(has_body: bool) -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN") or ""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "labflix-changelog",
    }
    if has_body:
        headers["Content-Type"] = "application/json"
    return headers


def next_link_from(link_header: str | None) -> str | None:
    if not link_header:
        return None
    match = NEXT_LINK_PATTERN.search(link_header)
    return match.group(1) if match else None


def github_fetch(
    url: str, *, method: str = "GET", body: dict[str, Any] | None = None
) -> tuple[Any, str | None]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers=github_headers(body is not None),
        method=method,
    )
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")
            payload = None if text == "" else json.loads(text)
            return payload, next_link_from(response.headers.get("Link"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API {method} {url} failed (HTTP {error.code}): {detail}"
        ) from error


def page_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("commits"), list):
        return payload["commits"]
    return []


def github_paginate(path: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    url: str | None = f"https://api.github.com{path}"
    while url:
        payload, next_url = github_fetch(url)
        items.extend(page_items(payload))
        url = next_url
    return items


def commits_between(
    repository: str, from_tag: str | None, head_sha: str
) -> list[dict[str, Any]]:
    if not from_tag:
        return commits_from_git_log(None, head_sha)
    compare_path = (
        f"/repos/{repository}/compare/"
        f"{urllib.parse.quote(from_tag, safe='')}..."
        f"{urllib.parse.quote(head_sha, safe='')}"
    )
    payload, _ = github_fetch(f"https://api.github.com{compare_path}")
    commits = (payload or {}).get("commits") or []
    ahead = (payload or {}).get("ahead_by") or 0
    if ahead > COMPARE_COMMIT_LIMIT or ahead > len(commits):
        return commits_from_git_log(from_tag, head_sha)
    return [normalize_api_commit(item) for item in commits]


def update_pull_request_changelog() -> None:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    with open(event_path, encoding="utf-8") as event_file:
        event = json.load(event_file)
    repository = os.environ["GITHUB_REPOSITORY"]
    number = event["pull_request"]["number"]
    current_body = event["pull_request"].get("body") or ""
    commits = [
        normalize_api_commit(item)
        for item in github_paginate(
            f"/repos/{repository}/pulls/{number}/commits?per_page=100"
        )
    ]
    next_body = inject_changelog(current_body, format_changelog(commits, repository))
    if next_body == current_body:
        sys.stdout.write("Changelog section already up to date.\n")
        return
    github_fetch(
        f"https://api.github.com/repos/{repository}/pulls/{number}",
        method="PATCH",
        body={"body": next_body},
    )
    sys.stdout.write(f"Updated changelog on pull request #{number}.\n")


def latest_published_tag(releases: list[dict[str, Any]]) -> str | None:
    for release in releases:
        if not release.get("draft") and release.get("tag_name") != DRAFT_TAG:
            return release.get("tag_name")
    return None


def upsert_next_draft(repository: str, notes: str, target: str) -> None:
    releases = github_paginate(f"/repos/{repository}/releases?per_page=100")
    next_release = next(
        (release for release in releases if release.get("tag_name") == DRAFT_TAG),
        None,
    )
    if next_release and not next_release.get("draft"):
        raise RuntimeError(
            'Release tag "next" is published. Change that tag to a version '
            "before the next production push."
        )
    if next_release:
        github_fetch(
            f"https://api.github.com/repos/{repository}/releases/{next_release['id']}",
            method="PATCH",
            body={"name": "Next", "body": notes, "draft": True},
        )
        return
    github_fetch(
        f"https://api.github.com/repos/{repository}/releases",
        method="POST",
        body={
            "tag_name": DRAFT_TAG,
            "name": "Next",
            "body": notes,
            "draft": True,
            "target_commitish": target,
        },
    )


def update_release_draft() -> None:
    repository = os.environ["GITHUB_REPOSITORY"]
    head_sha = os.environ["GITHUB_SHA"]
    releases = github_paginate(f"/repos/{repository}/releases?per_page=100")
    notes = format_release_notes(
        commits_between(repository, latest_published_tag(releases), head_sha),
        repository,
    )
    upsert_next_draft(repository, notes, head_sha)
    sys.stdout.write("Updated draft release Next.\n")


def main(argv: list[str]) -> int:
    command = argv[1] if len(argv) > 1 else None
    if command == "pr":
        update_pull_request_changelog()
        return 0
    if command == "release":
        update_release_draft()
        return 0
    sys.stderr.write(f"Unknown command: {command or '(none)'}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
