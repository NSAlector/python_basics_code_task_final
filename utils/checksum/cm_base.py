from ..io.io_base import IODataBase
import numpy as np


class CMBase:
    def calc_sum(self, data: 'IODataBase') -> int:
        raise NotImplementedError()
    
class CMPatch(CMBase):
    def calc_sum(self, data: 'IODataBase') -> int:
        if data.data is None:
            raise ValueError("Data not loaded")
            
        img = data.data

        if len(img.shape) == 3 and img.shape[2] == 3:
            c1 = img[:, :, 0].astype(float)
            c2 = img[:, :, 1].astype(float)
            c3 = img[:, :, 2].astype(float)
            gray = (c1 + c2 + c3) / 3.0
        else:
            gray = img

            
        H, W = gray.shape
        dy = H // 4
        dx = W // 4
        binary_string = ""
        for i in range(4):
            for j in range(4):
                patch = gray[i*dy : (i+1)*dy, j*dx : (j+1)*dx]
                
                val = np.mean(patch) if patch.size > 0 else 0
                
                binary_string += '1' if val > 127 else '0'
        
        return int(binary_string, 2)


class CMAvg(CMBase):
    """
    Class for middle intensive calculation
    """
    def calc_sum(self, data: 'IODataBase') -> int:
        if data.data is None:
            raise ValueError("Data not loaded")        
        img = data.data
        avg_val = np.mean(img)
        return int(avg_val)