from abc import ABC, abstractmethod
import os
from PIL import Image
import numpy as np

class IODataBase(ABC):
    """
    Базовый интерфейс для работы с данными.
    Реализации должны устанавливать self.data (numpy array) и self.filepath (str).
    """

    @abstractmethod
    def read(self, filepath: str):
        """Прочитать данные из filepath и сохранить в self.data (numpy array)"""
        raise NotImplementedError

    @abstractmethod
    def save(self, path: str):
        """Сохранить данные в указанный путь (формат зависит от реализации)"""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Количество элементов (пикселей)"""
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, idx: int):
        """Вернуть пиксель по индексу (может поддерживаться int или tuple)"""
        raise NotImplementedError


class ImageData(IODataBase):
    """
    Работа с изображениями .png, .jpg.
    self.data: numpy array shape (H, W, 3), dtype=uint8
    self.filepath: исходный путь
    """

    def __init__(self):
        self.data = None
        self.filepath = None

    def read(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'File not found: {filepath}')
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ('.png', '.jpg', '.jpeg'):
            raise ValueError(f'Unsupported image extension: {ext}')
        try:
            img = Image.open(filepath).convert('RGB')
            arr = np.asarray(img, dtype=np.uint8)
            if arr.ndim != 3 or arr.shape[2] != 3:
                raise ValueError('ImageData expects an RGB image after convert.')
            self.data = arr
            self.filepath = filepath
        except Exception as e:
            raise IOError(f'Failed to read image {filepath}: {e}')

    def save(self, path: str):
        if self.data is None:
            raise ValueError('No data to save.')
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        img = Image.fromarray(self.data)
        img.save(path)
        return path

    def __len__(self) -> int:
        if self.data is None:
            return 0
        h, w, _ = self.data.shape
        return h * w

    def __getitem__(self, idx):
        if self.data is None:
            raise IndexError('Data is empty.')
        h, w, _ = self.data.shape
        if isinstance(idx, tuple):
            r, c = idx
            if not (0 <= r < h and 0 <= c < w):
                raise IndexError('Index out of range.')
            return tuple(int(x) for x in self.data[r, c])
        if isinstance(idx, int):
            if idx < 0 or idx >= h * w:
                raise IndexError('Index out of range.')
            r = idx // w
            c = idx % w
            return tuple(int(x) for x in self.data[r, c])
        raise TypeError('Index must be int or tuple')


class TextImageData(IODataBase):
    """
    Текстовый формат:
    первые три значения: M N K
    далее M*N*K значений (row-major). Если K==3 — RGB.
    Сохраняем в numpy array shape (M, N, K) или (M, N) если K==1.
    """

    def __init__(self):
        self.data = None
        self.filepath = None
        self.M = None
        self.N = None
        self.K = None

    def read(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'File not found: {filepath}')
        ext = os.path.splitext(filepath)[1].lower()
        if ext != '.txt':
            raise ValueError('TextImageData expects a .txt file')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip().split()
            if len(content) < 3:
                raise ValueError('File must contain at least 3 integers (M N K)')
            M = int(content[0])
            N = int(content[1])
            K = int(content[2])
            if M <= 0 or N <= 0 or K <= 0:
                raise ValueError('M, N, K must be positive integers')
            expected = M * N * K
            values = content[3:]
            if len(values) < expected:
                raise ValueError(f'Not enough pixel values: expected {expected}, got {len(values)}')
            # take exactly expected values
            vals = list(map(int, values[:expected]))
            arr = np.array(vals, dtype=np.uint8)
            if K == 1:
                arr = arr.reshape((M, N))
            else:
                arr = arr.reshape((M, N, K))
            self.data = arr
            self.M = M
            self.N = N
            self.K = K
            self.filepath = filepath
        except Exception as e:
            raise IOError(f'Failed to read text image {filepath}: {e}')

    def save(self, path: str):
        if self.data is None:
            raise ValueError('No data to save.')
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        M = self.data.shape[0]
        N = self.data.shape[1]
        K = 1 if self.data.ndim == 2 else self.data.shape[2]
        flat = self.data.flatten().tolist()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"{M} {N} {K}\n")
            # write values in chunks for readability
            for i, v in enumerate(flat):
                f.write(str(int(v)))
                if i != len(flat) - 1:
                    f.write(' ')
        return path

    def __len__(self) -> int:
        if self.data is None:
            return 0
        if self.data.ndim == 2:
            return self.data.shape[0] * self.data.shape[1]
        return self.data.shape[0] * self.data.shape[1]

    def __getitem__(self, idx):
        if self.data is None:
            raise IndexError('Data is empty.')
        h = self.data.shape[0]
        w = self.data.shape[1]
        if isinstance(idx, tuple):
            r, c = idx
            if not (0 <= r < h and 0 <= c < w):
                raise IndexError('Index out of range.')
            val = self.data[r, c]
            if isinstance(val, np.ndarray):
                return tuple(int(x) for x in val)
            return int(val)
        if isinstance(idx, int):
            if idx < 0 or idx >= h * w:
                raise IndexError('Index out of range.')
            r = idx // w
            c = idx % w
            val = self.data[r, c]
            if isinstance(val, np.ndarray):
                return tuple(int(x) for x in val)
            return int(val)
        raise TypeError('Index must be int or tuple')
