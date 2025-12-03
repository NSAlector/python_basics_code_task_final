import os
from utils.io.io_base import TextIOData, ImageIOData
from utils.checksum.cm_base import Algorithm1, Algorithm2
from utils.hash_data.hash_base import HashBase


def process_dataset(files_to_process, algo):

    hash_table = HashBase(algo)

    for filepath in files_to_process:
        try:
            print(f"\nОбработка {filepath}:")

            if filepath.endswith(('.png', '.jpg', '.jpeg')):
                data = ImageIOData(filepath)
            elif filepath.endswith('.txt'):
                data = TextIOData(filepath)
            else:
                print(f"  Пропущен: неподдерживаемый формат")
                continue

            key = hash_table.add(data)
            print(f"  Успешно обработан, ключ={key}")

        except FileNotFoundError as e:
            print(f"  Файл не найден: {str(e)}")
        except ValueError as e:
            print(f"  Некорректные данные: {str(e)}")
        except Exception as e:
            print(f"  Ошибка {type(e).__name__}: {str(e)}")

    try:
        hash_table.json_save('output/hash_table.json')
        print(f"\nХеш-таблица сохранена в output/hash_table.json")
    except Exception as e:
        print(f"\nОшибка сохранения: {str(e)}")

    return hash_table


if __name__ == "__main__":

    files = []
    for filename in os.listdir("dataset"):
        files.append(str("dataset/" + filename))

    algo = Algorithm2()
    hash_table = process_dataset(files, algo)

    try:
        duplicates = hash_table.find_duplicates()
        if duplicates:
            print(f"\nНайдены дубликаты ({len(duplicates)} ключей):")
            for key, files in duplicates.items():
                print(f"  Ключ {key}:")
                for file in files:
                    print(f"    - {file}")
        else:
            print("\nДубликаты не найдены")
    except Exception as e:
        print(f"\nОшибка поиска дубликатов: {str(e)}")
