#isnta_handler.py
import os
import asyncio
import shutil
import glob
import discord
import instaloader
import settings as sett
from urllib.parse import urlparse

MAX_UPLOAD_BYTES = 24 * 1024 * 1024  # ~24MB safety

def _extract_shortcode(url: str) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split('/') if p]
    if not parts:
        raise ValueError("Invalid Instagram URL path")
    if len(parts) >= 2 and parts[0] in ('reel', 'p'):
        return parts[1]
    return parts[-1]

async def insta_command(message):
    user_message = str(message.content).strip()
    parts = user_message.split(maxsplit=1)
    if len(parts) < 2:
        return "Provide a link: !insta https://www.instagram.com/reel/XXXX/"
    url = parts[1].strip("<>")

    try:
        shortcode = _extract_shortcode(url)
    except Exception:
        return "Unable to parse Instagram link."

    # checked so far
    tmp_dir = os.path.join(sett.DATA_DIR, f"insta_{message.id}")
    os.makedirs(tmp_dir, exist_ok=True)

    try:
        def download_sync():
            L = instaloader.Instaloader(
                download_pictures=False,
                download_videos=True,
                download_video_thumbnails=False,
                save_metadata=False,
                compress_json=False,
                dirname_pattern=tmp_dir,
                filename_pattern="{shortcode}",
                quiet=True
            )
            ig_user = os.getenv("INSTAGRAM_USERNAME")
            ig_pass = os.getenv("INSTAGRAM_PASSWORD")
            if ig_user and ig_pass:
                try:
                    L.login(ig_user, ig_pass)
                except Exception:
                    pass
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            if not post.is_video:
                raise RuntimeError("Post is not a video.")
            # Download only video to reduce noise
            vurl = post.video_url
            if not vurl:
                raise RuntimeError("No video URL found.")
            import requests
            mp4_path = os.path.join(tmp_dir, f"{shortcode}.mp4")
            r = requests.get(vurl, stream=True, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            with open(mp4_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            return mp4_path

        mp4_path = await asyncio.to_thread(download_sync)

        if os.path.getsize(mp4_path) > MAX_UPLOAD_BYTES:
            return "Video too large to upload."

        await message.channel.send(
            file=discord.File(mp4_path, filename=os.path.basename(mp4_path))
        )
        return None
    except Exception as e:
        print(f"Insta download error: {e}")
        return "Unable to download that Instagram video."
    finally:
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as cleanup_err:
            print(f"Insta cleanup error: {cleanup_err}")