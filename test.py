from utils.io import load_image
from utils.checksum import PatchChecksum
from utils.hash_data import HashBase

if __name__ == "__main__":
    data = load_image("dataset/sar_1_gray.jpg")
    coder = PatchChecksum()
    table = HashBase(coder)
    table[0] = data
    table.json_save("output/hash_table.json")
    print(table._table)
