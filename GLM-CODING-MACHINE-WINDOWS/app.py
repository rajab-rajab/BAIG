import socket
import sys
import threading
import time
from pathlib import Path

import webview


ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from server import app, socketio  # noqa: E402


def is_port_open(host="127.0.0.1", port=5000):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def wait_for_server(host="127.0.0.1", port=5000, timeout=15):
    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_port_open(host, port):
            return True

        time.sleep(0.3)

    return False


def start_server():
    print("🚀 Starting Coding Machine Flask server...")

    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
    )


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    print("⏳ Waiting for Flask server to become ready...")

    ready = wait_for_server()

    if not ready:
        print("❌ Flask server did not start on http://127.0.0.1:5000")
        input("Press Enter to exit...")
        sys.exit(1)

    print("✅ Flask server is ready.")
    print("🪟 Opening Coding Machine desktop window...")

    webview.create_window(
        title="Coding Machine",
        url="http://127.0.0.1:5000",
        width=1400,
        height=900,
        min_size=(900, 600),
    )

    webview.start(debug=True)