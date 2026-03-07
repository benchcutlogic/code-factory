#!/usr/bin/env python3

import json
import os
import urllib.request

from common import load_repo_config


def github_request(url: str, method: str, token: str, data: dict | None = None) -> dict:
    encoded = None
    if data is not None:
        encoded = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=encoded, method=method)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request) as response:
        if response.length == 0:
            return {}
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    token = os.environ["GITHUB_TOKEN"]
    repository = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    head_sha = os.environ["HEAD_SHA"]
    config = load_repo_config().get("reviewAgent", {})
    rerun_comment = config.get("rerunComment")
    marker = "<!-- review-agent-auto-rerun -->"
    trigger = f"sha:{head_sha}"

    if not rerun_comment:
        print("No rerunComment configured. Skipping.")
        return 0

    comments_url = f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments"
    comments = github_request(comments_url, "GET", token)
    already_requested = any(
        marker in comment.get("body", "") and trigger in comment.get("body", "")
        for comment in comments
    )
    if already_requested:
        print("Rerun comment already exists for this head.")
        return 0

    github_request(
        comments_url,
        "POST",
        token,
        {"body": f"{marker}\n{rerun_comment}\n{trigger}"},
    )
    print("Posted review rerun comment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
