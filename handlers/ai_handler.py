#ai_handler.py
import settings as sett


async def ai_command(message):
    #Prepare the message for the AI
    user_message = str(message.content).lower()
    if (is_authorized(message)):
        try:
            prompt = user_message[4:]
            if prompt.startswith('['):
                return await handle_modifiers(message)
            if not prompt.strip():
                return 'Please provide a prompt'

            response = await get_ai_response(prompt)
            return response
        except Exception as e:
            print(f'AI Command Error: {e}')
            return 'unable to get response from ai'
    else:
        return 'Unavailable in this server'
    
    
#Returns a string containing the AI's response to a given prompt (string)
async def get_ai_response(prompt):
    try:
        ai_payload = sett.ai_settings(prompt)
        response = await sett.ai_client.chat.completions.create(**ai_payload)
        content =  response.choices[0].message.content.strip()

        #Temp fix to discord message size limit
        if len(content) > 1900: #discords message limit
            content = content[:1900] + "... (truncated)"

        return content
    except Exception as e:
        print(f'AI error: {e}')
        return 'unable to get response from ai'


async def handle_modifiers(message):
    user_message = str(message.content).lower()
    prompt = user_message[4:]
    # Will handle changing ai settings (currently doesnt save)
    #!ai [model] ...
    if prompt.startswith('[model] ') and (message.author.id == sett.BOT_OWNER):
        prompt = prompt[8:]
        sett.current_model = prompt
        return f"Model is now: {prompt}"
    #!ai [personality] ...
    if prompt.startswith('[personality] '):
        prompt = prompt[14:]
        sett.current_personality = prompt
        return f"Personality is now: {prompt}"
    #!ai [current]
    if prompt.startswith('[current]'):
        return f"Current settings\n Model: {sett.current_model}\n Personality: {sett.current_personality}"
    else:
        return "incorrect modifier usage"


        

def is_authorized(message):
    return (
        (message.guild and message.guild.id == sett.PRIMARY_GUILD) or
        (message.author.id == sett.BOT_OWNER) or
        (message.author.id in sett.AI_ALLOWED_USERS)
    )


