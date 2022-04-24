import sys
from pathlib import Path
from loguru import logger


# This is the general format most logs will use
BASE_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | ' \
              '<cyan>{name} -> {extra[child_name]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - ' \
              '<level>{message}</level>'


def get_logger(log_name: str, log_dir_path: Path = None, show_backtrace: bool = True,
               base_level: str = 'DEBUG') -> logger:
    """Retrieves the loguru.logger object with proper config set up

    Examples:
        Getting just the logger
        >>>log = get_logger(log_name='my_app')
        Making a child instance of the above
        >>>child_log = log.bind(child_name='some_process')
    """
    handlers = [
        {
            'sink': sys.stdout,
            'level': base_level,
            'format': BASE_FORMAT,
            'backtrace': show_backtrace
        }
    ]
    if log_dir_path is not None:
        # Add a filepath to the handlers list
        # First, ensure all the directories are made
        log_dir_path.mkdir(parents=True, exist_ok=True)
        handlers.append({
            'sink': log_dir_path.joinpath(f'{log_name}.log'),
            'level': base_level,
            'rotation': '1 day',
            'retention': '30 days',
            'format': BASE_FORMAT,
            'enqueue': True,
            'backtrace': show_backtrace
        })
    config = {
        'handlers': handlers,
        'extra': {
            'child_name': 'main'
        }
    }
    logger.configure(**config)
    return logger
