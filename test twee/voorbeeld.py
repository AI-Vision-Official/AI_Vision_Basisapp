# modules/voorbeeld.py
MODULE_NAME = "Voorbeeld / Example"

def run():
    try:
        from tkinter import messagebox
        messagebox.showinfo("Voorbeeld / Example", "Dit is een voorbeeldmodule.\nThis is an example module.")
    except Exception:
        print("Voorbeeldmodule uitgevoerd. / Example module executed.")
