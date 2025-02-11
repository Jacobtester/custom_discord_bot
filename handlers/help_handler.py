#help_handler.py


async def help_command() -> str:
    message = "~Help~~~~~~~~~~~~~~\n"
    message += "!help - Display this message\n"
    message += "!who - Display your username\n"
    message += "!whoid - Display your user ID\n"
    message += "!roll - Roll a dice\n"
    message += "!ai [prompt] - ChatGPT AI\n"
    message += "!wash [user] - Wash a user\n"
    message += "!wipe - Wipe chat\n"
    message += "!lol [RiotID]#[Tagline] wr - Get winrate for last 10 games\n"
    message += "!play [url] - Play a song\n"
    message += "!queue [url] - Add a song to the queue\n"
    message += "!skip - Skip current song\n"
    message += "!clear - Clear the queue\n"
    message += "!pause - Pause current song\n"
    message += "!resume - Resume current song\n"
    message += "!stop - Stop current song, & remove bot from call\n"

    return message