#здесь собраны все модули, которые надо было создать.
# main как запуск и использование этих функций
#также отсутствует, т е программа не запустится, поэтому чисто на посмотреть
#тот код, который успела написать

import json

class IODataBase:
    def read(self, filepath):
        if not filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        with open(filepath, 'rb') as f:
            bin_d = f.read()
    def save(self, path):
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")
        with open(path, 'w') as f:
            f.write(bin_d)
    def __len__(self)->int:

    def __getitem__(self, idx: int):
        
class IODBtxt(IODataBase):
    def __init__(self):
        super().__init__()
    def read(self, filepath):
        if not filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        with open(filepath, 'r') as f:
            txt = f.read()
    def save(self, path):
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")
        with open(path, 'w') as f:
            f.write(txt)
    def getMNKdata(self, path):
        with open(path, 'r') as f:
            # далее будем предполагать что одно значение - одна строка
            m = int(f.readline())
            n = int(f.readline())
            k = int(f.readline())
            mnk = m*n*k

class HashBase:
    def __init__(self, key_coder: CMBase):
        self.key_coder = key_coder
    def json_save(self, path):
        with open('./output/hash_table.json', 'w', encoding= 'utf-8') as f:
            json.dump(self.key_coder, f)
    def __getitem__(self, key: int):
        if key in self.key_coder:
            return self.key_coder[key]
    def __setitem__(self, key: int, data: IODataBase):
        self.key_coder[key] = data
    def __delitem__(self, key: int):
        if key in self.key_coder:
            del self.key_coder[key]


class CMBase:
    def calc_sum(self, data: IODataBase ) ->int:

class CMBalgF(CMBase):
    def __init__(self, data: IODataBase):
        super().__init__()
        self.data = data
    def algFirst(self, data):


class CMBalgS(CMBase):
    def __init__(self, data: IODataBase):
        super().__init__()
        self.data = data
    def algSecond(self, data):