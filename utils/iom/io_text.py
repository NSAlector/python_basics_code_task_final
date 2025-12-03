import os
import numpy as np
from io_base import IODataBase

class IOText(IODataBase):
    def __init__(self):
        self.data = None   # numpy array
        self.M = self.N = self.K = None

    def read(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден {filepath}")
        
        if os.path.splitext(filepath)[1].lower() is not ".txt":
            raise ValueError(f"Недопустимое расширение файла {filepath}")

        self.path = filepath
        with open(filepath, 'r') as f:
            header = f.readline().strip().split()
            self.M, self.N, self.K = map(int, header)

            values = []
            for line in f:
                values.extend(line.strip().split())

        values = list(map(float, values))
        arr = np.array(values).reshape(self.M, self.N, self.K)
        self.data = arr
        return arr

    def save(self, path):
        if self.data is None:
            raise ValueError("Nothing to save. Call read() first or assign data manually.")

        M, N, K = self.data.shape
        with open(path, 'w') as f:
            f.write(f"{M} {N} {K}\n")
            flat = self.data.reshape(-1)
            for v in flat:
                f.write(f"{v} ")

    def __len__(self)->int:
        if self.data is None:
            return 0
        return self.data.shape[0] * self.data.shape[1]

    def __getitem__(self, idx):
        if self.data is None:
            raise ValueError("Data not loaded.")

        if not isinstance(idx, tuple) or len(idx) != 2:
            raise TypeError("Index must be a tuple (i, j).")

        i, j = idx
        return self.data[i, j]
    
    def height(self):
        return self.data.shape[0]
        
    def width(self):
        return self.data.shape[1]