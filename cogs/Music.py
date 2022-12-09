import discord
from time import sleep
import wavelink

class Music(discord.Cog):
    #region [Private Attributes]
    __musicQueue = []
    #endregion
    
    def __init__(self, bot) -> None:
        self.__bot = bot
    
    #region [Events listeners]
    @discord.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        # deletes the music that was played before
        self.__musicQueue.pop(0)
        
        bot_voiceClient = player.guild.voice_client;
        await self.__PlayMusic(bot_voiceClient)
    #endregion
    
    #region [Discord commands]
    @discord.slash_command(description = "Commande qui permet de faire jouer au bot la musique que l'on souhaite")
    @discord.option("search", description = "Nom ou lien youtube de la musique")
    async def play(self, ctx, *, search: str):
        # Let bot finish all he needs before send a response
        await ctx.defer();
        
        author_voiceClient = ctx.author.voice
        bot_voiceClient = ctx.voice_client
        
        if not author_voiceClient:
            await ctx.respond("Vous ne pouvez pas mettre de musique si vous n'etes pas dans un salon vocal !")
            return
        
        if bot_voiceClient and bot_voiceClient.channel.id != author_voiceClient.channel.id:
            await ctx.respond("Vous ne pouvez pas mettre de musique si vous n'etes pas dans le meme salon vocal que le bot !")
            return
        
        try:
            song = await wavelink.YouTubeTrack.search(search, return_first=True)
        except Exception:
            await ctx.respond("La musique que vous avez sugéré n'a pas été trouvée... Veuillez réssayer plus tard !")
            return
        else:
            self.__musicQueue.append(song)
            
        if not bot_voiceClient:
            bot_voiceClient = await author_voiceClient.channel.connect(cls=wavelink.Player)
        
        await ctx.respond(embed=self.__MessageAddedToQueue())
        
        if not bot_voiceClient.is_playing():
            await self.__PlayMusic(bot_voiceClient)
    #endregion
    
    #region [Private methods]
    async def __PlayMusic(self, bot_voiceClient : discord.VoiceClient) -> None:
        """This method is designed to play the musics in the music queue through the bot voice client

        Args:
            bot_voiceClient (discord.VoiceClient): The bot voice client
        """
        if len(self.__musicQueue) == 0:
            sleep(2)
            await bot_voiceClient.disconnect()
            return
            
        await bot_voiceClient.play(self.__musicQueue[0])
    
    def __MessageAddedToQueue(self) -> discord.Embed:
        message = discord.Embed(
            title="Liste d'attente",
            description=f"Votre musique à bien été ajoutée à la liste d'attente. Position : {len(self.__musicQueue)-1}",
            colour=0xffffff
        )
        
        return message
    #endregion
    
def setup(bot):
    bot.add_cog(Music(bot))