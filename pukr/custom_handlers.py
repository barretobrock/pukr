import logging

from loguru._logger import Logger


class InterceptHandler(logging.Handler):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def emit(self, record):
        # Get corresponding loguru level if it exists
        try:
            level = self.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find call whence the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        self.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
