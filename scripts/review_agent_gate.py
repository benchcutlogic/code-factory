#!/usr/bin/env python3

import json
import os
import sys
import time
import urllib.error
import urllib.request

from common import load_repo_config


def github_api(url: str, token: str) -> dict:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    required = os.environ.get("REVIEW_REQUIRED", "false").lower() == "true"
    config = load_repo_config().get("reviewAgent", {})
    check_name = config.get("checkRunName", "")
    acceptable = set(config.get("acceptableConclusions", ["success"]))
    timeout_minutes = int(config.get("timeoutMinutes", 20))
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    head_sha = os.environ.get("HEAD_SHA", "")

    if not required:
        print("Review agent is not required for this PR. Passing.")
        return 0

    if not check_name:
        print("Review agent is required but no checkRunName is configured.", file=sys.stderr)
        return 1

    if not token or not repository or not head_sha:
        print("Missing GitHub context for review agent validation.", file=sys.stderr)
        return 1

    deadline = time.time() + timeout_minutes * 60
    api_url = f"https://api.github.com/repos/{repository}/commits/{head_sha}/check-runs"

    while time.time() < deadline:
        payload = github_api(api_url, token)
        for check_run in payload.get("check_runs", []):
            if check_run.get("name") != check_name:
                continue
            status = check_run.get("status")
            conclusion = check_run.get("conclusion")
            if status != "completed":
                break
            if conclusion in acceptable:
                print(f"Review agent check `{check_name}` completed with `{conclusion}`.")
                return 0
            print(f"Review agent check `{check_name}` completed with `{conclusion}`.", file=sys.stderr)
            return 1
        time.sleep(30)

    print(f"Timed out waiting for review agent check `{check_name}` on {head_sha}.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as error:
        print(f"GitHub API request failed: {error}", file=sys.stderr)
        raise SystemExit(1)
