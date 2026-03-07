import fnmatch
import json
import os
import pathlib
import subprocess
from typing import Any


ROOT = pathlib.Path.cwd()


def load_json(path: pathlib.Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = merge_dict(current, value)
        else:
            merged[key] = value
    return merged


def load_policy(control_repo: pathlib.Path) -> dict[str, Any]:
    default_policy = load_json(
        control_repo / "policy" / "default-risk-policy.json",
        {},
    )
    repo_policy = load_json(ROOT / ".code-factory" / "policy.json", {})
    return merge_dict(default_policy, repo_policy)


def load_repo_config() -> dict[str, Any]:
    return load_json(ROOT / ".code-factory" / "config.json", {})


def git_changed_files(base_sha: str, head_sha: str) -> list[str]:
    if not base_sha or not head_sha:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}..{head_sha}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches_any(path: str, patterns: list[str]) -> bool:
    normalized = path.lstrip("./")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def compute_risk_tier(files: list[str], rules: dict[str, list[str]]) -> str:
    order = ["critical", "high", "medium", "low"]
    for tier in order:
        patterns = rules.get(tier, [])
        if any(matches_any(path, patterns) for path in files):
            return tier
    return "low"


def any_changed(files: list[str], patterns: list[str]) -> bool:
    return any(matches_any(path, patterns) for path in files)


def set_output(key: str, value: str) -> None:
    target = os.environ.get("GITHUB_OUTPUT")
    if not target:
        return
    with open(target, "a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def stringify_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"))


def repo_file_exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()
