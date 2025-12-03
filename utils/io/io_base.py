import cv2
import numpy as np


class IODataBase:
    """
    Base class for data processing
    """
    def __init__(self):
        self.data = None
        self.path = None

    def read(self, filepath):
        pass

    def save(self, path):
        pass

    def __len__(self) -> int:
        if self.data is not None:
            return len(self.data)
        return 0
    
    def __getitem__(self, idx):
        if self.data is not None:
            return self.data[idx]
        raise ValueError("Data is not loaded")

class ImageIO(IODataBase):
    """
    Class for reading images
    """
    def read(self, filepath) -> np.ndarray:
        data = cv2.imread(filepath)
        if data is None:
            raise ValueError(f"Could not read image from")
        self.data = data
        self.path = filepath
        return self.data

class TextIO(IODataBase):
    """
    Class for reading/saving text
    """
    def read(self, filepath) -> np.ndarray:
        with open(filepath, "r") as file:
            source = file.read().split()
        
        if len(source) < 3:
            raise ValueError("File too short")

        M, N, K = map(int, source[:3])
        
        pixel_values_str = source[3:]
        
        if len(pixel_values_str) != M * N * K:
            raise ValueError(f"Data length mismatch. Expected {M*N*K}, got {len(pixel_values_str)}")

        pixel_values = list(map(int, pixel_values_str))
        
        self.data = np.array(pixel_values, dtype=np.uint8).reshape((M, N, K))
        self.path = filepath
        return self.data
    
    def save(self, path):
        if self.data is None:
            raise ValueError("No data for saving")
        M, N, K = self.data.shape
        flat_data = self.data.flatten()
        with open(path, "w") as file:
            file.write(f"{M} {N} {K} ")
            file.write(" ".join(map(str, flat_data)))

def io_process(filepath):
    """Type checker"""
    if filepath.split('.')[-1] == 'txt':
        return TextIO()
    elif filepath.split('.')[-1] in ['png', 'jpg', 'jpeg']:
        return ImageIO()
    else:
        return IODataBase()

