#settings.py
import os
import discord
import yt_dlp
from openai import AsyncOpenAI

PRIMARY_GUILD = int(os.getenv("PRIMARY_GUILD"))
BOT_OWNER = int(os.getenv("BOT_OWNER"))
WASHING = int(os.getenv("WASHING"))
MACHINE = int(os.getenv("MACHINE"))
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


#Change these as needed
def intent_settings():
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.message_content = True
    return intents


def ai_settings(prompt):
    return {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.7
    }


def ffmpeg_settings():
    yt_dl_opts = {"format": "bestaudio/best"} 
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    return ytdl, ffmpeg_options