from barcode import Code128
from barcode.writer import ImageWriter
import base64

# 1. Генерация штрих-кода ======================================================
def create_barcode(phone, document):
    # Кодируем документ в Base64
    encoded_doc = base64.b64encode(document.encode()).decode()
    
    # Формируем данные с разделителем
    data = f"{phone}||{encoded_doc}"
    
    # Создаем штрих-код
    code = Code128(data, writer=ImageWriter())
    code.save("document_barcode", options={"write_text": False})
    print("Штрих-код сохранен: document_barcode.png")

# 2. Пример использования =====================================================
if __name__ == "__main__":
    phone_number = "+79123456789"
    document_name = "Договор №12345"
    
    
    create_barcode(phone_number, document_name)