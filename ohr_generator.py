from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime, timedelta

from constants import (
    FILL_FROM_LAST,
    FILL_WITH_CHANGED,
    FILL_WITH_DEFAULT,
    FILL_WITH_ZERO,
)
from pseudorandomlcg import PseudorandomLCG
from dataobjects import OHRDomainModel


class IOHRBuilder(ABC):
    @abstractmethod
    def buildID(self) -> None:
        pass

    @abstractmethod
    def buildVolume(self) -> None:
        pass

    @abstractmethod
    def buildPrice(self) -> None:
        pass

    @abstractmethod
    def buildSide(self) -> None:
        pass

    @abstractmethod
    def buildTags(self) -> None:
        pass

    @abstractmethod
    def buildNote(self) -> None:
        pass

    @abstractmethod
    def buildStatus(self) -> None:
        pass

    @abstractmethod
    def buildInstrument(self) -> None:
        pass

    @abstractmethod
    def buildDatetime(self) -> None:
        pass

    @abstractmethod
    def buildSeriesList(self) -> None:
        pass

    @abstractmethod
    def getResult(self) -> OHRDomainModel:
        pass


class OHRBuilder1(IOHRBuilder):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self._config: dict = config
        self._random_generator: PseudorandomLCG = PseudorandomLCG()
        self._data: OHRDomainModel = OHRDomainModel
        self._series_list = []

    def buildID(self) -> None:
        random_values_list = self._random_generator.getPRIntegerList(
            self._config["Seeds"]["ID"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator: IFieldGenerator = IDGenerator(random_values_list, self._series_list)
        self._data.id = generator.generateData()

    def buildInstrument(self) -> None:
        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Instrument"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator: IFieldGenerator = ISNGenerator(
            random_values_list,
            list(dict(self._config["Data"]["InstrumentAndPrice"]).keys()),
            self._series_list,
        )
        self._data.instrument = generator.generateData()

    def buildSide(self) -> None:
        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Side"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator: IFieldGenerator = ISNGenerator(
            random_values_list, self._config["Data"]["Side"], self._series_list
        )
        self._data.side = generator.generateData()

    def buildNote(self) -> None:
        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Notes"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator: IFieldGenerator = ISNGenerator(
            random_values_list, self._config["Data"]["Notes"], self._series_list
        )
        self._data.note = generator.generateData()

    def buildPrice(self) -> None:
        generator_px_init: IFieldGenerator = PxInitGenerator(
            self._data.instrument, self._config["Data"]["InstrumentAndPrice"]
        )
        self._data.px_init = generator_px_init.generateData()

        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Px_Fill"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator_px_fill: IFieldGenerator = PxFillGenerator(
            random_values_list,
            self._data.px_init,
            self._data.status,
            self._config["Dependencies"]["ParametersToStatus"],
            self._config["Parameters"]["variationUnits"],
            self._config["Parameters"]["digitsInPrice"],
        )
        self._data.px_fill = generator_px_fill.generateData()

    def buildVolume(self) -> None:
        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Volume_Init"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator_volume_init: IFieldGenerator = VolumeInitGenerator(
            self._config["Parameters"]["minVolume"],
            self._config["Parameters"]["maxVolume"],
            random_values_list,
            self._series_list,
        )
        self._data.volume_init = generator_volume_init.generateData()

        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Volume_Fill"],
            self._config["OrdersRecordsParameters"]["total"],
        )
        generator_volume_fill: IFieldGenerator = VolumeFillGenerator(
            self._data.volume_init,
            self._config["Parameters"]["minVolume"],
            random_values_list,
            self._data.status,
            self._config["Dependencies"]["ParametersToStatus"],
        )
        self._data.volume_fill = generator_volume_fill.generateData()

    def buildTags(self) -> None:
        random_values_lists = self._random_generator.getPRFloatListOfLists(
            self._config["Seeds"]["Tags"],
            self._config["OrdersRecordsParameters"]["total"],
            len(self._config["Data"]["Tags"]),
        )
        generator: IFieldGenerator = TagsGenerator(
            random_values_lists, self._config["Data"]["Tags"], self._series_list
        )
        self._data.tags = generator.generateData()

    def buildDatetime(self) -> None:
        random_values_lists = self._random_generator.getPRFloatListOfLists(
            self._config["Seeds"]["Datetime"],
            self._config["OrdersRecordsParameters"]["total"],
            len(self._config["Data"]["Status"]),
        )
        generator: IFieldGenerator = DatetimeGenerator(
            random_values_lists,
            datetime.strptime(
                self._config["Parameters"]["baseDatetime"],
                self._config["Parameters"]["baseDatetimeFormat"],
            ),
            self._config["Parameters"]["timeFrameMilliseconds"],
            self._config["Parameters"]["datetimeFormat"],
            self._config["OrdersRecordsParameters"]["orders"],
        )
        self._data.datetime = generator.generateData()

    def buildStatus(self) -> None:
        count: int = 0
        for order in self._config["OrdersRecordsParameters"]["orders"]:
            count += order["count"] * len(order["Statuses"])

        random_values_list = self._random_generator.getPRFloatList(
            self._config["Seeds"]["Status"], count
        )
        generator: IFieldGenerator = StatusGenerator(
            random_values_list,
            self._config["Data"]["Status"],
            self._config["OrdersRecordsParameters"]["orders"],
        )
        self._data.status = generator.generateData()

    def buildSeriesList(self) -> None:
        index = 0
        for ohr_params_ in self._config["OrdersRecordsParameters"]["orders"]:
            for order_number in range(ohr_params_["count"]):
                for status_type in ohr_params_["Statuses"]:
                    self._series_list.append(index)
                index += 1

    def getResult(self) -> OHRDomainModel:
        return self._data


