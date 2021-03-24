from typing import Any, List


class OHRDTO:
    instrument: str = ""
    px_init: float = 0.0
    px_fill: float = 0.0
    volume_init: int = 0
    volume_fill: int = 0
    id: str = ""
    tags: str = ""
    note: str = ""
    side: str = ""
    datetime: str = ""
    status: str = ""


class OHRDomainModel:
    instrument: List[str] = []
    px_init: List[float] = []
    px_fill: List[float] = []
    volume_init: List[int] = []
    volume_fill: List[int] = []
    id: List[str] = []
    tags: List[str] = []
    note: List[str] = []
    side: List[str] = []
    datetime: List[str] = []
    status: List[str] = []


class OHRDomainModelToDTOMapper:
    @staticmethod
    def mapToDTO(data: OHRDomainModel) -> List[OHRDTO]:
        ohr_dto_list: List[OHRDTO] = []
        for index in range(len(data.id)):

            order_history_record_dto: OHRDTO = OHRDTO()

            order_history_record_dto.id = data.id[index]
            order_history_record_dto.datetime = data.datetime[index]
            order_history_record_dto.instrument = data.instrument[index]
            order_history_record_dto.note = data.note[index]
            order_history_record_dto.px_fill = data.px_fill[index]
            order_history_record_dto.px_init = data.px_init[index]
            order_history_record_dto.side = data.side[index]
            order_history_record_dto.status = data.status[index]
            order_history_record_dto.tags = data.tags[index]
            order_history_record_dto.volume_fill = data.volume_fill[index]
            order_history_record_dto.volume_init = data.volume_init[index]

            ohr_dto_list.append(order_history_record_dto)

        return ohr_dto_list
