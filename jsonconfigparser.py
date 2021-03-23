import json
from mylogger import MyLogger


class JSONConfigParser:
    def __init__(self) -> None:
        self._logger = MyLogger.getLogger(__name__)
        self._setDefaultConfig()

    def _setDefaultConfig(self) -> None:
        self._logger.info("Initializing default config")
        self._default_config = {
            "Logging": {
                "loggingLevel": 10,
                "logsFolder": "./logs/",
                "loggingDatetimeFormat": "%Y-%m-%d %I:%M:%S",
                "loggingFormat": "[%(asctime)s.%(msecs)03d]:%(levelname)s: %(message)s",
            },
            "Seeds": {
                "ID": 1,
                "Px_Init": 2,
                "Px_Fill": 3,
                "Volume_Init": 4,
                "Volume_Fill": 5,
                "Status": 6,
                "Datetime": 7,
                "Instrument": 8,
                "Side": 9,
                "Tags": 10,
                "Notes": 11,
            },
            "Data": {
                "Instrument_Price": [],
                "Tags": [],
                "Side": [],
                "Notes": [],
                "Status": [
                    ["New"],
                    ["InProcess"],
                    ["Fill", "PartialFill", "Cancel"],
                    ["Done"],
                ],
            },
            "Parameters": {
                "baseDatetime": "17.02.2021 15:35:15.673",
                "baseDatetimeFormat": "%d.%m.%Y %H:%M:%S.%f",
                "datetimeFormat": "%d.%m.%Y %H:%M:%S.%f",
                "timeFrameMilliseconds": 86400000,
                "digitsInPrice": 6,
                "maxVolume": 1000000,
                "minVolume": 1000,
                "variationUnits": 100,
                "tableName": "orders_history",
                "databaseName": "orders",
            },
            "OrdersRecordsParameters": {
                "total": 0,
                "orders": [],
            },
            "Dependencies": {
                "ParametersToStatus": {
                    "New": 0,
                    "InProcess": 0,
                    "Fill": 1,
                    "PartialFill": 2,
                    "Cancel": 0,
                    "Done": 3,
                },
            },
        }

    def loadFrom(self, file_path: str) -> dict:
        self._logger.info("Starting loading config")
        config = self._parseJSON(file_path=file_path)
        config = self._overrideDefaultConfig(self.getDefaultConfig(), config)
        self._logger.info("Finished loading config")
        return config

    def getDefaultConfig(self) -> dict:
        return self._default_config

    def _overrideDefaultConfig(self, default_config: dict, new_config: dict) -> dict:
        self._logger.info("Starting overriding default config")
        for key in new_config:
            if key in default_config:  # if key is in both default_config and new_config
                if isinstance(default_config[key], dict) and isinstance(
                    new_config[key], dict
                ):  # if the key is dict Object
                    self._overrideDefaultConfig(default_config[key], new_config[key])
                else:
                    default_config[key] = new_config[key]
            else:  # if the key is not in dict default_config , add it to dict default_config
                default_config.update({key: new_config[key]})
        self._logger.info("Finished overriding default config")
        return default_config

    def _parseJSON(self, file_path: str) -> dict:
        self._logger.info("Starting parsing config file (json)")
        try:
            with open(file_path) as jsonFile:
                json_file_data = json.load(jsonFile)
        except Exception as exception:
            self._logger.error(exception)
            return dict()

        return json_file_data
