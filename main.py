from logging import Logger
from ohr_factory import OHRGenerator
import os.path

from constants import CONFIG_FILE_PATH
from jsonconfigparser import JSONConfigParser
from mylogger import MyLogger

logger: Logger = MyLogger.getLogger(__name__)
config_parser: JSONConfigParser = None
config: dict = {}


def init():
    global config_parser
    config_parser = JSONConfigParser()


def setup():
    global config
    global logger
    logger.info("Searching for config file")
    if os.path.isfile(CONFIG_FILE_PATH):
        logger.info("Config file was found. Retrieving configuration")
        config = config_parser.loadFrom(CONFIG_FILE_PATH)
    else:
        logger.info("Config file was not found. Using default config")
        config = config_parser.getDefaultConfig()    
    MyLogger.setLoggingConfig(
        logger_format=config["Logging"]["loggingFormat"],
        logger_datetime_format=config["Logging"]["loggingDatetimeFormat"],
        logger_level=config["Logging"]["loggingLevel"],
        # logger_file_path=config["Logging"]["logsFolder"],
    )
    logger = MyLogger.getLogger(__name__)


def workflow():
    generateOHR()

def generateOHR():
    generator: OHRGenerator = OHRGenerator(config)
    generator.setOHRBuilder()
    generator.setRepository()
    generator.generateData()
    generator.saveData()
    logger.info("Saved data")

if __name__ == "__main__":
    try:
        init()
        setup()
        workflow()
    except Exception as exc:
        logger.error(exc)
        logger.error(exc.with_traceback())
        print(exc.with_traceback())
