"""
Примеры использования модулей проекта python_basics_code_task_final
"""
import os
from pathlib import Path
from utils.io.io_base import ImageData, TextImageData
from utils.checksum.cm_base import CMAlg1, CMAlg2
from utils.hash_data.hash_base import HashBase
from utils.test import build_hash_table, choose_io_class

# Базовая директория
BASE_DIR = Path(__file__).resolve().parent


def example_1_read_image():
    """Пример 1: Чтение изображения"""
    print("=" * 60)
    print("ПРИМЕР 1: Чтение изображения")
    print("=" * 60)
    
    image_path = BASE_DIR / 'dataset' / 'example.png'  # Замените на реальный путь
    
    if not image_path.exists():
        print(f"Файл не найден: {image_path}")
        return
    
    try:
        # Создаем объект для работы с изображением
        img_data = ImageData()
        img_data.read(str(image_path))
        
        print(f"Файл: {image_path.name}")
        print(f"Размер: {img_data.data.shape}")
        print(f"Количество пикселей: {len(img_data)}")
        print(f"Первый пиксель (RGB): {img_data[0]}")
        print(f"Пиксель (0,0): {img_data[(0, 0)]}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_2_read_text_image():
    """Пример 2: Чтение текстового представления изображения"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 2: Чтение текстового изображения")
    print("=" * 60)
    
    text_path = BASE_DIR / 'dataset' / 'example.txt'
    
    if not text_path.exists():
        print(f"Файл не найден: {text_path}")
        return
    
    try:
        txt_data = TextImageData()
        txt_data.read(str(text_path))
        
        print(f"Файл: {text_path.name}")
        print(f"Размеры (M x N x K): {txt_data.M} x {txt_data.N} x {txt_data.K}")
        print(f"Форма данных: {txt_data.data.shape}")
        print(f"Первый пиксель: {txt_data[0]}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_3_checksum_algorithms():
    """Пример 3: Вычисление контрольных сумм"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 3: Вычисление контрольных сумм")
    print("=" * 60)
    
    # Используем первый доступный файл из dataset
    dataset_path = BASE_DIR / 'dataset'
    files = list(dataset_path.glob('*'))
    
    if not files:
        print("Нет файлов в dataset")
        return
    
    file_path = files[0]
    
    try:
        # Загружаем данные
        io_obj = choose_io_class(str(file_path))
        io_obj.read(str(file_path))
        
        # Алгоритм 1: патчи 4x4
        alg1 = CMAlg1()
        checksum1 = alg1.calc_sum(io_obj)
        
        # Алгоритм 2: среднее значение
        alg2 = CMAlg2()
        checksum2 = alg2.calc_sum(io_obj)
        
        print(f"Файл: {file_path.name}")
        print(f"Контрольная сумма (Алгоритм 1): {checksum1} (binary: {bin(checksum1)})")
        print(f"Контрольная сумма (Алгоритм 2): {checksum2}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_4_hash_table_basic():
    """Пример 4: Основные операции с хеш-таблицей"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 4: Основные операции с хеш-таблицей")
    print("=" * 60)
    
    # Создаем хеш-таблицу с алгоритмом 1
    coder = CMAlg1()
    table = HashBase(coder)
    
    dataset_path = BASE_DIR / 'dataset'
    files = list(dataset_path.glob('*'))[:3]  # Берем первые 3 файла
    
    if not files:
        print("Нет файлов в dataset")
        return
    
    try:
        print("Добавление элементов:")
        for file_path in files:
            io_obj = choose_io_class(str(file_path))
            io_obj.read(str(file_path))
            key = coder.calc_sum(io_obj)
            
            # Явное указание ключа
            table[key] = io_obj
            print(f"  Добавлено: key={key}, file={file_path.name}")
        
        print(f"\nВсего элементов в таблице: {len(table)}")
        
        # Получение элемента
        first_key = list(table.keys())[0]
        print(f"\nПолучение элемента по ключу {first_key}:")
        print(f"  Путь: {table[first_key]}")
        
        # Проверка наличия ключа
        print(f"\nКлюч {first_key} в таблице: {first_key in table}")
        print(f"Ключ 99999 в таблице: {99999 in table}")
        
        # Удаление элемента
        print(f"\nУдаление элемента с ключом {first_key}")
        del table[first_key]
        print(f"Элементов после удаления: {len(table)}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_5_auto_key_generation():
    """Пример 5: Автоматическая генерация ключей"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 5: Автоматическая генерация ключей")
    print("=" * 60)
    
    coder = CMAlg1()
    table = HashBase(coder)
    
    dataset_path = BASE_DIR / 'dataset'
    files = list(dataset_path.glob('*'))[:2]
    
    if not files:
        print("Нет файлов в dataset")
        return
    
    try:
        for file_path in files:
            # Автоматическая генерация ключа (key=None)
            io_obj = choose_io_class(str(file_path))
            io_obj.read(str(file_path))
            
            table[None] = io_obj  # Ключ генерируется автоматически
            
            # Находим только что добавленный ключ
            last_key = list(table.keys())[-1]
            print(f"Автоматически сгенерирован ключ {last_key} для {file_path.name}")
        
        print(f"\nВсего элементов: {len(table)}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


def example_6_exception_handling():
    """Пример 6: Обработка исключений"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 6: Обработка исключений")
    print("=" * 60)
    
    coder = CMAlg1()
    table = HashBase(coder)
    
    # 1. Несуществующий файл
    print("1. Попытка загрузить несуществующий файл:")
    try:
        img = ImageData()
        img.read('nonexistent.png')
    except FileNotFoundError as e:
        print(f"   ✓ Перехвачено: {e}")
    
    # 2. Неподдерживаемый формат
    print("\n2. Попытка загрузить файл неподдерживаемого формата:")
    try:
        io_obj = choose_io_class('file.bmp')
    except ValueError as e:
        print(f"   ✓ Перехвачено: {e}")
    
    # 3. Получение несуществующего ключа
    print("\n3. Попытка получить несуществующий ключ:")
    try:
        value = table[12345]
    except KeyError as e:
        print(f"   ✓ Перехвачено: {e}")
    
    # 4. Добавление дубликата ключа
    print("\n4. Попытка добавить дубликат ключа:")
    dataset_path = BASE_DIR / 'dataset'
    files = list(dataset_path.glob('*'))
    
    if files:
        try:
            file_path = files[0]
            io_obj = choose_io_class(str(file_path))
            io_obj.read(str(file_path))
            key = coder.calc_sum(io_obj)
            
            table[key] = io_obj
            print(f"   Добавлен ключ {key}")
            
            # Попытка добавить снова
            table[key] = io_obj
        except KeyError as e:
            print(f"   ✓ Перехвачено: {e}")
    
    # 5. Выход за границы данных
    print("\n5. Попытка получить пиксель за пределами изображения:")
    if files:
        try:
            io_obj = choose_io_class(str(files[0]))
            io_obj.read(str(files[0]))
            pixel = io_obj[999999]
        except IndexError as e:
            print(f"   ✓ Перехвачено: {e}")


def example_7_build_full_table():
    """Пример 7: Построение полной таблицы из dataset"""
    print("\n" + "=" * 60)
    print("ПРИМЕР 7: Построение полной хеш-таблицы")
    print("=" * 60)
    
    try:
        # Строим таблицу с разными политиками
        print("\nРежим: skip duplicates")
        table = build_hash_table(
            algorithm=1,
            duplicate_policy='skip'
        )
        
        print(f"\n✓ Таблица построена: {len(table)} уникальных записей")
        
        # Показываем первые 5 записей
        print("\nПервые 5 записей:")
        for i, (key, path) in enumerate(table.items()):
            if i >= 5:
                break
            print(f"  {key:6d} -> {Path(path).name}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    # Запускаем все примеры
    example_1_read_image()
    example_2_read_text_image()
    example_3_checksum_algorithms()
    example_4_hash_table_basic()
    example_5_auto_key_generation()
    example_6_exception_handling()
    example_7_build_full_table()
    
    print("\n" + "=" * 60)
    print("ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ")
    print("=" * 60)