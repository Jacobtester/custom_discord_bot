#riot_handler.py
import requests
from settings import RIOT_API_KEY


async def riot_command(message):
    user_message = str(message.content).lower()
    try:
        _, riot_id, command = user_message.split()
        if command == "wr":
            name, tagline = riot_id.split('#')
            return await get_lol_winrate(name, tagline)
    except ValueError:
        return "Invalid command format. Please use `!lol [RiotID]#[Tagline] wr`."
    return None


async def get_lol_winrate(name, tagline):
    try:
        #Get Summoner ID
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}?api_key={RIOT_API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error fetching LoL stats: {response.status_code} - {response.reason}"

        summoner_data = response.json()
        puuid = summoner_data.get("puuid")

        if not puuid:
            return "Unable to fetch summoner PUUID."

        #Get Last 10 Matches
        match_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={RIOT_API_KEY}"
        match_response = requests.get(match_url)

        if match_response.status_code != 200:
            return f"Error fetching match history: {match_response.status_code} - {match_response.reason}"

        match_ids = match_response.json()

        if not match_ids:
            return "No recent matches found."

        win_count = 0
        match_results = []

        #Get Match Details
        for match_id in match_ids:
            match_detail_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}"
            match_detail_response = requests.get(match_detail_url)

            if match_detail_response.status_code != 200:
                return f"Error fetching match details: {match_detail_response.status_code} - {match_detail_response.reason}"

            match_data = match_detail_response.json()
            participants = match_data['info']['participants']

            #Find the participant with the given puuid
            for participant in participants:
                if participant['puuid'] == puuid:
                    champion_name = participant['championName']
                    win_status = "Win" if participant['win'] else "Lose"
                    match_results.append(f"{champion_name} - {win_status}")

                    if participant['win']:
                        win_count += 1
                    break

        #Prepare the output string
        win_rate = (win_count / 10) * 100
        result_str = f"W/R for the last 10 games: {win_rate:.0f}%\n" + "\n".join(match_results)
        return result_str

    except Exception as e:
        print(f"Error fetching LoL stats: {e}")
        return "Unable to fetch League of Legends stats."