import os
import numpy as np
from .io_base import IODataBase


class IOTextData(IODataBase):

    def read(self, filepath):

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")

        # Проверка расширения файла
        if not filepath.lower().endswith('.txt'):
            raise ValueError("Файл должен иметь расширение .txt")

        try:
            with open(filepath, 'r') as f:
                # Читаем все числа из файла
                numbers = []
                for line in f:
                    numbers.extend(map(float, line.strip().split()))

                if len(numbers) < 3:
                    raise ValueError("Файл должен содержать как минимум 3 числа (M, N, K)")

                # Первые три числа: высота, ширина, количество каналов
                M = int(numbers[0])  # высота
                N = int(numbers[1])  # ширина
                K = int(numbers[2])  # каналы

                # Проверка количества данных
                expected_values = M * N * K
                if len(numbers) - 3 != expected_values:
                    raise ValueError(f"Ожидалось {expected_values} значений, "
                                     f"получено {len(numbers) - 3}")

                # Извлекаем данные пикселей
                pixel_data = numbers[3:]

                # Формируем массив numpy
                if K == 1:
                    # Оттенки серого
                    self.data = np.array(pixel_data, dtype=np.uint8).reshape(M, N)
                elif K == 3:
                    # RGB изображение
                    self.data = np.array(pixel_data, dtype=np.uint8).reshape(M, N, K)
                else:
                    raise ValueError(f"Неподдерживаемое количество каналов: K={K}")

                self.shape = self.data.shape
                self.filepath = filepath

                return self

        except ValueError as e:
            raise ValueError(f"Ошибка при чтении файла {filepath}: {str(e)}")
        except Exception as e:
            raise IOError(f"Ошибка ввода-вывода при чтении {filepath}: {str(e)}")

    def save(self, path):
        """Сохранение данных в текстовый файл"""
        if self.data is None:
            raise ValueError("Нет данных для сохранения")

        try:
            with open(path, 'w') as f:
                # Записываем размеры
                height, width = self.shape[0], self.shape[1]
                channels = 1 if len(self.shape) == 2 else self.shape[2]

                f.write(f"{height} {width} {channels}\n")

                # Записываем данные пикселей
                flat_data = self.data.flatten()
                # Записываем построчно для читаемости
                for i in range(0, len(flat_data), 10):
                    chunk = flat_data[i:i + 10]
                    f.write(" ".join(map(str, chunk)) + "\n")

            return True

        except Exception as e:
            raise IOError(f"Ошибка при сохранении в файл {path}: {str(e)}")