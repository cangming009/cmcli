"""Main cmcli app — unified CLI for search, extract, bilibili, tts."""

from __future__ import annotations

import typer

from cmcli import __version__
from cmcli.search import search as search_fn
from cmcli.extract import app as extract_app
from cmcli.bilibili import app as bilibili_app
from cmcli.tts import app as tts_app

app = typer.Typer(
    name="cmcli",
    help="[bold cyan]cmcli[/bold cyan] — CMC's unified CLI\n\n"
         "  🔍 search   SearXNG metasearch (docker: searxng-core)\n"
         "  📦 extract  Video subtitle extraction (url-tools)\n"
         "  📺 bilibili opencli bilibili commands\n"
         "  🔊 tts      Local Qwen3-TTS voice synthesis\n\n"
         "Examples:\n"
         "  cmcli search \"AI Agent\" --engine bing,baidu\n"
         "  cmcli extract https://www.bilibili.com/video/BVxxxx\n"
         "  cmcli bilibili user-videos 18052876 --limit 5\n"
         "  cmcli tts speak --text \"你好\" --voice me -o hello.wav\n",
    no_args_is_help=True,
)

app.command("search")(search_fn)
app.add_typer(extract_app, name="extract")
app.add_typer(bilibili_app, name="bilibili")
app.add_typer(tts_app, name="tts")


@app.command()
def version(
    short: bool = typer.Option(False, "--short", help="Short version"),
) -> None:
    """Print cmcli version."""
    from rich.console import Console
    console = Console()
    if short:
        console.print(__version__)
    else:
        console.print(f"[bold cyan]cmcli[/bold cyan] v{__version__}")


if __name__ == "__main__":
    app()
