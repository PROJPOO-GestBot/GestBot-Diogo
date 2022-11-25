import os
import discord
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')    

@bot.event
async def on_ready():
    print(f"The bot is now ready : {bot.user}")

bot.run(os.getenv('BOT_KEY'))