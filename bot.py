import os
import discord
import wavelink
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')    

async def lavalink_nodes_connect():
    """Connect to our Lavalink nodes."""
    
    await wavelink.NodePool.create_node(
        bot=bot,
        host=os.getenv("LAVALINK_IP"),
        port=os.getenv("LAVALINK_PORT"),
        password=os.getenv("LAVALINK_PASSWORD")
    ) # create the node

@bot.event
async def on_ready():
    await lavalink_nodes_connect()
    print(f"The bot is now ready : {bot.user}")

bot.run(os.getenv('BOT_TOKEN'))