from string import Template

from discord.ext import commands

from load_env import load_error_log_channel_id, load_log_channel_id


class LogHandler:
    def __init__(self) -> None:
        self.log_channel_id = load_log_channel_id()
        self.error_log_channel_id = load_error_log_channel_id()

        self._message_template = Template("$tag: $message ($author_name@$guild_name#$channel_name)")

    async def log(self, bot: commands.Bot, message: str) -> None:
        await self._send(bot, self.log_channel_id, message)

    async def error(self, bot: commands.Bot, message: str) -> None:
        await self._send(bot, self.error_log_channel_id, message)

    async def command_log(self, bot: commands.Bot, ctx: commands.Context, tag: str, message: str) -> None:
        await self._command_message_send(bot, ctx, self.log_channel_id, tag, message)

    async def command_error(self, bot: commands.Bot, ctx: commands.Context, tag: str, message: str) -> None:
        await self._command_message_send(bot, ctx, self.error_log_channel_id, tag, message)

    async def _send(
        self,
        bot: commands.Bot,
        channel_id: int | None,
        message: str,
    ) -> None:
        if channel_id is None:
            return

        channel = bot.get_channel(channel_id)

        if channel is None:
            raise RuntimeError(f"Channel not found. ID: {channel_id}")

        await channel.send(message)

    async def _command_message_send(
        self,
        bot: commands.Bot,
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
            bot,
            channel_id,
            self._message_template.substitute(
                tag=tag,
                guild_name=guild_name,
                channel_name=channel_name,
                author_name=author_name,
                message=message,
            ),
        )
