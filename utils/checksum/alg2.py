import numpy as np

from ..io.io_base import IODataBase
from ..checksum.cm_base import CMBase


class CMAlgorithm2(CMBase):
    def calc_sum(self, data: IODataBase) -> int:
        img = np.array(data.data, dtype=np.float32)
        if img.ndim == 3 and img.shape[2] == 3:
            gray = img.mean(axis=2)
        else:
            gray = img
        mean_val = gray.mean()
        return int(mean_val)
