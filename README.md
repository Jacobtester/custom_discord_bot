# custom_discord_bot
Custom Discord Bot is a simple (for now) discord bot aiming to be easily expandable.

## Current Commands
- !help - Display this message
- !who - Display your username
- !whoid - Display your user ID
- !roll - Roll a dice
- !ai [prompt] - ChatGPT AI
- !wash [user] - Wash a user
- !wipe - Wipe chat
- !lol [RiotID]#[Tagline] wr - Get winrate for last 10 games
- !play [url] - Play a song
- !queue [url] - Add a song to the queue
- !skip - Skip current song
- !clear - Clear the queue
- !pause - Pause current song
- !resume - Resume current song
- !stop - Stop current song, & remove bot from call

## Setup & Installation
- Clone the repositiory and ensure you have Python 3.10+ installed.
- Then install the dependecies using: pip install -r requirements.txt
- Create an .env file in the root directory with your varius Tokens, API keys, Server/User ids.  
Should look like  
DISCORD_TOKEN=your_discord_bot_token  
RIOT_API_KEY=your_riot_api_key  
OPENAI_API_KEY=your_openai_api_key  
PRIMARY_GUILD=your_server_id  
BOT_OWNER=your_user_id  
WASHING=channel_id_for_wash  
MACHINE=channel_id_for_machine  
- launch with: python main.py

## Extra Info
The washing machine command moves a person from one designated channel to another designated channel a few times before returning them to their previous channel. This command was added because those in my server have a habbit of deafing themselves in the call while remaining at their pc and in the call. This tends to bring them back quick if we need them because they hear the loud leaving and joining call over and over.
BOT_OWNER and PRIMARY_GUILD, are currently used to limit who and what servers are allowed to use the openai api.

## To be added
- The ability to disable features (like riot or openai)
- Make certain environment variables unnecessary
- Implement any features that seem interesting, fun, or useful