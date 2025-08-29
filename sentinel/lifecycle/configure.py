from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from sentinel.logger import logger

app = typer.Typer(help="Manage SSH config and host entries")

SSH_DIR = Path.home() / ".ssh"
CONFIG_FILE = SSH_DIR / "config"
console = Console()


def parse_config() -> dict:
    """
    Parse ~/.ssh/config into a dict of hosts.
    Returns: { "host_alias": { "HostName": ..., "User": ..., "IdentityFile": ... } }
    """
    if not CONFIG_FILE.exists():
        return {}

    hosts = {}
    current_host = None
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("host "):
                current_host = line.split(maxsplit=1)[1]
                hosts[current_host] = {}
            elif current_host:
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    key, value = parts
                    hosts[current_host][key] = value
    return hosts


@app.command("list")
def list_hosts():
    """
    List all hosts from SSH config.
    """
    hosts = parse_config()
    if not hosts:
        typer.echo("No hosts found in SSH config.")
        return

    table = Table(title="SSH Config Hosts")
    table.add_column("Host", style="cyan", no_wrap=True)
    table.add_column("HostName", style="green")
    table.add_column("User", style="yellow")
    table.add_column("IdentityFile", style="magenta")

    for host, details in hosts.items():
        table.add_row(
            host,
            details.get("HostName", "-"),
            details.get("User", "-"),
            details.get("IdentityFile", "-"),
        )

    console.print(table)


@app.command("describe")
def describe(host: str = typer.Argument(..., help="Host alias to describe")):
    """
    Show details of a specific host from SSH config.
    """
    hosts = parse_config()
    if host not in hosts:
        typer.echo(f"❌ Host '{host}' not found in SSH config.")
        return

    details = hosts[host]
    console.print(f"[bold cyan]Host:[/bold cyan] {host}")
    console.print(f"[bold green]HostName:[/bold green] {details.get('HostName', '-')}")
    console.print(f"[bold yellow]User:[/bold yellow] {details.get('User', '-')}")
    console.print(f"[bold magenta]IdentityFile:[/bold magenta] {details.get('IdentityFile', '-')}")
    logger.info(f"[Configure] Described host {host}")


@app.command("remove")
def remove(host: str = typer.Argument(..., help="Host alias to remove")):
    """
    Remove a host entry from SSH config and delete its keys.
    """
    if not CONFIG_FILE.exists():
        typer.echo("No SSH config found.")
        return

    lines = CONFIG_FILE.read_text().splitlines()
    new_lines = []
    skip = False
    removed_identity = None

    for line in lines:
        if line.lower().startswith("host "):
            if line.split(maxsplit=1)[1] == host:
                skip = True
                continue
            else:
                skip = False
        if skip:
            if line.strip().lower().startswith("identityfile"):
                removed_identity = line.split(maxsplit=1)[1].strip()
            continue
        new_lines.append(line)

    if len(new_lines) == len(lines):
        typer.echo(f"❌ Host '{host}' not found in SSH config.")
        return

    CONFIG_FILE.write_text("\n".join(new_lines) + "\n")
    logger.info(f"[Configure] Removed host {host} from SSH config")

    # Delete associated key files if they exist
    if removed_identity:
        priv = Path(removed_identity).expanduser()
        pub = priv.with_suffix(".pub")
        for key_file in [priv, pub]:
            if key_file.exists():
                key_file.unlink()
                logger.info(f"[Configure] Deleted key file {key_file}")

    typer.echo(f"✅ Host '{host}' removed from SSH config and keys deleted (if found).")