import discord
import json
from time import sleep
import wavelink


class Music(discord.Cog):
    # region [Private Attributes]
    __music_queue = []
    __music_error_messages = json.load(open("./data/error_messages.json"))["music"]
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
        
        if not await self.__user_voice_client_checks(ctx):
            return
        
        if search.startswith("http") or "www." in search:
            if not self.__link_check(search):
                await ctx.respond(self.__music_error_messages["not_youtube_link"])
                return
        
        try:
            song = await wavelink.YouTubeTrack.search(search, return_first=True)
        except TypeError:
            await ctx.respond(self.__music_error_messages["can_not_use_playlist"])
            return
        except IndexError:
            await ctx.respond(self.__music_error_messages["music_not_found"])
            return
        else:
            self.__music_queue.append([song,ctx.channel.id])

        bot_voice_client = ctx.voice_client
        
        if not bot_voice_client:
            author_voice_client = ctx.author.voice
            bot_voice_client = await author_voice_client.channel.connect(cls=wavelink.Player)

        await ctx.respond(embed=self.__message_added_to_queue())

        if not bot_voice_client.is_playing():
            await self.__play_music(bot_voice_client)

    @discord.slash_command(description="Commande qui permet d'arrêter la musique. Cette commande fait également le bot quitter le salon.")
    async def stop(self, ctx):
        if not await self.__user_voice_client_checks(ctx):
            return
        
        bot_voice_client = ctx.voice_client
        
        if bot_voice_client == None:
            await ctx.respond(self.__music_error_messages["bot_not_connected"])
            return
            
        self.__music_queue.clear()
        await bot_voice_client.stop()
        sleep(2)
        await bot_voice_client.disconnect()
        
        await ctx.respond("A bientôt ! :wave:")
    
    @discord.slash_command(description="Commande qui permet de mettre en pause la musique.")
    async def pause(self, ctx):
        if not await self.__user_voice_client_checks(ctx):
            return
        
        bot_voice_client = ctx.voice_client
        
        if bot_voice_client == None:
            await ctx.respond(self.__music_error_messages["bot_not_connected"])
            return
        
        if bot_voice_client.is_paused():
            await bot_voice_client.resume()
            await ctx.respond(f"La lecutre a été reprise par <@{ctx.author.id}> !")
        else:
            await bot_voice_client.pause()
            await ctx.respond(f"La musique a été mise en pause par <@{ctx.author.id}> !")
    
    @discord.slash_command(description="Commande permettant de sauter la musique actuelle.")
    async def skip(self, ctx):
        if not await self.__user_voice_client_checks(ctx):
            return
        
        bot_voice_client = ctx.voice_client
        
        if bot_voice_client == None:
            await ctx.respond(self.__music_error_messages["bot_not_connected"])
            return
        
        await ctx.respond("Je passe à la musique suivante :thumbsup:")
        await bot_voice_client.stop()
    
    @discord.slash_command(description="Commande qui permet de voir les prochaines musiques (max 6) présentes dans la liste d'attente.")
    async def queue(self, ctx):
        if len(self.__music_queue) == 0:
            await ctx.respond("La liste d'attente est actuellement vide !")
            return
        
        await ctx.respond(embed=self.__message_musics_in_queue())
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
        
        await self.__bot.get_channel(self.__music_queue[0][1]).send(embed=self.__message_now_playing())
        await bot_voice_client.play(self.__music_queue[0][0])

    def __link_check(self, link : str) -> bool:
        """This method is designed to check if the link passed in params is a Youtube link.

        Args:
            link (str): The link to check

        Returns:
            bool: True if the link is valid, False if not
        """
        valid_youtube_links = ["https://www.youtube.com/","https://youtu.be/", "www.youtube.com"]
        
        for valid_link in valid_youtube_links:
            if valid_link in link:
                return True
        
        return False
    
    async def __user_voice_client_checks(self, ctx : discord.ApplicationContext) -> bool:
        """This method is designed to check the current state of the user voice client.

        Args:
            ctx (discord.ApplicationContext): The actual context

        Returns:
            bool: True if user respects all conditions, false if one of them isn't respected
        """
        
        author_voice_client = ctx.author.voice
        bot_voice_client = ctx.voice_client

        if not author_voice_client:
            await ctx.respond(self.__music_error_messages["user_not_in_a_voice_channel"])
            return False

        if bot_voice_client and bot_voice_client.channel.id != author_voice_client.channel.id:
            await ctx.respond(self.__music_error_messages["user_not_in_same_voice_channel_of_bot"])
            return False
        
        return True
    
    def __message_added_to_queue(self) -> discord.Embed:
        message = discord.Embed(
            title="Liste d'attente",
            # TODO REVIEW Line too long (ide proposition)
            description=f"Votre musique à été ajoutée à la liste d'attente. Position : {len(self.__music_queue) - 1}",
            colour=0xffffff
        )
        return message
    
    def __message_now_playing(self) -> discord.Embed:
        message = discord.Embed(
            title="Maintenant",
            description=f"**{self.__music_queue[0][0].title}**",
            url=self.__music_queue[0][0].uri,
            colour=0xffffff
        )
        message.set_image(url = self.__music_queue[0][0].thumbnail)
        return message
    
    def __message_musics_in_queue(self) -> discord.Embed:
        message = discord.Embed(
            title="Liste d'attente",
            colour=0xffffff
        )
        
        for idx, music in enumerate(self.__music_queue[1:], start=1):
            if idx > 6:
                break
            
            message.add_field(
                name=f"{idx}:",
                value=f"[{music[0].title}]({music[0].uri})",
            )
        
        return message
    # endregion

def setup(bot):
    bot.add_cog(Music(bot))
