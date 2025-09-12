#settings.py
import os
import discord
import yt_dlp
import json
from openai import AsyncOpenAI

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SETTINGS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PRIMARY_GUILD = int(os.getenv("PRIMARY_GUILD", "0"))
BOT_OWNER = int(os.getenv("BOT_OWNER", "0"))
WASHING = int(os.getenv("WASHING", "0"))
MACHINE = int(os.getenv("MACHINE", "0"))
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
try:
    ai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
except:
    ai_client = None


#Change these as needed
def intent_settings():
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.message_content = True
    return intents


def ffmpeg_settings():
    yt_dl_opts = {"format": "bestaudio/best"} 
    ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    return ytdl, ffmpeg_options


def active_features():
    return {
        "Youtube": True,
        "OpenAI": bool(OPENAI_API_KEY) and ai_client is not None and BOT_OWNER != 0 and PRIMARY_GUILD != 0,
        "Riot": bool(RIOT_API_KEY),
        "Washing":  WASHING != 0 and MACHINE != 0,
    }


# AI RELATED SETTINGS ~~~
current_model = "gpt-4.1-mini"
current_personality = ""
enable_image = False

# Image settings
current_image_model = "gpt-image-1"
image_size = "1024x1024"   # 256x256, 512x512, 1024x1024
image_quality = "medium" # standard or hd for dalle,  low, medium, high for gpt1

def ai_settings(prompt):
    if current_model in ["gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-5-chat-latest"]:
        return {
        "model": current_model,
        "messages": [
            {"role": "system", "content": current_personality},
            {"role": "user", "content": prompt}
        ],
        "max_completion_tokens": 2000,
        }

    return {
        "model": current_model,
        "messages": [
            {"role": "system", "content": current_personality},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }

def ai_image_settings(prompt):
    return {
        "model": current_image_model,
        "prompt": prompt,
        "size": image_size,
        "quality": image_quality,
        #"response_format": "b64_json",  # not supported for gpt1 cooked
        "n": 1
    }


# Allowed users for AI commands (so its not just bot owner and primary guild)
def loaded_allowed_users():
    # Paths and filenames
    filepath = os.path.join(DATA_DIR, "ai_allowed_users.json")

    # Create the data directory if it doesn't exist
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    # Does the file exist? If not, create it
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump({"allowed_users": []}, f, indent=4)
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get("allowed_users", [])
    except Exception as e:
        print(f"[Settings] Failed to load allowed users: {e}")
        return []  # Return list, not set

AI_ALLOWED_USERS = loaded_allowed_users()

'''  Default AI settings function previous
return {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7
    }
'''
