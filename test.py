import os
from utils.io.io import ImageIO, TextIO
from utils.checksum.cm import Algorithm1, Algorithm2
from utils.hash_data.hash_base import HashBase

if __name__=="__main__":
    print('test')
    dataset_dir = "dataset"
    output_dir = "output"
    output_file = os.path.join(output_dir, "base.json")
    
    hashBase = HashBase(key_coder=Algorithm1())
    # hashBase = HashBase(key_coder=Algorithm2())
    
    for filename in os.listdir(dataset_dir):
        filepath = os.path.join(dataset_dir, filename)
        io_obj = None
        if filename.endswith(('.png', '.jpg')):
            io_obj = ImageIO()
        elif filename.endswith('.txt'):
            io_obj = TextIO()
        if io_obj is not None:
            print(f"Обработка: {filename}")
            io_obj.read(filepath)
            if io_obj.data is not None:
                hashBase[None] = io_obj
     
    hashBase.json_save(output_file)
    print(f"Результат сохранен в {output_file}")