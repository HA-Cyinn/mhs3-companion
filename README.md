# MHS3 Companion — Python

Prototype de compagnon mobile-first pour Monster Hunter Stories 3.

> Projet de fan non officiel. Données et images : [Game8](https://game8.co/games/Monster-Hunter-Stories-3). Monster Hunter Stories 3 © CAPCOM.

## Architecture

- **Une seule fenêtre** : les écrans sont des `CTkFrame`, aucune popup pour naviguer.
- **`monsters.json`** : données issues du tableau Game8 fourni.
- **`Monster`** : modèle métier qui lit les données JSON.
- **`counters.py`** : règle universelle Power → Speed → Technical → Power.
- **UI** : accueil, détail monstre et règles dans la même fenêtre.

Le JSON contient actuellement 131 entrées de monstres et leurs patterns d'attaque disponibles dans la source fournie. Les valeurs `Unknown` présentes dans la source sont conservées comme telles plutôt que devinées.

## Lancer

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

## Version mobile (PWA)

Le dossier `web/` contient un prototype installable sur téléphone, en HTML/CSS/JS sans dépendance, utilisable hors ligne (service worker).

```powershell
python scripts\build_web.py          # régénère web/data.json et web/img/ depuis app/data
python -m http.server 8765 --directory web
```

Ouvre ensuite `http://<ip-du-pc>:8765/` depuis le téléphone (même Wi-Fi), puis « Ajouter à l'écran d'accueil ». Pour la mise en ligne, héberge `web/` en HTTPS (GitHub Pages, Netlify…), et incrémente `VERSION` dans `web/sw.js` après chaque régénération.

## Tests

```powershell
.venv\Scripts\python.exe -m pytest -q
```
