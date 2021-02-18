import json
import datetime
import logging
from constants import CONFIG_FILE_PATH, CONFIG_DEFAULT_FILE_PATH, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def overrideConfig(a, b):
    for key in b:
        if key in a:  # if key is in both a and b
            if isinstance(a[key], dict) and isinstance(
                b[key], dict
            ):  # if the key is dict Object
                overrideConfig(a[key], b[key])
            else:
                a[key] = b[key]
        else:  # if the key is not in dict a , add it to dict a
            a.update({key: b[key]})
    return a


def parseConfig() -> dict:

    configDefault = parseJson(CONFIG_DEFAULT_FILE_PATH)
    config = parseJson(CONFIG_FILE_PATH)

    # configDefault.update(configDefault)

    config = overrideConfig(configDefault, config)

    return config


def parseJson(filePath) -> dict:

    try:
        with open(filePath) as jsonFile:
            jsonFileData = json.load(jsonFile)
    except Exception as exception:
        logger.error(exception)
        return dict()

    return jsonFileData


def setLoggingParameters(config):
    logging.basicConfig(
        filename=config["Logging"]["logsFolder"] + str(datetime.date.today()) + ".txt",
        format=config["Logging"]["loggingFormat"],
        datefmt=config["Logging"]["loggingDatetimeFormat"],
        level=config["Logging"]["loggingLevel"],
    )


def run() -> dict:

    logger.info("Setting up config")

    config = parseConfig()
    setLoggingParameters(config)

    logger.info("Finished setting up config")

    return config