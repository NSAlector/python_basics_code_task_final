import os
import numpy as np
from PIL import Image
from iom.io_base import IODataBase

class IOImage(IODataBase):
    def __init__(self):
        self.data = None   # numpy array
        self.path = None

    def read(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден {filepath}")
        
        if os.path.splitext(filepath)[1].lower() not in [".png", ".jpg"]:
            raise ValueError(f"Недопустимое расширение файла {filepath}")

        self.path = filepath
        img = Image.open(filepath).convert("RGB")
        self.data = np.array(img)
        return self.data

    def save(self, path):
        if self.data is None:
            raise ValueError("Nothing to save.")
        img = Image.fromarray(self.data.astype(np.uint8))
        img.save(path)

    def __len__(self):
        if self.data is None:
            return 0
        # количество пикселей
        return self.data.shape[0] * self.data.shape[1]

    def __getitem__(self, idx):
        if self.data is None:
            raise ValueError("Data not loaded.")

        return self.data[idx]
    
    def height(self):
        return self.data.shape[0]
        
    def width(self):
        return self.data.shape[1]