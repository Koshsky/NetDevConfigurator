# from tkinter import Tk, PhotoImage

# root = Tk()
# root.title("Images and Icons")
# icon = PhotoImage(file="images/Icon.png")
# root.tk.call("wm", "iconphoto", root._w, icon)
# root.geometry("400x400")
# root.mainloop()

from utils import find_most_recent_file

if __name__ == "__main__":
    print(find_most_recent_file("/srv/tftp/firmware", "*"))
