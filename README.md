# VideoTracker_G1

Logiciel de pointage permettant de relever les positions d’un objet en mouvement au cours du temps à l’aide de la souris. On obtient ainsi la position de ce point sur chaque image de la vidéo. Ces informations permettent ensuite de faire une étude cinématique et énergétique de l’objet étudié. Le logiciel est développé en Python, et dépend de [Pillow](https://pypi.org/project/pillow/) et [OpenCV](https://pypi.org/project/opencv-python/).

## Installation

Télécharger la dernière [release](https://gitlab.emi.u-bordeaux.fr/tipiault/videotracker_g1/-/releases) ou cloner le dépot avec `git clone git@gitlab.emi.u-bordeaux.fr:tipiault/videotracker_g1.git`. Dans le dossier de l'application, exécuter :

```sh
pip install -r requirements.txt
python src/Application.py
```

## Fonctionnalités

- Définir l'origine et l'échelle du repère
- Afficher les graphiques pour x(t), y(t) et y(x)
- Afficher les valeurs obtenues dans un tableau
- Enregistrer les données au format CSV
- Lire la vidéo en entier et image par image
- Raccourcis clavier pour charger une vidéo et quitter l'application

## Bugs connus

- Charger une nouvelle vidéo alors qu'une vidéo est déjà chargée ne fonctionne pas encore

## Lancer les tests unitaires

Depuis la racine du projet, avec unittest installé :
```sh
python -m unittest discover tests/
```