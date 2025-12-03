import numpy as np
from ..io.io_base import IODataBase


class CMBase:

    def calc_sum(self, data: IODataBase) -> int:
        raise NotImplementedError("Метод должен быть реализован в подклассе")