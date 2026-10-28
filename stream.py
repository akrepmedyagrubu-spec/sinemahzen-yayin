import os
import re
import signal
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
LOGO = ROOT / "yayin_logo.png"
HLS_DIR = ROOT / "hls"
PLAYLIST = HLS_DIR / "live.m3u8"
PORT = int(os.environ.get("PORT") or os.environ.get("SERVER_PORT") or "8080")


def stop(signum, frame):
    raise SystemExit(0)


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)


def find_videos():
    allowed = {".mp4", ".mkv", ".mov", ".webm", ".m4v", ".avi"}
    found = []
    for path in VIDEO_DIR.iterdir():
        match = re.fullmatch(r"(\d+)", path.stem)
        if path.is_file() and path.suffix.lower() in allowed and match:
            found.append((int(match.group(1)), path))
    return [path for _, path in sorted(found)]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HLS_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        if self.path.lower().endswith(".m3u8"):
            self.send_header("Content-Type", "application/vnd.apple.mpegurl")
        elif self.path.lower().endswith(".ts"):
            self.send_header("Content-Type", "video/mp2t")
        super().end_headers()


def run_ffmpeg():
    try:
        import imageio_ffmpeg
    except ImportError:
        print("FFmpeg paketi eksik. requirements.txt dosyasini yukleyip yeniden baslatin.", flush=True)
        return 1

    HLS_DIR.mkdir(exist_ok=True)
    while True:
        videos = find_videos()
        if not videos:
            print("videos/ klasorune 1.mp4, 2.mp4... seklinde video ekleyin.", flush=True)
            time.sleep(15)
            continue
        if not LOGO.is_file():
            print("Logo bulunamadi: yayin_logo.png (logo eklenene kadar yayin baslamaz).", flush=True)
            time.sleep(15)
            continue

        concat = ROOT / "videos.txt"
        lines = []
        for video in videos:
            safe_path = str(video.resolve()).replace("'", "'\\''")
            lines.append(f"file '{safe_path}'")
        concat.write_text("\n".join(lines) + "\n", encoding="utf-8")

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        # Sablon, videodan logoya kucuk bir bosluk birakir; logo oranini korur.
        cmd = [ffmpeg, "-hide_banner", "-loglevel", "warning", "-nostdin",
               "-stream_loop", "-1", "-f", "concat", "-safe", "0", "-i", str(concat),
               "-i", str(LOGO), "-filter_complex",
               "[0:v]scale=-2:420:flags=fast_bilinear,fps=20[base];"
               "[1:v]scale=140:-1[logo];[base][logo]overlay=12:12:format=auto[v]",
               "-map", "[v]", "-map", "0:a:0?", "-c:v", "libx264", "-preset", "veryfast",
               "-tune", "zerolatency", "-pix_fmt", "yuv420p", "-b:v", "900k", "-maxrate", "1100k",
               "-bufsize", "1800k", "-g", "40", "-keyint_min", "40", "-sc_threshold", "0",
               "-c:a", "aac", "-b:a", "96k", "-ar", "44100", "-ac", "2", "-f", "hls",
               "-hls_time", "4", "-hls_list_size", "8", "-hls_delete_threshold", "2",
               "-hls_flags", "delete_segments+append_list+omit_endlist+independent_segments",
               "-hls_segment_filename", str(HLS_DIR / "segment_%06d.ts"), str(PLAYLIST)]
        print("Yayin basliyor. Video sirasi: " + ", ".join(p.name for p in videos), flush=True)
        try:
            subprocess.run(cmd, check=False)
        except FileNotFoundError:
            print("FFmpeg calistirilamadi.", flush=True)
        print("FFmpeg durdu; 5 saniye icinde yeniden baslatilacak.", flush=True)
        time.sleep(5)


def main():
    VIDEO_DIR.mkdir(exist_ok=True)
    HLS_DIR.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    threading.Thread(target=run_ffmpeg, daemon=True).start()
    print(f"HTTP/HLS sunucusu port {PORT} uzerinde acik. Akis: /live.m3u8", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
