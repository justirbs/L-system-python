# L-system

## Description
Ce projet permet de générer des images et des formes selon un axiome et des paramètres grace à la librairie Turtle. Pour cela, il faut inscrire dans un fichier les différents paramètres comme : l’axiome, les règles de croissances, les angles, le niveau souhaité, …
Le programme permet de lire ce fichier et de générer le L-system au niveau demandé.

## Fichiers d'entrée
Un fichier de configuration des paramètres contient les informations suivantes :
- l'axiome qui représente la première forme
- la règle qui défini comment la forme va se développer
- l'angle 
- le niveau
- la taille 

Vous pourrez retrouver plusieurs exemples de fichiers : 
- `Tests/cherry_tree`
- `Tests/penrose`
- `Tests/tree`

## Lancement du programme
Pour lancer le programme, il faut ouvrir un terminal à la racine du projet et taper la commande suivante.
```
python l-system.py 
```
Vous pouvez également définir le fichier d'entrée et de sortie avec des options.
```
python l-system.py -i <fichier_entree> -o <fichier_sortie>
```