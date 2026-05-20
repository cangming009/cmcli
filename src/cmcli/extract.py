"""Extract subcommand — wraps url-tools extract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Path to url-tools CLI (also from url-tools-cli in user's cli dir)
URL_TOOLS_BINS = [
    "/opt/anaconda3/bin/url-tools",
    Path.home() / "Desktop/claude/cli/url-tools-cli/bin/url-tools",
    Path.home() / "anaconda3/bin/url-tools",
]
SEARXNG_URL = "http://localhost:8080"
VIDEO_SUBTITLE_SERVICE = Path.home() / "Desktop/claude/video-subtitle-txt"


def _find_url_tools() -> str:
    for p in URL_TOOLS_BINS:
        if Path(p).exists():
            return str(p)
    # try PATH
    r = subprocess.run(["which", "url-tools"], capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip()
    console.print("[red]✗ url-tools not found in PATH or known locations[/red]")
    console.print("[yellow]→ Install: cd ~/Desktop/claude/cli/url-tools-cli && pip install -e .[/yellow]")
    raise typer.Exit(1)


app = typer.Typer(name="extract", help="Extract subtitles/content from B站/YouTube URLs via url-tools")


@app.command()
def main(
    url: str = typer.Argument(..., help="Video URL (B站 or YouTube)"),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text, srt, json"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path"),
    json_flag: bool = typer.Option(False, "--json", help="Output JSON (url-tools native)"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress stdout"),
) -> None:
    """Extract video subtitle/transcript using url-tools CLI."""
    url_tools_bin = _find_url_tools()

    cmd = [url_tools_bin, "extract", url]
    if json_flag:
        cmd.append("--json")
    if format != "text":
        cmd.extend(["--format", format])
    if quiet:
        cmd.append("--quiet")
    if output:
        cmd.extend(["--output", output])

    if not quiet:
        console.print(f"[cyan]→[/cyan] Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=False)
    sys.exit(result.returncode)
