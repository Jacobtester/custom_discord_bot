#ai_handler.py
import io
import settings as sett
import discord
import os
import base64

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

            #Return prompt case-sensitivity, then ship
            prompt = str(message.content)[4:]
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
        prompt = str(message.content)[18:] #case-sensitive again
        sett.current_personality = prompt
        return f"Personality is now: {prompt}"
    #!ai [current]
    if prompt.startswith('[current]'):
        return f"Current settings\n Model: {sett.current_model}\n Personality: {sett.current_personality}"
    if prompt.startswith('[enable image]') and (message.author.id == sett.BOT_OWNER):
        sett.enable_image = True
        return f"Generative images now available"
    if prompt.startswith('[disable image]') and (message.author.id == sett.BOT_OWNER):
        sett.enable_image = False
        return f"Generative images disabled"
    if prompt.startswith('[image]') and sett.enable_image is True: 
        try:
            # Use the original (non-lowered) content to preserve prompt casing
            raw = str(message.content)[4:]  # strip "!ai "
            if raw.lower().startswith('[image]'):
                image_prompt = raw[len('[image]'):].strip()
            else:
                image_prompt = ""
            if not image_prompt:
                return "Please provide an image prompt"

            # Build payload and generate image
            payload = sett.ai_image_settings(image_prompt)
            result = await sett.ai_client.images.generate(**payload)

            # Validate and decode
            if not result or not result.data or not getattr(result.data[0], "b64_json", None):
                print("AI image error: Missing b64_json in response")
                return "Image generation failed"

            b64 = result.data[0].b64_json
            img_bytes = base64.b64decode(b64)

            # Save to data/ temporarily, send, then clean up
            filename = f"ai_image_{message.id}.png"
            filepath = os.path.join(sett.DATA_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(img_bytes)

            await message.channel.send(file=discord.File(filepath, filename=filename))

            try:
                os.remove(filepath)
            except Exception as cleanup_err:
                print(f'AI image cleanup error: {cleanup_err}')
            return None
        except Exception as e:
            print(f'AI image error: {e}')
            return 'unable to generate image'
    else:
        return "incorrect modifier usage"
    


        

def is_authorized(message):
    return (
        (message.guild and message.guild.id == sett.PRIMARY_GUILD) or
        (message.author.id == sett.BOT_OWNER) or
        (message.author.id in sett.AI_ALLOWED_USERS)
    )


