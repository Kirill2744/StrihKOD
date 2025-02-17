#Библиотеки
import os
import cv2
from pyzbar import pyzbar
from barcode import Code128
from barcode.writer import ImageWriter
from openpyxl import Workbook, load_workbook

# Функция для генерации штрих-кода
def generate_barcode(data, filename):
    code = Code128(data, writer=ImageWriter())
    code.save(filename, options={"write_text": False})
    print(f"Штрих-код сохранен в файл: {filename}.png")

# Функция для сканирования штрих-кода
def scan_barcode():
    # Захват видео с камеры
    cap = cv2.VideoCapture(0)

    while True:
        # Чтение кадра
        ret, frame = cap.read()

        # Поиск штрих-кодов в кадре
        barcodes = pyzbar.decode(frame)

        # Если найден штрих-код
        if barcodes:
            for barcode in barcodes:
                # Извлечение данных
                barcode_data = barcode.data.decode("utf-8")
                print(f"Сканировано: {barcode_data}")

                # Остановка видео
                cap.release()
                cv2.destroyAllWindows()

                return barcode_data

        # Отображение кадра
        cv2.imshow("Сканирование штрих-кода", frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()

# Функция для записи данных в Excel
def write_to_excel(filename, phone_number, document_name):
    # Проверка существования файла
    if os.path.exists(filename):
        workbook = load_workbook(filename)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Номер телефона", "Название документа"])  # Заголовки

    # Добавление данных
    sheet.append([phone_number, document_name])

    # Сохранение файла
    workbook.save(filename)
    print(f"Данные добавлены в файл: {filename}")

# Основной код
if __name__ == "__main__":
    # Генерация штрих-кода
    phone_number = "+79123456789"
    document_name = "Договор оказания услуг"
    barcode_data = f"{phone_number}|{document_name}"  # Формат данных
    generate_barcode(barcode_data, "barcode_temp")

    # Сканирование штрих-кода
    print("Наведите камеру на штрих-код...")
    scanned_data = scan_barcode()

    # Разделение данных
    if scanned_data:
        scanned_phone, scanned_document = scanned_data.split("|")

        # Запись в Excel
        write_to_excel("barcode_data.xlsx", scanned_phone, scanned_document)
    else:
        print("Штрих-код не был сканирован.")