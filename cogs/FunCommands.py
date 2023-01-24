import os
import discord
import random
from blagues_api import BlaguesAPI
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

class FunCommands(discord.Cog):
    def __init__(self, bot) -> None:
        self.__bot = bot
        
    @discord.slash_command(description="Commande qui permet de jouer au jeu *Pierre, Papier, Ciseau*.")
    @discord.option(name="choice", choices=["Pierre", "Papier", "Ciseau"])
    async def rock_paper_scissors(self, ctx : discord.ApplicationContext, choice : str):
        possibilities = ["Pierre", "Papier", "Ciseau"]
        possibilities_emojis = [":rock:", ":page_facing_up:", ":scissors:"]
        random_choice = random.choice(possibilities)
        
        if choice == random_choice:
            winner_id = -1
        elif random_choice == possibilities[0]:
            if choice == possibilities[2]:
                winner_id = ctx.bot.user.id
            else:
                winner_id = ctx.author.id
        elif random_choice == possibilities[1]:
            if choice == possibilities[0]:
                winner_id = ctx.bot.user.id
            else:
                winner_id = ctx.author.id
        elif random_choice == possibilities[2]:
            if choice == possibilities[1]:
                winner_id = ctx.bot.user.id
            else:
                winner_id = ctx.author.id
            
        bot_choice_emoji = possibilities_emojis[possibilities.index(random_choice)]
        user_choice_emoji = possibilities_emojis[possibilities.index(choice)]
        
        message = f"{bot_choice_emoji} (<@{ctx.bot.user.id}>) X {user_choice_emoji} (<@{ctx.author.id}>)\n\n"
        
        if winner_id == -1: message += "Egalité !"
        else: message += f"Le gagnant est <@{winner_id}> :trophy: !"
        
        await ctx.respond(message)
        
    @discord.slash_command(description="Le bot fait une blague")
    @discord.option(name="type",choices=["Global", "Dev", "Dark", "Limit", "Beauf", "Blondes"])
    async def joke(self, ctx : discord.ApplicationContext, type : str):
        blagues = BlaguesAPI(os.getenv("BLAGUES_API_KEY"))
        
        blague = await blagues.random_categorized(type.lower())
        
        blague_infos = [blague.joke, blague.answer]
        
        await ctx.respond(f"{blague_infos[0]}\n\n\n\n{blague_infos[1]}")
        
    @discord.slash_command(description="Commande qui permet de récupérer les top actualités d'un jour d'un pays.")
    @discord.option(name="category",choices=["Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])
    async def news(self, ctx : discord.ApplicationContext, category : str):
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
        
        news_list = news_api.get_top_headlines(
            language="fr",
            category=category.lower()
        )
        
        news = random.choice(news_list["articles"])
        
        message = discord.Embed(
            title=news["title"],
            description=news["description"],
            url=news["url"],
            color=0xffffff
        )
        
        if news["urlToImage"]:
            message.set_image(url=news["urlToImage"])
            
        await ctx.respond(embed=message)
    
def setup(bot):
    bot.add_cog(FunCommands(bot))