import numpy as np
from checksum.cm_base import CMBase
from iom.io_base import IODataBase

class CMAlgo1(CMBase):

    def calc_sum(self, data: IODataBase ) ->int:
        img = data.data

        if img.ndim == 3 and img.shape[2] == 3:
            gray = img.mean(axis=2)
        else:
            gray = img.astype(np.float32)

        H, W = gray.shape
        H_crop = H - (H % 4)
        W_crop = W - (W % 4)
        gray_cropped = gray[:H_crop, :W_crop]

        bin_array = []
        for i in range(0, H_crop, 4):
            for j in range(0, W_crop, 4):
                patch = gray_cropped[i:i+4, j:j+4]
                mean_val = patch.mean()
                bin_array.append(1 if mean_val > 127 else 0)

        checksum = 0
        for bit in bin_array:
            checksum = (checksum << 1) | bit

        return hex(checksum)