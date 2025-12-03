from abc import ABC, abstractmethod
from ..io.io_base import IODataBase
import numpy as np

class CMBase(ABC):
    """
    Базовый класс для вычисления контрольной суммы.
    """

    @abstractmethod
    def calc_sum(self, data: IODataBase) -> int:
        """Вычислить контрольную сумму/ключ (int)"""
        raise NotImplementedError


class CMAlg1(CMBase):
    """
    Алгоритм 1:
    - конвертация в оттенки серого усреднением RGB
    - разбивка на 4x4 = 16 патчей (каждый размером M/4 x N/4)
    - для каждого патча вычислить среднюю интенсивность
    - бинаризация по порогу 127 -> 1/0
    - собрать ровно 16 бит в целое число
    """

    def calc_sum(self, data: IODataBase) -> int:
        if not hasattr(data, 'data') or data.data is None:
            raise ValueError('Provided data object has no .data')
        
        arr = data.data
        if not isinstance(arr, np.ndarray):
            arr = np.asarray(arr)
        
        # convert to grayscale
        if arr.ndim == 3 and arr.shape[2] == 3:
            gray = arr.mean(axis=2)
        elif arr.ndim == 2:
            gray = arr.astype(np.float64)
        else:
            raise ValueError('Unsupported data shape for CMAlg1')
        
        h, w = gray.shape
        
        # Валидация: изображение должно быть достаточно большим для разбивки
        if h < 4 or w < 4:
            raise ValueError(f'Image too small for CMAlg1: {h}x{w}. Minimum size is 4x4 pixels.')
        
        # Разбивка на 4x4 = 16 патчей
        # Каждый патч размером (h/4) x (w/4)
        patch_h = h / 4.0
        patch_w = w / 4.0
        
        patch_means = []
        
        # Проходим по 4 рядам и 4 колонкам патчей
        for i in range(4):
            for j in range(4):
                # Вычисляем границы патча (используем float для точности)
                start_row = int(i * patch_h)
                end_row = int((i + 1) * patch_h)
                start_col = int(j * patch_w)
                end_col = int((j + 1) * patch_w)
                
                # Извлекаем патч
                patch = gray[start_row:end_row, start_col:end_col]
                
                # Вычисляем среднее значение интенсивности для патча
                if patch.size > 0:
                    patch_means.append(float(patch.mean()))
                else:
                    # На случай ошибок округления
                    patch_means.append(0.0)
        
        # Должно быть ровно 16 патчей
        if len(patch_means) != 16:
            raise RuntimeError(f'Expected 16 patches, got {len(patch_means)}')
        
        # Бинаризация: > 127 -> 1, иначе -> 0
        bits = [1 if m > 127.0 else 0 for m in patch_means]
        
        # Формируем 16-битное число
        value = 0
        for b in bits:
            value = (value << 1) | int(b)
        
        return int(value)


class CMAlg2(CMBase):
    """
    Алгоритм 2:
    - средняя интенсивность всех пикселей (по всем каналам)
    - возвращаем округлённое целое
    """

    def calc_sum(self, data: IODataBase) -> int:
        if not hasattr(data, 'data') or data.data is None:
            raise ValueError('Provided data object has no .data')
        
        arr = data.data
        if not isinstance(arr, np.ndarray):
            arr = np.asarray(arr)
        
        # Проверка что данные не пусты
        if arr.size == 0:
            raise ValueError('Data array is empty')
        
        # mean across all values and channels
        mean = float(arr.mean())
        return int(round(mean))
