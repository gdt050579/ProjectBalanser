
import os
import logging
import logging.handlers
import functools
from typing import Callable
from timeit import default_timer as timer


class Logger:
    # Custom Formatters
    class ColourFormatter(logging.Formatter):
        LEVEL_COLOURS = [
            (logging.DEBUG, "\x1b[37;1m"),
            (logging.INFO, "\x1b[34;1m"),
            (logging.WARNING, "\x1b[33;1m"),
            (logging.ERROR, "\x1b[31m"),
            (logging.CRITICAL, "\x1b[41m"),
        ]

        FORMATS = {
            level: logging.Formatter(
                f"\x1b[37;1m%(asctime)s\x1b[0m | {colour}%(levelname)-8s\x1b[0m | \x1b[36;1m%(module)s\x1b[0m | \x1b[35m%(funcName)s\x1b[0m | %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, colour in LEVEL_COLOURS
        }

        def format(self, record):
            formatter = self.FORMATS.get(record.levelno)
            if formatter is None:
                formatter = self.FORMATS[logging.DEBUG]

            # Override the traceback to always print in red
            if record.exc_info:
                text = formatter.formatException(record.exc_info)
                record.exc_text = f"\x1b[31m{text}\x1b[0m"

            output = formatter.format(record)

            # Remove the cache layer
            record.exc_text = None
            return output

    class DefaultFormatter(logging.Formatter):
        def __init__(self):
            super().__init__(fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(funcName)s | %(message)s")

    # Custom Handlers
    class ConsoleHandler(logging.StreamHandler):
        def __init__(self, initialFormatter: logging.Formatter):
            super().__init__()
            self.setLevel(logging.DEBUG)
            self.setFormatter(initialFormatter)

    class FileLogHandler(logging.FileHandler):
        def __init__(self, filePath: str, initialFormatter: logging.Formatter):
            super().__init__(f"{filePath}.log")
            self.setLevel(logging.DEBUG)
            self.setFormatter(initialFormatter)

    class FileErrorHandler(logging.FileHandler):
        def __init__(self, filePath: str, initialFormatter: logging.Formatter):
            super().__init__(f"{filePath}.err")
            self.setLevel(logging.WARNING)
            self.setFormatter(initialFormatter)

    # init the logger
    __loggerInstance = logging.getLogger("balanser")
    __loggerInstance.setLevel(logging.DEBUG)

    __logger = __loggerInstance

    # formatter
    __formatter = DefaultFormatter()
    __coloredFormatter = ColourFormatter()

    # console handler
    __consoleHandler = ConsoleHandler(__coloredFormatter)
    __loggerInstance.addHandler(__consoleHandler)

    # file handlers
    __fullLogFileHandlers = dict()
    __errorsLogFileHandlers = dict()

    @staticmethod
    def logOnTheDisk(filePath: str) -> None:
        logger = Logger.__loggerInstance

        filePath = os.path.abspath(filePath)
        dirPath = os.path.dirname(filePath)
        os.makedirs(dirPath, exist_ok=True)

        if filePath not in Logger.__fullLogFileHandlers:
            fileHandler = Logger.FileLogHandler(filePath, Logger.__formatter)
            logger.addHandler(fileHandler)
            Logger.__fullLogFileHandlers[filePath] = fileHandler

        if filePath not in Logger.__errorsLogFileHandlers:
            fileHandler = Logger.FileErrorHandler(filePath, Logger.__formatter)
            logger.addHandler(fileHandler)
            Logger.__errorsLogFileHandlers[filePath] = fileHandler

    @staticmethod
    def stopLogOnTheDisk(filePath: str) -> None:
        logger = Logger.__loggerInstance

        filePath = os.path.abspath(filePath)

        if filePath in Logger.__fullLogFileHandlers:
            fileHandler = Logger.__fullLogFileHandlers[filePath]
            logger.removeHandler(fileHandler)
            fileHandler.close()
            del Logger.__fullLogFileHandlers[filePath]

        if filePath in Logger.__errorsLogFileHandlers:
            fileHandler = Logger.__errorsLogFileHandlers[filePath]
            logger.removeHandler(fileHandler)
            fileHandler.close()
            del Logger.__errorsLogFileHandlers[filePath]

    # Wrappers for using the actual value of the Logger.__logger
    @staticmethod
    def debug(msg, *args, **kwargs):
        Logger.__logger.debug(msg, stacklevel=kwargs.pop("stacklevel", 2), *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        Logger.__logger.info(msg, stacklevel=kwargs.pop("stacklevel", 2), *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        Logger.__logger.warning(msg, stacklevel=kwargs.pop("stacklevel", 2), *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        Logger.__logger.error(msg, stacklevel=kwargs.pop("stacklevel", 2), *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        Logger.__logger.exception(msg, stacklevel=kwargs.pop("stacklevel", 3), *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        Logger.__logger.critical(msg, stacklevel=kwargs.pop("stacklevel", 2), *args, **kwargs)


debug = Logger.debug
info = Logger.info
warning = Logger.warning
error = Logger.error
exception = Logger.exception
critical = Logger.critical
logOnTheDisk = Logger.logOnTheDisk
stopLogOnTheDisk = Logger.stopLogOnTheDisk


class FunctionDebug:
    def __init__(self, function: Callable):
        functools.update_wrapper(self, function)
        self.__function = function

    def __call__(self, *args, **kwargs):
        functionName = getattr(self.__function, "__name__", "UnknownFunction")

        debug(f"Function {functionName} called with arguments {args} and keyword arguments {kwargs}", stacklevel=3)

        start = timer()
        result = self.__function(*args, **kwargs)
        end = timer()

        debug(f"Function {functionName} returned {result} in {round(end - start, 2)} seconds", stacklevel=3)

        return result

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)

