import discord
import time
from discord import app_commands
import random
import os

# Keep-alive script om de bot wakker te houden
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Client class voor de bot
class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name='minesremium', description='minespremium')
async def mines(interaction: discord.Interaction, tile_amt: int, round_id: str):
    required_role_id = 1277383973936300102
    user_roles = [role.id for role in interaction.user.roles]
    if required_role_id not in user_roles:
        em = discord.Embed(color=0xff0000)
        em.add_field(name='Error', value="You do not have the required role.")
        await interaction.response.send_message(embed=em)
        return

    if not interaction.channel.permissions_for(interaction.user).send_messages:
        em = discord.Embed(color=0xff0000)
        em.add_field(name='Error', value="You do not have permission to use this command in this channel.")
        await interaction.response.send_message(embed=em)
        return

    if len(round_id) == 36:
        start_time = time.time()
        grid = ['💣'] * 25
        already_used = []

        count = 0
        while tile_amt > count:
            a = random.randint(0, 24)
            if a in already_used:
                continue
            already_used.append(a)
            grid[a] = '💎'
            count += 1

        chance = random.randint(45, 95)
        if tile_amt < 4:
            chance -= 15

        em = discord.Embed(color=0x0025ff)
        em.add_field(name='Grid', value="\n" + "```" + grid[0] + grid[1] + grid[2] + grid[3] + grid[4] + "\n" +
                    grid[5] + grid[6] + grid[7] + grid[8] + grid[9] + "\n" +
                    grid[10] + grid[11] + grid[12] + grid[13] + grid[14] + "\n" +
                    grid[15] + grid[16] + grid[17] + grid[18] + grid[19] + "\n" +
                    grid[20] + grid[21] + grid[22] + grid[23] + grid[24] +
                    "```\n" + f"**Accuracy**\n```{chance}%```\n**Round ID**\n```{round_id}```\n**Response Time:**\n```{str(int(time.time() - start_time))}```")
        em.set_footer(text='made by Ultrab')
        await interaction.response.send_message(embed=em)
    else:
        em = discord.Embed(color=0xff0000)
        em.add_field(name='Error', value="Invalid round id")
        await interaction.response.send_message(embed=em)

# Start de keep-alive functie om te zorgen dat de bot wakker blijft
keep_alive()

# Haal het token op uit een omgevingsvariabele
client.run(os.getenv('DISCORD_TOKEN'))
