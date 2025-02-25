#command_check.py
from handlers import help_handler
from handlers import roll_handler
from handlers import wash_handler
from handlers import chatwipe_handler
from handlers import ai_handler
from handlers import riot_handler
from handlers import music_handler
from settings import active_features

active_features = active_features()

async def check_command(message, client) -> str:
    user_message = str(message.content).lower()

    #Basic commands
    if user_message == "!help":
        return await help_handler.help_command()
    
    if user_message == "!roll":
        return await roll_handler.roll_command()
    
    if user_message == "!who":
        return f"User: {message.author}"

    if user_message == "!whoid":
        return f"User ID: {message.author.id}"


    #Advanced commands
    if user_message.startswith("!wash") and active_features["Washing"]:
        member_to_wash = user_message[6:]
        rmsg = await wash_handler.wash_command(member_to_wash, message, client)
        return rmsg

    if user_message.startswith(("!wipe", "!cw", "!chatwipe")):
        return await chatwipe_handler.chatwipe_command(message)
    
    if user_message.startswith("!ai") and active_features["OpenAI"]:
        return await ai_handler.ai_command(message)
    
    if user_message.startswith("!lol") and active_features["Riot"]:
        return await riot_handler.riot_command(message)
    
    if user_message.startswith(("!play", "!pause", "!stop", "!skip", "!queue", "!clear","!resume")) and active_features["Youtube"]:
        return await music_handler.music_command(message, client)

    return None

