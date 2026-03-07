#!/usr/bin/env python3

import os
import pathlib
import sys

from common import any_changed, compute_risk_tier, git_changed_files, load_policy, load_repo_config, set_output, stringify_json


def main() -> int:
    control_repo = pathlib.Path(os.environ["CODE_FACTORY_DIR"])
    base_sha = os.environ.get("BASE_SHA", "")
    head_sha = os.environ.get("HEAD_SHA", "")

    policy = load_policy(control_repo)
    repo_config = load_repo_config()
    changed_files = git_changed_files(base_sha, head_sha)
    risk_tier = compute_risk_tier(changed_files, policy.get("riskTierRules", {}))
    required_checks = policy.get("mergePolicy", {}).get(risk_tier, {}).get("requiredChecks", ["risk-policy-gate", "CI Pipeline"])

    docs_drift_rules = policy.get("docsDriftRules", {})
    control_paths = docs_drift_rules.get("controlPlanePaths", [])
    docs_paths = docs_drift_rules.get("docsPaths", [])
    docs_ok = True
    if control_paths and docs_paths and any_changed(changed_files, control_paths):
        docs_ok = any_changed(changed_files, docs_paths)

    browser_config = repo_config.get("browserEvidence", {})
    review_config = repo_config.get("reviewAgent", {})
    browser_required = any_changed(changed_files, browser_config.get("requiredPaths", []))
    review_required = any_changed(changed_files, review_config.get("requiredPaths", []))

    summary_lines = [
        "## Code Factory preflight",
        f"- Risk tier: `{risk_tier}`",
        f"- Changed files: `{len(changed_files)}`",
        f"- Required checks: `{', '.join(required_checks)}`",
        f"- Browser evidence required: `{browser_required}`",
        f"- Review agent required: `{review_required}`",
        f"- Docs drift check: `{docs_ok}`",
    ]

    summary_target = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_target:
        with open(summary_target, "a", encoding="utf-8") as handle:
            handle.write("\n".join(summary_lines) + "\n")

    set_output("risk_tier", risk_tier)
    set_output("required_checks", stringify_json(required_checks))
    set_output("browser_required", str(browser_required).lower())
    set_output("review_required", str(review_required).lower())
    set_output("changed_files", stringify_json(changed_files))

    if not docs_ok:
        print("Control-plane files changed without a matching documentation update.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
