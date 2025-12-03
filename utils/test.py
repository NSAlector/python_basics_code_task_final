from iom.io_image import IOImage
from checksum.cm_alg1 import CMAlgo1
from checksum.cm_alg2 import CMAlgo2
from hash_data.hash_base import HashBase


def main():
    # --- 1. Загружаем данные ---
    img = IOImage()
    img.read("../dataset/sar_1_gray.jpg")
    print("Размер:", len(img), "пикселей")
    print("Пиксель (10, 20):", img[10][20])




    # --- 2. Считаем контрольную сумма ---
    cm2 = CMAlgo2()
    cm1 = CMAlgo1()
    key1 = cm1.calc_sum(img)
    key2 = cm2.calc_sum(img)

    print("Checksum (algo1):", key1)
    print("Checksum (algo2):", key2)


    # --- 3. Добавляем в hash-таблицу ---
    htable = HashBase(key_coder=cm1)

    htable[key1] = img
    print("Записано:", htable[key1])

    htable[key1] = img


    # --- 4. Удаление ---
    #del htable[key1]

    # --- 5. Сохранение результата ---
    htable.json_save("../output/hash_table.json")

if __name__=="__main__":
    main()