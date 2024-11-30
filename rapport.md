## Partie 1 : Données 



**Question: Quel est l'origine des données (lien, source)?**
Les données que nous avons choisi d'utiliser sont celles des [notes attribuées par les utilisateurs de Steam pour différents jeux](https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data) ainsi que leur revue textuelle. Ces [revues](https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_user_reviews.json.gz) et ces [données de jeux](https://datarepo.eng.ucsd.edu/mcauley_group/data/steam/australian_users_items.json.gz)sont d'origine d'Australie car la Version 2 de ces datasets ne possèdent pas de résultat de revue (positive ou négative). ***REVOIR AVEC TEAM***

**Question : Quel est le contexte du jeu de données, exemple: vente en ligne?**
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
Il est à noter que la quantité de revues est aussi prise en compte pour l'appréciation finale.

* Vérifiez vos données, effectuez un prétraitement (en Python) si nécessaire (pas besoin
de les faire sur Neo4J).
* Documenter les différentes étapes dans votre rapport dans une **section prétraitement des données**.