import discord
from discord.ext import commands
import asyncio
import requests
from pydoc import describe

embed_title = "Server Name" #title of the embed/name of the server
status_channel = 1234567890 #status channel id
server_ip = "0.0.0.0:30110" #server ip and port
bot_token = "qwertyuiop" #bot token, from https://discord.com/developers/applications

bot = commands.Bot(command_prefix="qwashrzdl;", help_command=None) #some random letters as we don't need a prefix

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('THE BOT IS READY')
    channel = bot.get_channel(status_channel)
    message_sent = "no"
    while True:
        embed = discord.Embed(title = embed_title, colour=discord.Colour.dark_red())
        #check if the server is online
        try:
            info = requests.get(f'http://{server_ip}/players.json').json()
            status = "online"
            embed.add_field(name="Status", value="Online 🟢")
        except:
            status = "offline"
            embed.add_field(name="Status", value="Offline 🔴")

        #if the server is online, get the players
        if status == "online":
            players = []
            for item in info:
                if isinstance(item, dict):
                    players.append(item["name"])
            #check if there are no players online
            if players:
                embed.add_field(name="Players", value="\n".join(players))
            else:
                embed.add_field(name="Players", value="No players online")
                
        else:
            pass

        if message_sent == "no":
            #delete the previous status message
            await channel.purge(limit=1)
            #send the new status message
            message = await channel.send(embed=embed)
            message_sent = "yes"
        elif message_sent == "yes":
            await message.edit(embed=embed)
        else:
            pass

        await asyncio.sleep(10)

bot.run(bot_token)