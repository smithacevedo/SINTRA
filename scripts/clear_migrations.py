import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
deleted_files = []

for root, dirs, files in os.walk(BASE_DIR):
    # Saltar entornos virtuales y dependencias
    if 'env' in root or 'venv' in root or 'site-packages' in root:
        continue

    if "migrations" in dirs:
        migrations_path = os.path.join(root, "migrations")
        for file in os.listdir(migrations_path):
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(migrations_path, file)
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"Eliminado: {file_path}")

print(f"\n Se eliminaron {len(deleted_files)} archivos de migraciones (sin borrar __init__.py).")