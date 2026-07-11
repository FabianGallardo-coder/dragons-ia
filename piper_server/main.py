import io
import json
import os
import subprocess
import wave
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

VOICES_DIR = Path("/voices")
DEFAULT_VOICE = os.getenv("TTS_VOICE", "es_MX/claude/high/es_MX-claude-high")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))


class PiperHandler(BaseHTTPRequestHandler):

    def _send_json(self, code: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_audio(self, wav_bytes: bytes):
        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(wav_bytes)))
        self.end_headers()
        self.wfile.write(wav_bytes)

    def do_GET(self):
        if self.path == "/health":
            return self._send_json(200, {"status": "ok"})
        self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/synthesize":
            return self._send_json(404, {"error": "not found"})

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        text = body.get("text", "").strip()
        if not text:
            return self._send_json(400, {"error": "text is required"})

        voice = body.get("voice") or DEFAULT_VOICE
        model_path = VOICES_DIR / f"{voice}.onnx"

        if not model_path.exists():
            return self._send_json(400, {
                "error": f"Voice model not found: {model_path}"
            })

        try:
            result = subprocess.run(
                ["piper", "--model", str(model_path), "--output-raw"],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=30,
            )
            if result.returncode != 0:
                return self._send_json(500, {
                    "error": f"Piper error: {result.stderr.decode(errors='replace')}"
                })

            raw_audio = result.stdout
            buf = io.BytesIO()
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(22050)
                wf.writeframes(raw_audio)
            return self._send_audio(buf.getvalue())

        except subprocess.TimeoutExpired:
            return self._send_json(504, {"error": "piper timed out"})
        except Exception as exc:
            return self._send_json(500, {"error": str(exc)})

    def log_message(self, fmt, *args):
        print(f"[piper-server] {args[0]}" if args else fmt)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), PiperHandler)
    print(f"[piper-server] listening on {HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
