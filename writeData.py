from constants import LOGGER_NAME, DUMP_FILE_PATH, MYSQL_DATETIME_FORMAT
import logging

logger = logging.getLogger(LOGGER_NAME)


def writeData(tableName, databaseName, *data):
    records = composeDataIntoInsert(tableName, *data)
    logger.info("Starting writing records to file")
    try:
        with open(DUMP_FILE_PATH, "w") as dumpFile:
            dumpFile.write(
                "CREATE DATABASE IF NOT EXISTS `{0}`;".format(databaseName)
                + "USE `{0}`;DROP TABLE IF EXISTS `{1}`;".format(
                    databaseName, tableName
                )
                + "CREATE TABLE `{0}` (ID VARCHAR(10), Instrument VARCHAR(10), Px_Init DOUBLE, Px_Fill DOUBLE, Side VARCHAR(10), Volume_Init DOUBLE, Volume_Fill DOUBLE, Datetime_Transaction DATETIME(3), Status_Transaction VARCHAR(30), Note VARCHAR(255), Tags TEXT);\n".format(
                    tableName
                )
            )
            for record in records:
                dumpFile.write("{}\n".format(record))
    except Exception as exc:
        logger.error(exc)
    finally:
        logger.info("Finished writing records to file")


def composeDataIntoInsert(
    tableName,
    idList,
    sideList,
    instrumentList,
    px_InitList,
    px_FillList,
    volume_InitList,
    volume_FillList,
    notesList,
    tagsList,
    statusList,
    datetimeList,
):
    logger.info("Starting composing data in insert")
    records = []
    for index in range(len(idList)):
        row = "INSERT INTO `{}` VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', STR_TO_DATE('{}', '{}'), '{}', '{}', '{}');".format(
            tableName,
            idList[index],
            instrumentList[index],
            px_InitList[index],
            px_FillList[index],
            sideList[index],
            volume_InitList[index],
            volume_FillList[index],
            datetimeList[index],
            MYSQL_DATETIME_FORMAT,
            statusList[index],
            notesList[index],
            tagsList[index],
        )
        records.append(row)

    logger.info("Finished composing data")
    return records