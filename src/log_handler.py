from string import Template
from typing import TYPE_CHECKING, cast

from discord.ext import commands

if TYPE_CHECKING:
    import discord


class LogHandler:
    def __init__(
        self, bot: commands.Bot, log_channel_id: int | None = None, error_log_channel_id: int | None = None
    ) -> None:
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.error_log_channel_id = error_log_channel_id

        self._message_template = Template("$tag: $message ($author_name@$guild_name#$channel_name)")

    async def log(self, message: str) -> None:
        await self._send(self.log_channel_id, message)

    async def error(self, message: str) -> None:
        await self._send(self.error_log_channel_id, message)

    async def command_log(self, ctx: commands.Context, tag: str, message: str) -> None:
        await self._command_message_send(ctx, self.log_channel_id, tag, message)

    async def command_error(self, ctx: commands.Context, tag: str, message: str) -> None:
        await self._command_message_send(ctx, self.error_log_channel_id, tag, message)

    async def _send(
        self,
        channel_id: int | None,
        message: str,
    ) -> None:
        if channel_id is None:
            return

        channel = cast("discord.TextChannel", self.bot.get_channel(channel_id))

        if channel is None:
            raise RuntimeError(f"Channel not found. ID: {channel_id}")

        await channel.send(message)

    async def _command_message_send(
        self,
        ctx: commands.Context,
        channel_id: int | None,
        tag: str,
        message: str,
    ) -> None:
        if channel_id is None:
            return

        guild_name = ctx.guild.name if ctx.guild else "???"
        channel_name = ctx.channel.name if isinstance(ctx.channel.name, str) else "???"
        author_name = ctx.author.name

        await self._send(
            channel_id,
            self._message_template.substitute(
                tag=tag,
                guild_name=guild_name,
                channel_name=channel_name,
                author_name=author_name,
                message=message,
            ),
        )
