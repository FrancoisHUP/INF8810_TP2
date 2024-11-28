# INF8810_TP2

1. Installez les librairies python. 
```bash
$ pip install -r requirements.txt
```

2. Assurez-vous d'avoir une version du logiciel Neo4j installée et en cours d'execution sur votre machine. Vous devrez changer le mot de passe et nom de l'utilisateur dans le fichier .env à la racine du dossier. 

Pour tester si le logiciel est bien activé, faites :
```bash
$ python utils/check_neo4j_status.py 
```

3. Télécharger les données :
```bash
$ python utils/download_data.py 
```