from typing import List

from dataobjects import OHRDTO
from constants import MYSQL_STRING_FORMAT

class MySQLTXTRepository:
    def __init__(self, config) -> None:
        self._data: List[OHRDTO] = []
        self._config = config

    def add(self, new_ohr: OHRDTO):
        self._data.append(new_ohr)

    def addRange(self, new_ohr_list: List[OHRDTO]) -> None:
        self._data.extend(new_ohr_list)

    def saveTo(self, file_path: str) -> None:
        db_name = self._config["Parameters"]["databaseName"]
        table_name = self._config["Parameters"]["tableName"]
        with open(file_path, "w") as file:
            for record in self._data:
                file.write(
                    MYSQL_STRING_FORMAT.format(
                        db_name,
                        table_name,
                        record.id,
                        record.instrument,
                        record.side,
                        record.px_init,
                        record.px_fill,
                        record.volume_init,
                        record.volume_fill,
                        record.status,
                        record.tags,
                        record.note,
                        record.datetime
                    )
                )

    def clear(self) -> None:
        self._data = []
