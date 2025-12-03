import numpy as np
from abc import abstractmethod
from PIL import Image


class IODataBase:
    @abstractmethod
    def read(self, filepath):
        pass

    @abstractmethod
    def save(self, path):
        pass

    @abstractmethod
    def __len__(self)->int:
        pass

    @abstractmethod
    def __getitem__(self, idx: int):
        pass


class IOTextData(IODataBase):
    def __init__(self):
        self.data = None

    def read(self, filepath):
        with open(filepath, 'r') as f:
            header = f.readline().strip().split()
            M, N, K = map(int, header)

            values = []
            for line in f:
                values.extend(map(float, line.split()))

        expected = M * N * K
        if len(values) != expected:
            raise ValueError(f"Ожидалось {expected} значений, получено {len(values)}")

        arr = np.array(values, dtype=np.float32)
        self.data = arr.reshape(M, N, K)

    def save(self, path):
        M, N, K = self.data.shape
        with open(path, 'w') as f:
            f.write(f"{M} {N} {K}")
            flat = self.data.reshape(-1)
            for val in flat:
                f.write(f"{val} ")
        print(f"Файл сохранен: {path}")

    def __len__(self):
        return self.data.size

    def __getitem__(self, idx):
        return self.data.reshape(-1, self.data.shape[-1])[idx]


class IOImageData(IODataBase):
    def __init__(self):
        self.data = None

    def read(self, filepath):
        img = Image.open(filepath).convert('RGB')
        self.data = np.array(img, dtype=np.uint8)

    def save(self, path):
        img = Image.fromarray(self.data.astype(np.uint8))
        img.save(path)
        print(f"Файл сохранен: {path}")

    def __len__(self):
        return self.data.shape[0] * self.data.shape[1]

    def __getitem__(self, idx):
        M, N, K = self.data.shape
        row = idx // N
        col = idx % N
        return self.data[row, col]

