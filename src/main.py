import discord
from discord.ext import commands

import load_env
from countdown_cog import CountdownCog
from log_handler import LogHandler


def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(
        command_prefix="!",
        intents=intents,
        description="レース用カウントダウンBot: !rc でテキストカウントダウン、!vrc でボイスカウントダウン",
    )

    logger = LogHandler(
        bot,
        log_channel_id=load_env.load_log_channel_id(),
        error_log_channel_id=load_env.load_error_log_channel_id(),
    )

    @bot.event
    async def on_ready() -> None:
        await logger.log(f"Wake up as {bot.user}")

    async def setup_hook() -> None:
        await bot.add_cog(CountdownCog(logger, load_env.load_countdown_source()))

    bot.setup_hook = setup_hook  # type: ignore[assignment]

    print("Starting bot...")
    token = load_env.load_bot_token()

    if token is None:
        print("Bot token not found. BOT_TOKEN environment variable is not set.")
        return

    bot.run(token, reconnect=True)


if __name__ == "__main__":
    main()
