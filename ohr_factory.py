from constants import DUMP_FILE_PATH
from dataobjects import OHRDomainModelToDTOMapper
from ohr_generator import IOHRBuilder, OHRBuilder1
from repository import MySQLTXTRepository


class OHRGenerator:
    def __init__(self, config: dict) -> None:
        self._config = config
        self._mapper = OHRDomainModelToDTOMapper()

    def setOHRBuilder(self) -> None:
        self._builder: IOHRBuilder = OHRBuilder1(self._config)
    
    def setRepository(self) -> None:
        self._repository = MySQLTXTRepository()

    def generateData(self) -> None:
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
    
    def saveData(self) -> None:
        data = self._mapper.mapToDTO(self._builder.getResult())
        self._repository.addRange(data)
        self._repository.saveTo(DUMP_FILE_PATH, "db", "tablename")