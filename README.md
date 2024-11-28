# INF8810_TP2

## 1. Installez les bibliothèques Python
```bash
$ pip install -r requirements.txt
```

## 2. Installation neo4j

Assurez-vous d'avoir une version du logiciel [Neo4j installée](https://neo4j.com/download/) et en cours d'exécution sur votre machine. Vous devrez changer le mot de passe et nom de l'utilisateur dans le fichier ```.env``` à la racine du dossier. 

Pour tester si le logiciel est bien installé et activé :

```bash
$ python utils/check_neo4j_status.py 
```

## 3. Télécharger les données

Pour les données brutes (jeu de données original)
```bash
$ python utils/download_raw_data.py
```

Pour les données pré-traitées / données utilisées pour neo4j ([Google Drive](https://drive.google.com/drive/folders/11onNyuwrslBDdj1rIh6C6hPV_UAbWvye?usp=sharing)) : 
```bash
$ python utils/download_csv_data.py
```

Les données doivent être enregistrées dans le dossier "data_csv/"  
```md
INF8810_TP2/
├── data_csv/
│   ├── aus_reviews.csv
│   ├── games_names.csv
│   ├── user_game.csv
├── .env
```

Avec le fichier ```.env```
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=your_username  # by default "neo4j"
NEO4J_PASSWORD=your_password # by default "neo4j"
```

## 4. Importer les données dans Neo4j
```bash
$ python utils/import_data_neo4j.py
```


