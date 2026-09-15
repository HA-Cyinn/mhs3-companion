# MHS3 Companion — Python

Prototype de compagnon mobile-first pour Monster Hunter Stories 3.

## Architecture

- **Une seule fenêtre** : les écrans sont des `CTkFrame`, aucune popup pour naviguer.
- **`monsters.json`** : données issues du tableau Game8 fourni.
- **`Monster`** : modèle métier qui lit les données JSON.
- **`counters.py`** : règle universelle Power → Speed → Technical → Power.
- **UI** : accueil, détail monstre et règles dans la même fenêtre.

Le JSON contient actuellement 131 entrées de monstres et leurs patterns d'attaque disponibles dans la source fournie. Les valeurs `Unknown` présentes dans la source sont conservées comme telles plutôt que devinées.

## Lancer

```powershell
py -m venv .venv
.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.venv\\Scripts\\python.exe app.py
```

## Tests

```powershell
.venv\\Scripts\\python.exe -m pytest -q
```
