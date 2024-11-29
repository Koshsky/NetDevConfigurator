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
        self.entity_1 = ttk.Label(self.frame, text="company")
        self.entity_1.grid(row=0, column=0, padx=5, pady=5)

        self.param_1_1 = ttk.Label(self.frame, text="name:")
        self.param_1_1.grid(row=0, column=1, padx=5, pady=5)
        self.field_1_1 = ttk.Entry(self.frame)
        self.field_1_1.grid(row=0, column=2, padx=5, pady=5)

        self.button_1 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 1"))
        self.button_1.grid(row=0, column=3, padx=5, pady=5)

        # Вторая строка
        self.entity_2 = ttk.Label(self.frame, text="firmware")
        self.entity_2.grid(row=1, column=0, padx=5, pady=5)

        self.param_2_1 = ttk.Label(self.frame, text="name:")
        self.param_2_1.grid(row=1, column=1, padx=5, pady=5)
        self.field_2_1 = ttk.Entry(self.frame)
        self.field_2_1.grid(row=1, column=2, padx=5, pady=5)

        self.button_2 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 2"))
        self.button_2.grid(row=1, column=3, padx=5, pady=5)

        # третий блок
        self.entity_3 = ttk.Label(self.frame, text="device")
        self.entity_3.grid(row=2, column=0, padx=5, pady=5)

        self.param_3_1 = ttk.Label(self.frame, text="name")
        self.param_3_1.grid(row=2, column=1, padx=5, pady=5)
        self.field_3_1 = ttk.Entry(self.frame)
        self.field_3_1.grid(row=2, column=2, padx=5, pady=5)

        self.param_3_2 = ttk.Label(self.frame, text="company")
        self.param_3_2.grid(row=3, column=1, padx=5, pady=5)
        self.field_3_2 = ttk.Entry(self.frame)
        self.field_3_2.grid(row=3, column=2, padx=5, pady=5)

        self.param_3_3 = ttk.Label(self.frame, text="dev_type")
        self.param_3_3.grid(row=4, column=1, padx=5, pady=5)
        self.field_3_3 = ttk.Entry(self.frame)
        self.field_3_3.grid(row=4, column=2, padx=5, pady=5)

        self.param_3_4 = ttk.Label(self.frame, text="prim_conf")
        self.param_3_4.grid(row=5, column=1, padx=5, pady=5)
        self.field_3_4 = ttk.Entry(self.frame)
        self.field_3_4.grid(row=5, column=2, padx=5, pady=5)

        self.param_3_5 = ttk.Label(self.frame, text="port_num")
        self.param_3_5.grid(row=6, column=1, padx=5, pady=5)
        self.field_3_5 = ttk.Entry(self.frame)
        self.field_3_5.grid(row=6, column=2, padx=5, pady=5)

        self.button_3 = tk.Button(self.frame, text="SUBMIT", command=lambda: self.on_button_click("SUBMIT 3"))
        self.button_3.grid(row=6, column=3, padx=5, pady=5)

    def on_button_click(self, button_name):
        print(f"{button_name} clicked")

# Пример использования
if __name__ == "__main__":
    root = tk.Tk()
    app = None  # Замените на ваш объект приложения, если необходимо
    data_tab = AddTab(root, app)
    root.mainloop()