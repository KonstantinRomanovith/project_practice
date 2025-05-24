import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from tkinter.scrolledtext import ScrolledText


class ModernTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Text Editor")
        self.root.geometry("1000x700")

        # Настройка стиля
        self.setup_style()

        # Текущие настройки шрифта
        self.current_font = "Segoe UI"
        self.current_size = 12

        # Создаем элементы интерфейса
        self.create_widgets()

        # Переменная для текущего файла
        self.current_file = None

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Настраиваем цвета для темной темы
        style.configure('.', background='#333333', foreground='white')
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='white')
        style.configure('TButton', background='#444444', foreground='white',
                        borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#555555')])
        style.configure('TMenubutton', background='#444444', foreground='white')
        style.configure('TCombobox', fieldbackground='#444444', foreground='white')

        # Стиль для текстового поля
        self.root.configure(bg='#333333')

    def create_widgets(self):
        # Главный контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель инструментов
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Кнопки файловых операций
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side=tk.LEFT)

        ttk.Button(btn_frame, text="📄 Новый", command=self.new_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📂 Открыть", command=self.open_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="💾 Сохранить", command=self.save_file, width=8).pack(side=tk.LEFT, padx=2)

        # Разделитель
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # Выбор шрифта
        font_frame = ttk.Frame(toolbar)
        font_frame.pack(side=tk.LEFT)

        ttk.Label(font_frame, text="Шрифт:").pack(side=tk.LEFT)

        self.font_family = tk.StringVar(value=self.current_font)
        font_names = sorted(font.families())
        font_menu = ttk.Combobox(font_frame, textvariable=self.font_family,
                                 values=font_names, width=20)
        font_menu.pack(side=tk.LEFT, padx=5)
        font_menu.bind('<<ComboboxSelected>>', self.update_font)

        ttk.Label(font_frame, text="Размер:").pack(side=tk.LEFT)

        self.font_size = tk.IntVar(value=self.current_size)
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36]
        size_menu = ttk.Combobox(font_frame, textvariable=self.font_size,
                                 values=sizes, width=4)
        size_menu.pack(side=tk.LEFT, padx=5)
        size_menu.bind('<<ComboboxSelected>>', self.update_font)

        # Текстовое поле с прокруткой
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        self.text_area = ScrolledText(text_frame, wrap=tk.WORD, undo=True,
                                      font=(self.current_font, self.current_size),
                                      bg='#252525', fg='white', insertbackground='white',
                                      selectbackground='#555555', selectforeground='white',
                                      padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Строка состояния
        self.status_bar = ttk.Label(main_frame, text="Готов", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Привязка событий
        self.text_area.bind('<KeyRelease>', self.update_status)

    def update_font(self, event=None):
        self.current_font = self.font_family.get()
        self.current_size = self.font_size.get()
        self.text_area.configure(font=(self.current_font, self.current_size))

    def update_status(self, event=None):
        text = self.text_area.get("1.0", tk.END)
        lines = text.count('\n')
        words = len(text.split())
        chars = len(text) - 1  # минус последний символ перевода строки
        self.status_bar.config(text=f"Строк: {lines} | Слов: {words} | Символов: {chars}")

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.status_bar.config(text="Создан новый документ")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", file.read())
                self.current_file = file_path
                self.status_bar.config(text=f"Открыт файл: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                self.status_bar.config(text=f"Файл сохранен: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                self.current_file = file_path
                self.status_bar.config(text=f"Файл сохранен как: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTextEditor(root)
    app.run()