import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os

def загрузить_документы_из_excel():
    """Загрузка данных из Excel файла"""
    # Указываем абсолютный путь к файлу
    путь_к_файлу = r"C:\Git\StrihKOD\документы.xlsx"
    
    try:
        # Проверка существования файла
        if not os.path.exists(путь_к_файлу):
            messagebox.showerror("Ошибка", f"Файл не найден по пути:\n{путь_к_файлу}")
            return None
            
        df = pd.read_excel(путь_к_файлу)
        return df[['Document Name', 'Document ID']]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки файла Excel:\n{str(e)}")
        return None

def создать_штрихкод(данные, имя_файла='штрихкод'):
    """Генерация штрих-кода"""
    try:
        код = Code128(данные, writer=ImageWriter())
        путь_сохранения = код.save(имя_файла)
        return путь_сохранения
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка генерации штрих-кода: {str(e)}")
        return None

def при_генерации():
    """Обработчик нажатия кнопки 'Создать'"""
    название_документа = выпадающий_список.get()
    телефон = поле_телефона.get()
    
    if not название_документа or not телефон:
        messagebox.showwarning("Внимание", "Выберите документ и введите номер телефона")
        return
    
    if not телефон.isdigit() or len(телефон) != 11:
        messagebox.showwarning("Внимание", "Номер телефона должен содержать ровно 11 цифр")
        return
    
    id_документа = документы[документы['Document Name'] == название_документа]['Document ID'].values
    if len(id_документа) == 0:
        messagebox.showwarning("Внимание", "ID документа не найден")
        return
    
    данные_штрихкода = f"{id_документа[0]}-{телефон}"
    путь_сохранения = создать_штрихкод(данные_штрихкода)
    
    if путь_сохранения:
        messagebox.showinfo("Успех", f"Штрих-код создан:\n{os.path.abspath(путь_сохранения)}")

# Настройка графического интерфейса
окно = tk.Tk()
окно.title("Генератор штрих-кодов для документов")

# Загрузка документов
документы = загрузить_документы_из_excel()
if документы is None:
    окно.destroy()
    exit()

# Выпадающий список с документами
ttk.Label(окно, text="Выберите документ:").grid(row=0, column=0, padx=10, pady=5)
выпадающий_список = ttk.Combobox(окно, values=документы['Document Name'].tolist())
выпадающий_список.grid(row=0, column=1, padx=10, pady=5)

# Поле ввода телефона
ttk.Label(окно, text="Введите номер телефона:").grid(row=1, column=0, padx=10, pady=5)
поле_телефона = ttk.Entry(окно)
поле_телефона.grid(row=1, column=1, padx=10, pady=5)

# Кнопка генерации
кнопка_генерации = ttk.Button(окно, text="Создать штрих-код", command=при_генерации)
кнопка_генерации.grid(row=2, column=0, columnspan=2, pady=10)

окно.mainloop()