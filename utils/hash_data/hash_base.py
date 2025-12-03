import os
import json
from typing import Union, Optional
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase

class HashBase:
    """
    Простейшая реализация хеш-таблицы:
    key (int) -> value (str: path to file)
    Магические методы для доступа по ключу.
    """

    def __init__(self, key_coder: CMBase):
        if not isinstance(key_coder, CMBase):
            raise TypeError('key_coder must be an instance of CMBase')
        self.key_coder = key_coder
        self._table = {}  # int -> str (path)

    def json_save(self, path: str):
        """Сохранить хеш-таблицу в JSON файл"""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        # Ensure values are serializable (strings)
        serializable = {str(k): v for k, v in self._table.items()}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
        return path

    def __getitem__(self, key: int) -> str:
        """Получить путь к файлу по ключу"""
        if not isinstance(key, int):
            raise TypeError('Key must be int')
        if key not in self._table:
            raise KeyError(f'Key {key} not found in hash table')
        return self._table[key]

    def __setitem__(self, key: Optional[int], data: Union[IODataBase, str]):
        """
        Добавить элемент в хеш-таблицу.
        
        Args:
            key: Ключ (int) или None/0 для автоматической генерации через key_coder
            data: IODataBase объект или путь к файлу (str)
        
        Если key is None или key == 0, то ключ вычисляется автоматически
        через self.key_coder.calc_sum()
        """
        # Обработка данных: получаем путь и IODataBase объект
        io_obj = None
        filepath = None
        
        if isinstance(data, str):
            # data - это путь к файлу
            filepath = data
            if not os.path.exists(filepath):
                raise FileNotFoundError(f'File not found: {filepath}')
            
            # Если нужна автогенерация ключа, загружаем файл
            if key is None or key == 0:
                # Импортируем функцию выбора класса
                from ..test import choose_io_class
                io_obj = choose_io_class(filepath)
                io_obj.read(filepath)
        else:
            # data - это IODataBase объект
            if not isinstance(data, IODataBase):
                raise TypeError('data must be IODataBase or filepath string')
            
            io_obj = data
            filepath = getattr(data, 'filepath', None)
            if filepath is None:
                raise ValueError('IODataBase object must have .filepath attribute')
            if not os.path.exists(filepath):
                raise FileNotFoundError(f'File not found: {filepath}')
        
        # Вычисление или проверка ключа
        if key is None or key == 0:
            # Автогенерация ключа
            if io_obj is None:
                raise ValueError('Cannot auto-generate key: data object not available')
            calculated_key = self.key_coder.calc_sum(io_obj)
            key = calculated_key
        else:
            # Проверка типа ключа
            if not isinstance(key, int):
                raise TypeError('Key must be int, None, or 0')
        
        # Проверка дубликатов
        if key in self._table:
            raise KeyError(f'Key {key} already exists in hash table. Existing path: {self._table[key]}')
        
        # Добавляем в таблицу
        self._table[key] = filepath

    def __delitem__(self, key: int):
        """Удалить элемент по ключу"""
        if not isinstance(key, int):
            raise TypeError('Key must be int')
        if key not in self._table:
            raise KeyError(f'Key {key} not found in hash table')
        del self._table[key]

    def __contains__(self, key: int) -> bool:
        """Проверить наличие ключа в таблице"""
        return key in self._table

    def __len__(self) -> int:
        """Количество элементов в таблице"""
        return len(self._table)

    def get_table(self):
        """Получить копию всей таблицы"""
        return dict(self._table)
    
    def keys(self):
        """Получить все ключи"""
        return self._table.keys()
    
    def values(self):
        """Получить все значения (пути к файлам)"""
        return self._table.values()
    
    def items(self):
        """Получить пары (ключ, значение)"""
        return self._table.items()
