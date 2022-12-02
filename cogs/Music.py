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
        bot_voiceChannel = player.guild.voice_client;
        await self.__PlayMusic(bot_voiceChannel=bot_voiceChannel)
    #endregion
    
    #region [Discord commands]
    @discord.slash_command()
    async def play(self, ctx, *, search: str):
        author_voiceChannel = ctx.author.voice
        bot_voiceChannel = ctx.voice_client
        
        if not author_voiceChannel:
            await ctx.respond("Vous ne pouvez pas mettre de musique si vous n'etes pas dans un salon vocal !")
            return
        
        if bot_voiceChannel and bot_voiceChannel.channel.id != author_voiceChannel.channel.id:
            await ctx.respond("Vous ne pouvez pas mettre de musique si vous n'etes pas dans le meme salon vocal que le bot !")
            return
            
        if not bot_voiceChannel:
            bot_voiceChannel = await author_voiceChannel.channel.connect(cls=wavelink.Player)
        
        song = await wavelink.YouTubeTrack.search(search, return_first=True)
        self.__musicQueue.append(song)
        
        await ctx.respond("Music was added to queue !")
        
        if not bot_voiceChannel.is_playing():
            await self.__PlayMusic(bot_voiceChannel=bot_voiceChannel)
    #endregion
    
    #region [Private methods]
    async def __PlayMusic(self, bot_voiceChannel : discord.VoiceClient) -> None:
        """This method is designed to play the musics in the music queue on discord

        Args:
            bot_voiceChannel (discord.VoiceClient): The bot voice client
        """
        if self.__musicQueue.count == 0:
            sleep(2)
            await bot_voiceChannel.disconnect()
            return
            
        await bot_voiceChannel.play(self.__musicQueue[0])
        self.__musicQueue.pop(0)
    #endregion
    
def setup(bot):
    bot.add_cog(Music(bot))