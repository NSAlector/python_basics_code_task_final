from abc import ABC, abstractmethod
from ..io.io_base import IODataBase
import numpy as np


class CMBase(ABC):
    @abstractmethod
    def calc_sum(self, data: IODataBase) -> int:
        raise NotImplementedError


class CMAlg1(CMBase):
    def _to_grayscale(self, arr: np.ndarray) -> np.ndarray:
        if arr.ndim == 3 and arr.shape[2] == 3:
            return arr.mean(axis=2)
        elif arr.ndim == 2:
            return arr.astype(np.float64)
        else:
            raise ValueError('Unsupported data shape for CMAlg1')

    def _get_patch_means(self, gray: np.ndarray, h: int, w: int) -> list:
        patch_h, patch_w = h / 4.0, w / 4.0
        patch_means = []

        for i in range(4):
            for j in range(4):
                start_row, end_row = int(i * patch_h), int((i + 1) * patch_h)
                start_col, end_col = int(j * patch_w), int((j + 1) * patch_w)

                patch = gray[start_row:end_row, start_col:end_col]
                patch_means.append(float(patch.mean()) if patch.size > 0 else 0.0)

        return patch_means

    def calc_sum(self, data: IODataBase) -> int:
        if not hasattr(data, 'data') or data.data is None:
            raise ValueError('Provided data object has no .data')

        arr = np.asarray(data.data)
        gray = self._to_grayscale(arr)

        h, w = gray.shape

        if h < 4 or w < 4:
            raise ValueError(f'Image too small for CMAlg1: {h}x{w}. Minimum size is 4x4 pixels.')

        patch_means = self._get_patch_means(gray, h, w)

        bits = [1 if m > 127.0 else 0 for m in patch_means]

        return int(''.join(map(str, bits)), 2)


class CMAlg2(CMBase):
    def calc_sum(self, data: IODataBase) -> int:
        if not hasattr(data, 'data') or data.data is None:
            raise ValueError('Provided data object has no .data')

        arr = np.asarray(data.data)

        if arr.size == 0:
            raise ValueError('Data array is empty')

        mean_intensity = np.mean(arr)

        return int(round(mean_intensity))
