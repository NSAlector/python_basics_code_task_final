from .io_base import IODataBase
from .io_image import IOImageData
from .io_text import IOTextData

def create_reader(filepath):
    import os

    ext = os.path.splitext(filepath)[1].lower()

    if ext in ['.png', '.jpg']:
        return IOImageData()
    elif ext == '.txt':
        return IOTextData()
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {ext}")


__all__ = ['IODataBase', 'IOImageData', 'IOTextData', 'create_reader']