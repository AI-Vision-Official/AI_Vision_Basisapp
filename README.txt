MijnBasisApp - Modulaire EXE bouwkit
===================================

Snelstart:
1. Plaats de map op je PC.
2. Zorg dat Python 3.10+ geïnstalleerd is (Windows).
3. Open terminal in de projectmap.

Start app:
> python main.py

Kies GUI of Console.
Maak nieuwe modules:
- Handmatig: voeg een .py bestand toe in modules/ met een callable run() functie.
- Of gebruik de Module-generator in de GUI (tab 'Module-generator').

Maak EXE:
> pip install pyinstaller
> pyinstaller --onefile --name=MijnBasisApp main.py

De exe komt in /dist/MijnBasisApp.exe

Auteur: Brigitte Schrijvers en ChatGPTv5
