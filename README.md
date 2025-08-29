# Sentinel – SSH Lifecycle Manager

Sentinel is a CLI tool for managing the lifecycle of SSH keys.  
It provides guided **wizard flows** for provisioning new keys, onboarding existing keys, and managing SSH configuration.

---

## Current Status

- **Provision wizard** – generate new SSH keys interactively.  
- **Onboard wizard** – import existing private or public keys (file or paste) interactively.  
- **Configure** – list, describe, and remove hosts from `~/.ssh/config`.  
- **Logging** – console, file (`~/.sentinel/sentinel.log`), and syslog (on RHEL).  
- **Shell completion** – available via Typer (`--install-completion`).  

---

## Development Setup

Sentinel is developed with [Python 3.12+] and [uv](https://github.com/astral-sh/uv) as the package manager.  
The recommended environment is GitHub Codespaces with a devcontainer.

### 1. Clone the repository
```bash
git clone https://github.com/Paul1404/Sentinel.git
cd Sentinel
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Run Sentinel
```bash
uv run python sentinel.py --help
```

---

## Usage

### Provision Wizard
Generate a new SSH key and update `~/.ssh/config`:
```bash
uv run python sentinel.py provision wizard
```

### Onboard Wizard
Import an existing private or public key:
```bash
uv run python sentinel.py onboard wizard
```

### Configure
List all hosts:
```bash
uv run python sentinel.py configure list
```

Describe a host:
```bash
uv run python sentinel.py configure describe <host>
```

Remove a host:
```bash
uv run python sentinel.py configure remove <host>
```

---

## Logging

Sentinel logs to multiple destinations:

- Console (always).  
- File: `~/.sentinel/sentinel.log` (or `/var/log/sentinel.log` if writable).  
- Syslog/journald on RHEL (`/dev/log`).  

---

## Shell Completion

Typer provides built‑in shell completion.

Show the completion script:
```bash
uv run python sentinel.py --show-completion
```

Install completion for your shell:
```bash
uv run python sentinel.py --install-completion
```

Reload your shell:
```bash
exec $SHELL
```

---

## Project Structure

```
sentinel.py              # Main CLI entrypoint
sentinel/
├── logger.py            # Logging setup
├── ssh_manager.py       # Low-level SSH operations
└── lifecycle/
    ├── provision.py     # Wizard for generating new keys
    ├── onboard.py       # Wizard for importing existing keys
    └── configure.py     # Manage SSH config (list, describe, remove)
```

---

## Development Notes

- Sentinel is built with [Typer](https://typer.tiangolo.com/) for CLI and [Rich](https://rich.readthedocs.io/) for output formatting.  
- Wizards use `typer.prompt` and `typer.confirm` for interactive flows.  
- SSH operations are handled via `ssh-keygen`, `ssh`, and file manipulation in `ssh_manager.py`.  
- Logging is centralized in `sentinel/logger.py`.  

---

## Roadmap

- Add **Distribute** stage (copy public keys to remote servers, import others’ keys).  
- Add **Maintain** stage (rotate keys, audit, backup/restore).  
- Add a **top‑level wizard** (`sentinel.py wizard`) to choose Provision, Onboard, or Configure from a single entrypoint.  
- Add developer tests with `pytest`.  
- Package Sentinel as a standalone binary (via PyInstaller or uv build).  

---

## License

MIT License – see [LICENSE](./LICENSE).