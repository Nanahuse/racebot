import os


def load_bot_token() -> str:
    result = os.environ.get("BOT_TOKEN")

    if result is None:
        raise RuntimeError("BOT_TOKEN is not set in environment variables.")

    return result


def load_log_channel_id() -> int | None:
    result = os.environ.get("LOG_CHANNEL_ID")

    if result is None:
        print("Warning: LOG_CHANNEL_ID is not set in environment variables.")
        return None

    return int(result)


def load_error_log_channel_id() -> int | None:
    result = os.environ.get("ERROR_LOG_CHANNEL_ID")

    if result is None:
        print("Warning: ERROR_LOG_CHANNEL_ID is not set in environment variables.")
        return None

    return int(result)
