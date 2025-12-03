import json
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase


class HashBase:

    def __init__(self, key_coder):
        if not isinstance(key_coder, CMBase):
            raise TypeError(f"key_coder должен быть экземпляром CMBase, получен {type(key_coder)}")

        self.key_coder = key_coder
        self._table = {}

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError(f"Ключ должен быть целым числом")

        if key not in self._table:
            raise KeyError(f"Ключ {key} отсутствует в хеш-таблице")

        return list(self._table[key])

    def __setitem__(self, key, data):
        if not isinstance(key, int):
            raise TypeError(f"Ключ должен быть целым числом")

        if not isinstance(data, IODataBase):
            raise TypeError(f"data должен быть экземпляром IODataBase, получен {type(data)}")

        if not hasattr(data, 'filepath') or data.filepath is None:
            raise ValueError("Данные должны иметь filepath для добавления в хеш-таблицу")

        try:
            with open(data.filepath, 'rb') as f:
                pass
        except:
            raise FileNotFoundError(f"Файл {data.filepath} не существует или недоступен")

        if key not in self._table:
            self._table[key] = []

        if data.filepath not in self._table[key]:
            self._table[key].append(data.filepath)

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError(f"Ключ должен быть целым числом")

        if key not in self._table:
            raise KeyError(f"Невозможно удалить: ключ {key} отсутствует в хеш-таблице")

        del self._table[key]

    def __contains__(self, key):
        if not isinstance(key, int):
            raise TypeError(f"Ключ должен быть целым числом, получен {type(key)}")

        return key in self._table

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        return iter(self._table.keys())

    def add(self, data):
        if not isinstance(data, IODataBase):
            raise TypeError(f"data должен быть экземпляром IODataBase, получен {type(data)}")

        if not hasattr(data, 'filepath') or data.filepath is None:
            raise ValueError("Данные должны иметь filepath для добавления в хеш-таблицу")

        try:
            with open(data.filepath, 'rb') as f:
                pass
        except:
            raise FileNotFoundError(f"Файл {data.filepath} не существует или недоступен")

        try:
            key = self.key_coder.calc_sum(data)
        except Exception as e:
            raise RuntimeError(f"Не удалось вычислить контрольную сумму для файла {data.filepath}: {str(e)}")

        self[key] = data
        return key

    def remove(self, key, filepath=None):
        if not isinstance(key, int):
            raise TypeError(f"Ключ должен быть целым числом")

        if key not in self._table:
            return False

        if filepath is None:
            del self[key]
            return True

        if filepath in self._table[key]:
            self._table[key].remove(filepath)
            # Если список пуст, удаляем ключ
            if not self._table[key]:
                del self[key]
            return True

        return False

    def get_files(self, key):
        try:
            return self[key]
        except KeyError:
            raise KeyError(f"Ключ {key} отсутствует в хеш-таблице")

    def get_all_keys(self):
        return list(self._table.keys())

    def get_all_files(self):
        all_files = []
        for files in self._table.values():
            all_files.extend(files)
        return all_files

    def find_duplicates(self):
        duplicates = {}
        for key, files in self._table.items():
            if len(files) > 1:
                duplicates[key] = list(files)
        return duplicates

    def clear(self):
        self._table.clear()

    def json_save(self, path):
        if not path or not isinstance(path, str):
            raise ValueError("Путь для сохранения не может быть пустым")

        if not path.endswith('.json'):
            raise ValueError(f"Файл должен иметь расширение .json, получен: {path}")

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json_data = {str(k): v for k, v in self._table.items()}
                json.dump(json_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise Exception(f"Ошибка при сохранении файла {path}: {str(e)}")

    def json_load(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except:
            raise Exception(f"Файл {path} не найден или недоступен")

        if not isinstance(json_data, dict):
            raise ValueError(f"JSON должен быть объектом, получен {type(json_data)}")

        new_table = {}
        for k, v in json_data.items():
            try:
                key_int = int(k)
            except:
                raise ValueError(f"Ключ {k} не может быть преобразован в int")

            if not isinstance(v, list):
                raise ValueError(f"Значение для ключа {k} должно быть списком, получен {type(v)}")

            for item in v:
                if not isinstance(item, str):
                    raise ValueError(f"Элементы списка должны быть строками, получен {type(item)}")

            new_table[key_int] = v

        self._table = new_table
