import functools
import inspect
import os
import time
from typing import Callable, ParamSpec, TypeVar

from .core import send_telegram_message

P = ParamSpec("P")
R = TypeVar("R")


def notify_telegram(func: Callable[P, R]) -> Callable[P, R]:
    """Send Telegram notifications on function start and completion.

    The decorated function sends a start message before execution, then sends a
    completion message with execution duration. If the function raises an
    exception, a failure message is sent with the exception type and duration,
    and the original exception is re-raised.

    Args:
        func: Function to decorate.

    Returns:
        A wrapped function with Telegram notifications.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        frame = inspect.currentframe()
        caller_frame = frame.f_back if frame is not None else None
        if caller_frame is None:
            script_name = "<interactive>"
        else:
            script_path = caller_frame.f_globals.get("__file__", "<interactive>")
            script_name = os.path.basename(script_path)
        func_name = func.__name__

        send_telegram_message(f"🚀 *[{script_name}]* function `{func_name}` started")
        start_time = time.perf_counter()

        try:
            result = func(*args, **kwargs)
        except Exception as error:
            duration_seconds = time.perf_counter() - start_time
            error_name = type(error).__name__
            send_telegram_message(
                f"❌ *[{script_name}]* function `{func_name}` failed ({error_name}) after {duration_seconds:.2f}s"
            )
            raise

        duration_seconds = time.perf_counter() - start_time
        send_telegram_message(
            f"✅ *[{script_name}]* function `{func_name}` finished successfully in {duration_seconds:.2f}s"
        )
        return result

    return wrapper
