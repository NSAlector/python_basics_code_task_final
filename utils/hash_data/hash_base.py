import os
import json
from checksum.cm_base import CMBase
from iom.io_base import IODataBase

class HashBase:
    def __init__(self, key_coder:CMBase):...
    def json_save(self, path): ...
    def __getitem__ (self, key: int):...
    def __setitem__ (self, key: int, data: IODataBase):...
    def __delitem__ (self, key: int):...
    

class HashBase:
    def __init__(self, key_coder: CMBase):
        self.key_coder = key_coder
        self.table = {}

    def json_save(self, path="./output/hash_table.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.table, f, indent=4, ensure_ascii=False)

    def __getitem__(self, key: int):
        return self.table.get(key)

    def __setitem__(self, key, data: IODataBase):
        if not hasattr(data, "path"):
            raise ValueError("IODataBase must contain .path attribute")

        self.table[key] = data.path

    def __delitem__(self, key: int):
        if key in self.table:
            del self.table[key]