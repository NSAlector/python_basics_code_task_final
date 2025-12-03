import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.dirname(current_dir)              

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.io.io_base import io_process
from utils.checksum.cm_base import CMPatch
from utils.hash_data.hash_base import HashBase

def main():
    dataset_dir = os.path.join(project_root, "dataset")
    output_dir = os.path.join(project_root, "output")
    output_file = os.path.join(output_dir, "hash_table.json")

    if not os.path.exists(dataset_dir):
        raise SystemError

    hasher = CMPatch()
    htable = HashBase(hasher)

    files = os.listdir(dataset_dir)
    print(f"Found {len(files)} files.")

    for name in files:
        path = os.path.join(dataset_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            io_obj = io_process(path)
            io_obj.read(path)
            key = hasher.calc_sum(io_obj)
            htable[key] = io_obj
            print(f"{name} -> {key}")
        except Exception as e:
            print(f"Error processing {name}: {e}")

    htable.json_save(output_file)
    print(f"Saved result to {output_file}")

if __name__ == "__main__":
    main()
