# ==============================================================================
#                 © 2025 Dedalus Labs, Inc. All Rights Reserved.
#                        PROPRIETARY AND CONFIDENTIAL
#             This source code is the property of Dedalus Labs, Inc.
#          Unauthorized copying or distribution is strictly prohibited.
# ==============================================================================

"""Lightweight, colorful, and developer-friendly logging using standard logging and Colorama."""

import logging
import os
import sys
import time
import traceback
from functools import wraps
from typing import Any, Optional, Callable

from colorama import Fore, Style, init as colorama_init

# Initialize Colorama
colorama_init(autoreset=True)

# Environment variable for debugging
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")


class SmartColorFormatter(logging.Formatter):
    """Combines Colorama's simplicity for coloring with custom formatting for readability."""

    COLORS = {
        logging.DEBUG: Fore.LIGHTMAGENTA_EX + Style.BRIGHT,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,  # Same as ERROR for emphasis
    }

    SYMBOLS = {
        logging.DEBUG: "›",
        logging.INFO: "•",
        logging.WARNING: "!",
        logging.ERROR: "×",
        logging.CRITICAL: "‼",
    }

    # Colors for other parts of the log message (can be customized further)
    TIME_COLOR = Fore.GREEN
    FILE_COLOR = Fore.BLUE
    # LEVEL_NAME_COLOR can be implicitly handled by COLORS if LEVEL_COLOR is just Style.BRIGHT

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        super().__init__(
            fmt
            or "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt or "%Y-%m-%d %H:%M:%S",
        )

    def format(self, record: logging.LogRecord) -> str:
        timing_indicator = ""
        if hasattr(record, "timing") and isinstance(record.timing, (int, float)):
            timing_indicator = self._format_timing(record.timing)

        level_color = self.COLORS.get(record.levelno, Fore.WHITE)
        symbol = self.SYMBOLS.get(record.levelno, "•")

        time_part = f"{self.TIME_COLOR}{self.formatTime(record)}{Style.RESET_ALL}"
        # Using record.levelname which is already part of the standard LogRecord
        level_part = f"{level_color}{symbol} {record.levelname}{Style.RESET_ALL}"
        file_part = (
            f"{self.FILE_COLOR}{record.filename}:{record.lineno}{Style.RESET_ALL}"
        )

        # Get the basic message
        message = record.getMessage()  # Handles %-style formatting if args are present

        # Add custom context attributes if they exist on the record
        # These would be added by LogContext or if logger.log(level, msg, extra={...}) is used
        extra_attrs = []
        standard_keys = list(
            logging.LogRecord("", 0, "", 0, "", (), None, None).__dict__.keys()
        ) + ["message", "asctime", "timing"]
        for key, value in record.__dict__.items():
            if key not in standard_keys:
                extra_attrs.append(
                    f"{Fore.MAGENTA}{key}{Style.RESET_ALL}={value!r}"
                )  # Example coloring for extras

        extra_part = ""
        if extra_attrs:
            extra_part = (
                f" ({Style.DIM}{Fore.WHITE}{', '.join(extra_attrs)}{Style.RESET_ALL})"
            )

        msg = f"{time_part} {level_part} {file_part} - {message}{extra_part}"

        if timing_indicator:
            msg = f"{msg} {timing_indicator}"

        if record.exc_info:
            exc_text = self._format_exception(record.exc_info)
            msg = f"{msg}\n{exc_text}"  # Newline before traceback

        return msg

    def _format_timing(self, ms: int) -> str:
        if ms > 2000:  # p99 territory
            return f"{Fore.RED + Style.BRIGHT}(!!! {ms}ms !!!){Style.RESET_ALL}"
        elif ms > 800:  # p95
            return f"{Fore.RED}({ms}ms){Style.RESET_ALL}"
        elif ms > 300:  # p75
            return f"{Fore.YELLOW}({ms}ms){Style.RESET_ALL}"
        elif ms < 50:  # p25 - blazing fast
            return f"{Fore.GREEN + Style.BRIGHT}({ms}ms 🔥){Style.RESET_ALL}"
        return f"{Fore.GREEN}({ms}ms){Style.RESET_ALL}"

    def _format_exception(self, exc_info: tuple) -> str:
        exc_type, exc_value, tb = exc_info

        noisy_paths = [
            "uvicorn",
            "fastapi",
            "pydantic",
            "starlette",
            "colorama",
            "logging",
            "sqlalchemy",
            "asyncio",
            "click",
            "pytest",
            "werkzeug",
            __file__,
        ]

        def frame_relevance(frame: traceback.FrameSummary) -> bool:
            if any(noisy_path in frame.filename for noisy_path in noisy_paths):
                return False

            project_root = os.getcwd()
            if frame.filename.endswith("/__init__.py") or frame.filename.endswith(
                "\\__init__.py"
            ):
                if not os.path.dirname(frame.filename).startswith(project_root):
                    return False
            return True

        tb_frames = traceback.extract_tb(tb)
        relevant_frames = [frame for frame in tb_frames if frame_relevance(frame)]

        formatted_lines = [f"{Fore.RED}Traceback:{Style.RESET_ALL}"]
        if not relevant_frames and tb_frames:
            formatted_lines.append(
                f"{Style.DIM}(No project frames found, showing last 3 frames){Style.RESET_ALL}"
            )
            relevant_frames = tb_frames[-3:]

        for frame in relevant_frames:
            filename_display = (
                os.path.relpath(frame.filename, os.getcwd())
                if frame.filename.startswith(os.getcwd())
                else os.path.basename(frame.filename)
            )
            code_line = frame.line.strip() if frame.line else ""
            is_project_frame = frame.filename.startswith(os.getcwd())

            line_style = "" if is_project_frame else Style.DIM
            func_style = Style.BRIGHT if is_project_frame else ""
            path_color = Fore.BLUE  # Consistent path color

            formatted_lines.extend(
                [
                    f"  {path_color}{filename_display}:{frame.lineno}{Style.RESET_ALL} in {func_style}{frame.name}{Style.RESET_ALL}",
                    f"    {line_style}{code_line}{Style.RESET_ALL}",
                ]
            )

        formatted_lines.append(
            f"{Fore.RED}{Style.BRIGHT}{exc_type.__name__}{Style.RESET_ALL}: {Fore.RED}{exc_value}{Style.RESET_ALL}"
        )
        return "\n".join(formatted_lines)


