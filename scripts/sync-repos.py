#!/usr/bin/env python3
"""Copy agent-charter plugins into other repositories, as sync.json says.

Each plugin lands verbatim at <repo>/.claude/skills/<plugin>/, where Claude Code
loads it as <plugin>@skills-dir (cloud sessions included) under its usual names.
The sync owns those folders and <repo>/.claude/agent-charter.json, which lists
the plugins it put there, and nothing else in the repository.

  sync-repos.py list                        repositories in sync.json, as JSON
  sync-repos.py apply DIR PLUGIN...         write the plugins into a local checkout
  sync-repos.py sync OWNER/REPO [options]   branch, commit, PR and merge one repo

Needs git and an authenticated gh. See MAINTAINING.md, "Syncing into repositories".
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = Path(".claude/agent-charter.json")
SKILLS = Path(".claude/skills")
SOURCE = "StephanRyatt/agent-charter"


def run(*cmd, cwd=None, check=True, capture=True):
    result = subprocess.run(cmd, cwd=cwd, check=False, text=True,
                            stdout=subprocess.PIPE if capture else None)
    if check and result.returncode != 0:
        sys.exit(f"command failed ({result.returncode}): {' '.join(cmd)}")
    return result.stdout.strip() if capture else ""


def load_config():
    config = json.loads((ROOT / "sync.json").read_text())
    known = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    for repo, entry in config["repos"].items():
        unknown = set(entry["plugins"]) - known
        if unknown:
            sys.exit(f"sync.json: {repo} names unknown plugins {sorted(unknown)}")
        if entry.get("merge", "auto") not in ("auto", "manual"):
            sys.exit(f"sync.json: {repo} merge must be auto or manual")
    return config


def plugin_version(name, ref):
    manifest = run("git", "show", f"{ref}:plugins/{name}/.claude-plugin/plugin.json", cwd=ROOT)
    return json.loads(manifest).get("version", "unversioned")


def managed_plugins(checkout):
    lock = checkout / LOCK
    return json.loads(lock.read_text())["plugins"] if lock.exists() else []


def apply(checkout, plugins, ref="HEAD"):
    """Make checkout's managed folders match plugins at ref. Returns the managed paths."""
    previous = managed_plugins(checkout)
    for name in plugins:
        target = checkout / SKILLS / name
        if name not in previous and (target.exists() or target.is_symlink()):
            sys.exit(f"{target} exists but the sync doesn't own it; move it first")
    for name in set(previous) | set(plugins):
        target = checkout / SKILLS / name
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            shutil.rmtree(target)
    (checkout / SKILLS).mkdir(parents=True, exist_ok=True)
    for name in plugins:
        # git archive copies the committed plugin only, never local edits.
        archive = subprocess.run(["git", "archive", ref, f"plugins/{name}"], cwd=ROOT,
                                 check=True, stdout=subprocess.PIPE).stdout
        subprocess.run(["tar", "-x", "--strip-components=1", "-C", str(checkout / SKILLS)],
                       input=archive, check=True)
    lock = {
        "source": f"https://github.com/{SOURCE}",
        "note": "Written by agent-charter's sync. Edit the plugins in agent-charter, not here.",
        "plugins": sorted(plugins),
    }
    if plugins:
        (checkout / LOCK).write_text(json.dumps(lock, indent=2) + "\n")
    elif (checkout / LOCK).exists():
        (checkout / LOCK).unlink()
    return [str(SKILLS / n) for n in set(previous) | set(plugins)] + [str(LOCK)]


def open_pr(repo, branch):
    prs = json.loads(run("gh", "pr", "list", "-R", repo, "--head", branch, "--state", "open",
                         "--json", "number"))
    return prs[0]["number"] if prs else None


def wait_for_checks(repo, number, timeout):
    """Return True when every check passed (or none exist), False on a failure."""
    deadline = time.time() + timeout
    time.sleep(20)  # give CI time to register its checks
    while True:
        result = subprocess.run(["gh", "pr", "view", str(number), "-R", repo,
                                 "--json", "statusCheckRollup"], text=True, capture_output=True)
        if result.returncode != 0:
            print(f"couldn't read checks: {result.stderr.strip()}")
            return False
        # Check runs report status and conclusion; commit statuses report state.
        states = {}
        for c in json.loads(result.stdout)["statusCheckRollup"]:
            name = c.get("name") or c.get("context")
            if (c.get("status") or "COMPLETED") != "COMPLETED":
                states[name] = "pending"
            else:
                outcome = c.get("conclusion") or c.get("state")
                states[name] = {"SUCCESS": "pass", "NEUTRAL": "pass", "SKIPPED": "pass",
                                "PENDING": "pending", "EXPECTED": "pending"}.get(outcome, "fail")
        failed = [n for n, s in states.items() if s == "fail"]
        if failed:
            print(f"checks failed: {', '.join(failed)}")
            return False
        if "pending" not in states.values():
            return True
        if time.time() > deadline:
            print("checks still pending at the timeout")
            return False
        time.sleep(30)


