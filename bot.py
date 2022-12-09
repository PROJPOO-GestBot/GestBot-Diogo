import os
import discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f"The bot is now ready : {client.user}")
    
client.run(os.getenv('BOT_TOKEN'))