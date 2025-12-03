import json
import os
from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase

class HashBase:
    def __init__(self, key_coder: 'CMBase'):
        self.key_coder = key_coder
        self.table = {}

    def json_save(self, path: str):
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.table, f, indent=4)

    def __getitem__(self, key: int):
        return self.table.get(key)

    def __setitem__(self, key: int, data: 'IODataBase'):
        final_key = key
        
        if not final_key: 
            if self.key_coder:
                final_key = self.key_coder.calc_sum(data)
            else:
                raise ValueError("Key is missing")
        
        if data.path:
            file_path = data.path
        else:
            file_path = "unknown"
            
        self.table[final_key] = file_path

    def __delitem__(self, key: int):
        if key in self.table:
            del self.table[key]
