import logging
from writeData import writeData
import setup
from constants import LOGGER_NAME
import ordersHistoryGenerator
import sys

logger = logging.getLogger(LOGGER_NAME)


def main():
    logger.info("Starting work")
    config = setup.run()
    try:
        data = ordersHistoryGenerator.generateData(config)
    except Exception as exc:
        logger.error(exc)
        sys.exit()
    writeData(
        config["Parameters"]["tableName"], config["Parameters"]["databaseName"], *data
    )


if __name__ == "__main__":
    main()