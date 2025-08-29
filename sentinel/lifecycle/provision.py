import os
import typer
from sentinel.logger import logger
from sentinel import ssh_manager

app = typer.Typer(help="Provision new SSH keys (wizard-style generator)")


@app.command("wizard")
def wizard():
    """
    Interactive wizard to generate a new SSH key and update SSH config.
    """
    typer.echo("\n=== Sentinel Provision Wizard ===")
    typer.echo("This will help you generate a new SSH key for connecting to a server.\n")

    # Step 1: Server identifier
    typer.echo("Step 1: Server Identifier")
    typer.echo("This is the unique name Sentinel will use to identify the server.")
    typer.echo("It will also be used for naming the key files and SSH config entry.")
    typer.echo("Examples: db01.example.com, 192.168.1.50\n")
    server = typer.prompt("Enter server identifier (FQDN or IP)")

    # Step 2: Username
    typer.echo("\nStep 2: Username")
    typer.echo("This is the user you log in as on the server.")
    typer.echo(f"Default is your current user: {os.getenv('USER', 'root')}\n")
    user = typer.prompt("Enter username", default=os.getenv("USER", "root"))

    # Step 3: Algorithm
    typer.echo("\nStep 3: Key Algorithm")
    typer.echo("Choose which type of SSH key to generate:")
    typer.echo("1) ed25519 (default, modern, secure, fast)")
    typer.echo("2) rsa 4096 (compatible, but larger and slower)")
    typer.echo("3) ecdsa (less common, not always recommended)\n")
    choice = typer.prompt("Select [1-3]", default="1")

    algo = "ed25519"
    if choice == "2":
        algo = "rsa"
    elif choice == "3":
        algo = "ecdsa"

    # Generate key
    try:
        key_path = ssh_manager.generate_key(server, user, algo)
        ssh_manager.update_config(server, user, key_path)
        typer.echo(f"\n✅ Key generated and config updated for {server}")
    except FileExistsError as e:
        logger.warning(str(e))
        typer.echo(f"❌ {e}")