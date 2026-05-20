# cmcli

> CMC's unified CLI: search, extract, bilibili — one tool for all your agentic workflows.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Features

| Command | Description |
|---|---|
| `cmcli search` | 🔍 SearXNG metasearch (privacy-friendly, 244 engines, local docker) |
| `cmcli extract` | 📦 Extract video subtitles from B站 / YouTube via url-tools |
| `cmcli bilibili` | 📺 Bilibili user videos, hot list, search via opencli |
| `cmcli tts` | 🔊 Local Qwen3-TTS voice synthesis via cm-tts |

## Install

### From source

```bash
cd ~/Desktop/claude/cli/cmcli
pip install -e .
```

Or with uv:

```bash
cd ~/Desktop/claude/cli/cmcli
uv pip install -e .
```

### Prerequisites

- **SearXNG** (docker) — for `cmcli search`
  ```bash
  docker run -d --name searxng-core \
    -p 8080:8080 \
    -v $(pwd)/settings.yml:/etc/searxng/settings.yml \
    searxng/searxng:latest
  ```

- **url-tools** — for `cmcli extract`
  ```bash
  cd ~/Desktop/claude/cli/url-tools-cli
  pip install -e .
  ```

- **opencli** (@jackwener/opencli) — for `cmcli bilibili`
  ```bash
  npm install -g @jackwener/opencli
  ```

- **cm-tts** (local Qwen3-TTS) — for `cmcli tts`
  ```bash
  cd ~/Desktop/claude/cli/cm-tts
  pip install -e .
  ```

---

## Commands

### 🔍 `cmcli search`

```bash
# Basic search
cmcli search "AI Agent"

# Specify engines
cmcli search "bilibili tools" --engine google,baidu

# Chinese results
cmcli search "大模型" --lang zh-CN

# Time filter
cmcli search "opencli" --time month

# Markdown output
cmcli search "Claude Code MCP" --engine google --md

# JSON output
cmcli search "Hermes Agent" --json
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--engine, -e` | `google` | Comma-separated engines |
| `--lang, -l` | `auto` | Language code |
| `--time` | — | `day`, `week`, `month`, `year` |
| `--limit, -n` | `10` | Max results |
| `--json` | false | Raw JSON output |
| `--md` | false | Markdown table output |

**Supported engines:** google, bing, baidu, sogou, brave, duckduckgo, github, arxiv, google_scholar, wikipedia, and 234 more.

---

### 📦 `cmcli extract`

```bash
# Extract from B站 video
cmcli extract https://www.bilibili.com/video/BV1TZ5Y6CEH1

# Output as SRT
cmcli extract <url> --format srt -o subtitle.srt

# JSON (url-tools native)
cmcli extract <url> --json
```

---

### 📺 `cmcli bilibili`

```bash
# User's recent videos
cmcli bilibili user-videos 18052876 --limit 5

# Search Bilibili
cmcli bilibili search "AI编程" --limit 10

# Hot list
cmcli bilibili hot --limit 20
```

---

### 🔊 `cmcli tts`

```bash
# Text-to-speech (requires cm-tts installed)
cmcli tts speak --text "你好世界" --voice me -o hello.wav

# From text file
cmcli tts speak --text-file article.txt --voice me -o article.wav

# Check environment
cmcli tts doctor
```

---

## Config

| Env | Default | Description |
|---|---|---|
| `SEARXNG_URL` | `http://localhost:8080` | SearXNG instance URL |

---

## License

MIT © cangming
