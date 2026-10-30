# MHS3 Companion — Web

Compagnon web installable (PWA), mobile-first, pour Monster Hunter Stories 3.

> Projet de fan non officiel. Données et images : [Game8](https://game8.co/games/Monster-Hunter-Stories-3). Monster Hunter Stories 3 © CAPCOM.

Le site est servi depuis `web/` et fonctionne hors ligne grâce à son service worker. Les fichiers sources des données et des images sont conservés dans `app/data/` ; le script Python de génération les transforme en ressources pour le site.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\build_web.py
.venv\Scripts\python.exe -m http.server 8765 --directory web
```

Ouvre ensuite `http://localhost:8765/` sur le PC ou `http://<ip-du-pc>:8765/` sur un téléphone connecté au même Wi-Fi. Pour installer l’application sur le téléphone, ouvre le site en HTTPS et choisis « Ajouter à l'écran d'accueil ». GitHub Pages déploie automatiquement le contenu de `web/` sur chaque push vers `main`.

Après une modification du code web ou des données, incrémente `VERSION` dans `web/sw.js` pour renouveler le cache des appareils.

## Tests

```powershell
.venv\Scripts\python.exe -m pip install pytest
.venv\Scripts\python.exe -m pytest -q
```
