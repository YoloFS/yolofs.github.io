#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["imageio-ffmpeg"]
# ///
"""Build demo.mp4, demo.gif, and cover.png from demo.html. Run: uv run demo.py

Screenshots every frame the page lists (?meta=1), joins them with their durations, then
derives a GIF for places that can't play MP4 (like a GitHub README) and the cover still.
"""
import glob, json, os, re, shutil, subprocess, tempfile

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "file://" + os.path.join(HERE, "demo.html")
SIZE = "1440,1080"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def find_chrome():
    """First Chrome found: macOS app, then Linux binaries, then a Playwright download."""
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium",
              *glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell"))]:
        if path := shutil.which(c):
            return path
    raise SystemExit("no Chrome found")


CHROME = find_chrome()


def chrome(*args, **kw):
    return subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", *args],
                          check=True, capture_output=True, text=True, **kw).stdout


def shot(png, query):
    chrome(f"--window-size={SIZE}", f"--screenshot={png}", f"{PAGE}?{query}")


def ffmpeg(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *args], check=True)


def steps():
    """Every frame as [scene, lines shown, seconds], read back from the page itself."""
    out = chrome("--dump-dom", PAGE + "?meta=1")
    return json.loads(re.search(r'<pre id="meta">(.*?)</pre>', out, re.S).group(1))


def build_mp4(out):
    with tempfile.TemporaryDirectory() as tmp:
        concat = []
        for i, (s, n, secs) in enumerate(steps()):
            png = os.path.join(tmp, f"{i:03}.png")
            shot(png, f"s={s}&n={n}")
            concat += [f"file '{png}'", f"duration {secs}"]
        concat.append(f"file '{png}'")  # the concat demuxer ignores the last duration otherwise
        listing = os.path.join(tmp, "frames.txt")
        open(listing, "w").write("\n".join(concat) + "\n")
        ffmpeg("-f", "concat", "-safe", "0", "-i", listing, "-vf", "fps=30,format=yuv420p",
               "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", out)


def main():
    os.chdir(HERE)
    build_mp4("demo.mp4")
    ffmpeg("-i", "demo.mp4", "-vf", "fps=10,scale=720:-1:flags=lanczos,split[a][b];"
           "[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none", "demo.gif")
    shot("cover.png", "s=0")


if __name__ == "__main__":
    main()
