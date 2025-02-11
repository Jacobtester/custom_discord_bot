#wash_handler.py
import discord
from re import match
from asyncio import sleep
from settings import WASHING, MACHINE


#Untested
async def wash_command(member_str, message, client):
    matched = match(r"<@!?(\d+)>", member_str)
    if not matched:
        print('Invalid member string')
        return 'unable to wash'
    
    member_id = int(matched.group(1))

    member = message.guild.get_member(int(member_id))
    washing = client.get_channel(WASHING)
    machine = client.get_channel(MACHINE)
    try:
        currentChannel = member.voice.channel
        for rotations in range(4):
            await member.move_to(washing)
            await sleep(.1)
            await member.move_to(machine)
            await sleep(.1)
        await member.move_to(currentChannel)
    except Exception as e:
        print(f'Error wash: {e}')
        return 'unable to wash'
    return None