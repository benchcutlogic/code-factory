#!/usr/bin/env python3

import json
import pathlib
import subprocess
import sys

from common import load_repo_config


ROOT = pathlib.Path.cwd()


def package_scripts() -> dict[str, str]:
    package_json = ROOT / "package.json"
    if not package_json.exists():
        return {}
    with package_json.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("scripts", {})


def infer_commands() -> list[str]:
    commands: list[str] = []
    if (ROOT / "pnpm-lock.yaml").exists():
        commands.append("corepack enable")
        commands.append("pnpm install --frozen-lockfile")
        scripts = package_scripts()
        for name in ["lint", "typecheck", "test", "build:ci", "build"]:
            if name in scripts:
                commands.append(f"pnpm run {name}")
    elif (ROOT / "package-lock.json").exists():
        commands.append("npm ci")
        scripts = package_scripts()
        for name in ["lint", "typecheck", "test", "build:ci", "build"]:
            if name in scripts:
                commands.append(f"npm run {name}")
    elif (ROOT / "package.json").exists():
        commands.append("npm install")
        scripts = package_scripts()
        for name in ["lint", "typecheck", "test", "build:ci", "build"]:
            if name in scripts:
                commands.append(f"npm run {name}")
    elif (ROOT / "Cargo.toml").exists():
        commands.append("cargo test --all")
    return commands


def run_command(command: str) -> None:
    print(f"$ {command}", flush=True)
    subprocess.run(command, shell=True, check=True)


def main() -> int:
    config = load_repo_config()
    commands = config.get("ci", {}).get("commands") or infer_commands()
    if not commands:
        print("No CI commands configured or inferred. Passing without execution.")
        return 0

    for command in commands:
        run_command(command)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print(f"Command failed with exit code {error.returncode}.", file=sys.stderr)
        raise SystemExit(error.returncode)
