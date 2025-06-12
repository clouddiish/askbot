import traceback
import functools

from utils.logger import logger
from config import DEV_USER_ID


def catch_generic_exception(fallback_channel_attr: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                # log the error that occurred during the execution of the function
                logger.error(f"unexpected error in {func.__name__}:\n%s", traceback.format_exc())

                # start the notification process to the dev
                try:
                    self = args[0]  # assuming 'self' is the first argument (for instance methods)
                    bot = self.bot

                    # determine if ctx is present (e.g., in command functions)
                    ctx = args[1] if len(args) > 1 and hasattr(args[1], "send") else None
                    channel = getattr(ctx, "channel", None)

                    # fallback if no channel is found
                    if not channel and fallback_channel_attr:
                        channel = getattr(self, fallback_channel_attr, None)

                    # notify dev
                    dev = await bot.fetch_user(DEV_USER_ID)
                    if channel:
                        await channel.send(f"ow something went wrong :-( Please check the logs {dev.mention}")
                    else:
                        # send DM to the dev if no valid channel is found
                        logger.warning("no valid fallback channel found for error notification")
                        await dev.send(
                            f"error happened in {func.__name__} and no fallback channel was found:\n\n{traceback.format_exc()}"
                        )
                except Exception as notify_err:
                    # log any failure in the notification process
                    logger.error(f"failed to notify dev: {notify_err}")

        return wrapper

    return decorator
