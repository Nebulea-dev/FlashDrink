# Application mobile Flash Drink

## Build l'application

**Nous conseillons très fortement de simplement télécharger l'application, qui se trouve dans [l'onglet release du git](https://github.com/Nebulea-dev/FlashDrink/releases/latest).**
Build l'application demande de nombreuses dépendances, beaucoup de configuration et des efforts de debug assez significatifs, parce que React Native est pas toujours très sympathique.

Si vous souhaitez tout de même build l'application vous même, alors suivez les instructions ci-dessous. 
Dans un premier temps, on se place dans le dossier `mobile-app` du dépot github, puis :

1. **Installez les dépendances**

Allez sur la [documentation de React Native](https://reactnative.dev/docs/set-up-your-environment) pour voir comment installer `node`, `JDK`, `Android Studio`, `Android SDK`, et comment les configurer

2. **Configurer l'application en mode Release**

Allez sur cet [article Medium](https://medium.com/@tywosemail/building-an-apk-file-for-a-react-native-android-project-involves-several-steps-e97d1294aafc) qui explique comment générer les clés publiques et privées de l'application, et où les placer

3. **Build l'application**

Exécutez le script `build.sh`, qui va générer l'APK `app-release.apk` à la racine du dossier `mobile-app`.

## Debugger l'application

**Pour débugger l'application, il vous faut un [environnement de développement React Native]((https://reactnative.dev/docs/set-up-your-environment).**

Dans un premier terminal, on lance le serveur metro :

```
npx react-native start
```

Puis, dans un second terminal, sans fermer le premier, on lance l'application :

```
npx react-native run-android
```
