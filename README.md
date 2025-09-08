# Calcul de Poinçonnement - Eurocode 2

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Une application de bureau moderne et intuitive développée pour les ingénieurs en génie civil. Ce logiciel permet de réaliser la vérification du poinçonnement pour les dalles en béton armé supportant des poteaux ou des voiles, conformément aux normes de l'Eurocode 2.

## Capture d'écran

![Capture d'écran de l'application Calcul de Poinçonnement](https://raw.githubusercontent.com/VOTRE_NOM_UTILISATEUR/VOTRE_DEPOT/main/screenshot.png)

## Fonctionnalités

-   **Calculs conformes à l'Eurocode 2** : Implémentation fidèle des formules de vérification au poinçonnement.
-   **Deux types d'éléments** : Prise en charge des **poteaux** rectangulaires et des **voiles**.
-   **Interface intuitive** : Saisie des données claire et affichage des résultats structuré pour une lecture rapide.
-   **Résultats détaillés** : Accès à tous les calculs intermédiaires (périmètre critique, effort tranchant réduit, coefficients, etc.).
-   **Verdict visuel immédiat** : Le résultat final ("OK" / "NON OK") est affiché en couleur pour une identification instantanée.
-   **Thèmes Clair et Sombre** : Un interrupteur permet de basculer entre les modes pour un meilleur confort visuel.
-   **Exécutable portable** : Peut être distribué comme un simple fichier `.exe` sans nécessiter d'installation de Python.

## Technologies utilisées

-   **Python 3** : Langage de programmation principal.
-   **CustomTkinter** : Bibliothèque pour la création de l'interface graphique moderne.
-   **PyInstaller** : Outil pour la création du fichier exécutable.

## Installation et Utilisation

### Pour les ingénieurs (Utilisateurs finaux)

La manière la plus simple d'utiliser le logiciel est de télécharger la dernière version exécutable.

1.  Allez sur la page [**Releases**](https://github.com/Hvni44/Calcul-de-Poinconnement-/releases) de ce dépôt.
2.  Téléchargez le fichier `CalculPoinconnement.exe` depuis la dernière version.
3.  Placez le fichier où vous le souhaitez et double-cliquez dessus pour le lancer. Aucune installation n'est requise.

### Pour les développeurs

Si vous souhaitez modifier le code source ou y contribuer :

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_DEPOT.git
    cd VOTRE_DEPOT
    ```

2.  **Installez les dépendances :**
    ```bash
    pip install customtkinter
    ```

3.  **Lancez l'application :**
    ```bash
    python app_poinconnement.py
    ```

## Comment générer l'exécutable

Pour recompiler le fichier `.exe` vous-même, assurez-vous que PyInstaller est installé (`pip install pyinstaller`), puis lancez la commande suivante depuis la racine du projet :

```bash
pyinstaller --name="CalculPoinconnement" --onefile --windowed --icon="icon.ico" app_poinconnement.py