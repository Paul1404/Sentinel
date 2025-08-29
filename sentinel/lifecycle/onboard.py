import sys
import os
import subprocess
from pathlib import Path
import typer
from sentinel.logger import logger
from sentinel import ssh_manager

app = typer.Typer(help="Onboard existing SSH keys (wizard-style importer)")


def test_private_key(server: str, user: str, key_path: Path):
    """
    Test an SSH private key by attempting a connection.
    """
    typer.echo("\nTesting private key...")
    try:
        subprocess.run(
            [
                "ssh",
                "-i", str(key_path),
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=5",
                f"{user}@{server}",
                "exit",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        typer.echo(f"✅ Successfully connected to {user}@{server} with {key_path}")
        logger.info(f"[Onboard] Key {key_path} successfully tested for {user}@{server}")
    except subprocess.CalledProcessError:
        typer.echo(f"❌ Failed to authenticate with {key_path}")
        logger.error(f"[Onboard] Failed to authenticate with {key_path}")
    except Exception as e:
        typer.echo(f"❌ Error testing key: {e}")
        logger.error(f"[Onboard] Error testing key: {e}")


@app.command("wizard")
def wizard():
    """
    Interactive wizard to onboard an existing SSH key (private or public).
    """
    typer.echo("\n=== Sentinel Onboard Wizard ===")
    typer.echo("This will help you import an existing SSH key into Sentinel.\n")

    # Step 1: Key type
    typer.echo("Step 1: Key Type")
    typer.echo("1) Private key (your side)")
    typer.echo("2) Public key (others' side)\n")
    choice = typer.prompt("Select [1-2]", default="1")

    if choice == "1":
        # Private key flow
        typer.echo("\nStep 2: Private Key Source")
        typer.echo("1) File path")
        typer.echo("2) Paste into terminal\n")
        method = typer.prompt("Select [1-2]", default="1")

        server = typer.prompt("Enter server identifier (FQDN or IP)")
        user = typer.prompt("Enter username", default=os.getenv("USER", "root"))

        if method == "1":
            key_path = Path(typer.prompt("Enter path to private key file"))
            dest_key = ssh_manager.import_key(server, user, key_path)
            ssh_manager.update_config(server, user, dest_key)
            typer.echo(f"\n✅ Private key imported from {key_path} and config updated for {server}")
        else:
            typer.echo("Paste your private key below. End with CTRL+D on a new line:")
            content = sys.stdin.read().strip()
            if not content.startswith("-----BEGIN"):
                typer.echo("❌ Invalid key format. Must start with '-----BEGIN'")
                return
            dest_key = ssh_manager.import_pasted_key(server, user, content)
            ssh_manager.update_config(server, user, dest_key)
            typer.echo(f"\n✅ Private key pasted and config updated for {server}")

        # Step 3: Test the key
        test = typer.confirm("Do you want to test this key now?", default=True)
        if test:
            test_private_key(server, user, dest_key)

    else:
        # Public key flow (unchanged)
        typer.echo("\nStep 2: Public Key Source")
        typer.echo("1) File path")
        typer.echo("2) Paste into terminal\n")
        method = typer.prompt("Select [1-2]", default="1")

        if method == "1":
            key_path = Path(typer.prompt("Enter path to public key file"))
            ssh_manager.import_public_key_file(key_path)
            typer.echo(f"\n✅ Public key imported from {key_path} into authorized_keys")
        else:
            typer.echo("Paste the public key below. End with CTRL+D on a new line:")
            content = sys.stdin.read().strip()
            if not content.startswith("ssh-"):
                typer.echo("❌ Invalid public key format. Must start with 'ssh-'")
                return
            ssh_manager.import_public_key_paste(content)
            typer.echo("\n✅ Public key pasted into authorized_keys")