import logging
from mylogger import MyLogger
from constants import DUMP_FILE_PATH
from dataobjects import OHRDomainModel, OHRDomainModelToDTOMapper
from ohr_generator import IOHRBuilder, OHRBuilder1
from repository import MySQLTXTRepository


class OHRGeneratorFactory:
    def __init__(self) -> None:
        self._logger = MyLogger.getLogger(__name__)

    def setOHRBuilder(self, builder: IOHRBuilder) -> None:
        self._builder: IOHRBuilder = builder

    def generateData(self) -> OHRDomainModel:
        self._logger.info("Builder type is {}".format(type(self._builder)))
        if isinstance(self._builder, OHRBuilder1):
            self._generateDataBuilder1()
        print(type(self._builder))
        return self._builder.getResult()

    def _generateDataBuilder1(self):
        self._builder.buildSeriesList()
        self._builder.buildStatus()
        self._builder.buildInstrument()

        self._builder.buildSide()
        self._builder.buildTags()
        self._builder.buildNote()
        self._builder.buildID()
        self._builder.buildPrice()
        self._builder.buildVolume()
        self._builder.buildDatetime()
