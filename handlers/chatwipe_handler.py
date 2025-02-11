#chatwipe_handler.py
from random import Random


async def chatwipe_command(message):
    print("Chatwipe command called")
    gifList = ["https://tenor.com/view/squidward-clean-cleaning-wipe-wiping-gif-6177877",
                   "https://tenor.com/view/toontown-clown-fish-clown-honk-honk-gif-21231893",
                   "https://tenor.com/view/mimir-the-piterroles-gif-22679697",
                   "https://media.discordapp.net/attachments/659630509894271001/773963990786506812/image0-3.gif",
                   "https://media.discordapp.net/attachments/750566460081832078/765334861157892198/image0.gif",
                   "https://tenor.com/view/horse-spin-horse-spin-video1-mov-gif-14777028",
                   "https://tenor.com/view/pog-fish-fish-mouth-open-gif-17487624",
                   "https://tenor.com/view/gerber-life-grow-up-plan-life-is-rigorous-pennies-a-day-the-bron-jame-gif-19487416",
                   "https://media.discordapp.net/attachments/773262925170606107/808155608451907604/image0-145.gif",
                   "https://tenor.com/view/among-us-who-asked-gif-18850795",
                   "https://tenor.com/view/hamster-hamstermeme-staring-watching-gif-13568561",
                   "https://tenor.com/view/loading-discord-loading-discord-boxes-squares-gif-16187521",
                   "https://media.discordapp.net/attachments/887512998049087489/887656813019951124/image0.gif",
                   "https://tenor.com/view/benjamin-bloons-bloons-td6-btd6-your-mother-gif-22733151"
                   ]
    randomGen = Random() 
    gifStr = randomGen.choice(gifList)

    for _ in range(4):
        await message.channel.send(gifStr)
    return None