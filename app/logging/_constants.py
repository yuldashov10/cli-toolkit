LOG_FILE_MAX_BYTES: int = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT: int = 5
LOG_FILE_FORMAT: str = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
LOG_CONSOLE_FORMAT: str = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT: str = "%d-%m-%Y %H:%M:%S"
LOG_CONSOLE_DATE_FORMAT: str = "%H:%M:%S"
