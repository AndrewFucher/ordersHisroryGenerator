from typing import List
from math import fmod

from mylogger import MyLogger
from constants import LCG_A, LCG_C, LCG_M, SEED_INCREMENTER


class PseudorandomLCG:
    def __init__(self) -> None:
        self._logger = MyLogger.getLogger(__name__)

    def getPRIntegerList(self, seed: int = 0, count: int = 0) -> List[int]:
        result_list: List[int] = []
        for iteration in range(count):
            seed = int(fmod(seed * LCG_A + LCG_C, LCG_M))
            result_list.append(seed)
        self._logger.info("Generated list of pseudorandom ingers")
        return result_list

    def getPRFloatList(self, seed: int = 0, count: int = 0) -> List[int]:
        result_list: List[float] = list(
            map(
                lambda x: x / LCG_M,
                self.getPRIntegerList(seed=seed, count=count),
            )
        )
        self._logger.info("Generated list of pseudorandom floats")
        return result_list

    def getPRFloatListOfLists(self, seed: int = 0, count_lists: int = 0, count_elements: int = 0) -> List[List[int]]:
        result_list: List[List[float]] = [[] for list_number in range(count_lists)]
        for el_index in range(count_elements):
            index = 0
            for r_n in self.getPRFloatList(seed, count_lists):
                result_list[index].append(r_n)
                index += 1
            seed += SEED_INCREMENTER
        
        return result_list