import os
import subprocess
import platform
import sys


def find_executable(name, search_paths=None):
    """Find the full path of an executable (e.g., clamdscan or freshclam)."""
    if search_paths is None:
        search_paths = os.environ["PATH"].split(os.pathsep)

    # Add common ClamAV installation paths on Windows
    if os.name == "nt":
        search_paths.extend([
            r"C:\Program Files\ClamAV",
            r"C:\Program Files (x86)\ClamAV"
        ])

    for path in search_paths:
        executable_path = os.path.join(path, name)
        if os.path.exists(executable_path):
            return executable_path
    return None


def is_clamav_installed():
    """Check if ClamAV is installed."""
    # Attempt to find clamdscan or freshclam in PATH
    clamdscan = find_executable("clamdscan.exe" if os.name == "nt" else "clamdscan")
    freshclam = find_executable("freshclam.exe" if os.name == "nt" else "freshclam")
    return bool(clamdscan and freshclam)


def install_clamav():
    """Guide users to install ClamAV manually on unsupported systems."""
    os_name = platform.system()

    if os_name == "Windows":
        print("ClamAV cannot be installed automatically on Windows.")
        print("Please download and install ClamAV from: https://www.clamav.net/downloads")
        return False
    elif os_name == "Linux":
        print("Installing ClamAV on Linux...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "clamav", "clamav-daemon"], check=True)
            return True
        except Exception as e:
            print(f"Error installing ClamAV on Linux: {e}")
            return False
    elif os_name == "Darwin":
        print("Installing ClamAV on macOS...")
        try:
            subprocess.run(["brew", "install", "clamav"], check=True)
            return True
        except Exception as e:
            print(f"Error installing ClamAV on macOS: {e}")
            return False
    else:
        print(f"Unsupported operating system: {os_name}")
        return False


def ensure_freshclam_config():
    """Ensure the freshclam.conf file exists and is configured correctly."""
    os_name = platform.system()
    if os_name == "Windows":
        config_path = r"C:\Program Files\ClamAV\freshclam.conf"
    else:
        config_path = "/etc/clamav/freshclam.conf"

    if not os.path.exists(config_path):
        print(f"freshclam.conf not found at {config_path}. Creating a default configuration...")
        try:
            with open(config_path, "w") as f:
                f.write("DatabaseMirror database.clamav.net\n")
                f.write("DatabaseCustomURL https://database.clamav.net\n")
            print(f"Created freshclam.conf at {config_path}")
        except Exception as e:
            print(f"Failed to create freshclam.conf: {e}")
            return False

    return True


def update_clamav_database():
    """Update the ClamAV virus database."""
    freshclam = find_executable("freshclam.exe" if os.name == "nt" else "freshclam")
    if not freshclam:
        print("Error: freshclam command not found. Ensure ClamAV is installed and in PATH.")
        return

    if not ensure_freshclam_config():
        print("Skipping database update due to missing or invalid freshclam.conf.")
        return

    try:
        print("Updating ClamAV database...")
        subprocess.run([freshclam], check=True)
        print("ClamAV database updated successfully.")
    except Exception as e:
        print(f"Error updating ClamAV database: {e}")


def start_clamav_daemon():
    """Start the ClamAV daemon."""
    os_name = platform.system()
    if os_name == "Windows":
        print("Starting ClamAV manually is required on Windows.")
    elif os_name == "Linux":
        try:
            print("Starting ClamAV daemon on Linux...")
            subprocess.run(["sudo", "systemctl", "start", "clamav-daemon"], check=True)
        except Exception as e:
            print(f"Error starting ClamAV daemon: {e}")
    elif os_name == "Darwin":
        try:
            print("Starting ClamAV daemon on macOS...")
            subprocess.run(["clamd"], check=True)
        except Exception as e:
            print(f"Error starting ClamAV daemon: {e}")


def setup_clamav():
    """Full setup for ClamAV."""
    if is_clamav_installed():
        print("ClamAV is already installed.")
    else:
        print("ClamAV is not installed. Attempting installation...")
        if not install_clamav():
            print("Failed to install ClamAV. Please install it manually and rerun this script.")
            sys.exit(1)

    update_clamav_database()
    start_clamav_daemon()
    print("ClamAV setup is complete.")


if __name__ == "__main__":
    setup_clamav()
