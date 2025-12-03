import os
import json
from typing import Union, Optional
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase


class HashBase:
    def __init__(self, key_coder: CMBase):
        if not isinstance(key_coder, CMBase):
            raise TypeError('key_coder must be an instance of CMBase')
        self.key_coder = key_coder
        self._table = {}

    def json_save(self, path: str):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        serializable = {str(k): v for k, v in self._table.items()}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
        return path

    def __getitem__(self, key: int) -> str:
        if not isinstance(key, int):
            raise TypeError('Key must be int')
        if key not in self._table:
            raise KeyError(f'Key {key} not found in hash table')
        return self._table[key]

    def __setitem__(self, key: Optional[int], data: Union[IODataBase, str]):
        io_obj = None
        filepath = None

        if isinstance(data, str):
            filepath = data
            if not os.path.exists(filepath):
                raise FileNotFoundError(f'File not found: {filepath}')

            if key is None or key == 0:
                from ..test import choose_io_class
                io_obj = choose_io_class(filepath)
                io_obj.read(filepath)
        else:
            if not isinstance(data, IODataBase):
                raise TypeError('data must be IODataBase or filepath string')
            io_obj = data
            filepath = getattr(data, 'filepath', None)
            if filepath is None:
                raise ValueError('IODataBase object must have .filepath attribute')
            if not os.path.exists(filepath):
                raise FileNotFoundError(f'File not found: {filepath}')

        if key is None or key == 0:
            if io_obj is None:
                raise ValueError('Cannot auto-generate key: data object not available')
            key = self.key_coder.calc_sum(io_obj)
        else:
            if not isinstance(key, int):
                raise TypeError('Key must be int, None, or 0')

        if key in self._table:
            raise KeyError(f'Key {key} already exists in hash table. Existing path: {self._table[key]}')

        self._table[key] = filepath

    def __delitem__(self, key: int):
        if not isinstance(key, int):
            raise TypeError('Key must be int')
        if key not in self._table:
            raise KeyError(f'Key {key} not found in hash table')
        del self._table[key]

    def __contains__(self, key: int) -> bool:
        return key in self._table

    def __len__(self) -> int:
        return len(self._table)

    def get_table(self):
        return dict(self._table)

    def keys(self):
        return self._table.keys()

    def values(self):
        return self._table.values()

    def items(self):
        return self._table.items()
