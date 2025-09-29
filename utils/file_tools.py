import os

def list_files(directory="."):
    """Geef een lijst van bestanden in de opgegeven map."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        return []
