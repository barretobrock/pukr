import sys
from typing import (
    Dict,
    Optional
)
from pathlib import Path
from loguru import logger


# This is the general format most logs will use
BASE_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | ' \
              '<cyan>{name} -> {extra[child_name]}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - ' \
              '<level>{message}</level>'
DEFAULT_EXTRAS = {'child_name': 'main'}


def handle_exception(exc_type, exc_value, exc_traceback):
    """This is used to patch over sys.excepthook so uncaught logs are also recorded"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # We'll log uncaught errors as critical to differentiate them from caught `error` level entries
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical('Uncaught exception:')


def get_logger(log_name: str, log_dir_path: Path = None, show_backtrace: bool = True,
               base_level: str = 'DEBUG', rotation: str = '7 days', retention: str = '30 days',
               config_extras: Dict[str, Optional[str]] = None) -> logger:
    """Retrieves the loguru.logger object with proper config set up

    Args:
        log_name: name of the log. used in generating the file name (e.g., {log_name}.log)
        log_dir_path: path to the log directory. if used, will:
            1) Enable a sink to log entries to file
            2) Establish a {log_name}.log file in that directory, if none exists.
                NB! The full path to the log directory doesn't have to already exist.
                Pathlib will create such if it detects that it doesn't yet exist.
        show_backtrace: if True, will leverage loguru's backtrace feature. This is a risky thing to use for
            production environments
        rotation: the period that covers a single log file
        retention: how long log files are kept
        base_level: the minimum log level to send entries to. Note that currently this is for all sinks used.
        config_extras: a dict of any extra

    Examples:
        Getting just the logger
        >>>log = get_logger(log_name='my_app')
        Making a child instance of the above
        >>>child_log = log.bind(child_name='some_process')
    """
    sys.excepthook = handle_exception
    handlers = [
        {
            'sink': sys.stdout,
            'level': base_level,
            'format': BASE_FORMAT,
            'backtrace': show_backtrace
        }
    ]
    if config_extras is None:
        config_extras = DEFAULT_EXTRAS
    if log_dir_path is not None:
        # Add a filepath to the handlers list
        # First, ensure all the directories are made
        log_dir_path.mkdir(parents=True, exist_ok=True)
        handlers.append({
            'sink': log_dir_path.joinpath(f'{log_name}.log'),
            'level': base_level,
            'rotation': rotation,
            'retention': retention,
            'format': BASE_FORMAT,
            'enqueue': True,
            'backtrace': show_backtrace
        })
    config = {
        'handlers': handlers,
        'extra': config_extras
    }
    logger.configure(**config)
    return logger
