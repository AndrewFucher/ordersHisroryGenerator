from logging import Logger
from ohr_factory import OHRGenerator
import os.path

from constants import CONFIG_FILE_PATH
from jsonconfigparser import JSONConfigParser
from mylogger import MyLogger


class Main:
    def __init__(self) -> None:
        self._config: dict = {}
        self._config_parser: JSONConfigParser = JSONConfigParser()
        self._logger: Logger = MyLogger.getLogger(__name__)

    def start(self) -> None:
        try:
            self.setup()
            self.workflow()
        except Exception as exc:
            self._logger.error(exc.with_traceback())

    def setup(self) -> None:
        self._logger.info("Searching for config file")
        if os.path.isfile(CONFIG_FILE_PATH):
            self._logger.info("Config file was found. Retrieving configuration")
            self._config = self._config_parser.loadFrom(CONFIG_FILE_PATH)
        else:
            self._logger.info("Config file was not found. Using default config")
            self._config = self._config_parser.getDefaultConfig()
        MyLogger.setLoggingConfig(
            logger_format=self._config["Logging"]["loggingFormat"],
            logger_datetime_format=self._config["Logging"]["loggingDatetimeFormat"],
            logger_level=self._config["Logging"]["loggingLevel"],
        )
        self._logger = MyLogger.getLogger(__name__)

    def workflow(self):
        self.generateOHR()

    def generateOHR(self):
        generator: OHRGenerator = OHRGenerator(self._config)
        generator.setOHRBuilder()
        generator.setRepository()
        generator.generateData()
        generator.saveData()
        self._logger.info("Saved data")


if __name__ == "__main__":
    main: Main = Main()
    main.start()
