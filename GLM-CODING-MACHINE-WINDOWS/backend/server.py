from pathlib import Path

from flask import Flask, send_file, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

app.config["SECRET_KEY"] = "coding-machine-secret"

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)


@app.route("/")
def index():
    index_path = FRONTEND_DIR / "index.html"

    if not index_path.exists():
        return (
            f"<h1>index.html not found</h1>"
            f"<p>Expected path: {index_path}</p>",
            404,
        )

    return send_file(index_path)


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "app": "Coding Machine",
            "frontend_dir": str(FRONTEND_DIR),
            "index_exists": (FRONTEND_DIR / "index.html").exists(),
        }
    )


@app.route("/<path:filename>")
def static_files(filename):
    file_path = FRONTEND_DIR / filename

    if file_path.exists() and file_path.is_file():
        return send_from_directory(FRONTEND_DIR, filename)

    return send_file(FRONTEND_DIR / "index.html")


@socketio.on("connect")
def handle_connect():
    print("✅ Client connected via Socket.IO")
    emit(
        "connection_response",
        {"message": "Connected to Coding Machine backend"}
    )


@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected")


@socketio.on("agent_message")
def handle_agent_message(data):
    message = data.get("message", "")
    print(f"📩 Received message: {message}")

    emit("agent_activity", {"type": "thinking"})

    socketio.sleep(1)

    emit(
        "agent_message_chunk",
        {
            "content": f"You said: {message}\n\nCoding Machine backend is connected successfully."
        },
    )

    emit("agent_message_complete", {"content": ""})


if __name__ == "__main__":
    print(f"Frontend directory: {FRONTEND_DIR}")
    print(f"Index exists: {(FRONTEND_DIR / 'index.html').exists()}")

    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True,
    )