# AGENTS.md — cmcli

## Who is this agent?

This is **cmcli**, a Python CLI tool for CMC's personal AI agent workflows.
It wraps three core tools: SearXNG (search), url-tools (subtitle extraction), and opencli (B站 automation).

## What this repo does

- `cmcli search <query>` — Metasearch via local SearXNG docker instance
- `cmcli extract <url>` — Extract subtitles from B站/YouTube videos
- `cmcli bilibili user-videos <uid>` — Fetch B站 user video list
- `cmcli bilibili search <keyword>` — Search B站 videos
- `cmcli bilibili hot` — Get B站 hot videos

## Architecture

```
cmcli/
├── src/cmcli/
│   ├── cli.py       # Main app (typer), registers subcommands
│   ├── search.py    # SearXNG search subcommand
│   ├── extract.py   # url-tools wrapper subcommand
│   └── bilibili.py  # opencli bilibili wrapper subcommands
├── pyproject.toml
└── README.md
```

## Adding new commands

1. Create a new `*.py` file under `src/cmcli/`
2. Use `typer.Typer` and `@app.command()` decorator
3. Import and register in `cli.py`:
   ```python
   from cmcli.newcmd import app as newcmd_app
   app.add_typer(newcmd_app, name="newcmd")
   ```

## Dependencies

- Python >= 3.12
- typer >= 0.12
- rich >= 13.0
- httpx >= 0.27

## Local dev

```bash
cd ~/Desktop/claude/cli/cmcli
pip install -e ".[dev]"
cmcli --help
```

## Running tests

```bash
pytest tests/
ruff check src/
```
