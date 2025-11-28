import load_env
from countdown_bot import bot


def main() -> None:
    token = load_env.load_bot_token()

    print("Starting bot...")

    bot.run(token, reconnect=True)


if __name__ == "__main__":
    main()
