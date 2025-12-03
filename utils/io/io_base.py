##import os
import numpy as np
from abc import ABC, abstractmethod


class IODataBase(ABC):
    """Базовый класс для работы с данными изображений"""

    def __init__(self):
        self.data = None  # Хранит данные изображения в виде numpy массива
        self.shape = None  # (высота, ширина, каналы)??
        self.filepath = None

    @abstractmethod
    def read(self, filepath):
        """Чтение данных из файла"""
        pass

    @abstractmethod
    def save(self, path):
        """Сохранение данных в файл"""
        pass

    def __len__(self):
        """Возвращает общее количество пикселей"""
        if self.data is not None:
            return self.data.size
        return 0

    def __getitem__(self, idx):
        if self.data is None:
            raise ValueError("Данные не загружены")

        if idx < 0 or idx >= len(self):
            raise IndexError(f"Индекс {idx} вне диапазона [0, {len(self) - 1}]")

        # Для 3D массива (с каналами)
        if len(self.data.shape) == 3:
            height, width, channels = self.data.shape
            y = idx // width
            x = idx % width
            return self.data[y, x]
        # Для 2D массива (оттенки серого)
        else:
            height, width = self.data.shape
            y = idx // width
            x = idx % width
            return self.data[y, x]

    def get_pixel(self, x, y):
        """Доступ к пикселю по координатам (x, y)"""
        if self.data is None:
            raise ValueError("Данные не загружены")

        if x < 0 or x >= self.shape[1] or y < 0 or y >= self.shape[0]:
            raise IndexError(f"Координаты ({x}, {y}) вне диапазона")

        return self.data[y, x]

    def to_grayscale(self):
        """Преобразование в оттенки серого (усреднение каналов)"""
        if self.data is None:
            raise ValueError("Данные не загружены")

        if len(self.data.shape) == 3:
            grayscale = np.mean(self.data, axis=2).astype(np.uint8)
            return grayscale
        return self.data.copy()
