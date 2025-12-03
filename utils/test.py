import os
from pathlib import Path
from .io.io_base import ImageData, TextImageData
from .checksum.cm_base import CMAlg1, CMAlg2
from .hash_data.hash_base import HashBase

# Определяем базовую директорию проекта (родитель папки utils)
BASE_DIR = Path(__file__).resolve().parent.parent


def choose_io_class(filepath: str):
    """
    Выбрать класс для чтения файла на основе расширения.
    
    Args:
        filepath: Путь к файлу
    
    Returns:
        Экземпляр класса IODataBase (ImageData или TextImageData)
    
    Raises:
        ValueError: Если расширение файла не поддерживается
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext in ('.png', '.jpg', '.jpeg'):
        return ImageData()
    elif ext == '.txt':
        return TextImageData()
    else:
        raise ValueError(f'Unsupported file extension: {ext}. Supported: .png, .jpg, .jpeg, .txt')


def build_hash_table(
    dataset_dir: str = None,
    output_path: str = None,
    algorithm: int = 1,
    duplicate_policy: str = 'skip'
):
    """
    Построить хеш-таблицу уникальных данных из директории dataset.
    
    Args:
        dataset_dir: Путь к папке с данными (по умолчанию BASE_DIR/dataset)
        output_path: Путь для сохранения JSON (по умолчанию BASE_DIR/output/hash_table.json)
        algorithm: Алгоритм контрольной суммы (1 или 2, по умолчанию 1)
        duplicate_policy: Политика обработки дубликатов:
            - 'skip': пропустить дубликат с предупреждением (по умолчанию)
            - 'overwrite': перезаписать существующий элемент
            - 'error': выбросить исключение
    
    Returns:
        HashBase: Построенная хеш-таблица
    
    Raises:
        FileNotFoundError: Если директория dataset не найдена
        ValueError: Если указан неверный алгоритм или политика дубликатов
    """
    # Установка путей по умолчанию
    if dataset_dir is None:
        dataset_dir = str(BASE_DIR / 'dataset')
    if output_path is None:
        output_path = str(BASE_DIR / 'output' / 'hash_table.json')
    
    # Проверка политики дубликатов
    if duplicate_policy not in ('skip', 'overwrite', 'error'):
        raise ValueError(f"Invalid duplicate_policy: {duplicate_policy}. Must be 'skip', 'overwrite', or 'error'")
    
    # Выбор алгоритма
    if algorithm == 1:
        coder = CMAlg1()
        print(f'Using Algorithm 1 (4x4 patch-based checksum)')
    elif algorithm == 2:
        coder = CMAlg2()
        print(f'Using Algorithm 2 (mean intensity checksum)')
    else:
        raise ValueError(f'Invalid algorithm: {algorithm}. Must be 1 or 2')
    
    table = HashBase(coder)
    
    # Проверка существования директории
    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        raise FileNotFoundError(f'Dataset directory not found: {dataset_dir}')
    if not dataset_path.is_dir():
        raise ValueError(f'Path is not a directory: {dataset_dir}')
    
    # Получаем список файлов
    files = sorted([f for f in dataset_path.iterdir() if f.is_file()])
    
    if not files:
        print(f'Warning: No files found in {dataset_dir}')
        return table
    
    print(f'Found {len(files)} files in {dataset_dir}')
    print('-' * 60)
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in files:
        try:
            # Выбираем класс для чтения файла
            io_obj = choose_io_class(str(file_path))
            
            # Читаем данные
            io_obj.read(str(file_path))
            
            # Вычисляем контрольную сумму
            key = coder.calc_sum(io_obj)
            
            # Обрабатываем дубликаты
            if key in table:
                existing_path = table[key]
                
                if duplicate_policy == 'skip':
                    print(f'⚠️  DUPLICATE: key={key} for {file_path.name}')
                    print(f'   Existing: {Path(existing_path).name} — skipping new file')
                    skipped_count += 1
                    continue
                    
                elif duplicate_policy == 'overwrite':
                    print(f'⚠️  DUPLICATE: key={key} for {file_path.name}')
                    print(f'   Overwriting: {Path(existing_path).name}')
                    del table[key]  # Удаляем старую запись
                    
                elif duplicate_policy == 'error':
                    raise KeyError(
                        f'Duplicate key {key} found!\n'
                        f'Existing file: {existing_path}\n'
                        f'New file: {file_path}'
                    )
            
            # Добавляем в таблицу (используем вычисленный ключ)
            table[key] = io_obj
            print(f'✓ Added: key={key:6d} <- {file_path.name}')
            processed_count += 1
            
        except ValueError as e:
            print(f'✗ ERROR processing {file_path.name}: {e}')
            error_count += 1
        except IOError as e:
            print(f'✗ IO ERROR processing {file_path.name}: {e}')
            error_count += 1
        except Exception as e:
            print(f'✗ UNEXPECTED ERROR processing {file_path.name}: {type(e).__name__}: {e}')
            error_count += 1
    
    # Итоговая статистика
    print('-' * 60)
    print(f'Processing complete:')
    print(f'  Successfully processed: {processed_count}')
    print(f'  Skipped (duplicates):   {skipped_count}')
    print(f'  Errors:                 {error_count}')
    print(f'  Total unique entries:   {len(table)}')
    
    # Сохраняем результат
    try:
        saved_path = table.json_save(output_path)
        print(f'\n✓ Hash table saved to: {saved_path}')
    except Exception as e:
        print(f'\n✗ Failed to save hash table: {e}')
        raise
    
    return table

if __name__ == "__main__":
    # Запуск с параметрами по умолчанию
    try:
        table = build_hash_table(
            algorithm=1,  # Используем алгоритм 1
            duplicate_policy='skip'  # Пропускаем дубликаты
        )
        print(f'\n✓ Successfully built hash table with {len(table)} unique entries')
    except Exception as e:
        print(f'\n✗ Failed to build hash table: {e}')
        raise
