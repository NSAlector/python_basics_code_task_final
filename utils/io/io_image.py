import os
import cv2
import numpy as np
from .io_base import IODataBase


class IOImageData(IODataBase):
    """Класс для работы с изображениями (PNG, JPG)"""

    def read(self, filepath):

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")

        # Проверка расширения файла
        valid_extensions = ['.png', '.jpg', '.jpeg']
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in valid_extensions:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}. "
                             f"Поддерживаются: {valid_extensions}")

        # Чтение изображения с помощью OpenCV
        # OpenCV читает в формате BGR, преобразуем в RGB??
        image_bgr = cv2.imread(filepath)
        if image_bgr is None:
            raise ValueError(f"Не удалось прочитать изображение: {filepath}")

        # Конвертация BGR -> RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        self.data = image_rgb
        self.shape = image_rgb.shape
        self.filepath = filepath

        return self

    def save(self, path):
        """Сохранение изображения в файл (хотя не ясно зачем)"""
        if self.data is None:
            raise ValueError("Нет данных для сохранения")

        # Конвертация RGB -> BGR для OpenCV
        image_bgr = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, image_bgr)
        return True