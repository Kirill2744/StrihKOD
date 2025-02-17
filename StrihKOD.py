#Библиотеки
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageFont, ImageDraw

# Данные для штрих-кода
phone_number = "+79123456789"
document_name = "Договор оказания услуг"

# Создаем штрих-код
code = Code128(phone_number, writer=ImageWriter())

# Сохраняем временное изображение без текста
temp_filename = "barcode_temp"
code.save(temp_filename, options={"write_text": False})

# Открываем изображение для добавления текста
img = Image.open(f"{temp_filename}.png")
draw = ImageDraw.Draw(img)

# Загружаем шрифт (укажите путь к вашему .ttf файлу с поддержкой кириллицы)
try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

# Текст для отображения
text = f"{phone_number}\n{document_name}"

# Рассчитываем размер текста
text_width, text_height = draw.textsize(text, font=font)

# Позиция текста: по центру внизу
x = (img.width - text_width) / 2
y = img.height - text_height - 10  # Отступ снизу 10 пикселей

# Добавляем текст
draw.text((x, y), text, font=font, fill="black")

# Сохраняем финальное изображение
img.save("barcode_with_text.png")

# Удаляем временный файл
import os
os.remove(f"{temp_filename}.png")

print("Штрих-код успешно создан: barcode_with_text.png")