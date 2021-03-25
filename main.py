import logging
from typing import List
from logging import Logger
import os.path

from dataobjects import OHRDTO, OHRDomainModel, OHRDomainModelToDTOMapper
from repository import MySQLTXTRepository
from ohr_generator import OHRBuilder1
from ohr_factory import OHRGeneratorFactory
from constants import CONFIG_FILE_PATH, DUMP_FILE_PATH
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

    def workflow(self) -> None:
        data: OHRDomainModel = self.generateOHR()
        self._logger.info("Generated data (Domain Model)")
        
        converted_data: List[OHRDTO] = OHRDomainModelToDTOMapper.mapToDTO(data)
        self._logger.info("Converted data to DTO")

        repository: MySQLTXTRepository = MySQLTXTRepository(self._config)
        repository.addRange(converted_data)
        repository.saveTo(DUMP_FILE_PATH)
        self._logger.info("Saved data to {}".format(DUMP_FILE_PATH))
        

    def generateOHR(self) -> OHRDomainModel:
        generator: OHRGeneratorFactory = OHRGeneratorFactory()
        generator.setOHRBuilder(OHRBuilder1(self._config))
        return generator.generateData()


if __name__ == "__main__":
    main: Main = Main()
    main.start()
