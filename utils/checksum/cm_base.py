from abc import abstractmethod

from ..io.io_base import IODataBase

class CMBase:
    @abstractmethod
    def calc_sum(self, data: IODataBase ) -> int:
        pass