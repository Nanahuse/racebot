import asyncio

import discord
from discord.ext import commands

from log_handler import LogHandler
from semaphore import Semaphore

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


async def countdown_with_voice(ctx: commands.Context, vc: discord.VoiceClient, source: str) -> None:
    audio_source = discord.FFmpegPCMAudio(source)

    vc.play(audio_source)

    await countdown(ctx)
    await wait_until_finish_playing(vc)


async def wait_until_finish_playing(vc: discord.VoiceClient) -> None:
    while vc.is_playing():  # noqa: ASYNC110
        await asyncio.sleep(0.1)


# Cog


class CountdownCog(commands.Cog):
    def __init__(self, logger: LogHandler, countdown_source: str) -> None:
        super().__init__()

        self.logger: LogHandler = logger
        self.countdown_source: str = countdown_source

        self._text_channel_semaphore = Semaphore()
        self._voice_channel_semaphore = Semaphore()
        self._voice_lock = asyncio.Lock()

    @property
    def qualified_name(self) -> str:
        return "Countdown"

    @commands.command(help="テキストでレースカウントダウンを行います。")
    async def rc(self, ctx: commands.Context) -> None:
        await self.logger.command_log(ctx, "rc", "start")

        with self._text_channel_semaphore.acquire(ctx.channel.id) as is_text_channel_acquired:
            if not is_text_channel_acquired:
                await self.logger.command_log(ctx, "rc", "cancelled: countdown busy.")
                return

            await asyncio.sleep(1)

            await countdown(ctx)

            await self.logger.command_log(ctx, "rc", "finish")

    @commands.command(
        help="テキストでのカウントと共にボイスチャンネルでカウントダウン音声を再生します。ボイスチャンネル参加必須。"
    )
    async def vrc(self, ctx: commands.Context) -> None:
        await self.logger.command_log(ctx, "vrc", "start")

        if ctx.author.voice is None:
            await ctx.send(
                "`!vrc`コマンドはボイスチャンネルに参加していないと使えません。\n読み上げが不要な場合は`!rc`コマンドが使えます。"
            )
            await self.logger.command_log(ctx, "vrc", "cancelled: not in voice channel.")
            return

        voice_channel: discord.VoiceChannel = ctx.author.voice.channel

        with (
            self._text_channel_semaphore.acquire(ctx.channel.id) as is_text_channel_acquired,
            self._voice_channel_semaphore.acquire(voice_channel.id) as is_voice_channel_acquired,
        ):
            if not is_text_channel_acquired:
                await self.logger.command_log(ctx, "vrc", "cancelled: text countdown busy.")
                return

            if not is_voice_channel_acquired:
                await self.logger.command_log(ctx, "vrc", "cancelled: voice countdown busy.")
                return

            async with self._voice_lock:
                try:
                    if ctx.voice_client is None:
                        vc: discord.VoiceClient = await voice_channel.connect()
                    elif isinstance(ctx.voice_client, discord.VoiceClient):
                        vc: discord.VoiceClient = ctx.voice_client
                        await vc.move_to(voice_channel)
                    else:
                        await ctx.send("ボイスチャンネルへの接続に失敗しました。もう一度お試しください。")
                        await self.logger.command_log(ctx, "vrc", "cancelled: voice client invalid.")
                        return

                    await asyncio.sleep(1)

                    await asyncio.wait_for(
                        countdown_with_voice(ctx, vc, self.countdown_source),
                        timeout=30,
                    )

                    await asyncio.sleep(2)

                finally:
                    if vc is not None and vc.is_connected():
                        await vc.disconnect()

        await self.logger.command_log(ctx, "vrc", "finish")
