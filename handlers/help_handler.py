#help_handler.py
from settings import active_features
active_features = active_features()


async def help_command() -> str:
    message = "~Help~~~~~~~~~~~~~~\n"
    message += "!help - Display this message\n"
    message += "!who - Display your username\n"
    message += "!whoid - Display your user ID\n"
    message += "!roll - Roll a dice\n"
    message += "!wipe - Wipe chat\n"
    
    if active_features["OpenAI"]: 
        message += "!ai [prompt] - ChatGPT AI\n"
        message += "!ai [model] (Model name) - Replaces OpenAI model, only available for bot owner\n"
        message += "!ai [personality] (Personality string) - Gives the AI personality instuctions\n"
        message += "!ai [current] - Returns the current AI model and personality instructions\n"
    if active_features["Washing"]:
        message += "!wash [user] - Wash a user\n"
    if active_features["Riot"]: 
        message += "!lol [RiotID]#[Tagline] wr - Get winrate for last 10 games\n"
    if active_features["Youtube"]:
        message += "!play [url] - Play a song\n"
        message += "!queue [url] - Add a song to the queue\n"
        message += "!skip - Skip current song\n"
        message += "!clear - Clear the queue\n"
        message += "!pause - Pause current song\n"
        message += "!resume - Resume current song\n"
        message += "!stop - Stop current song, & remove bot from call\n"

    return message