from ..io.io_base import IOTextData, IOImageData

def load_data(filepath: str):
    if filepath.endswith('.txt'):
        loader = IOTextData()
    elif filepath.endswith('.png') or filepath.endswith('.jpg'):
        loader = IOImageData()
    else:
        raise ValueError("Неизвестный формат файла")
    loader.read(filepath)
    return loader