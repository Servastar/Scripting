# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, filedialog
from collections import defaultdict
import pymorphy3
import re
import sys
import os


class WordFrequencyAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор частоты слов")
        self.root.geometry("800x600")

        # Скрываем консоль (только для Windows)
        self.hide_console()

        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Инициализация морфологического анализатора
        self.morph = pymorphy3.MorphAnalyzer()

        # Создание интерфейса
        self.create_widgets()
        self.create_menu()

    def hide_console(self):
        """Скрывает консольное окно в Windows"""
        if os.name == 'nt':
            try:
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32')
                user32 = ctypes.WinDLL('user32')
                kernel32.GetConsoleWindow.restype = ctypes.c_void_p
                console_window = kernel32.GetConsoleWindow()
                if console_window:
                    user32.ShowWindow(console_window, 0)  # SW_HIDE
            except Exception:
                pass

    def on_close(self):
        """Обработчик закрытия приложения"""
        self.root.destroy()
        sys.exit(0)

    def create_widgets(self):
        """Создаёт элементы интерфейса"""
        # Ввод текста
        self.input_label = tk.Label(self.root, text="Введите текст для анализа:")
        self.input_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.input_text = scrolledtext.ScrolledText(
            self.root, width=80, height=15, wrap=tk.WORD, font=("Arial", 10)
        )
        self.input_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        # Кнопка анализа
        self.analyze_button = tk.Button(
            self.root,
            text="Проанализировать текст",
            command=self.analyze_text,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5,
        )
        self.analyze_button.pack(pady=10)

        # Вывод результатов
        self.output_label = tk.Label(self.root, text="Результаты анализа:")
        self.output_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.output_text = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=15,
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED,
        )
        self.output_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        # Контекстные меню
        self.create_context_menus()

    def create_menu(self):
        """Создаёт главное меню"""
        menubar = Menu(self.root)

        # Меню "Файл"
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Вставить текст", command=self.paste_text, accelerator="Ctrl+V")
        file_menu.add_command(label="Очистить всё", command=self.clear_all)
        file_menu.add_command(label="Сохранить результаты", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close, accelerator="Alt+F4")
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Правка"
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Копировать результаты", command=self.copy_results, accelerator="Ctrl+C")
        menubar.add_cascade(label="Правка", menu=edit_menu)

        # Меню "Справка"
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menubar)

        # Горячие клавиши
        self.root.bind("<Control-v>", lambda e: self.paste_text())
        self.root.bind("<Control-V>", lambda e: self.paste_text())
        self.root.bind("<Control-c>", lambda e: self.copy_results())
        self.root.bind("<Control-C>", lambda e: self.copy_results())

    def create_context_menus(self):
        """Создаёт контекстные меню"""
        # Для поля ввода
        self.input_context_menu = Menu(self.root, tearoff=0)
        self.input_context_menu.add_command(label="Вставить", command=self.paste_text)
        self.input_context_menu.add_command(label="Очистить", command=self.clear_input)
        self.input_text.bind("<Button-3>", self.show_input_context_menu)

        # Для поля вывода
        self.output_context_menu = Menu(self.root, tearoff=0)
        self.output_context_menu.add_command(label="Копировать", command=self.copy_results)
        self.output_text.bind("<Button-3>", self.show_output_context_menu)

    def show_input_context_menu(self, event):
        self.input_context_menu.tk_popup(event.x_root, event.y_root)

    def show_output_context_menu(self, event):
        self.output_context_menu.tk_popup(event.x_root, event.y_root)

    def show_about(self):
        about_text = """Анализатор частоты слов
Версия 1.0

Приложение представляет собой окно с двумя многострочными текстовыми полями, и одной кнопкой.
Приложение считает количество повторяющихся слов в тексте, вставленном в одно из текстовых полей, в другом текстовом поле появляется результат поиска, на первой строке наиболее часто встречающееся слово через тире количество раз, сколько оно употребляется в тексте, на последней строчке наиболее редкое слово. 
Приложение обрабатывает большие объемы текстовой информации, рассказы, небольшие произведения. 

Разработчик: Чубыкин М.И. группа: АСУбз-22-1"""
        messagebox.showinfo("О программе", about_text)

    def paste_text(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            messagebox.showwarning("Ошибка", "Буфер обмена пуст или содержит не текст")

    def copy_results(self):
        results = self.output_text.get("1.0", tk.END).strip()
        if results:
            self.root.clipboard_clear()
            self.root.clipboard_append(results)
            messagebox.showinfo("Успех", "Результаты скопированы в буфер обмена")
        else:
            messagebox.showwarning("Ошибка", "Нет результатов для копирования")

    def save_results(self):
        results = self.output_text.get("1.0", tk.END).strip()
        if not results:
            messagebox.showwarning("Ошибка", "Нет результатов для сохранения")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(results)
            messagebox.showinfo("Успех", "Результаты успешно сохранены!")

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)

    def clear_all(self):
        self.clear_input()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def normalize_word(self, word):
        clean_word = re.sub(r"[^\w]", "", word.lower())
        if not clean_word:
            return None
        parsed = self.morph.parse(clean_word)[0]
        return parsed.normal_form

    def analyze_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Ошибка", "Введите текст для анализа")
            return

        words = re.findall(r"\b[\w'-]+\b", text)
        word_counts = defaultdict(int)

        for word in words:
            normalized = self.normalize_word(word)
            if normalized:
                word_counts[normalized] += 1

        if not word_counts:
            self.show_result("Не найдено слов для анализа")
            return

        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]

        result = []
        result.append(f"САМОЕ ЧАСТОЕ СЛОВО: {sorted_words[0][0]} - {sorted_words[0][1]}")
        result.append("\nЧастота слов:\n")

        for word, count in sorted_words:
            result.append(f"{word} — {count}")

        result.append(f"\n\nСАМОЕ РЕДКОЕ СЛОВО: {sorted_words[-1][0]} - {sorted_words[-1][1]}")

        self.show_result("\n".join(result))

    def show_result(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordFrequencyAnalyzer(root)
    root.mainloop()