import sys
import os

# ===== CONFIGURATIE =====
APP_NAME = "MijnProject"
APP_VERSION = "1.0.0"
AUTHOR = "Brigitte Schrijvers"

def main():
    print(f"Welkom bij {APP_NAME} v{APP_VERSION} door {AUTHOR}")
    print("Dit is een basis EXE-template. Voeg hier je eigen code toe.")
    print("Kies een optie:")
    print("1. Hallo wereld")
    print("2. Toon bestandslocatie")
    print("3. Afsluiten")

    keuze = input("Maak een keuze (1-3): ").strip()

    if keuze == "1":
        print("Hallo wereld!")
    elif keuze == "2":
        print("Dit programma draait vanaf:", os.path.abspath(sys.argv[0]))
    elif keuze == "3":
        print("Tot ziens!")
        sys.exit(0)
    else:
        print("Ongeldige keuze!")

if __name__ == "__main__":
    main()
    input("\nDruk op Enter om af te sluiten...")
