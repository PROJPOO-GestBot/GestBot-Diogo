import discord
import random

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
        
def setup(bot):
    bot.add_cog(FunCommands(bot))