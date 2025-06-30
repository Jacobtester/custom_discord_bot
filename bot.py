#bot.py
#libraries
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
import command_check
import settings

TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = '!', intents=settings.intent_settings())


def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} now running')
    
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        #Output messages to console
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        guild = (str(message.guild) if message.guild else "Direct Message")
        print(f"({guild}) {username} said: '{user_message}' ({channel})")

        #Command check and handle
        if(user_message.startswith("!")):
            try:
                response = await command_check.check_command(message, client)
                if response:
                    await message.channel.send(response)
            except Exception as e:
                print(f"Bot Error: " + e)


    client.run(TOKEN)