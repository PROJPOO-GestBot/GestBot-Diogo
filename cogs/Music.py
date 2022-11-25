import discord
from time import sleep
import wavelink

class Music(discord.Cog):
    _music_queue = []
    
    def __init__(self, bot) -> None:
        self._bot = bot
    
    @discord.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        bot_voiceChannel = player.guild.voice_client;
        await self._play_music(bot_voiceChannel=bot_voiceChannel)
    
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
        self._music_queue.append(song)
        
        await ctx.respond("Music was added to queue !")
        
        if not bot_voiceChannel.is_playing():
            await self._play_music(bot_voiceChannel=bot_voiceChannel)
        
    async def _play_music(self, bot_voiceChannel):
        if self._music_queue.count == 0:
            sleep(2)
            await bot_voiceChannel.disconnect()
            return
            
        await bot_voiceChannel.play(self._music_queue[0])
        self._music_queue.pop(0)

def setup(bot):
    bot.add_cog(Music(bot))