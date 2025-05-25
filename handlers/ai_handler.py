#ai_handler.py
import settings as sett


async def ai_command(message):
    #Prepare the message for the AI
    user_message = str(message.content).lower()
    if (is_authorized(message)):
        try:
            prompt = user_message[4:]
            if not prompt.strip():
                return 'Please provide a prompt'

            response = await get_ai_response(prompt)
            return response
        except Exception as e:
            print(f'AI Command Error: {e}')
            return 'unable to get response from ai'
    else:
        return 'Unavailable in this server'
    
    
async def get_ai_response(prompt):
    try:
        ai_payload = sett.ai_settings(prompt)
        response = await sett.ai_client.chat.completions.create(**ai_payload)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f'AI error: {e}')
        return 'unable to get response from ai'


def is_authorized(message):
    return (
        (message.guild and message.guild.id == sett.PRIMARY_GUILD) or
        (message.author.id == sett.BOT_OWNER) or
        (message.author.id in sett.AI_ALLOWED_USERS)
    )
