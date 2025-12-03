import json
import os
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase


class HashBase:
    def __init__(self, key_coder: CMBase):
        if not isinstance(key_coder, CMBase):
            raise TypeError("key_coder must be CMBase")
        self.key_coder = key_coder
        self._table = {}

    def json_save(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be str")
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._table, f, ensure_ascii=False, indent=2)

    def __getitem__(self, key: int):
        if key not in self._table:
            raise KeyError("key not found")
        return self._table[key]

    def __setitem__(self, key: int, data: IODataBase):
        if not isinstance(data, IODataBase):
            raise TypeError("data must be IODataBase")
        if not getattr(data, "path", None):
            raise ValueError("data.path must be set")
        if key is None or key == 0:
            key = self.key_coder.calc_sum(data)
        if key in self._table:
            raise KeyError("key already exists")
        self._table[int(key)] = data.path

    def __delitem__(self, key: int):
        if key not in self._table:
            raise KeyError("key not found")
        del self._table[key]
