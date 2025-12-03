import numpy as np
import cv2


class IODataBase:
    def __init__(self, filepath=None):
        self._data = None
        self.filepath = filepath
        if filepath:
            try:
                self.read(filepath)
            except Exception as e:
                raise ValueError(f"Ошибка при инициализации файла {filepath}: {e}")

    def read(self, filepath):
        raise NotImplementedError("Метод read должен быть реализован в подклассе")

    def save(self, path):
        raise NotImplementedError("Метод save должен быть реализован в подклассе")

    def __len__(self):
        if self._data is None:
            return 0
        return self._data.size

    def __getitem__(self, idx):
        if self._data is None:
            raise ValueError("Данные не загружены.")

        try:
            if isinstance(idx, (int, slice, tuple)):
                return self._data[idx]
            else:
                raise TypeError(f"Некорректный тип индекса: {type(idx)}")
        except IndexError as e:
            shape_str = str(self._data.shape)
            raise IndexError(f"Индекс выходит за границы данных размера {shape_str}")
        except Exception as e:
            raise TypeError(f"Ошибка при доступе по индексу: {str(e)}")

    @property
    def data(self):
        if self._data is None:
            raise ValueError("Данные не загружены.")
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError(f"Ожидается np.ndarray, получен {type(value)}")
        self._data = value

    @property
    def shape(self):
        if self._data is None:
            raise ValueError("Данные не загружены.")
        return self._data.shape

    def to_grayscale(self):
        if self._data is None:
            raise ValueError("Данные не загружены.")

        if len(self._data.shape) == 3 and self._data.shape[2] == 3:
            # RGB изображение
            try:
                return (self._data[:, :, 0] * 0.299 +
                        self._data[:, :, 1] * 0.587 +
                        self._data[:, :, 2] * 0.114).astype(np.uint8)
            except Exception as e:
                raise ValueError(f"Ошибка при конвертации в grayscale: {str(e)}")
        elif len(self._data.shape) == 2:
            # Уже в оттенках серого
            return self._data.astype(np.uint8)
        else:
            shape_str = str(self._data.shape)
            raise ValueError(f"Неподдерживаемая форма данных: {shape_str}. Ожидается (H, W) или (H, W, 3)")


class ImageIOData(IODataBase):
    def read(self, filepath):
        try:
            img = cv2.imread(filepath, cv2.IMREAD_COLOR)

            if img is None:
                raise ValueError(f"Не удалось прочитать изображение: {filepath}")

            # Конвертируем BGR в RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self._data = img_rgb
            self.filepath = filepath

            return img_rgb

        except Exception as e:
            raise Exception(f"Ошибка чтения {filepath}: {str(e)}")

    def save(self, path):
        pass

    def to_grayscale(self):
        if self._data is None:
            raise ValueError("Данные не загружены")

        if len(self._data.shape) == 3 and self._data.shape[2] == 3:
            gray = (self._data[:, :, 0] * 0.299 +
                    self._data[:, :, 1] * 0.587 +
                    self._data[:, :, 2] * 0.114).astype(np.uint8)
            return gray
        elif len(self._data.shape) == 2:
            return self._data.astype(np.uint8)
        else:
            raise ValueError(f"Неподдерживаемая форма: {self._data.shape}")


class TextIOData(IODataBase):
    def read(self, filepath):
        try:
            if not filepath.endswith('.txt'):
                raise ValueError(f"Файл должен иметь расширение .txt")

            with open(filepath, 'r') as f:
                content = f.read()

            if not content.strip():
                raise ValueError(f"Файл пуст")

            values = list(map(float, content.split()))

            if len(values) < 3:
                raise ValueError(f"Нужно минимум 3 значения")

            M, N, K = int(values[0]), int(values[1]), int(values[2])

            if M <= 0 or N <= 0 or K <= 0:
                raise ValueError(f"Некорректные размеры")

            if K not in (1, 3):
                raise ValueError(f"K должен быть 1 или 3")

            pixel_data = values[3:]
            expected_count = M * N * K

            if len(pixel_data) != expected_count:
                raise ValueError(f"Ожидается {expected_count} значений")

            # Проверяем значения
            for i, val in enumerate(pixel_data):
                if not (0 <= val <= 255):
                    raise ValueError(f"Пиксель {i}: {val} вне диапазона")

            self._data = np.array(pixel_data).reshape(M, N, K).astype(np.uint8)
            self.filepath = filepath

            return self._data

        except Exception as e:
            raise Exception(f"Ошибка чтения {filepath}: {str(e)}")

    def save(self, path):
        pass
