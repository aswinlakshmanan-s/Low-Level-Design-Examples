import threading
import datetime
from enum import Enum, auto
from typing import List

# --- Step 1: Define Log Levels ---
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

# --- Step 2: Define the Log Message ---
class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.timestamp = datetime.datetime.now()
        self.level = level
        self.message = message

    def format(self) -> str:
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.level.name}: {self.message}"

# --- Step 3: Abstract Handler Interface ---
class LogHandler:
    def write(self, log_msg: LogMessage):
        raise NotImplementedError

# --- Step 4: Concrete Handlers ---
class ConsoleHandler(LogHandler):
    def write(self, log_msg: LogMessage):
        print(log_msg.format())

class FileHandler(LogHandler):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = threading.Lock()

    def write(self, log_msg: LogMessage):
        with self.lock:
            with open(self.file_path, "a") as f:
                f.write(log_msg.format() + "\n")

# --- Step 5: Logger Configuration ---
class LogConfig:
    def __init__(self, level: LogLevel, handlers: List[LogHandler]):
        self.level = level
        self.handlers = handlers

# --- Step 6: Main Logger (Thread-safe) ---
class Logger:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, config: LogConfig):
        self.config = config
        self.log_lock = threading.Lock()

    @classmethod
    def get_instance(cls, config: LogConfig = None):
        with cls._lock:
            if cls._instance is None and config:
                cls._instance = Logger(config)
            return cls._instance

    def log(self, level: LogLevel, message: str):
        if level.value >= self.config.level.value:
            log_msg = LogMessage(level, message)
            with self.log_lock:
                for handler in self.config.handlers:
                    handler.write(log_msg)

    # Helper methods for each level
    def debug(self, message): self.log(LogLevel.DEBUG, message)
    def info(self, message): self.log(LogLevel.INFO, message)
    def warning(self, message): self.log(LogLevel.WARNING, message)
    def error(self, message): self.log(LogLevel.ERROR, message)
    def fatal(self, message): self.log(LogLevel.FATAL, message)
