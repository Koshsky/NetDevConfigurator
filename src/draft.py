import tkinter as tk

window = tk.Tk()
lbl_titles = [
    "Name",
    "Surname",
    "Address1",
    "Address2",
    "City",
    "Region",
    "Post index",
    "Country",
]
frame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5)
# TODO: это очень важно!!!
# -------------------------------------
frame.columnconfigure(list(range(8)), minsize=40, weight=1)
frame.rowconfigure(list(range(20)), minsize=20)
frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
# -------------------------------------
print(tk.BOTH)
for row in range(len(lbl_titles)):
    label = tk.Label(master=frame, text=f"{lbl_titles[row]}:")
    label.grid(column=0, row=row, sticky=tk.W + tk.E)
    entry = tk.Entry(master=frame)
    entry.grid(column=1, row=row, sticky=tk.W + tk.E)

window.mainloop()
