import os
import sys

# Добавляем пути для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.io import create_reader, IOImageData, IOTextData
from utils.checksum import Algorithm1, Algorithm2
from utils.hash_data import HashBase


def process_dataset(dataset_path="./dataset", algorithm="algorithm1"):

    if not os.path.exists(dataset_path):
        print(f"Ошибка: Каталог {dataset_path} не найден")
        return None

    # Выбираем алгоритм
    if algorithm == "algorithm1":
        key_coder = Algorithm1()
    elif algorithm == "algorithm2":
        key_coder = Algorithm2()
    else:
        print(f"Ошибка: Неизвестный алгоритм {algorithm}")
        return None

    # Создаем хеш-таблицу
    hash_table = HashBase(key_coder)

    # Счетчики
    total_files = 0
    successful_files = 0
    error_files = []

    print(f"Обработка каталога: {dataset_path}")
    print(f"Используемый алгоритм: {algorithm}")
    print("=" * 50)

    # Рекурсивный обход каталога
    for root, dirs, files in os.walk(dataset_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            total_files += 1

            try:
                print(f"Обработка файла {total_files}: {filename}")

                # Создаем соответствующий ридер
                reader = create_reader(filepath)

                # Читаем файл
                data = reader.read(filepath)

                # Добавляем в хеш-таблицу
                key = hash_table.add_data(data)

                print(f"  ✓ Успешно. Ключ: {key}")
                successful_files += 1

            except Exception as e:
                print(f"  ✗ Ошибка: {str(e)}")
                error_files.append((filename, str(e)))


    if error_files:
        print("\nФайлы с ошибками:")
        for filename, error in error_files[:5]:  # Показываем первые 5 ошибок
            print(f"  {filename}: {error}")
        if len(error_files) > 5:
            print(f"  ... и еще {len(error_files) - 5} ошибок")

    # Сохраняем хеш-таблицу
    try:
        saved_path = hash_table.json_save()
        print(f"\nХеш-таблица сохранена: {saved_path}")
    except Exception as e:
        print(f"\nОшибка при сохранении хеш-таблицы: {str(e)}")

    return hash_table





def main():
    """Основная функция"""
    print("=" * 60)
    print("СИСТЕМА УНИКАЛЬНЫХ ДАННЫХ ИЗОБРАЖЕНИЙ")
    print("=" * 60)

    # Создаем пример структуры каталогов
    if not os.path.exists("./dataset"):
        print("Создаю пример структуры каталогов...")
        os.makedirs("./dataset/images", exist_ok=True)
        os.makedirs("./dataset/text_data", exist_ok=True)

        # Создаем пример текстового файла
        sample_text = """3 3 3
255 0 0 0 255 0 0 0 255
0 0 0 128 128 128 255 255 255
100 100 100 150 150 150 200 200 200"""

        with open("./dataset/text_data/sample.txt", "w") as f:
            f.write(sample_text)

        print("Созданы примеры файлов в ./dataset")

    # Запускаем обработку с алгоритмом 1
    print("\nЗАПУСК ОБРАБОТКИ С АЛГОРИТМОМ 1")
    hash_table1 = process_dataset("./dataset", "algorithm1")

    print("\n" + "=" * 60)

    # Запускаем обработку с алгоритмом 2
    print("\nЗАПУСК ОБРАБОТКИ С АЛГОРИТМОМ 2")
    hash_table2 = process_dataset("./dataset", "algorithm2")




if __name__ == "__main__":
    main()