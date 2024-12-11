## Partie 1 : Données 



### Quelle est l'origine des données?
Les données que nous avons choisi d'utiliser sont celles des [notes attribuées par les utilisateurs de Steam pour différents jeux](https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data) ainsi que leur revue textuelle. Ces [revues](https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_user_reviews.json.gz) et ces [données de jeux](https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_users_items.json.gz) sont d'origine d'Australie.

### Quel est le contexte du jeu de données?
Les données sont celles des revues Steam comme celle-ci:![steam review](Sample_review.png "Steam Review")

La photo et le nom d'utilisateur a été enlevé mais est disponible dans le dataset que nous utiliserons. Ces revues sont faites sur la page du magasin de Steam qui fait de la vente en ligne  de jeux dématerialisés, de logiciels, de bandes son originales et de quelques produits physiques comme la Steam Deck et de matériel de réalité virtuelle. Tous les produits vendus sur la plateforme ont des revues ainsi qu'une note en pourcentage (bonne/mauvaises revues * 100) qui détermine son appréciation. Cela peut varier entre *Overwhelmingly Negative*, *Very Negative*, *Mostly Negative*, *Negative*, *Mixed*, *Mostly Positive*, *Positive*,  *Very Positive* et finalement *Overwhelmingly Positive*.
Les pondérations sont les suivantes:

```
%score  |   #reviews   |  rating  |   confidence

95 - 100 | 500+ reviews | positive | overwhelmingly
85 - 100 |  50+ reviews | positive | very
80 - 100 |  10+ reviews | positive | -
70 -  79 |  10+ reviews | positive | mostly
40 -  69 |  10+ reviews | mixed    | -
20 -  39 |  10+ reviews | negative | mostly
 0 -  19 |  10+ reviews | negative | -
 0 -  19 |  50+ reviews | negative | very
 0 -  19 | 500+ reviews | negative | overwhelmingly
 
 ```


### Prétraitement des données
Le prétraitement ainsi que la vérification des données se trouve dans [pretraitement_items.ipynb](pretraitement_items.ipynb). Pour collecter les informations que nous voulions, il a fallu nettoyer les sources de données et nous avons débuté par importer les fichiers JSON comme dictionnaires python puis les convertir en fichiers CSV pour utiliser avec Neo4J. Nos fichiers qui seront créés à partir des données de ``australian_users_items.json`` sont: *Games*, *User Lib* et *User Data*. Il est à noter que les détails de l'implémentation se retrouve dans [pretraitement_items.ipynb](pretraitement_items.ipynb).

#### Games
Pour ce fichier de prétraiement nous nous intéressont aux clées suivantes: `game_id` (id du jeu dans la base de données Steam), `name` (nom du jeu), `temps_total_joué` (temps total joué par tous les utilisateurs qui possèdent ce jeu) et `nombre_joueurs_joué`(nombre de joueurs différents ayant ce jeu et ayant joué). Il est à préciser que nous itérons sur tous les joueurs et ne comptabilisons que les joueurs ayant un temps de jeu supérieur à 0. Nous convertissons par la suite le dictionnaire en dataframe pour la sauvegarde en CSV. Nous simplifions également le temps de jeu en heures (il est normalement en minutes) pour réduire la taille du fichier et parce que la perte de temps de jeu dans l'étape d'arrondissement (1 minute jouée devient 1h, par exemple 61 minutes devient 2 heures) est dérisoire lorsque l'on parle de milliers d'heures comme c'est le cas pour `Counter-Strike: Global Offensive` avec ses `13086405` heures de jeu. Nous calculons aussi le temps médian d'un joueur sur chaque jeu afin de potentiellement utiliser cette mesure par la suite. Le tout est enregistré dans `./data_csv/games_data.csv` sur le Google Drive.

