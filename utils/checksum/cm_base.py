from ..io.io_base import IODataBase


class CMBase:
    def calc_sum(self, data: IODataBase) -> int:
        raise NotImplementedError


class PatchChecksum(CMBase):
    def calc_sum(self, data: IODataBase) -> int:
        if not isinstance(data, IODataBase):
            raise TypeError("data must be IODataBase")
        arr = data.as_gray()
        if arr.ndim != 2:
            raise ValueError("grayscale image must be 2D")
        m = arr.shape[0]
        n = arr.shape[1]
        if m % 4 != 0 or n % 4 != 0:
            raise ValueError("image size must be divisible by 4")
        ph = m // 4
        pw = n // 4
        result = 0
        for i in range(4):
            for j in range(4):
                patch = arr[i * ph:(i + 1) * ph, j * pw:(j + 1) * pw]
                mean = float(patch.mean())
                bit = 1 if mean > 127 else 0
                result = (result << 1) | bit
        return int(result)


class MeanChecksum(CMBase):
    def calc_sum(self, data: IODataBase) -> int:
        if not isinstance(data, IODataBase):
            raise TypeError("data must be IODataBase")
        arr = data.as_gray()
        mean = float(arr.mean())
        return int(round(mean))
