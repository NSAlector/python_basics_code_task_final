import numpy as np
from .cm_base import CMBase
from ..io.io_base import IODataBase


class Algorithm1(CMBase):


    def calc_sum(self, data: IODataBase) -> int:

        try:
            # 1. Преобразование в оттенки серого
            grayscale = data.to_grayscale()
            height, width = grayscale.shape

            # Проверяем, что изображение достаточно велико для патчей 4x4
            if height < 4 or width < 4:
                raise ValueError(f"Изображение слишком мало для патчей 4x4: "
                                 f"{height}x{width}")

            # 2. Разбиение на патчи 4x4
            # Вычисляем, сколько полных патчей 4x4 помещается
            patches_h = height // 4
            patches_w = width // 4

            if patches_h == 0 or patches_w == 0:
                raise ValueError("Изображение слишком мало для извлечения патчей 4x4")

            # Создаем массив для хранения средних значений патчей
            patch_means = []

            for i in range(patches_h):
                for j in range(patches_w):
                    # Извлекаем патч 4x4
                    patch = grayscale[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4]

                    # 3.1. Рассчитываем среднее значение интенсивностей
                    mean_value = np.mean(patch)

                    # 3.2. Бинаризация
                    binary_value = 1 if mean_value > 127 else 0
                    patch_means.append(binary_value)

            # Если у нас меньше 16 патчей, дополняем нулями
            while len(patch_means) < 16:
                patch_means.append(0)

            # Берем первые 16 патчей (если их больше)
            patch_means = patch_means[:16]

            # 4. Формирование 16-битного числа
            key = 0
            for bit in patch_means:
                key = (key << 1) | bit

            return key

        except Exception as e:
            raise ValueError(f"Ошибка при вычислении контрольной суммы (Алгоритм 1): {str(e)}")