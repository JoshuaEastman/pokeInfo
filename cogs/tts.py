import logging
import asyncio
import discord
import tempfile
from pydub import AudioSegment
from discord.ext import commands
from config.config import config
from utils.tts_utils import generate_tts_audio

personal_user_id = int(config.personal_user_id)
logger = logging.getLogger(__name__)

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tts")
    async def tts(self, ctx, channel_name: str = None, *, message: str = None):
        if ctx.author.id != personal_user_id:
            await ctx.send("You do not have permission to use this command.")
            logger.info(f"User {ctx.author} tried to use TTS command but is not authorized.")
            return
        
        if not message:
            await ctx.send("Please include a message to speak.")
            return
        
        # Find target in VC
        target_channel = None
        if channel_name:
            for vc in ctx.guild.voice_channels:
                if vc.name.lower() == channel_name.lower():
                    target_channel = vc
                    break
            if not target_channel:
                await ctx.send(f"Channel '{channel_name}' not found.")
                return
        else:
            if ctx.author.voice:
                target_channel = ctx.author.voice.channel
            else:
                await ctx.send("You are not connected to a voice channel, and no channel name was provided.")
                return       

        audio_bytes = generate_tts_audio(message)
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp.write(audio_bytes.read())
        temp.close()

        audio_segment = AudioSegment.from_mp3(temp.name)
        wav_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_segment.export(wav_temp.name, format="wav")

        if ctx.voice_client is None: # Not connected to a voice channel
            vc = await target_channel.connect()
        else:
            if ctx.voice_client.channel != target_channel:
                await ctx.voice_client.move_to(target_channel)
            vc = ctx.voice_client

        await asyncio.sleep(1)  # Wait for the bot to connect to the channel

        vc.play(discord.FFmpegPCMAudio(wav_temp.name))
        logger.info(f"Playing TTS in {target_channel.name} for user {ctx.author}.")

        while vc.is_playing():
            await asyncio.sleep(1)

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.author.id != personal_user_id:
            await ctx.send("You do not have permission to use this command.")
            logger.info(f"User {ctx.author} tried to use leave command but is not authorized.")
            return
        
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I'm not connected to a voice channel.")

async def setup(bot: commands.Bot):
    await bot.add_cog(TTS(bot))
    print("TTS Cog loaded.") 