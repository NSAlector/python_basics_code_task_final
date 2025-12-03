import numpy as np
from checksum.cm_base import CMBase
from iom.io_base import IODataBase

class CMAlgo2(CMBase):

    def calc_sum(self, data: IODataBase ) ->int:

        H = data.data.shape[0]
        W = data.data.shape[1]

        total = 0
        count = H * W

        for i in range(H):
            for j in range(W):
                px = data[i, j]

                if isinstance(px, np.ndarray) or isinstance(px, (list, tuple)):
                    gray = sum(px) / len(px)
                else:
                    gray = float(px)

                total += gray

        return total / count