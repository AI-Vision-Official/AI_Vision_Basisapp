import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# ====== Config ======
SCRIPT_FOLDER = "scripts"  # plaats hier je Python of batch scripts

# ====== Functies ======
def run_script(script_name):
    script_path = os.path.join(SCRIPT_FOLDER, script_name)
    if os.path.exists(script_path):
        try:
            # .py scripts via python, .bat via shell
            if script_name.endswith(".py"):
                subprocess.Popen(["python", script_path], shell=True)
            elif script_name.endswith(".bat") or script_name.endswith(".cmd"):
                subprocess.Popen([script_path], shell=True)
            else:
                messagebox.showinfo("Info", f"Can't run this file type: {script_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run {script_name}\n{e}")
    else:
        messagebox.showwarning("Not found", f"{script_name} does not exist in {SCRIPT_FOLDER}")

def get_script_list():
    if not os.path.exists(SCRIPT_FOLDER):
        os.makedirs(SCRIPT_FOLDER)
    return [f for f in os.listdir(SCRIPT_FOLDER) if f.endswith((".py",".bat",".cmd"))]

# ====== GUI ======
root = tk.Tk()
root.title("AI VISION Command Center")
root.geometry("700x500")

# Tab Control
tabControl = ttk.Notebook(root)
tab_utils = ttk.Frame(tabControl)
tab_scripts = ttk.Frame(tabControl)
tab_settings = ttk.Frame(tabControl)
tabControl.add(tab_utils, text='Utilities')
tabControl.add(tab_scripts, text='Scripts')
tabControl.add(tab_settings, text='Settings')
tabControl.pack(expand=1, fill="both")

# ---- Utilities Tab ----
lbl_utils = tk.Label(tab_utils, text="Utilities Section", font=("Arial",14))
lbl_utils.pack(pady=20)

# ---- Scripts Tab ----
lbl_scripts = tk.Label(tab_scripts, text="Available Scripts:", font=("Arial",12))
lbl_scripts.pack(pady=10)

script_listbox = tk.Listbox(tab_scripts, width=60, height=15)
script_listbox.pack(pady=5)

# Buttons
btn_run = tk.Button(tab_scripts, text="Run Selected Script", command=lambda: run_script(script_listbox.get(tk.ACTIVE)))
btn_refresh = tk.Button(tab_scripts, text="Refresh List", command=lambda: refresh_scripts())
btn_run.pack(pady=5)
btn_refresh.pack(pady=5)

def refresh_scripts():
    script_listbox.delete(0, tk.END)
    for script in get_script_list():
        script_listbox.insert(tk.END, script)

refresh_scripts()  # initial load

# ---- Settings Tab ----
lbl_settings = tk.Label(tab_settings, text="Settings Section", font=("Arial",14))
lbl_settings.pack(pady=20)
tk.Label(tab_settings, text="You can add configuration options here.").pack(pady=5)

root.mainloop()
