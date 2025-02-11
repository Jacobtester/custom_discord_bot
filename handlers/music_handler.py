#music_handler.py
import asyncio
import discord
from settings import ffmpeg_settings

voice_clients = {}
queues = {}
ytdl, ffmpeg_options = ffmpeg_settings()


#Basically another command_check, but for music commands
async def music_command(message, client):
    user_message = str(message.content).lower()

    if user_message.startswith("!play"):
        return await play_command(message, client)
    
    if user_message.startswith("!pause"):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as e:
            print(e)
    
    if user_message.startswith("!resume"):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as e:
            print(e)

    if user_message.startswith("!stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
            del voice_clients[message.guild.id]
        except Exception as e:
            print(e)

    if user_message.startswith("!queue"):
        try:
            if message.guild.id not in queues:
                queues[message.guild.id] = []
            queues[message.guild.id].append(str(message.content).split()[1])
            return "Added to queue"
        except Exception as e:
            print(f"Error adding to queue: {e}")
            return "Error adding to queue"
        
    if user_message.startswith("!clear"):
        if message.guild.id in queues:
            queues[message.guild.id].clear()
            return "Queue cleared"
        else:
            return "Queue is already empty"
        
    if user_message.startswith("!skip"):
        return await skip_command(message, client)

    return None


async def play_command(message, client, url=None):
        try:
            if message.guild.id in voice_clients and voice_clients[message.guild.id].is_connected():
                voice_client = voice_clients[message.guild.id]
            else:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(f'Error connecting to voice channel: {e}')
            return "Error connecting to voice channel"

        try:
            if url is None:
                url = message.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[message.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(message, client), loop))
        except Exception as e:
            print(f'Error playing song: {e}')
            return "Error playing song"


async def play_next(message, client):
    if queues[message.guild.id] != []:
        url = queues[message.guild.id].pop(0)
        await play_command(message, client, url)
    return None


async def skip_command(message, client):
    try:
        if message.guild.id in voice_clients:
            voice_client = voice_clients[message.guild.id]
            voice_client.stop()
            if queues.get(message.guild.id):
                await play_next(message, client)
            else:
                print("Queue is empty")
        else:
            print("Not in voice channel")
    except Exception as e:
        print(f"Error skipping song: {e}")
        return "Error skipping song"
            