"""SearXNG search command — registered as `cmcli search <query>`."""

from __future__ import annotations

import json
from typing import Optional

import httpx
import typer
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_URL = "http://localhost:8080"


def search(
    query: str = typer.Argument(..., help="Search query"),
    engine: str = typer.Option("bing,baidu", "--engine", "-e",
        help="Comma-separated engines (google,baidu,bing,github,arxiv,...)"),
    lang: str = typer.Option("auto", "--lang", "-l",
        help="Language code (auto, zh-CN, en, ...)"),
    time_range: Optional[str] = typer.Option(None, "--time",
        help="Time range: day, week, month, year"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    md: bool = typer.Option(False, "--md", help="Output as Markdown list"),
    searx_url: str = typer.Option(DEFAULT_URL, "--url", help="SearXNG URL"),
) -> None:
    """Search using local SearXNG instance.

    Examples:

        cmcli search "AI Agent"
        cmcli search "bilibili tools" --engine google,baidu --lang zh-CN
        cmcli search "opencli" --time month --md
    """
    params = {
        "q": query,
        "format": "json",
        "engines": engine,
        "language": lang,
        "limit": limit,
    }
    if time_range:
        params["time_range"] = time_range

    try:
        resp = httpx.get(
            f"{searx_url.rstrip('/')}/search",
            params=params,
            timeout=15,
            follow_redirects=True,
        )
        resp.raise_for_status()
        data = resp.json()
    except httpx.ConnectError:
        console.print(f"[red]✗ Cannot connect to SearXNG at {searx_url}[/red]")
        console.print("[yellow]→ Is docker searxng-core running?  docker start searxng-core[/yellow]")
        raise typer.Exit(1)
    except httpx.HTTPStatusError as e:
        console.print(f"[red]✗ HTTP {e.response.status_code}[/red]")
        raise typer.Exit(1)

    results = data.get("results", [])
    if not results:
        console.print("[dim]No results found.[/dim]")
        return

    if json_output:
        console.print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if md:
        _print_markdown(query, results)
        return

    table = Table(title=f"🔍 {query}", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="white")
    table.add_column("Engine", style="dim", width=10)
    table.add_column("Date", style="dim", width=12)

    for i, r in enumerate(results[:limit], 1):
        title = r.get("title", "")[:80]
        url = r.get("url", "")
        table.add_row(
            str(i),
            f"[link={url}]{title}[/link]",
            r.get("engine", ""),
            r.get("publishedDate", "—"),
        )

    console.print(table)
    console.print(
        f"\n[dim]✓ {len(results)} results  ·  engine={engine}"
        f"  ·  {data.get('time','?')}s[/dim]"
    )


def _print_markdown(query: str, results: list) -> None:
    lines = [
        f"## 🔍 {query}",
        "",
        "| # | 标题 | 来源 | 日期 |",
        "|---|---|---|---|",
    ]
    for i, r in enumerate(results, 1):
        title = r.get("title", "")[:60].replace("|", "\\|")
        url = r.get("url", "")
        lines.append(
            f"| {i} | [{title}]({url}) | {r.get('engine','')} | {r.get('publishedDate','—')} |"
        )
    console.print("\n".join(lines))
