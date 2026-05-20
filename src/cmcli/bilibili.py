"""Bilibili subcommand — wraps opencli bilibili commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

console = Console()

OPENCLI_BINS = [
    Path.home() / "npm-global/bin/opencli",
    Path.home() / "Desktop/claude/cli/opencli/bin/opencli",
]
OPENCLI_BIN = None
for p in OPENCLI_BINS:
    if p.exists():
        OPENCLI_BIN = str(p)
        break


def _run_opencli(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    if OPENCLI_BIN:
        cmd = [OPENCLI_BIN] + args
    else:
        cmd = ["opencli"] + args  # rely on PATH
    return subprocess.run(cmd, **kwargs)


app = typer.Typer(name="bilibili", help="Bilibili tools via opencli (user-videos, search, ...)")


@app.command("user-videos")
def user_videos(
    uid: str = typer.Argument(..., help="Bilibili user UID"),
    limit: int = typer.Option(5, "--limit", "-n", help="Number of videos"),
    format: str = typer.Option("md", "--format", "-f", help="Output format: md, json, csv"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress extra output"),
) -> None:
    """Fetch recent videos from a Bilibili user (by UID)."""
    args = ["bilibili", "user-videos", uid, "--limit", str(limit), "-f", format]
    if quiet:
        args.append("--quiet")

    result = _run_opencli(args, capture_output=False)
    sys.exit(result.returncode)


@app.command("search")
def bilibili_search(
    keyword: str = typer.Argument(..., help="Search keyword"),
    limit: int = typer.Option(20, "--limit", "-n", help="Number of results"),
    format: str = typer.Option("md", "--format", "-f", help="Output format: md, json"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress extra output"),
) -> None:
    """Search Bilibili videos by keyword."""
    args = ["bilibili", "search", keyword, "--limit", str(limit), "-f", format]
    if quiet:
        args.append("--quiet")

    result = _run_opencli(args, capture_output=False)
    sys.exit(result.returncode)


@app.command("hot")
def bilibili_hot(
    limit: int = typer.Option(20, "--limit", "-n", help="Number of results"),
    format: str = typer.Option("md", "--format", "-f", help="Output format: md, json"),
) -> None:
    """Get Bilibili hot videos (public API, no auth required)."""
    args = ["bilibili", "hot", "--limit", str(limit), "-f", format]
    result = _run_opencli(args, capture_output=False)
    sys.exit(result.returncode)
