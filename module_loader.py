# utils/module_loader.py
import importlib
import os
import sys

MODULES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

def safe_import_module(module_name: str):
    try:
        if module_name in globals():
            mod = importlib.reload(globals()[module_name])
        else:
            mod = importlib.import_module(module_name)
        globals()[module_name] = mod
        return mod, None
    except Exception as e:
        return None, e

def load_modules():
    found = {}
    if not os.path.isdir(MODULES_DIR):
        return found
    for entry in os.listdir(MODULES_DIR):
        if entry.startswith("_"):
            continue
        if entry.endswith(".py"):
            name = entry[:-3]
            mod, err = safe_import_module(name)
            if mod and hasattr(mod, "run") and callable(getattr(mod, "run")):
                display = getattr(mod, "MODULE_NAME", name)
                found[display] = getattr(mod, "run")
            else:
                def make_err_func(n=name, e=err):
                    def _err():
                        raise RuntimeError(f"Module '{n}' laadde niet goed: {e}")
                    return _err
                found[name] = make_err_func()
    return found