def sync(repo, ref, dry_run, no_merge, timeout):
    config = load_config()
    if repo not in config["repos"]:
        sys.exit(f"{repo} is not in sync.json")
    entry = config["repos"][repo]
    branch = config["branch"]
    commit = run("git", "rev-parse", ref, cwd=ROOT)
    work = Path(tempfile.mkdtemp(prefix="agent-charter-sync-"))
    try:
        checkout = work / "repo"
        run("gh", "repo", "clone", repo, str(checkout), "--", "--filter=blob:none", "--quiet")
        base = run("git", "rev-parse", "--abbrev-ref", "origin/HEAD", cwd=checkout).split("/", 1)[1]
        run("git", "switch", "-q", "-C", branch, f"origin/{base}", cwd=checkout)
        removed = sorted(set(managed_plugins(checkout)) - set(entry["plugins"]))
        owned = apply(checkout, entry["plugins"], ref)
        run("git", "add", "-A", "--", *owned, cwd=checkout)
        existing = open_pr(repo, branch)
        if not run("git", "diff", "--cached", "--name-only", cwd=checkout):
            print(f"{repo}: already up to date with agent-charter {commit[:7]}")
            if existing and not dry_run:
                run("gh", "pr", "close", str(existing), "-R", repo, "--delete-branch",
                    "--comment", f"Superseded: {base} already matches agent-charter {commit[:7]}.")
            return
        versions = ", ".join(f"{n} {plugin_version(n, ref)}" for n in entry["plugins"])
        title = f"Sync agent-charter plugins ({versions})"
        body = "\n".join([
            f"Copies agent-charter plugins at [{commit[:7]}](https://github.com/{SOURCE}/commit/{commit}) "
            f"into `.claude/skills/`, where Claude Code loads them as `<plugin>@skills-dir`, "
            "cloud sessions included.",
            "",
            f"- Plugins: {versions}",
            *( [f"- Removed: {', '.join(removed)}"] if removed else [] ),
            "",
            "Opened by agent-charter's sync workflow. It changes only the folders listed in "
            "`.claude/agent-charter.json` and that file. Edit the plugins in agent-charter, not here; "
            "the next sync overwrites local edits.",
        ])
        print(run("git", "diff", "--cached", "--stat", cwd=checkout))
        if dry_run:
            print(f"{repo}: dry run, would open: {title}")
            return
        run("git", "commit", "-q", "-m", f"{title}\n\nagent-charter {commit}", cwd=checkout)
        run("git", "push", "-q", "--force", "origin", branch, cwd=checkout)
        head = run("git", "rev-parse", "HEAD", cwd=checkout)
        if existing:
            run("gh", "pr", "edit", str(existing), "-R", repo, "--title", title, "--body", body)
            number = existing
        else:
            url = run("gh", "pr", "create", "-R", repo, "--base", base, "--head", branch,
                      "--title", title, "--body", body)
            number = int(url.rstrip("/").rsplit("/", 1)[1])
        print(f"{repo}: PR #{number}")
        if no_merge or entry.get("merge", "auto") == "manual":
            return
        # Merge only this PR, and only while it changes nothing but the sync's own paths.
        files = run("gh", "pr", "diff", str(number), "-R", repo, "--name-only").splitlines()
        stray = [f for f in files if not any(f == o or f.startswith(o + "/") for o in owned)]
        if stray:
            sys.exit(f"{repo}: PR #{number} touches paths the sync doesn't own: {stray}")
        if not wait_for_checks(repo, number, timeout):
            sys.exit(f"{repo}: PR #{number} left open for review")
        run("gh", "pr", "merge", str(number), "-R", repo, "--squash", "--delete-branch",
            "--match-head-commit", head)
        print(f"{repo}: merged PR #{number}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p_apply = sub.add_parser("apply")
    p_apply.add_argument("checkout", type=Path)
    p_apply.add_argument("plugins", nargs="*")
    p_apply.add_argument("--ref", default="HEAD")
    p_sync = sub.add_parser("sync")
    p_sync.add_argument("repo")
    p_sync.add_argument("--ref", default="HEAD")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.add_argument("--no-merge", action="store_true")
    p_sync.add_argument("--timeout", type=int, default=1800, help="seconds to wait for checks")
    args = parser.parse_args()
    if args.command == "list":
        print(json.dumps(sorted(load_config()["repos"])))
    elif args.command == "apply":
        load_config()
        apply(args.checkout.resolve(), args.plugins, args.ref)
    else:
        sync(args.repo, args.ref, args.dry_run, args.no_merge, args.timeout)


if __name__ == "__main__":
    main()
