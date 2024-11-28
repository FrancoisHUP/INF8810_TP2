# Instructions Projet 2

Préparé par Jean-Francois Rajotte

Automne 2024

## Objectif
L'objectif de ce projet est de développer un système de recommandation à partir des outils de base Neo4j.

## Consignes de remise du travail
Le travail doit être remis au plus tard le **8 décembre (23h55)**.

**Important:** Pour chaque jour de retard, vous perdrez 5% de votre note.
Après 7 jours, votre résultat sera 0.
Pas de période de grâce une fois le délai écoulé.

Vous pouvez travailler en équipe de 3 personnes maximum.


## Critères d'évaluation
Ce TP est noté sur 30 points et compte pour 30% de votre note finale.

Vous devez vous assurez de donner des instructions complètes: quelles commandes envoyer, où mettre les fichiers...

* Remise sur Moodle
  * un rapport Markdown ou Word incluant:
    * le nom des membres de votre équipe
    * chacune des étapes décrites ci-dessous, clairement identifiées par un titre.
    * les réponses aux questions
  * Autre(s) fichier(s) (e.g. script de nettoyage python) utilisés pour le projet. 
* Votre rapport doit donner toutes les commandes pour reproduire votre travail avec *copier-coller*.
* Aucune librairie de recommandation ou de calcul de similarité ne peut être utilisée pour le projet.

### Originalité
Vous serez évalué sur la consistance de vos traitements et la complétude et les détails dans votre rapport par rapport aux spécifications ainsi que l’optimalité et la qualité du code.
Il ne faut pas vous limiter à reprendre les exemples du cours. Dans le cas contraire, vous serez pénalisé.
En effet, vous serez évalué sur l’originalité de votre travail.

**Le non-respect des modalités sera pénalisé.**

* La présentation en général et les fichiers remis: 3/30
    * Clarté du travail en général
    * Les tâches des sections "**Ce qui vous devez faire**" doivent être identifiées et chaque question doit être répondu clairement.
    * Les commandes pour chaque étapes doivent être clairement identifiées.

* Implémentation, discussion: 27/30

## Partie 1 : Données (5 points)

Identifiez, analysez et choisissez vos sources de données (Voir section Projet 2 *Répertoire des
datasets des systèmes de recommandation (Ref. Julian McAuley, UCSD)* dans votre site
de cours Moodle ou d’autres datasets de votre choix).

**Ce qui vous devez faire**:
* Question: Quel est l'origine des données (lien, source)?
* Question : Quel est le contexte du jeu de données, exemple: vente en ligne?
* Vérifiez vos données, effectuez un prétraitement (en Python) si nécessaire (pas besoin
de les faire sur Neo4J).
* Documenter les différentes étapes dans votre rapport dans une **section prétraitement des données**.

## Partie 2 : Chargement dans neo4j (10 points)

* Question : Quelles données chargez-vous dans neo4j?
* Question : Faites-vous des traitements/modifications lors du chargement?
* Chargez vos données en utilisant uniquement NEO4J
* Incluez vos requêtes et décrivez vos étapes dans votre rapport.


## Partie 3 : Recommandation (12 points)
Créer une un système de recommandation.
Seulement à titre d’exemple (ça dépandéra naturellement des données choisies et le domaine d’application), recommandez un ensemble de chansons à un utilisateur sur la base d’une chanson (donnée en entrée) que ce même utilisateur a aimé. 
En d’autres termes, l’utilisateur Reiaz a aimé la chanson C1, votre solution va recommander à l’utilisateur Reiaz les chansons C2, C3 et C4 que potentiellement il va aimer. 
Utilisez les exemples de requêtes et de types d’approches de recommandation (basée contenu, filtrage collaboratif et hybride) étudiés en classe pour créer votre propre requête de recommandation (Votre propre requête – pas une reprise des exemples du cours).

**Ce qui vous devez faire**:
* Question : Quelle recommandation proposez-vous?
  * Qu'est-ce qui est recommandé?
  * À qui ou quoi faites-vous cette recommandation?
* Créez une requête pour faire une recommandation en fonction de votre source de données.
* Décrivez en détail l’approche de votre requête de recommandation et incluez votre code dans votre rapport.
