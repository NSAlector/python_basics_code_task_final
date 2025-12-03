from ..checksum.cm_base import CMBase
from ..io.io_base import IODataBase
import os
import json

class HashBase:
    def __init__(self, key_coder:CMBase):
        self.key_coder = key_coder
        self.table = {}
    def json_save(self, path):
        try:
            dir = os.path.dirname(path)
            if dir and not os.path.exists(dir):
                os.makedirs(dir)

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.table, f, indent=4)
                
        except Exception as e:
            print(f"Ошибка при сохранении json фалйа: {e}")
    def __getitem__ (self, key: int):
        return self.table.get(key)
    def __setitem__ (self, key: int, data: IODataBase):
        if key is None or 0:
            try:
                key = self.key_coder.calc_sum(data)
                self.table[key] = data.filepath
            
            except:
                print("Ошибка при добавлении!")
        else:    
            self.table[key] = data.filepath
    def __delitem__ (self, key: int):
        if key in self.table:
            del self.table[key]