class IFieldGenerator(ABC):
    @abstractmethod
    def generateData(self) -> List[Any]:
        pass


class IDGenerator(IFieldGenerator):
    def __init__(self, random_values_list: List[int], series_list: List[int]) -> None:
        super().__init__()
        self._random_values_list = random_values_list
        self._series_list = series_list

    def generateData(self) -> List[Any]:
        id_list: List[str] = list(
            map(lambda id: "{0:0{1}X}".format(id, 10), self._random_values_list)
        )
        result_list: List[str] = [id_list[index] for index in self._series_list]
        return result_list


class PxInitGenerator(IFieldGenerator):
    def __init__(
        self, instrument_list: List[str], instrument_price_values: dict
    ) -> None:
        super().__init__()
        self._instrument_list = instrument_list
        self._instrument_price_values = instrument_price_values

    def generateData(self) -> List[Any]:
        result_list: List[float] = [
            self._instrument_price_values[instrument]
            for instrument in self._instrument_list
        ]
        return result_list


class PxFillGenerator(IFieldGenerator):
    def __init__(
        self,
        random_values_list: List[int],
        px_init_list: List[float],
        status_list: List[str],
        f_to_s_dep: Dict[str, int],
        units_variation: int,
        digits_in_price: int,
    ) -> None:
        super().__init__()
        self._random_values_list = random_values_list
        self._px_init_list = px_init_list
        self._status_list = status_list
        self._f_to_s_dep = f_to_s_dep
        self._units_variation = units_variation
        self._digits_in_price = digits_in_price

    def generateData(self) -> List[Any]:
        last = 0
        price_with_variation = 0
        q = iter(self._status_list)
        w = iter(self._random_values_list)
        result_list: List[float] = []
        for index in range(len(self._px_init_list)):
            status = next(q)
            if self._f_to_s_dep[status] == FILL_WITH_ZERO:
                result_list.append(0)
                last = 0
                continue
            if self._f_to_s_dep[status] in [FILL_WITH_DEFAULT, FILL_WITH_CHANGED]:
                t = 10 ** (self._digits_in_price - len(str(int(self._px_init_list[index]))))
                price_with_variation = (
                    int(next(w) * 2 * (self._units_variation + 1))
                    - (self._units_variation + 1)
                ) / t + self._px_init_list[index]
                price_with_variation = int(price_with_variation * t) / t
                result_list.append(price_with_variation)
                last = price_with_variation
                continue
            if self._f_to_s_dep[status] == FILL_FROM_LAST:
                result_list.append(last)

        return result_list


class VolumeInitGenerator(IFieldGenerator):
    def __init__(
        self,
        min_val: int,
        max_val: int,
        random_values_list: List[float],
        series_list: List[int],
    ) -> None:
        super().__init__()
        self._min_val = min_val
        self._max_val = max_val
        self._random_values_list = random_values_list
        self._series_list = series_list

    def generateData(self) -> List[Any]:
        volume_init_list: List[int] = list(
            map(
                lambda r: int((self._max_val - self._min_val) * r + self._min_val)
                // 1000
                * 1000,
                self._random_values_list,
            )
        )
        result_list: List[int] = [
            volume_init_list[index] for index in self._series_list
        ]
        return result_list