class LogContext:
    """Context manager to add temporary context to log records."""

    def __init__(self, logger_instance: logging.Logger, **kwargs: Any):
        self.logger = logger_instance
        self.kwargs = kwargs
        self._old_factory: Optional[Callable[..., logging.LogRecord]] = None

    def __enter__(self) -> logging.Logger:
        self._old_factory = self.logger.makeRecord

        # Keep a reference to the old factory for the new factory to call
        original_make_record = self._old_factory

        def new_factory(*args: Any, **factory_kwargs: Any) -> logging.LogRecord:
            # call original factory to get a record
            record = original_make_record(*args, **factory_kwargs)
            # then add our custom context
            for k, v in self.kwargs.items():
                setattr(record, k, v)
            return record

        self.logger.makeRecord = new_factory
        return self.logger

    def __exit__(self, *args: Any) -> None:
        if self._old_factory is not None:
            self.logger.makeRecord = self._old_factory


# @wraps is good practice but functools.wraps needs to be imported
# from functools import wraps # Assuming it's at the top if used. It is.
def timed(func: Callable) -> Callable:
    """Simplified but effective timing decorator that adds 'timing' to log records."""

    @wraps(func)  # functools.wraps should be imported
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        func_name = func.__name__
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_ms = int((end_time - start_time) * 1000)
            # Add timing as an extra field for the formatter to pick up
            logger.info(f"{func_name} completed", extra={"timing": elapsed_ms})
            return result
        except Exception:
            end_time = time.perf_counter()
            elapsed_ms = int((end_time - start_time) * 1000)
            # Log error with timing and exc_info for traceback
            logger.error(
                f"{func_name} failed", exc_info=True, extra={"timing": elapsed_ms}
            )
            raise  # Re-raise the exception

    return wrapper


