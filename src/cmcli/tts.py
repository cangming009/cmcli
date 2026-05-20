"""TTS subcommand — wraps cm-tts (local Qwen3-TTS)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console

console = Console()

CM_TTS_BINS = [
    Path.home() / ".local/bin/cm-tts",
    Path.home() / "anaconda3/bin/cm-tts",
    Path.home() / "Desktop/claude/cli/cm-tts/.venv/bin/cm-tts",
]
CM_TTS_BIN = None
for p in CM_TTS_BINS:
    if p.exists():
        CM_TTS_BIN = str(p)
        break


def _run_cm_tts(args: list[str]) -> None:
    if CM_TTS_BIN:
        cmd = [CM_TTS_BIN] + args
    else:
        cmd = ["cm-tts"] + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


app = typer.Typer(name="tts", help="Text-to-speech via cm-tts (Qwen3-TTS, local)")


@app.command()
def speak(
    text: str = typer.Option("", "--text", "-t", help="Text to synthesize"),
    text_file: str = typer.Option("", "--text-file", "-f", help="Text file"),
    voice: str = typer.Option("me", "--voice", "-v", help="Voice profile name"),
    out: str = typer.Option("./outputs/tts.wav", "--out", "-o", help="Output path"),
    fmt: str = typer.Option("wav", "--format", help="Output format: wav, mp3"),
    speed: float = typer.Option(1.0, "--speed", help="Speed: 0.5-2.0"),
) -> None:
    """Synthesize speech from text or file."""
    args = ["speak"]
    if text:
        args += ["--text", text]
    if text_file:
        args += ["--text-file", text_file]
    args += ["--voice", voice, "--out", out, "--format", fmt, "--speed", str(speed), "--json", "--quiet"]
    _run_cm_tts(args)


@app.command()
def doctor() -> None:
    """Check cm-tts environment."""
    _run_cm_tts(["doctor"])


@app.command()
def profile(
    action: str = typer.Argument("list", help="Action: create/list/delete"),
    name: str = typer.Option("", "--name", "-n", help="Profile name"),
    ref_audio: str = typer.Option("", "--ref-audio", help="Reference audio path"),
    ref_text: str = typer.Option("", "--ref-text", help="Reference audio text"),
) -> None:
    """Manage voice profiles."""
    args = ["profile", action]
    if name:
        args += ["--name", name]
    if ref_audio:
        args += ["--ref-audio", ref_audio]
    if ref_text:
        args += ["--ref-text", ref_text]
    _run_cm_tts(args)
