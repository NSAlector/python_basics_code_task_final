import json
import os
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase


class HashBase:

    def __init__(self, key_coder: CMBase):

        if not isinstance(key_coder, CMBase):
            raise TypeError("key_coder должен быть экземпляром CMBase")

        self.key_coder = key_coder
        self.hash_table = {}
        self.collisions = 0  # Счетчик коллизий

    def __getitem__(self, key: int):

        if key not in self.hash_table:
            raise KeyError(f"Ключ {key} не найден в хеш-таблице")
        return self.hash_table[key]

    def __setitem__(self, key: int, data: IODataBase):

        if not isinstance(data, IODataBase):
            raise TypeError("data должен быть экземпляром IODataBase")

        if data.filepath is None:
            raise ValueError("Данные должны содержать путь к файлу")

        # Проверяем на коллизии (уже существующий ключ)
        if key in self.hash_table:
            # Проверяем, тот же ли это файл
            if self.hash_table[key] != data.filepath:
                self.collisions += 1
                # Перезаписываем (или можно выбрать другую стратегию)
                # В данном случае перезаписываем новым файлом

        self.hash_table[key] = data.filepath

    def __delitem__(self, key: int):

        if key not in self.hash_table:
            raise KeyError(f"Ключ {key} не найден в хеш-таблице")
        del self.hash_table[key]

    def add_data(self, data: IODataBase):

        key = self.key_coder.calc_sum(data)
        self[key] = data
        return key

    def json_save(self, path=None):
        if path is None:
            # Создаем директорию output, если её нет
            output_dir = "./output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            path = os.path.join(output_dir, "hash_table.json")

        try:
            # Преобразуем ключи в строки для JSON
            json_data = {str(k): v for k, v in self.hash_table.items()}

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            print(f"Хеш-таблица сохранена в {path}")
            print(f"Всего элементов: {len(self.hash_table)}")
            print(f"Коллизий: {self.collisions}")

            return path

        except Exception as e:
            raise IOError(f"Ошибка при сохранении JSON: {str(e)}")

    def __len__(self):
        """Возвращает количество элементов в хеш-таблице"""
        return len(self.hash_table)

    def __contains__(self, key):
        """Проверка наличия ключа в хеш-таблице"""
        return key in self.hash_table

    def keys(self):
        """Возвращает все ключи хеш-таблицы"""
        return list(self.hash_table.keys())

    def values(self):
        """Возвращает все значения хеш-таблицы"""
        return list(self.hash_table.values())

    def items(self):
        """Возвращает пары ключ-значение хеш-таблицы"""
        return list(self.hash_table.items())

    def clear(self):
        """Очистка хеш-таблицы"""
        self.hash_table.clear()
        self.collisions = 0
