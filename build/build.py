import os
import sys
import platform
import stat
import urllib.request
import subprocess

# Add project root to path so paths resolve correctly from build/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Determine platform
system = platform.system().lower()
machine = platform.machine().lower()

# Map Python architecture to Tailwind releases architecture
if "windows" in system:
    os_name = "windows"
    ext = ".exe"
elif "darwin" in system:
    os_name = "macos"
    ext = ""
else:
    os_name = "linux"
    ext = ""

if machine in ["x86_64", "amd64"]:
    arch = "x64"
elif machine in ["arm64", "aarch64"]:
    arch = "arm64"
elif machine in ["armv7l"]:
    arch = "armv7"
else:
    print(f"Unsupported architecture: {machine}")
    sys.exit(1)

# Construct specific binary filename
TAILWIND_VERSION = "v3.4.17" # Pinning to a stable version
binary_name = f"tailwindcss-{os_name}-{arch}{ext}"
download_url = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/{binary_name}"

def download_tailwind():
    """Download Tailwind CLI executable if it doesn't exist."""
    if not os.path.exists(binary_name):
        print(f"Downloading {binary_name} from {download_url}...")
        urllib.request.urlretrieve(download_url, binary_name)
        
        # Make the downloaded file executable (Linux/macOS)
        if ext == "":
            st = os.stat(binary_name)
            os.chmod(binary_name, st.st_mode | stat.S_IEXEC)
        print("Download complete.")

def build_tailwind():
    """Run Tailwind CLI to build the CSS."""
    # Ensure binary exists
    download_tailwind()

    # Determine paths relative to project root
    input_css = os.path.join(PROJECT_ROOT, "static", "css", "input.css")
    output_css = os.path.join(PROJECT_ROOT, "static", "css", "main.css")
    executable = os.path.abspath(binary_name)

    # Base command arguments
    cmd = [executable, "-i", input_css, "-o", output_css]

    # Check for watch flag argument
    if "--watch" in sys.argv:
        print("Running tailwindcss in watch mode...")
        cmd.append("--watch")
    else:
        print("Building tailwindcss with minify...")
        cmd.append("--minify")

    print(f"Executing: {' '.join(cmd)}")
    
    try:
        if "--watch" in sys.argv:
             # Run asynchronously without capturing output allowing streaming
             subprocess.run(cmd)
        else:
             subprocess.run(cmd, check=True)
        print("Tailwind build finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tailwindcss: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_tailwind()
