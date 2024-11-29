import tkinter as tk
from tkinter import ttk
import psycopg2

class AddTab:
    def __init__(self, parent, app):
        self.frame = ttk.Frame(parent)
        self.app = app
        self.create_widgets()
        self.frame.pack(padx=10, pady=10)

    def create_widgets(self):
        # Первая строка
        self.label1 = ttk.Label(self.frame, text="company")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.name1 = ttk.Label(self.frame, text="name:")
        self.name1.grid(row=0, column=1, padx=5, pady=5)

        self.field1 = ttk.Entry(self.frame)
        self.field1.grid(row=0, column=2, padx=5, pady=5)

        self.button1 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 1"))
        self.button1.grid(row=0, column=3, padx=5, pady=5)

        # Вторая строка
        self.label3 = ttk.Label(self.frame, text="firmware")
        self.label3.grid(row=1, column=0, padx=5, pady=5)

        self.name2 = ttk.Label(self.frame, text="name:")
        self.name2.grid(row=1, column=1, padx=5, pady=5)

        self.field2 = ttk.Entry(self.frame)
        self.field2.grid(row=1, column=2, padx=5, pady=5)

        self.button2 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 2"))
        self.button2.grid(row=1, column=3, padx=5, pady=5)

        # третий блок
        self.device_label = ttk.Label(self.frame, text="device")
        self.device_label.grid(row=2, column=0, padx=5, pady=5)

        self.name3 = ttk.Label(self.frame, text="name")
        self.name3.grid(row=2, column=1, padx=5, pady=5)
        self.field2 = ttk.Entry(self.frame)
        self.field2.grid(row=2, column=2, padx=5, pady=5)

        self.name23 = ttk.Label(self.frame, text="company")
        self.name23.grid(row=3, column=1, padx=5, pady=5)
        self.field22 = ttk.Entry(self.frame)
        self.field22.grid(row=3, column=2, padx=5, pady=5)

        self.name13 = ttk.Label(self.frame, text="dev_type")
        self.name13.grid(row=4, column=1, padx=5, pady=5)
        self.field21 = ttk.Entry(self.frame)
        self.field21.grid(row=4, column=2, padx=5, pady=5)

        self.name321 = ttk.Label(self.frame, text="prim_conf")
        self.name321.grid(row=5, column=1, padx=5, pady=5)
        self.field212 = ttk.Entry(self.frame)
        self.field212.grid(row=5, column=2, padx=5, pady=5)

        self.name33 = ttk.Label(self.frame, text="port_num")
        self.name33.grid(row=6, column=1, padx=5, pady=5)
        self.field122 = ttk.Entry(self.frame)
        self.field122.grid(row=6, column=2, padx=5, pady=5)

        self.button234 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 3"))
        self.button234.grid(row=6, column=3, padx=5, pady=5)

    def on_button_click(self, button_name):
        print(f"{button_name} clicked")

# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    app = None  # Замените на ваш объект приложения, если необходимо
    data_tab = AddTab(root, app)
    root.mainloop()