# main.py
import sys
import os
from utils.module_loader import load_modules
import gui

APP_NAME = "MijnBasisApp"
APP_VERSION = "1.0.0"
AUTHOR = "Auteur: Brigitte Schrijvers en ChatGPTv5"

LOCALES = {
    "nl": {
        "choose_mode": "Kies een modus:",
        "console_mode": "1. Console-modus",
        "gui_mode": "2. Grafische modus",
        "choose_lang": "Kies een taal / Choose a language:",
        "lang_nl": "1. Nederlands",
        "lang_en": "2. English"
    },
    "en": {
        "choose_mode": "Choose a mode:",
        "console_mode": "1. Console mode",
        "gui_mode": "2. Graphical mode",
        "choose_lang": "Kies een taal / Choose a language:",
        "lang_nl": "1. Nederlands",
        "lang_en": "2. English"
    }
}

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def console_menu(locale):
    messages = LOCALES[locale]
    while True:
        clear_console()
        print(f"{APP_NAME} v{APP_VERSION} - {AUTHOR}")
        print("=" * 50)
        modules = load_modules()
        names = list(modules.keys())
        for i, name in enumerate(names, start=1):
            print(f"{i}. {name}")
        # localized labels
        if locale == "nl":
            print(f"{len(names)+1}. Vernieuwen")
            print(f"{len(names)+2}. Afsluiten")
        else:
            print(f"{len(names)+1}. Refresh modules")
            print(f"{len(names)+2}. Exit")

        keuze = input("\nMaak een keuze: ").strip()
        try:
            keuze_i = int(keuze)
            if keuze_i == len(names) + 1:
                # refresh: just loop, load_modules reads fresh next iteration
                continue
            if keuze_i == len(names) + 2:
                if locale == "nl":
                    print("Tot ziens!")
                else:
                    print("Goodbye!")
                sys.exit(0)
            func = list(modules.values())[keuze_i - 1]
            func()
        except Exception as e:
            if locale == "nl":
                print("Ongeldige keuze of fout tijdens uitvoeren:", e)
            else:
                print("Invalid choice or error during execution:", e)
            input("Druk op Enter om verder te gaan..." if locale == "nl" else "Press Enter to continue...")

if __name__ == "__main__":
    clear_console()
    # taalkeuze
    print("==============================================")
    print("Kies een taal / Choose a language:")
    print("1. Nederlands")
    print("2. English")
    lang_choice = input("\nMaak een keuze (1-2): ").strip()
    locale = "nl" if lang_choice == "1" else "en"

    messages = LOCALES[locale]
    clear_console()
    print(f"{APP_NAME} v{APP_VERSION} - {AUTHOR}")
    print("=" * 50)
    print(messages["choose_mode"])
    print(messages["console_mode"])
    print(messages["gui_mode"])
    keuze = input("\nMaak een keuze (1-2): ").strip()

    if keuze == "1":
        console_menu(locale)
    elif keuze == "2":
        gui.start_gui(APP_NAME, APP_VERSION, AUTHOR, locale)
    else:
        if locale == "nl":
            print("Ongeldige keuze!")
        else:
            print("Invalid choice!")
