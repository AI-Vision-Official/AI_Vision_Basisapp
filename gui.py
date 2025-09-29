# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.module_loader import load_modules, MODULES_DIR
import os
import textwrap

# Teksten per taal
TEXT = {
    "nl": {
        "tab_functions": "Functies",
        "tab_generator": "Module-generator",
        "tab_about": "Over",
        "make_module_label": "Maak een nieuwe module (.py) in de map 'modules/'",
        "module_name": "Module naam (zonder .py):",
        "module_desc": "Optionele omschrijving:",
        "btn_make": "Maak module",
        "btn_refresh": "Vernieuwen",
        "btn_close": "Afsluiten",
        "module_created": "Module gemaakt",
        "module_exists": "Bestand bestaat al. Overschrijven?",
        "invalid_name": "Gebruik alleen letters, cijfers en underscore, begin niet met een cijfer.",
        "fill_name": "Vul een module naam in."
    },
    "en": {
        "tab_functions": "Functions",
        "tab_generator": "Module generator",
        "tab_about": "About",
        "make_module_label": "Create a new module (.py) in the 'modules/' folder",
        "module_name": "Module name (without .py):",
        "module_desc": "Optional description:",
        "btn_make": "Create module",
        "btn_refresh": "Refresh",
        "btn_close": "Close",
        "module_created": "Module created",
        "module_exists": "File exists. Overwrite?",
        "invalid_name": "Use only letters, digits and underscore, don't start with a digit.",
        "fill_name": "Please enter a module name."
    }
}

def start_gui(app_name, app_version, author, locale="nl"):
    texts = TEXT.get(locale, TEXT["nl"])

    root = tk.Tk()
    root.title(f"{app_name} v{app_version}")
    root.geometry("750x520")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # TAB: Functies (automatisch geladen)
    tab_modules = ttk.Frame(notebook)
    notebook.add(tab_modules, text=texts["tab_functions"])

    # frame voor knoppen (scrollable)
    canvas = tk.Canvas(tab_modules)
    scrollbar = ttk.Scrollbar(tab_modules, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # TAB: Generator
    tab_gen = ttk.Frame(notebook)
    notebook.add(tab_gen, text=texts["tab_generator"])

    gen_label = ttk.Label(tab_gen, text=texts["make_module_label"], wraplength=600)
    gen_label.pack(pady=8)

    entry_frame = ttk.Frame(tab_gen)
    entry_frame.pack(pady=6)

    ttk.Label(entry_frame, text=texts["module_name"]).grid(row=0, column=0, sticky="w")
    module_name_var = tk.StringVar()
    ttk.Entry(entry_frame, textvariable=module_name_var, width=30).grid(row=0, column=1, padx=6)

    ttk.Label(entry_frame, text=texts["module_desc"]).grid(row=1, column=0, sticky="w")
    desc_var = tk.StringVar()
    ttk.Entry(entry_frame, textvariable=desc_var, width=50).grid(row=1, column=1, padx=6)

    def create_module():
        name = module_name_var.get().strip()
        if not name:
            messagebox.showwarning("Error", texts["fill_name"])
            return
        # simple name validation
        if not name.isidentifier():
            messagebox.showwarning("Error", texts["invalid_name"])
            return
        path = os.path.join(MODULES_DIR, f"{name}.py")
        if os.path.exists(path):
            if not messagebox.askyesno("Exists", texts["module_exists"]):
                return
        desc = desc_var.get().strip()
        template = MODULE_TEMPLATE.format(module_name=name, description=desc)
        try:
            os.makedirs(MODULES_DIR, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(template)
            messagebox.showinfo(texts["module_created"], f"{name}.py")
            refresh_modules_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create module: {e}")

    ttk.Button(tab_gen, text=texts["btn_make"], command=create_module).pack(pady=6)

    # TAB: Over
    tab_over = ttk.Frame(notebook)
    notebook.add(tab_over, text=texts["tab_about"])
    about_text = f"{app_name} v{app_version}\n{author}\n\nModulaire EXE-bouwkit.\nPlaats .py-bestanden in modules/ met een run() functie."
    if locale == "en":
        about_text = f"{app_name} v{app_version}\n{author}\n\nModular EXE builder kit.\nPlace .py files in modules/ with a run() function."
    ttk.Label(tab_over, text=about_text, wraplength=600, justify="center").pack(expand=True)

    # Onderin knoppen: Vernieuwen en Afsluiten
    bottom = ttk.Frame(root)
    bottom.pack(fill="x", pady=6)

    def refresh_modules_ui():
        for child in scroll_frame.winfo_children():
            child.destroy()
        modules = load_modules()
        for name, func in modules.items():
            def make_cmd(f):
                def _cmd():
                    try:
                        f()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                return _cmd
            b = ttk.Button(scroll_frame, text=name, width=48, command=make_cmd(func))
            b.pack(pady=4, padx=6)
        count_lbl.config(text=f"Modules loaded: {len(modules)}" if locale == "en" else f"Modules geladen: {len(modules)}")

    ttk.Button(bottom, text=texts["btn_refresh"], command=refresh_modules_ui).pack(side="left", padx=8)
    count_lbl = ttk.Label(bottom, text="Modules geladen: 0")
    count_lbl.pack(side="left")
    ttk.Button(bottom, text=texts["btn_close"], command=root.destroy).pack(side="right", padx=8)

    # ensure modules dir exists and load
    os.makedirs(MODULES_DIR, exist_ok=True)
    refresh_modules_ui()
    root.mainloop()


# Bilingual module template (NL + EN fallback)
MODULE_TEMPLATE = textwrap.dedent("""\
    # Module: {module_name}.py
    # {description}

    MODULE_NAME = "{module_name}"

    def run():
        \"\"\"Hoofdfunctie van de module.
        Dit wordt aangeroepen door de main app (console en GUI).
        Pas deze functie aan met je eigen logica.
        \"\"\"
        # Try GUI message first (works when GUI is open), otherwise fallback to console (NL/EN)
        try:
            from tkinter import messagebox
            messagebox.showinfo("Module {module_name}", "Module {module_name} is succesvol uitgevoerd.\\nModule {module_name} executed successfully.")
        except Exception:
            print("Module {module_name} uitgevoerd. / executed.")
""")
