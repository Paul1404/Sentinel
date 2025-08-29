#!/usr/bin/env python3
import typer
from sentinel.logger import logger
from sentinel.lifecycle import provision, onboard, configure

# Main Typer app
app = typer.Typer(
    help="Sentinel - SSH Lifecycle Manager\n\n"
         "Manage SSH keys and configuration with a guided lifecycle approach."
)

# Register lifecycle subcommands
app.add_typer(provision.app, name="provision", help="Provision new SSH keys (generator)")
app.add_typer(onboard.app, name="onboard", help="Onboard existing SSH keys (importer)")
app.add_typer(configure.app, name="configure", help="Manage SSH config (list, describe, remove)")


@app.callback()
def main():
    """
    Sentinel CLI entrypoint.
    """
    logger.info("Starting Sentinel CLI")


if __name__ == "__main__":
    app()