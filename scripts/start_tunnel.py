import subprocess
import time
import sys


def start():
    print("🚀 Starting Mangatarem Cultural Map...")

    # 1. Start the Flask app in the background using uv
    # We use subprocess.Popen so it runs concurrently with the tunnel
    try:
        flask_process = subprocess.Popen(
            ["uv", "run", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print("✅ Flask server initializing...")
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        sys.exit(1)

    print("🌐 Starting Cloudflare Tunnel (Quick Share)...")
    time.sleep(5)  # Give Flask a bit more time to bind to port 5000

    # 2. Start Cloudflare Tunnel using npx with config file
    # This uses the permanent 'gomangatarem-map' tunnel
    try:
        print("💡 Starting permanent tunnel using scripts/config.yml...")
        # On Windows, shell=True is often required to find npx.cmd
        subprocess.run(
            ["npx", "cloudflared", "tunnel", "--config", "scripts/config.yml", "run"],
            shell=True,
        )
    except KeyboardInterrupt:
        print("\n👋 Gracefully stopping services...")
        flask_process.terminate()
        print("✅ Done.")
    except Exception as e:
        print(f"❌ Tunnel error: {e}")
        flask_process.terminate()


if __name__ == "__main__":
    start()
