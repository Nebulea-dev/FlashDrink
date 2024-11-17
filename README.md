# FlashDrink

Projet Object Connecté de 3A ENSIMAG. Code et documentation pour un distributeur de boisson avec lecteur RFID

# Compiler et téléverser le projet sur un arduino Yùn Mini

## Pour Linux

### Prérequis

- **`Arduino CLI` :** Vous aurez besoin d'installer arduino-cli pour compiler et téléverser le projet.

- **Core Arduino :** Le core arduino:avr est requis pour travailler avec la carte Yùn Mini.

### Installation

1. Installer `Arduino CLI` :

```
sudo snap install arduino-cli
```

- _Version recommandée_

```
sudo snap install arduino-cli --channel=1.1.0/stable
```

2. Installer le core Arduino :

```
arduino-cli core update-index
arduino-cli core install arduino:avr
```

### Compilation du projet

- Utiliser le script de compilation qui va générer les fichiers dans le répertoire `build`

```
./arduino-build.sh
```

### Téléversement sur l'Arduino

1. Trouver le port machine auquel est connecté le `Yùn Mini`

```
arduino-cli board list
```

2. **Si la compilation a été un succès**, vous pouvez téléverser le projet depuis le script :

```
./arduino-upload.sh $PORT
```
