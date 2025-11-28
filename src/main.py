from time import sleep

import load_env
from countdown_bot import bot


def main() -> None:
    token = load_env.load_bot_token()

    print("Starting bot...")

    while True:
        try:
            bot.run(token)
        except Exception as e:  # noqa: BLE001
            print(f"Bot crashed: {e}. Restarting in 5 seconds...")
            sleep(5)


if __name__ == "__main__":
    main()