class VolumeFillGenerator(IFieldGenerator):
    def __init__(
        self,
        volume_init_list: List[int],
        min_val: int,
        random_values_list: List[float],
        status_list: List[str],
        f_to_s_dep: Dict[str, int],
    ) -> None:
        super().__init__()
        self._random_values_list = random_values_list
        self._volume_init_list = volume_init_list
        self._status_list = status_list
        self._f_to_s_dep = f_to_s_dep
        self._min_val = min_val

    def generateData(self) -> List[Any]:
        last = 0
        volume = 0
        q = iter(self._status_list)
        w = iter(self._random_values_list)
        result_list: List[int] = []
        for index in range(len(self._volume_init_list)):
            status = next(q)
            if self._f_to_s_dep[status] == FILL_WITH_ZERO:
                result_list.append(0)
                last = 0
                continue
            if self._f_to_s_dep[status] == FILL_WITH_DEFAULT:
                volume = self._volume_init_list[index]
                result_list.append(volume)
                last = volume
                continue
            if self._f_to_s_dep[status] == FILL_WITH_CHANGED:
                volume = (
                    int(
                        (self._volume_init_list[index] - self._min_val) * next(w)
                        + self._min_val
                    )
                    // 1000
                    * 1000
                )
                result_list.append(volume)
                last = volume
                continue
            if self._f_to_s_dep[status] == FILL_FROM_LAST:
                result_list.append(last)

        return result_list


class StatusGenerator(IFieldGenerator):
    def __init__(
        self,
        random_values_list: List[float],
        statuses: List[List[str]],
        ohr_params: List[Dict[str, Any]],
    ) -> None:
        super().__init__()
        self._random_values_list = random_values_list
        self._statuses = statuses
        self._ohr_params = ohr_params

    def generateData(self) -> List[Any]:
        result_list: List[str] = []
        q = iter(self._random_values_list)
        for ohr_params_ in self._ohr_params:
            for order_number in range(ohr_params_["count"]):
                for status_type in ohr_params_["Statuses"]:
                    a = self._statuses[status_type]
                    result_list.append(a[int(len(a) * next(q))])

        return result_list


class DatetimeGenerator(IFieldGenerator):
    def __init__(
        self,
        random_values_lists: List[List[float]],
        base_datetime: datetime,
        time_frame_m: int,
        datetime_fmt: str,
        ohr_params: List[Dict[str, Any]],
    ) -> None:
        super().__init__()
        self._random_values_lists = random_values_lists
        self._base_datetime = base_datetime
        self._time_frame_m = time_frame_m
        self._datetime_fmt = datetime_fmt
        self._ohr_params = ohr_params

    def generateData(self) -> List[Any]:
        result_list: List[str] = []
        q = iter(self._random_values_lists)
        for ohr_params_ in self._ohr_params:
            for order_number in range(ohr_params_["count"]):
                a = iter(next(q))
                t_d: int = 0
                for status_type in ohr_params_["Statuses"]:
                    t_d = int((self._time_frame_m - t_d) * next(a) + t_d)
                    d: datetime = self._base_datetime
                    d += timedelta(milliseconds=t_d)
                    result_list.append(d.strftime(self._datetime_fmt)[:-3])

        return result_list


# Instrument Side Notes Generator
class ISNGenerator(IFieldGenerator):
    def __init__(
        self,
        random_values_list: List[float],
        data_list: List[str],
        series_list: List[int],
    ) -> None:
        super().__init__()
        self._random_values_list = random_values_list
        self._data_list = data_list
        self._series_list = series_list

    def generateData(self) -> List[Any]:
        result_data_list: List[str] = [
            self._data_list[int(len(self._data_list) * r)]
            for r in self._random_values_list
        ]
        result_list: List[str] = [
            result_data_list[index] for index in self._series_list
        ]
        return result_list


class TagsGenerator(IFieldGenerator):
    def __init__(
        self,
        random_values_lists: List[List[float]],
        tags_list: List[str],
        series_list: List[int],
    ) -> None:
        super().__init__()
        self._random_values_lists = random_values_lists
        self._tags_list = tags_list
        self._series_list = series_list

    def generateData(self) -> List[Any]:
        tags_list: List[str] = []
        tags: List[str] = []
        for r_v in self._random_values_lists:
            tags = []
            for tag_number in range(len(r_v)):
                if r_v[tag_number] > 0.5:
                    tags.append(self._tags_list[tag_number])
            tags_list.append(",".join(tags))

        result_list: List[str] = [tags_list[index] for index in self._series_list]
        return result_list
