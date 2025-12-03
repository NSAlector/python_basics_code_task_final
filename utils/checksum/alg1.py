import numpy as np

from ..io.io_base import IODataBase
from ..checksum.cm_base import CMBase


class CMAlgorithm1(CMBase):
    def calc_sum(self, data: IODataBase) -> int:
        img = np.array(data.data, dtype=np.float32)
        if img.ndim == 3 and img.shape[2] == 3:
            gray = img.mean(axis=2)
        else:
            gray = img

        M, N = gray.shape
        patch_size = 4

        n_patches_h = M // patch_size
        n_patches_w = N // patch_size

        if n_patches_h == 0 or n_patches_w == 0:
            raise ValueError("Изображение слишком маленькое для патчей 4x4")

        patch_means = np.zeros((n_patches_h, n_patches_w), dtype=np.float32)
        for i in range(n_patches_h):
            for j in range(n_patches_w):
                block = gray[i*patch_size:(i+1)*patch_size,
                             j*patch_size:(j+1)*patch_size]
                patch_means[i,j] = block.mean()

        flat = patch_means.flatten()
        bits = (flat[:16] > 127).astype(int)

        checksum = 0
        for b in bits:
            checksum = (checksum << 1) | b

        return checksum