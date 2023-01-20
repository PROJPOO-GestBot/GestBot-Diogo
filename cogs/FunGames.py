import discord
import random

class FunGames(discord.Cog):
    def __init__(self, bot) -> None:
        self.__bot = bot
        
    @discord.slash_command(description="Commande qui permet de jouer au jeu *Pierre, Papier, Ciseau*.")
    @discord.option(name="choice", choices=["Pierre", "Papier", "Ciseau"])
    async def rock_paper_scissors(self, ctx : discord.ApplicationContext, choice : str):
        possibilities = ["Pierre", "Papier", "Ciseau"]
        possibilities_emojis = [":rock:", ":page_facing_up:", ":scissors:"]
        random_choice = random.choice(possibilities)
        
        message = f"{possibilities_emojis[possibilities.index(random_choice)]} (<@{ctx.bot.user.id}>) X {possibilities_emojis[possibilities.index(choice)]} (<@{ctx.author.id}>)\n\n"
        winner_message = ""
        
        if choice == random_choice:
            winner_message += "Egalité !"   
        elif random_choice == possibilities[0]:
            if choice == possibilities[2]:
                winner_message = f"Le gagnant est <@{ctx.bot.user.id}> :trophy: !"
            else:
                winner_message = f"Le gagnant est <@{ctx.author.id}> :trophy: !"
        elif random_choice == possibilities[1]:
            if choice == possibilities[0]:
                winner_message = f"Le gagnant est <@{ctx.bot.user.id}> :trophy: !"
            else:
                winner_message = f"Le gagnant est <@{ctx.author.id}> :trophy: !"
        elif random_choice == possibilities[2]:
            if choice == possibilities[1]:
                winner_message = f"Le gagnant est <@{ctx.bot.user.id}> :trophy: !"
            else:
                winner_message = f"Le gagnant est <@{ctx.author.id}> :trophy: !"
            
        await ctx.respond(message+winner_message)
def setup(bot):
    bot.add_cog(FunGames(bot))

            