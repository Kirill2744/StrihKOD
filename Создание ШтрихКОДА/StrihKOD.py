import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os

class PhoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор штрих-кодов")
        
        # Инициализация данных
        self.documents = []
        self.load_excel_data()
        
        # Создание виджетов
        self.create_widgets()
        
        #Загрузка данных из Excel
    def load_excel_data(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл Excel с документами",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            if not file_path:
                raise FileNotFoundError
                
            df = pd.read_excel(file_path)
            
            # Проверка необходимых столбцов
            if 'ID' not in df.columns or 'Название документа' not in df.columns:
                raise ValueError("Файл должен содержать столбцы 'ID' и 'Название документа'")
            
            self.documents = list(zip(df['ID'], df['Название документа']))
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки файла: {str(e)}")
            self.documents = []

    def create_widgets(self):
        # Выбор документа
        ttk.Label(self.root, text="Выберите документ:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.doc_combobox = ttk.Combobox(self.root, state="readonly", width=40)
        self.doc_combobox.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        # Заполнение комбобокса данными из Excel
        if self.documents:
            display_names = [f"{doc[1]}" for doc in self.documents]
            self.doc_combobox['values'] = display_names
            self.doc_combobox.current(0)
        else:
            self.doc_combobox['state'] = 'disabled'
        
        # Ввод данных
        ttk.Label(self.root, text="Введите данные для штрих-кода:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.data_var = tk.StringVar()
        self.data_entry = ttk.Entry(self.root, textvariable=self.data_var, width=40)
        self.data_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        # Добавляем placeholder (подсказку)
        self.data_entry.insert(0, "Введите текст или номер")
        self.data_entry.config(foreground="grey")
        
        # Привязываем события для placeholder
        self.data_entry.bind("<FocusIn>", self.clear_placeholder)
        self.data_entry.bind("<FocusOut>", self.set_placeholder)
        
        # Кнопка генерации штрих-кода
        ttk.Button(self.root, text="Сгенерировать штрих-код", command=self.generate_barcode).grid(row=2, column=0, columnspan=2, pady=10)

# Удаляет placeholder при фокусе на поле ввода
    def clear_placeholder(self, event):
        if self.data_entry.get() == "Введите текст или номер":
            self.data_entry.delete(0, tk.END)
            self.data_entry.config(foreground="black")

# Устанавливает placeholder, если поле пустое
    def set_placeholder(self, event):
        if not self.data_entry.get():
            self.data_entry.insert(0, "Введите текст или номер")
            self.data_entry.config(foreground="grey")
# Генерация штрих-кода без текста под ним
    def generate_barcode(self):
        if not self.documents:
            messagebox.showerror("Ошибка", "Документы не загружены!")
            return
            
        selected_index = self.doc_combobox.current()
        doc_id, doc_name = self.documents[selected_index]
        
        # Получаем текст из поля ввода
        user_input = self.data_var.get()
        
        # Проверка, что поле не пустое и не содержит placeholder
        if not user_input or user_input == "Введите текст или номер":
            messagebox.showerror("Ошибка", "Введите данные для штрих-кода!")
            return
            
        # Создаем данные для штрих-кода
        barcode_data = f"{doc_id}-{user_input}"
        
        try:
            # Генерация штрих-кода
            code = barcode.get('code128', barcode_data, writer=ImageWriter())
            
            # Настройки для отключения текста под штрих-кодом
            options = {
                'write_text': False,  # Отключаем текст под штрих-кодом
                'module_height': 15.0,  # Высота штрих-кода
                'quiet_zone': 6.67,  # Отступы вокруг штрих-кода
            }
            
            # Сохраняем файл
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"barcode_{doc_id}"
            )
            
            if file_path:
                code.save(file_path, options=options)
                messagebox.showinfo("Успешно", 
                                  f"Штрих-код сохранен по пути:\n{file_path}\n"
                                  f"Данные: {barcode_data}")
                os.startfile(os.path.dirname(file_path))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x200")
    app = PhoneApp(root)
    root.mainloop()