import os
import sys
import logging
import tkinter
from tkinter import *
from tkinter import ttk, StringVar
from pprint import pprint
from scrapli import Scrapli
#from NetDevConfigurator.config import Config
from modules.db import *
from modules.ssh_connect import ssh_connect
from modules.http_connect import http_connect

def main():
    root = Tk()
    root.title('Net Device Configurator')
    root.geometry('640x480')
    canvas = Canvas(root, width=640, height=480)
    canvas.pack(anchor=CENTER, expand=1)

    combo_label = ttk.Label(canvas, text="Manufacture:")
    combo_label.place(x=50, y=50)

    def get_selected_value():
        selected = selected_man.get()
        print(f"Selected value: {selected}")

    selected_man = tkinter.StringVar()
    combo = ttk.Combobox(canvas, textvariable=selected_man, values=import_man())
    combo.place(x=50, y=70)

    combo_label = ttk.Label(canvas, text="Model:")
    combo_label.place(x=50, y=100)

    combo = ttk.Combobox(canvas, values=import_model())
    combo.place(x=50, y=120)

    def get_entry_value():
        entry_value = certName.get()
        print(entry_value)

    certName_label = ttk.Label(canvas, text="Name cert:")
    certName_label.place(x=50, y=150)

    certName = ttk.Entry(canvas)
    certName.place(x=50, y=170)

    def btnUpd_click():
        get_entry_value()

    def btnConf_click():
        ssh_connect()

    btnUpd = ttk.Button(canvas, text="Update", command=btnUpd_click)
    canvas.create_window(50, 400, anchor=NW, window=btnUpd, width=100, height=40)
    btnConf = ttk.Button(text="Configure",command=btnConf_click)
    canvas.create_window(200, 400, anchor=NW, window=btnConf, width=100, height=40)

    root.mainloop()

if __name__ == "__main__":
    main()
