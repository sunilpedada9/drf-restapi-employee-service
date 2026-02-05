import logging
import os

class LoggingConfig:

    def __init__(self):
        print("In LoggingConfig")
        self.level = os.environ["LOGGER_LEVEL"]
        self.level = logging.INFO if self.level.lower()=='info' else logging.DEBUG
        logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",level=self.level)