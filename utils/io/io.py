from msilib.schema import File
import numpy as np
import cv2
from .io_base import IODataBase

class ImageIO(IODataBase):
    def read(self, filepath: str):
        try:
            img_bgr = cv2.imread(filepath)
            if img_bgr is None:
                raise FileNotFoundError(f"Ошибка! Изображение не найдено: {filepath}")
            self.data = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) #bgr to rgb
            self.filepath = filepath
            
        except:
            print("Ошибка при чтении изображения!")

    def save(self, path: str):
        if self.data is not None:
            try:
                if len(self.data.shape) == 3 and self.data.shape[2] == 3:
                    img_bgr = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR) #color, rgb to bgr
                else:
                    img_bgr = self.data #gray
                
                cv2.imwrite(path, img_bgr)
            except:
                print("Ошибка при сохранении изображения!")
        else:
            print("Невозможно сохранить изображение, массив данных пуст.")
            
class TextIO(IODataBase):
    def read(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                text = f.read().split()
                
            if text is None:
                raise FileNotFoundError(f"Ошибка! Текстовый файл не найден: {filepath}")

            m, n, k = int(text[0]), int(text[1]), int(text[2])
            values = list(map(int, text[3:]))
            
            if len(values) != m * n * k:
                raise ValueError("Ошибка! Неверное количество значений в файле")

            self.data = np.array(values, dtype=np.uint8).reshape((m, n, k))
            self.filepath = filepath
            
        except:
            print("Ошибка при чтении текстового файла!")

    def save(self, path: str):
        if self.data is not None:
            m, n, k = self.data.shape
            header = f"{m}\n{n}\n{k}\n"
            body = "\n".join(map(str, self.data.flatten()))
            with open(path, 'w') as f:
                f.write(f"{header}\n{body}")
        else:
            print("Невозможно сохранить текстовый файл, массив данных пуст.")