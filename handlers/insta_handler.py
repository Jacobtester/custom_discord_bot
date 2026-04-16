#isnta_handler.py
import os
import asyncio
import shutil
import discord
import yt_dlp
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
        clean_url = f"https://www.instagram.com/reel/{shortcode}/"
    except Exception:
        return "Unable to parse Instagram link."

    tmp_dir = os.path.join(sett.DATA_DIR, f"insta_{message.id}")
    os.makedirs(tmp_dir, exist_ok=True)
    mp4_path = os.path.join(tmp_dir, f"{shortcode}.mp4")

    # yt-dlp options specifically tailored for Instagram integration and Discord limits
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': mp4_path,
        'quiet': True,
        'no_warnings': True,
        'max_filesize': MAX_UPLOAD_BYTES,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        def download_sync():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([clean_url])
            return mp4_path

        # Run yt-dlp download in a background thread to prevent blocking the bot
        await asyncio.to_thread(download_sync)

        if not os.path.exists(mp4_path):
             return "Unable to download that Instagram video."
             
        if os.path.getsize(mp4_path) > MAX_UPLOAD_BYTES:
            return "Video too large to upload."

        # Send the video and tag who originally posted the link
        await message.channel.send(
            content=f"Shared by {message.author.mention}:",
            file=discord.File(mp4_path, filename=os.path.basename(mp4_path))
        )
        
        # Try to delete the original !insta message
        try:
            await message.delete()
        except discord.Forbidden:
            pass # Bot lacks permission
        except discord.NotFound:
            pass # Message already deleted
        except discord.HTTPException:
            pass # General discord error

        return None

    except Exception as e:
        print(f"Insta download error: {e}")
        return "Unable to download that Instagram video."
    finally:
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as cleanup_err:
            print(f"Insta cleanup error: {cleanup_err}")