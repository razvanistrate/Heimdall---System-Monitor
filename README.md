# Heimdall 🔱

> A terminal-based system monitor built with Python and Textual 

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-TUI-1a1a2e?style=flat-square)
![psutil](https://img.shields.io/badge/psutil-system-green?style=flat-square)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

## Overview

Heimdall is a modern system monitor that lives entirely in your terminal. Inspired by the all-seeing Norse god, it watches over your machine's CPU, memory, disk, and processes in real time — with a clean, keyboard-navigable TUI interface powered by [Textual](https://github.com/Textualize/textual).

No GUI. No bloat. Just your system, laid bare.


## Features

- **CPU monitoring** — per-core usage, frequency, and load average
- **Memory & swap** — usage breakdown with visual progress bars
- **Disk I/O** — per-partition usage and read/write stats
- **Process list** — sortable table with per-process CPU and memory usage
- **Real-time updates** — live refresh with configurable interval

## Tech Stack

| Tool | Role |
|------|------|
| [Python 3.11+](https://python.org) | Core language |
| [Textual](https://github.com/Textualize/textual) | TUI framework |
| [psutil](https://github.com/giampaolo/psutil) | System metrics collection |
| [uv](https://github.com/astral-sh/uv) | Package & project management |


## Requirements

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) — install it with:

bash:
curl -LsSf https://astral.sh/uv/install.sh | sh


## Installation

# Clone the repository
git clone https://github.com/razvanistrate/Heimdall---System-Monitor.git 
&& cd heimdall

# Create virtual environment and install dependencies
uv sync

# Run Heimdall
uv run heimdall

## Usage

bash:
uv run heimdall

### Keyboard shortcuts

## Project Structure


heimdall/
├── heimdall/
│   ├── __init__.py
│   ├── app.py          # Main Textual app entry point
│   ├── cpu.py          # CPU monitoring module
│   ├── memory.py       # Memory & swap module
│   ├── disk.py         # Disk usage & I/O module
│   └── processes.py    # Process list module
├── pyproject.toml
└── README.md


## Development

bash:
# Install dev dependencies
uv sync --dev

# Run in development mode
uv run heimdall

# Run tests
uv run pytest

## Roadmap

- [V] Network I/O monitoring
- [X] GPU usage (via `gputil` / `pynvml`)
- [X] Configurable refresh rate via CLI flags
- [V] Color theme support
- [V] macOS full support for all modules

## License

MIT — see [LICENSE](LICENSE) for details.

<p align="center">
  <i>Heimdall watches. Always.</i>
</p>
