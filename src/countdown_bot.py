import asyncio

import discord
from discord.ext import commands

from load_env import load_countdown_source
from log_handler import LogHandler
from semaphore import Semaphore

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="レース用カウントダウンBot: !rc でテキストカウントダウン、!vrc でボイスカウントダウン",
)

channel_semaphore = Semaphore()
logger = LogHandler()
voice_lock = asyncio.Lock()

# Bot Events and Commands


@bot.event
async def on_ready() -> None:
    await logger.log(bot, f"Wake up as {bot.user}")  # noqa: G004


@bot.command(help="テキストでレースカウントダウンを行います。")
async def rc(ctx: commands.Context) -> None:
    await logger.command_log(bot, ctx, "rc", "start")

    with channel_semaphore.acquire(ctx.channel.id) as is_acquired:
        if not is_acquired:
            await logger.command_log(bot, ctx, "rc", "cancelled: countdown busy.")
            return

        await asyncio.sleep(1)

        await countdown(ctx)

        await logger.command_log(bot, ctx, "rc", "finish")


@bot.command(
    help="テキストでのカウントと共にボイスチャンネルでカウントダウン音声を再生します。ボイスチャンネル参加必須。"
)
async def vrc(ctx: commands.Context) -> None:
    await logger.command_log(bot, ctx, "vrc", "start")

    if ctx.author.voice is None:
        await ctx.send(
            "`!vrc`コマンドはボイスチャンネルに参加していないと使えません。\n読み上げが不要な場合は`!rc`コマンドが使えます。"
        )
        await logger.command_log(bot, ctx, "vrc", "cancelled: not in voice channel.")
        return

    voice_channel: discord.VoiceChannel = ctx.author.voice.channel

    with (
        channel_semaphore.acquire(ctx.channel.id) as is_acquired,
        channel_semaphore.acquire(voice_channel.id) as is_acquired_voice,
    ):
        if not is_acquired:
            await logger.command_log(bot, ctx, "vrc", "cancelled: text countdown busy.")
            return

        if not is_acquired_voice:
            await logger.command_log(bot, ctx, "vrc", "cancelled: voice countdown busy.")
            return

        async with voice_lock:
            try:
                if ctx.voice_client is None:
                    vc: discord.VoiceClient = await voice_channel.connect()
                else:
                    vc: discord.VoiceClient = ctx.voice_client
                    await vc.move_to(voice_channel)

                await asyncio.sleep(1)

                audio_source = discord.FFmpegPCMAudio(load_countdown_source())

                vc.play(audio_source)

                await countdown(ctx)

                await wait_until_finish_playing(vc)

                await asyncio.sleep(2)

            finally:
                await vc.disconnect()

    await logger.command_log(bot, ctx, "vrc", "finish")


# Helper Functions


async def delayed_send(ctx: commands.Context, delay: float, message: str) -> None:
    await asyncio.sleep(delay)
    await ctx.send(message)


async def countdown(ctx: commands.Context) -> None:
    await asyncio.gather(
        delayed_send(ctx, 0, "The race will start in 10 seconds!"),
        delayed_send(ctx, 5, "The race will start in 5 seconds!"),
        delayed_send(ctx, 7, "3"),
        delayed_send(ctx, 8, "2"),
        delayed_send(ctx, 9, "1"),
        delayed_send(ctx, 10, "Go!"),
    )


async def wait_until_finish_playing(vc: discord.VoiceClient) -> None:
    while vc.is_playing():  # noqa: ASYNC110
        await asyncio.sleep(0.1)
