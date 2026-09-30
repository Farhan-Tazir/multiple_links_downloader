import os
import shutil
import subprocess
import sys


def is_ytdlp_installed() -> bool:
    """Checks if yt-dlp is installed and executable in PATH or as a Python module."""
    # Check system PATH executable
    if shutil.which("yt-dlp"):
        return True

    # Check python module
    try:
        import yt_dlp  # noqa: F401

        return True
    except ImportError:
        return False


def run_powershell_cmd(command: str) -> subprocess.CompletedProcess:
    """Executes a PowerShell command from Python."""
    ps_executable = "powershell.exe" if os.name == "nt" else "pwsh"
    return subprocess.run(
        [ps_executable, "-Command", command],
        text=True,
    )


def install_ytdlp_via_powershell():
    """Uses PowerShell to search for and install yt-dlp using winget."""
    print("you dont have install the yt-dpl")
    print("searching for ytdlp")

    # Run winget search via PowerShell
    run_powershell_cmd('winget search "yt-dlp"')

    print("\nInstalling yt-dlp via winget...")
    # Run winget install via PowerShell
    result = run_powershell_cmd(
        'winget install --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements'
    )

    if result.returncode != 0:
        print("\n[!] Winget installation failed or was cancelled.")
        print("Fallback: Installing yt-dlp via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])


def process_links_file(file_path: str = "links.txt"):
    """Reads links line by line from links.txt and downloads audio as MP3."""
    if not os.path.exists(file_path):
        print(f"[!] File '{file_path}' does not exist.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        # Filter out empty lines or comments
        links = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    if not links:
        print(f"[!] '{file_path}' is empty. No links to process.")
        return

    print(f"\nFound {len(links)} link(s) in '{file_path}'. Starting download process...\n")

    # Process each link with counter m
    m = 1
    for link in links:
        print(f"--- Processing link {m} of {len(links)} ---")
        print(f"URL: {link}")

        # Run yt-dlp command to extract audio as mp3
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", link]
        result = subprocess.run(cmd)

        if result.returncode == 0:
            print(f"✓ Link {m} downloaded successfully!\n")
        else:
            print(f"✗ Link {m} failed to download.\n")

        m += 1  # Increment counter


def main():
    # 1. Check installation
    if not is_ytdlp_installed():
        # Install yt-dlp if not present
        install_ytdlp_via_powershell()

    # 2. Re-verify or execute download loop (If installed or after installation)
    if is_ytdlp_installed():
        process_links_file("links.txt")
    else:
        print("\n[!] Unable to verify yt-dlp installation. Please restart your terminal/script.")


if __name__ == "__main__":
    main()
