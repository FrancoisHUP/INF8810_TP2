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
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```
 
> **_NOTE:_** Par default, le mot de passe et nom d'utilisateur sont "neo4j"

## 4. Importer les données dans Neo4j

Cette opération prend un certain temps (2h+)

```bash
$ python utils/import_data_neo4j.py
```

```
Starting data imporing process...
=== Connected as user : neo4j ===

=== File Summary ===
Games file: data_csv/games_data_bins.csv, Rows: 1854
Users file: data_csv/users_data.csv, Rows: 71504
User-Game Relationships file: data_csv/users_games.csv, Rows: 2643793
Reviews file: data_csv/aus_reviews.csv, Rows: 53533
=====================
Loading games...
Games Progress: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1854/1854 [00:04<00:00, 406.63it/s] 
Loading users...
Users Progress: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 71504/71504 [00:57<00:00, 1235.17it/s] 
Loading user-game relationships...
Relationships Progress: 100%|████████████████████████████████████████████████████████████████████████████████████████████| 2643793/2643793 [2:15:11<00:00, 325.92it/s] 
Loading reviews...
Reviews Progress: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 53533/53533 [02:57<00:00, 302.32it/s]

=== Sample Games ===
Game ID: 10, Name: Counter-Strike
Game ID: 50, Name: Half-Life: Opposing Force
Game ID: 70, Name: Half-Life
Game ID: 130, Name: Half-Life: Blue Shift
Game ID: 300, Name: Day of Defeat: Source

=== Sample Users ===
User ID: 76561197970982479
User ID: js41637
User ID: evcentric
User ID: Riot-Punch
User ID: doctr

=== Sample Reviews ===
User ID: Bennysaputra, Game ID: 10, Review: Cool game
User ID: 76561198040188061, Game ID: 10, Review: this game is the 1# online action game is awesome, it's better than Team fortress games and other mutiplit-player games
User ID: mayshowganmore, Game ID: 10, Review: THE BEST FPS GAME!!!!!
User ID: BestinTheWorldThund3r, Game ID: 10, Review: One of the best childhood games i have ever played! 10/10 !
User ID: apex124, Game ID: 10, Review: Que decir de este gran juego?? Comence a jugarlo alla por 2002, y he vuelto a jugarlo ahora, y me satisface tanto como antes.   

=== Metrics Report ===
Games added: 1854
Users added: 71504
Relationships added: 2643793
Reviews added: 53533
======================
Data successfully loaded into Neo4j!
```