#### User Lib
Pour cette section nous nous intéressons à chaque paire *Joueur-Jeu* et comme pour *Games*, nous convertissons le temps de jeu en heures. Les clées qui nous intéressent cette fois sont: `user_id` (id du joueur), `game_id` (id du jeu), `playtime (hours)` (nombre d'heures que ce joueur a sur le jeu) et `active (bool)` (le joueur as-t-il joué au jeu dans les deux dernières semaine?). Suite aux calculs le fichier résultant est le `./data_csv/users_data.csv` sur le Google Drive.

#### User Data
Pour le *User Data*, nous voulions définir le joueur ou utilisateur avec ces clées: `user_id`, `games_count` (nombre de jeux possédés), `total_playtime` (temps de jeu total sur tous les jeux) et `most_played_game_id` (à quel jeu cet utilisateur as-t-il le plus joué). 

#### Calcul des Bins
Nous voulions nous donner une idée de la répartition du temps de jeu parmi la population de joueur et c'est le but des *Bins*. Il s'agit simplement d'une division en 5 de la population des joueurs et de leur temps de jeu moyen afin de pouvoir se faire une idée sur la communauté du jeu. Est-il abandonné rapidement ou possède une communauté de joueurs assidus? Nous trouvions l'exercice intéressant et potentiellement utile plus tard. Suite aux calculs le résultat est enregistré sur `./data_csv/games_data_bins.csv` dans le Google Drive.

#### Réduction des données
Nous avons décidé de réduire la taille de nos données afin de ne pas faire de traitements inutiles et par contraintes de stockage.
##### Games 
Pour cela nous avons retiré de la liste des jeux tous ceux qui ont moins de 100 propirétaires ainsi que les jeux dont le temps de jeu médian est plus petit ou égal à une heure (convertie). Cela vient éliminer 9124 jeux qui n'ont pas d'intérêt pour notre système. N'importe qui peut créer son jeu sur Steam moyennant une somme de 100$ et beaucoup de ces projets sont abandonnés. Nous sommes confiant que ces jeux ne nous serons pas utiles. 
##### User Lib
Nous avons les jeux concernés par l'étape précédente de *User Lib* même si l'utilisateur y a déjà joué.
##### User Reviews
Nous avons retiré les mauvais jeux des reviews de notre source de données afin de garder uniquement les reviews des jeux que nous allons utiliser.


## Partie 2 : Chargement dans neo4j 

### À NOTER
Toutes les instructions qui concernent nos opérations Neo4J se trouvent dans notre [README.md](README.md).

Le fichier [import_data_neo4j.py](import_data_neo4j.py) est le responsable du chargement dans Neo4J
### Quelles données chargez-vous dans neo4j?

Nous chargeons les 4 fichiers obtenus lors du prétraitement : 
* ``GAMES_FILE =  "data_csv/games_data_bins.csv"``
* ``USER_GAME_FILE = "data_csv/users_games.csv"``
* ``REVIEWS_FILE = "data_csv/aus_reviews.csv"``
* ``USER_FILE = "data_csv/users_data.csv"``


### Faites-vous des traitements/modifications lors du chargement?
Oui nous établissons des contraintes d'unicité pour les jeux et les utilisateurs. 

### Étapes suivies

#### Éxécution globale

L'éxécution de l'importation en entier se fait par le biais de cette commande (voir notre [README.md](README.md)):
```bash
$ python utils/import_data_neo4j.py
```

#### Métriques
Nous définissons des métriques qui seront utiles pour notre usage: `games_added`, `users_added`, `relationships_added` et `reviews_added`. Il est important de noter que les requêtes qui suivront dans les prochaines sections n'inclueront pas les métriques et se trouvent à la fin de celles-ci dans leurs fonction respectives. Voir [./utils/import_data_neo4j.py](./utils/import_data_neo4j.py) pour plus de précisions.

#### Chargement des jeux
La fonction `load_games` permet de charger les jeux à partir de `GAMES_FILE` et la requête est la suivante: 
```
MERGE (g:Game {game_id: $game_id})
    ON CREATE SET 
        g.name = $name,
        g.time_played = toInteger($time_played),
        g.player_count = toInteger($player_count),
        g.median_time_played = toInteger($median_time_played),
        g.max_bin_1 = toInteger($max_bin_1),
        g.max_bin_2 = toInteger($max_bin_2),
        g.max_bin_3 = toInteger($max_bin_3),
        g.max_bin_4 = toInteger($max_bin_4),
        g.max_bin_5 = toInteger($max_bin_5)
```
Nous avons les champs suivants: ``name`` (nom du jeu), ``time_played`` (temps de jeu de tous les joueurs), ``player_count`` (nombre de joueurs), ``median_time_played`` (temps de jeu médian), ``max_bin_x`` (heures de jeu du top 20% des joueurs). Si le jeu existe déjà le noeud n'est pas recréé.

#### Chargement des utilisateurs
Comme pour les jeux les utilisateurs ont leurs informations importées dans Neo4j mais par le biais du fichier `USERS_FILE` dans la fonction `load_users` et voici la requête:
```
MERGE (u:User {user_id: $user_id})
    ON CREATE SET 
        u.items_count = toInteger($items_count),
        u.played_games = toInteger($played_games),
        u.total_playtime = toInteger($total_playtime),
        u.most_played_game_id = $most_played_game_id
```
Nous avons les champs suivants: ``items_count`` (nombre de jeux possédés par le joueur), ``played_games`` (jeux dont le joueur a un temps de jeu positif), ``total_playtime`` (temps de jeu total) et ``most_played_game_id`` (jeu auquel il a le plus joué).

#### Chargement des relations Joueur-Jeu

La fonction `load_user_game_relationships` utilise le fichier `USER_GAME_FILE` et a pour but de modéliser les relations entre ces deux concepts. Les deux attributs qui seront établis dans cette étape sont: `playtime` et `active` qui sont des champs du fichier source grâce au prétraitement. Voici la requête:

```
MERGE (u:User {user_id: $user_id})
MERGE (g:Game {game_id: $game_id})
MERGE (u)-[r:PLAYS]->(g)
ON CREATE SET r.playtime = toInteger($playtime),
            r.active = $active
```
#### Chargement des avis (reviews)

La fonction `load_reviews` utilise comme paramètre le fichier `REVIEWS_FILE` et les champs résultants sont: `funny` (combien d'utilisateurs on trouvé l'avis amusant), `posted` (date de l'avis), `last_edited` (date de la dernière modification de l'avis), `helpful` (combien d'utilisateurs ont trouvé que l'avis était utile), `recommend` (indique s'il s'agit ou non d'une recommendation/avis positif) et `review` (le texte de l'avis). Voici la requête:
```
MERGE (u:User {user_id: $user_id})
MERGE (g:Game {game_id: $item_id})
MERGE (u)-[r:REVIEWS {funny: $funny, posted: $posted, 
                        last_edited: $last_edited, helpful: $helpful, 
                        recommend: $recommend, review: $review}]->(g)
```

## Partie 3 : Recommandation
Le fichier [./utils/neo4j_recommender.py](./utils/neo4j_recommender.py) contient tout le code de nos recommendations.
### Quelle recommandation proposez-vous?
Nous proposons trois recommendations: 

#### Recommendation des jeux basés sur le filtrage collaboratif
Voici notre requête:

```
    MATCH (target:User {user_id: $user_id})-[:PLAYS]->(g:Game)<-[:PLAYS]-(similar:User)
    WITH target, similar, COUNT(g) AS shared_games
    ORDER BY shared_games DESC
    LIMIT 10
    MATCH (similar)-[:PLAYS]->(recommended:Game)
    WHERE NOT (target)-[:PLAYS]->(recommended)
    RETURN recommended.game_id AS game_id, recommended.name AS name, COUNT(*) AS popularity
    ORDER BY popularity DESC, recommended.name
    LIMIT $top_n
```
La requête suit ces étapes :
* Correspondre à l'utilisateur cible et trouver les jeux auxquels il a joué.
* Identifier les utilisateurs similaires ayant joué aux mêmes jeux et compter les jeux partagés.
* Trier les utilisateurs similaires par nombre de jeux partagés.
* Limiter le nombre d'utilisateurs similaires (pour des raisons de performance).
* Trouver les jeux joués par les utilisateurs similaires.
* Exclure les jeux auxquels l'utilisateur cible a déjà joué.
* Retourner les jeux recommandés avec leur popularité et leurs noms.
* La popularité est calculée comme le nombre d'utilisateurs similaires ayant joué au jeu recommandé.
* Trier par popularité puis par ordre alphabétique.
* Limiter le nombre de recommandations.

#### Recommendation des jeux basés sur les habitudes de jeu de l'utilisateur
Voici notre requête:
```
MATCH (target:User {user_id: $user_id})-[:PLAYS]->(g:Game)
WITH target, avg(g.median_time_played) AS user_avg_time, avg(g.player_count) AS user_avg_players
MATCH (similar:Game)
WHERE NOT (target)-[:PLAYS]->(similar)
AND ABS(similar.median_time_played - user_avg_time) < 10
AND ABS(similar.player_count - user_avg_players) < 100
RETURN similar.game_id AS game_id, similar.name AS name,
    ABS(similar.median_time_played - user_avg_time) AS time_diff,
    ABS(similar.player_count - user_avg_players) AS player_diff
ORDER BY time_diff, player_diff
LIMIT $top_n
```

* Trouver l'utilisateur cible.
* Rechercher les jeux auxquels cet utilisateur a joué.
* Calculer la moyenne du temps médian de jeu (``user_avg_time``) et le nombre moyen de joueurs (``user_avg_players``) pour les jeux joués par l'utilisateur cible.
* Trouver les jeux similaires auxquels l'utilisateur cible n'a pas encore joué.
* Filtrer les jeux similaires pour s'assurer que :
    * La différence entre le temps médian de jeu du jeu similaire et la moyenne du temps de jeu de l'utilisateur cible est inférieure à 10.
    * La différence entre le nombre de joueurs du jeu similaire et la moyenne des joueurs de l'utilisateur cible est inférieure à 100.
* Retourner les recommandations de jeux similaires
* Trier les jeux similaires par différence de temps de jeu en ordre croissant, puis par différence de nombre de joueurs en ordre croissant.
* Limiter le nombre de recommandations retournées à une valeur donnée (``$top_n``).

#### Recommendation hybride
Il s'agit d'un mélange entre les deux solutions précédentes. Cette approche permet de trouver les jeux auxquels des utilisateurs ayant les mêmes intérêts jouent PUIS de filtrer ces résultats pour augmenter la pertinence. Voici notre requête: 
```
MATCH (target:User {user_id: $user_id})-[:PLAYS]->(g:Game)
WITH target, avg(g.median_time_played) AS user_avg_time, avg(g.player_count) AS user_avg_players
MATCH (target)-[:PLAYS]->(g:Game)<-[:PLAYS]-(similar:User)
WITH target, user_avg_time, user_avg_players, similar, COUNT(g) AS shared_games
ORDER BY shared_games DESC
LIMIT 10
MATCH (similar)-[:PLAYS]->(recommended:Game)
WHERE NOT (target)-[:PLAYS]->(recommended)
AND ABS(recommended.median_time_played - user_avg_time) < 10
AND ABS(recommended.player_count - user_avg_players) < 100
RETURN recommended.game_id AS game_id, recommended.name AS name, 
    COUNT(*) AS popularity, 
    ABS(recommended.median_time_played - user_avg_time) AS time_diff, 
    ABS(recommended.player_count - user_avg_players) AS player_diff
ORDER BY popularity DESC, time_diff ASC, player_diff ASC
LIMIT $top_n
```
* Trouver l'utilisateur cible.
* Rechercher les jeux auxquels cet utilisateur a joué.
* Calculer la moyenne du temps médian de jeu ``user_avg_time`` et le nombre moyen de joueurs ``user_avg_players`` pour les jeux joués par l'utilisateur cible.
* Identification des utilisateurs similaires :
* Trouver les utilisateurs similaires qui ont joué aux mêmes jeux que l'utilisateur cible.
* Compter le nombre de jeux partagés avec ces utilisateurs similaires (``shared_games``).
* Trier les utilisateurs similaires par le nombre de jeux partagés, en ordre décroissant.
* Limiter la liste aux 10 utilisateurs similaires les plus proches (pour des raisons de performance).
* Trouver les jeux joués par les utilisateurs similaires qui ne sont pas encore joués par l'utilisateur cible.
* Filtrer les jeux recommandés pour s'assurer que :

    * La différence entre le temps médian de jeu du jeu recommandé et la moyenne du temps de jeu de l'utilisateur cible est inférieure à 10.

    * La différence entre le nombre de joueurs du jeu recommandé et la moyenne des joueurs de l'utilisateur cible est inférieure à 100.
* Retourner les jeux recommandés.
* Trier les jeux recommandés par popularité en ordre décroissant, puis par différence de temps de jeu en ordre croissant, et enfin par différence de nombre de joueurs en ordre croissant.

* Limiter le nombre de recommandations retournées à une valeur donnée (``$top_n``).
