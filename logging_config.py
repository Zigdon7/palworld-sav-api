import logging
import time


class LoggerManager:
    def __init__(self, name=__name__, log_file="app.log", formatter=None):
        self.logger = logging.getLogger(name)
        self.clear_handlers()  # Remove any existing handlers
        self._configure_logger(log_file, formatter)

    def _configure_logger(self, log_file, formatter=None):
        self.logger.setLevel(logging.DEBUG)  # Set the logging level

        # Create a file handler and set its level to DEBUG
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler and set its level to DEBUG
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter
        if not formatter:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def clear_handlers(self):
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log errors with traceback"""
        self.logger.error(msg, *args, **kwargs, exc_info=True)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def set_level(self, level):
        """Set the logging level for both the logger and its handlers."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def add_handler(self, handler):
        """Add a new handler to the logger."""
        self.logger.addHandler(handler)

    def remove_handler(self, handler):
        """Remove a handler from the logger."""
        self.logger.removeHandler(handler)

    class Timer:
        """A context manager to measure execution time and log it."""
        def __init__(self, logger, operation_name="operation"):
            self.start_time = None
            self.logger = logger
            self.operation_name = operation_name

        def __enter__(self):
            self.start_time = time.time()

        def __exit__(self, exc_type, exc_val, exc_tb):
            elapsed_time = time.time() - self.start_time
            self.logger.info(f"{self.operation_name} took {elapsed_time:.2f} seconds")

    def time_it(self, operation_name="operation"):
        """Utility function to get the Timer context manager."""
        return self.Timer(self, operation_name)