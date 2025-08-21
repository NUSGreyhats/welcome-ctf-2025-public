import os
from pathlib import Path
from zipfile import is_zipfile
import random
import string
from flask import Flask, request, redirect, url_for, Response, render_template, session
from uuid import uuid4
import subprocess

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = random.randbytes(8)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


def new_path():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )


def list_storage_entries(session_id: string) -> list[str]:
    items: list[str] = []
    for _, _, files in os.walk(STORAGE_DIR / session_id, followlinks=False):
        for f in sorted(files):
            href = url_for("serve_file", filename=f)
            items.append(f"<a href='{href}'>{f}</a> ")
    if not items:
        items.append("<em>(empty)</em>")
    return items


@app.get("/")
def index():
    if not session.get("id"):
        session["id"] = str(uuid4())

    return render_template("index.html", entries=list_storage_entries(session["id"]))


@app.post("/upload")
def upload():
    f = request.files.get("file")
    if not f:
        return redirect(url_for("index"))

    if not session.get("id"):
        session["id"] = str(uuid4())

    target = STORAGE_DIR / session["id"] / f.filename

    # Prevent file traversal!
    if target.parent != (STORAGE_DIR / session["id"]):
        return Response("No LFI for you!", status=403)

    target.parent.mkdir(parents=True, exist_ok=True)
    f.save(target)

    if is_zipfile(target):
        # Handle zip files!
        subprocess.call(["unzip", "-d", str(target.parent), str(target)])
        os.remove(target)

    return redirect(url_for("index"))


@app.get("/files/<path:filename>")
def serve_file(filename: str):
    if not session.get("id"):
        session["id"] = str(uuid4())

    rel_path = Path(filename)
    full_path = STORAGE_DIR / session["id"] / rel_path

    if not full_path.is_file():
        return Response("No file found", status=404)

    try:

        def _gen():
            with open(full_path, "rb") as fh:
                while True:
                    chunk = fh.read(8192)
                    if not chunk:
                        break
                    yield chunk

        return Response(_gen(), headers={"Content-Type": "application/octet-stream"})
    except FileNotFoundError:
        return Response("Not found", status=404)
    except PermissionError:
        return Response("Permission denied", status=403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
