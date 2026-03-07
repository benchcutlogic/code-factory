#!/usr/bin/env python3

import os
import subprocess
import sys

from common import load_repo_config


def run_command(command: str) -> None:
    print(f"$ {command}", flush=True)
    subprocess.run(command, shell=True, check=True)


def main() -> int:
    required = os.environ.get("BROWSER_REQUIRED", "false").lower() == "true"
    config = load_repo_config().get("browserEvidence", {})
    capture_command = config.get("captureCommand")
    verify_command = config.get("verifyCommand")

    if capture_command:
        run_command(capture_command)
    if verify_command:
        run_command(verify_command)

    if required and not verify_command:
        print("Browser evidence is required but no verify command is configured.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)