def log_group(description: str) -> LogContext:
    """Helper for creating a LogContext for logical groups of logs, adding group description and start time."""
    return LogContext(
        logger,  # Assumes global logger is accessible here
        group=description,
        group_start_time=time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
        ),  # Formatted start time
    )


def setup_logger() -> logging.Logger:
    """Sets up a logger with SmartColorFormatter, logging to stdout."""
    logger_instance = logging.getLogger(__name__)  # Or a specific name like "app"

    # Prevent multiple handlers if re-initialized (e.g., in tests or interactive sessions)
    if logger_instance.hasHandlers():
        logger_instance.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = SmartColorFormatter()
    handler.setFormatter(formatter)

    logger_instance.addHandler(handler)
    logger_instance.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    logger_instance.propagate = (
        False  # Important to prevent duplicate logs if root logger also has handlers
    )

    return logger_instance


# Global logger instance
logger = setup_logger()

if __name__ == "__main__":
    logger.info(
        "Logger Showcase: Initializing examples...",
        extra={"version": "1.0.0", "debug_mode": DEBUG},
    )
    logger.debug(
        "Detailed debug message for setup.", extra={"internal_step": "config_loaded"}
    )

    # 1. Using log_group for a conceptual block of operations
    with log_group("User Onboarding Process"):
        logger.info(
            "Starting new user registration.", extra={"user_email": "test@example.com"}
        )
        time.sleep(0.03)  # Should trigger blazing fast 🔥
        logger.info(
            "Validated user input.", extra={"timing": 30}
        )  # Manually add timing for display
        logger.warning("Password strength is moderate.", extra={"strength_score": 65})
        logger.info("User account created.")

    # 2. Using @timed decorator for various scenarios
    @timed
    def quick_task_timed():
        logger.debug("Executing quick_task_timed...")
        time.sleep(0.02)  # Blazing fast 🔥
        return "Quick task finished!"

    @timed
    def data_processing_timed(data_size_kb: int):
        logger.info(f"Processing {data_size_kb}KB of data...")
        if data_size_kb < 100:
            time.sleep(0.4)  # p75 (yellow)
        elif data_size_kb < 1000:
            time.sleep(0.9)  # p95 (red)
        else:
            time.sleep(2.5)  # p99 (!!! red !!!)
        return f"Processed {data_size_kb}KB."

    @timed
    def failing_operation_timed():
        logger.info("Attempting a risky operation...")
        time.sleep(0.1)  # Normal green

        # This will cause a nested error for traceback demo
        def cause_error():
            a = {}
            return a["non_existent_key"]

        cause_error()
        return "This won't be reached."

    quick_task_timed()
    data_processing_timed(data_size_kb=50)
    data_processing_timed(data_size_kb=500)
    data_processing_timed(data_size_kb=1500)

    try:
        failing_operation_timed()
    except KeyError as e:
        # The @timed decorator already logged the error with exc_info=True.
        # This critical log shows how one might log a follow-up action or summary.
        logger.critical(
            f"Handled expected KeyError from failing_operation_timed: {e}",
            exc_info=False,  # Avoid duplicate traceback
            extra={"recovery_attempted": False},
        )

    # 3. Using LogContext for broader contextual logging
    with LogContext(logger, request_id="req-abc-987", user_id="usr-xyz-123"):
        logger.info(
            "API request received.", extra={"endpoint": "/api/data", "method": "POST"}
        )
        time.sleep(0.015)  # Blazing fast 🔥
        logger.info("Request validated.", extra={"timing": 15})
        logger.error(
            "Failed to connect to external service.",
            extra={"service_name": "auth_provider", "attempt": 1, "timeout_s": 5},
        )
        logger.info("API request processing finished.")

    # 4. Final log to signify completion
    logger.info(
        "Logger showcase finished.", extra={"final_status": "All examples executed"}
    )
