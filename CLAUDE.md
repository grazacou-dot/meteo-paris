Stack : Python 3, API open-meteo (sans clé), HTML/CSS/JS vanilla

Structure :
- meteo.py (collecte)
- meteo.json (données)
- dashboard.html (affichage)
- requirements.txt

Villes suivies : Paris et Lyon

Pas de framework frontend, pas de base de données

Pour ajouter une ville : ajouter ses coordonnées dans le dictionnaire CITIES dans meteo.py

Lancer le dashboard : python -m http.server 8080 puis ouvrir localhost:8080/dashboard.html