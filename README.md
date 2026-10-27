# PDF Password Manager

Application Windows portable permettant d'ajouter, modifier ou supprimer un mot de passe sur un fichier PDF via une interface graphique simple.

## Aperçu

PDF Password Manager est un utilitaire développé en Python avec Tkinter et PyPDF.

L'objectif est de fournir une solution rapide et facile pour protéger ou déprotéger des fichiers PDF sans utiliser de services en ligne.

## Fonctionnalités

- Ajout d'un mot de passe sur un PDF
- Modification d'un mot de passe existant
- Suppression d'un mot de passe
- Interface graphique simple et intuitive
- Confirmation avant écrasement d'un fichier
- Application 100 % locale
- Aucune connexion Internet requise
- Exécutable portable Windows

## Capture d'écran

Ajoutez ici une capture de l'application si vous souhaitez illustrer le projet.

## Téléchargement

Téléchargez la dernière version depuis la section Releases du dépôt GitHub.

## Utilisation

### Ajouter un mot de passe

1. Sélectionner le PDF.
2. Choisir l'action « Ajouter ».
3. Saisir le nouveau mot de passe.
4. Lancer le traitement.

### Modifier un mot de passe

1. Sélectionner le PDF.
2. Choisir l'action « Modifier ».
3. Saisir le mot de passe actuel.
4. Saisir le nouveau mot de passe.
5. Valider.

### Supprimer un mot de passe

1. Sélectionner le PDF.
2. Choisir l'action « Supprimer ».
3. Saisir le mot de passe actuel.
4. Valider.

## Technologies utilisées

- Python
- Tkinter
- PyPDF
- PyInstaller

## Sécurité

- Aucun envoi de données sur Internet
- Aucun stockage des mots de passe
- Traitement effectué localement sur la machine
- Aucune dépendance à un service tiers

## Construction depuis les sources

```bash
pip install pypdf
python pdf_password_manager.py
```

Création de l'exécutable :

```bash
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico --add-data "icon.ico;." pdf_password_manager.py
```

## Auteur

Theo COUTARD

GitHub : https://github.com/ATHEO-INFORMATIQUE

## Licence

Projet distribué à des fins éducatives et professionnelles.