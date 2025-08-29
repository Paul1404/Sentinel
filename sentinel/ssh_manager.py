import subprocess
from pathlib import Path
from sentinel.logger import logger

SSH_DIR = Path.home() / ".ssh"
CONFIG_FILE = SSH_DIR / "config"


def ensure_ssh_dir():
    SSH_DIR.mkdir(mode=0o700, exist_ok=True)


def generate_key(server: str, user: str, algo: str = "ed25519") -> Path:
    """
    Generate a new SSH key for a server.
    Returns the path to the private key.
    """
    ensure_ssh_dir()
    key_name = f"id_{algo}_{server}"
    key_path = SSH_DIR / key_name

    if key_path.exists():
        raise FileExistsError(f"Key already exists: {key_path}")

    if algo == "rsa":
        cmd = ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", str(key_path), "-C", f"{user}@{server}", "-N", ""]
    elif algo == "ecdsa":
        cmd = ["ssh-keygen", "-t", "ecdsa", "-f", str(key_path), "-C", f"{user}@{server}", "-N", ""]
    else:  # default ed25519
        cmd = ["ssh-keygen", "-t", "ed25519", "-f", str(key_path), "-C", f"{user}@{server}", "-N", ""]

    logger.info(f"Generating {algo} key for {user}@{server}")
    subprocess.run(cmd, check=True)

    key_path.chmod(0o600)
    if key_path.with_suffix(".pub").exists():
        key_path.with_suffix(".pub").chmod(0o644)

    return key_path


def import_key(server: str, user: str, key_path: Path) -> Path:
    """
    Import an existing private key for a server.
    Returns the path to the copied private key.
    """
    ensure_ssh_dir()

    if not key_path.exists():
        raise FileNotFoundError(f"Key file not found: {key_path}")

    dest_key = SSH_DIR / f"id_imported_{server}"
    dest_pub = dest_key.with_suffix(".pub")

    logger.info(f"Importing key {key_path} for {user}@{server}")

    dest_key.write_bytes(key_path.read_bytes())
    dest_key.chmod(0o600)

    if key_path.with_suffix(".pub").exists():
        dest_pub.write_bytes(key_path.with_suffix(".pub").read_bytes())
        dest_pub.chmod(0o644)

    return dest_key


def update_config(server: str, user: str, key_path: Path):
    """
    Add a host entry to ~/.ssh/config for the given server and key.
    """
    ensure_ssh_dir()
    with open(CONFIG_FILE, "a") as f:
        f.write(f"\nHost {server}\n")
        f.write(f"    HostName {server}\n")
        f.write(f"    User {user}\n")
        f.write(f"    IdentityFile {key_path}\n")

    logger.info(f"Updated SSH config for {server} with key {key_path}")

def import_pasted_key(server: str, user: str, key_content: str) -> Path:
    """
    Import a pasted private key string into ~/.ssh and return its path.
    """
    ensure_ssh_dir()
    dest_key = SSH_DIR / f"id_imported_{server}"

    logger.info(f"Importing pasted private key for {user}@{server}")
    dest_key.write_text(key_content)
    dest_key.chmod(0o600)

    return dest_key


def import_public_key_file(key_path: Path):
    """
    Import a public key file into authorized_keys.
    """
    ensure_ssh_dir()
    auth_keys = SSH_DIR / "authorized_keys"
    auth_keys.touch(mode=0o600, exist_ok=True)

    if not key_path.exists():
        raise FileNotFoundError(f"Public key file not found: {key_path}")

    content = key_path.read_text().strip()
    with open(auth_keys, "a") as f:
        f.write(content + "\n")

    logger.info(f"Imported public key from {key_path} into authorized_keys")


def import_public_key_paste(content: str):
    """
    Import a pasted public key string into authorized_keys.
    """
    ensure_ssh_dir()
    auth_keys = SSH_DIR / "authorized_keys"
    auth_keys.touch(mode=0o600, exist_ok=True)

    with open(auth_keys, "a") as f:
        f.write(content + "\n")

    logger.info("Imported pasted public key into authorized_keys")