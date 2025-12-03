import numpy as np
from .cm_base import CMBase
from ..io.io_base import IODataBase


class Algorithm2(CMBase):


    def calc_sum(self, data: IODataBase) -> int:

        try:
            # Преобразование в оттенки серого
            grayscale = data.to_grayscale()

            # Вычисление среднего значения интенсивности
            mean_intensity = np.mean(grayscale)

            # Округление до целого
            return int(round(mean_intensity))

        except Exception as e:
            raise ValueError(f"Ошибка при вычислении контрольной суммы (Алгоритм 2): {str(e)}")