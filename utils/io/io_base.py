import numpy as np

class IODataBase:
    def __init__(self):
        self.data = None
        self.filepath = None
    def read(self, filepath):
        raise NotImplementedError
    def save(self, path):
        raise NotImplementedError
    def __len__(self)->int:
        if self.data is not None:
            return self.data.size
        return 0
    def __getitem__(self, idx: int):
        if self.data is not None:
            return self.data.flat[idx]
        raise ValueError("Ошибка! Массив данных пуст")

