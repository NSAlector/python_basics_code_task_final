import numpy as np
from ..io.io_base import IODataBase


class CMBase:
    def calc_sum(self, data):
        raise NotImplementedError("Метод calc_sum должен быть реализован в подклассе")


class Algorithm1(CMBase):
    def calc_sum(self, data):
        if data.data is None:
            return 0
        img = data.data

        if len(img.shape) == 3 and img.shape[2] == 3:
            gray = np.mean(img, axis=2)
        else:
            gray = img
        h, w = gray.shape

        step_h = h // 4
        step_w = w // 4

        bits_list = []
        for i in range(4):
            for j in range(4):
                patch = gray[i*step_h:(i+1)*step_h, j*step_w:(j+1)*step_w]
                if patch.size > 0:
                    avg_val = np.mean(patch)
                else:
                    avg_val = 0

                if avg_val > 127:
                    bits_list.append(1)
                else:
                    bits_list.append(0)

        bits_string = "".join(map(str, bits_list))
        num = int(bits_string, 2)
        return num


class Algorithm2(CMBase):
    def calc_sum(self, data):
        if data.data is None:
            return 0
        img = data.data
        num = int(np.mean(img))
        return num
