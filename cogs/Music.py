import discord
from time import sleep
import wavelink


class Music(discord.Cog):
    # region [Private Attributes]
    __music_queue = []
    # endregion

    def __init__(self, bot) -> None:
        self.__bot = bot

    # region [Events listeners]
    @discord.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        # deletes the music that was played before
        self.__music_queue.pop(0)

        bot_voice_client = player.guild.voice_client;
        await self.__play_music(bot_voice_client)
    # endregion

    # region [Discord commands]
    @discord.slash_command(description="Commande qui permet de faire jouer au bot la musique que l'on souhaite")
    @discord.option("search", description="Nom ou lien youtube de la musique")
    async def play(self, ctx, *, search: str):
        # Let bot finish all he needs before send a response
        await ctx.defer();

        author_voice_client = ctx.author.voice
        bot_voice_client = ctx.voice_client

        if not author_voice_client:
            # TODO REVIEW All message content should be loaded from outside the code (db, json file,....)
            await ctx.respond("Vous ne pouvez pas mettre de musique si vous n'êtes pas dans un salon vocal !")
            return

        if bot_voice_client and bot_voice_client.channel.id != author_voice_client.channel.id:
            await ctx.respond(
                "Vous ne pouvez pas mettre de musique si vous n'êtes pas dans le meme salon vocal que le bot !")
            return

        try:
            song = await wavelink.YouTubeTrack.search(search, return_first=True)
        except Exception:
            # TODO Review Too Broad Exception (from IDE input)
            # TODO Review Use more specific exception. Never use Exception directly (either another exception type,
            #  or filter by message content)
            await ctx.respond("La musique que vous avez sugérée n'a pas été trouvée... Veuillez réssayer plus tard !")
            return
        else:
            self.__music_queue.append(song)

        if not bot_voice_client:
            bot_voice_client = await author_voice_client.channel.connect(cls=wavelink.Player)

        await ctx.respond(embed=self.__message_added_to_queue())

        if not bot_voice_client.is_playing():
            await self.__play_music(bot_voice_client)

    # endregion

    # region [Private methods]
    async def __play_music(self, bot_voice_client: discord.VoiceClient) -> None:
        """This method is designed to play the musics in the music queue through the bot voice client

        Args:
            bot_voice_client (discord.VoiceClient): The bot voice client
        """
        if len(self.__music_queue) == 0:
            sleep(2)
            await bot_voice_client.disconnect()
            return

        await bot_voice_client.play(self.__music_queue[0])

    def __message_added_to_queue(self) -> discord.Embed:
        message = discord.Embed(
            title="Liste d'attente",
            # TODO REVIEW Line too long (ide proposition)
            description=f"Votre musique à bien été ajoutée à la liste d'attente. Position : {len(self.__music_queue) - 1}",
            colour=0xffffff
        )
        return message
    # endregion


def setup(bot):
    bot.add_cog(Music(bot))
