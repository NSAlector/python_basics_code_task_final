import os
from abc import ABC, abstractmethod
import numpy as np
from PIL import Image


class IODataBase(ABC):
    def __init__(self, data=None, path=None):
        self.data = None
        self.path = None
        if data is not None:
            self.set_data(data)
        if path is not None:
            self.path = path

    @abstractmethod
    def read(self, filepath):
        raise NotImplementedError

    @abstractmethod
    def save(self, path):
        raise NotImplementedError

    def set_data(self, data):
        arr = np.asarray(data)
        if arr.ndim not in (2, 3):
            raise ValueError("data must be 2D or 3D array")
        self.data = arr.astype(np.uint8)

    def __len__(self) -> int:
        if self.data is None:
            return 0
        if self.data.ndim == 2:
            return int(self.data.shape[0] * self.data.shape[1])
        return int(self.data.shape[0] * self.data.shape[1])

    def __getitem__(self, idx: int):
        if self.data is None:
            raise IndexError("no data")
        size = len(self)
        if idx < 0 or idx >= size:
            raise IndexError("index out of range")
        h = self.data.shape[0]
        w = self.data.shape[1]
        y = idx // w
        x = idx % w
        if self.data.ndim == 2:
            return int(self.data[y, x])
        pixel = self.data[y, x]
        return tuple(int(v) for v in pixel)

    @property
    def shape(self):
        if self.data is None:
            return None
        return self.data.shape

    def as_gray(self):
        if self.data is None:
            raise ValueError("no data")
        if self.data.ndim == 2:
            return self.data.astype(np.float32)
        if self.data.ndim == 3 and self.data.shape[2] == 3:
            arr = self.data.astype(np.float32)
            return arr.mean(axis=2)
        raise ValueError("unsupported image format")


class TextImageIO(IODataBase):
    def read(self, filepath):
        if not isinstance(filepath, str):
            raise TypeError("filepath must be str")
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)
        if not filepath.lower().endswith(".txt"):
            raise ValueError("expected .txt file")
        with open(filepath, "r", encoding="utf-8") as f:
            tokens = f.read().split()
        if len(tokens) < 3:
            raise ValueError("file is too short")
        try:
            m = int(tokens[0])
            n = int(tokens[1])
            k = int(tokens[2])
        except ValueError:
            raise ValueError("invalid header values")
        if m <= 0 or n <= 0 or k <= 0:
            raise ValueError("dimensions must be positive")
        total = m * n * k
        values = tokens[3:]
        if len(values) < total:
            raise ValueError("not enough pixel data")
        arr = np.array(list(map(int, values[:total])), dtype=np.uint8)
        if k == 1:
            data = arr.reshape((m, n))
        else:
            data = arr.reshape((m, n, k))
        self.set_data(data)
        self.path = filepath
        return self

    def save(self, path):
        if self.data is None:
            raise ValueError("no data")
        if not isinstance(path, str):
            raise TypeError("path must be str")
        m = self.data.shape[0]
        n = self.data.shape[1]
        if self.data.ndim == 2:
            k = 1
            flat = self.data.reshape(-1)
        else:
            k = self.data.shape[2]
            flat = self.data.reshape(-1)
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{m} {n} {k}\n")
            f.write(" ".join(str(int(v)) for v in flat))
        self.path = path


class ImageFileIO(IODataBase):
    def read(self, filepath):
        if not isinstance(filepath, str):
            raise TypeError("filepath must be str")
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg"):
            raise ValueError("unsupported image type")
        img = Image.open(filepath)
        if img.mode not in ("L", "RGB"):
            img = img.convert("RGB")
        arr = np.array(img, dtype=np.uint8)
        self.set_data(arr)
        self.path = filepath
        return self

    def save(self, path):
        if self.data is None:
            raise ValueError("no data")
        if not isinstance(path, str):
            raise TypeError("path must be str")
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        arr = self.data
        if arr.ndim == 2:
            img = Image.fromarray(arr.astype(np.uint8), mode="L")
        else:
            img = Image.fromarray(arr.astype(np.uint8), mode="RGB")
        img.save(path)
        self.path = path


def load_image(filepath):
    ext = os.path.splitext(str(filepath))[1].lower()
    if ext == ".txt":
        obj = TextImageIO()
    elif ext in (".png", ".jpg", ".jpeg"):
        obj = ImageFileIO()
    else:
        raise ValueError("unsupported file type")
    return obj.read(filepath)
