import json
import os

from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase


class HashBase:
    def __init__(self, key_coder: CMBase):
        if not isinstance(key_coder, CMBase):
            raise TypeError("key_coder должен быть наследником CMBase")
        self.key_coder = key_coder
        self._hash_table = {}

    def __getitem__(self, key: int) -> str:
        if not isinstance(key, int):
            raise TypeError("Ключ должен быть целым числом")
        if key not in self._hash_table:
            raise KeyError(f"Элемент с ключом {key} отсутствует")
        return self._hash_table[key]

    def __setitem__(self, key: int, data: IODataBase):
        if not isinstance(key, int):
            raise TypeError("Ключ должен быть целым числом")
        if not isinstance(data, IODataBase):
            raise TypeError("data должен быть наследником IODataBase")
        if not hasattr(data, 'data') or data.data is None:
            raise ValueError("data не содержит загруженных данных")

        filepath = getattr(data, 'filepath', None)
        if filepath is None:
            raise ValueError("data должен иметь атрибут filepath")
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Файл {filepath} не найден")

        self._hash_table[key] = filepath

    def __delitem__(self, key: int):
        if not isinstance(key, int):
            raise TypeError("Ключ должен быть целым числом")
        if key not in self._hash_table:
            raise KeyError(f"Элемент с ключом {key} отсутствует")
        del self._hash_table[key]

    def __contains__(self, key: int) -> bool:
        return key in self._hash_table

    def __len__(self) -> int:
        return len(self._hash_table)

    def __iter__(self):
        return iter(self._hash_table.items())

    def json_save(self, path: str = "./output/hash_table.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._hash_table, f, indent=4)
        except Exception as e:
            raise IOError(f"Ошибка при сохранении JSON: {e}")
