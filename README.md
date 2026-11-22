# Romans des Légendes de Dwarf Fortress

Projet d’écriture à partir d’un export **Legends** en anglais. Le français est la première langue de rédaction. La chronologie du monde et les références aux événements sont communes à toutes les éditions.

## Fichiers de travail

| Fichier | Fonction |
| --- | --- |
| [Fiche de source](sources/README.md) | Identifier le monde et l’export utilisé. |
| [Chronologie](reperes/chronologie.csv) | Retrouver chaque événement dans l’export et suivre sa place dans le roman. |
| [Glossaire multilingue](reperes/glossaire.csv) | Conserver les noms d’origine et les traductions retenues pour chaque langue. |
| [Plan du manuscrit français](manuscrits/fr/plan.md) | Choisir le point de vue, la période et l’ordre des chapitres. |
| [Modèle de chapitre](modeles/chapitre.md) | Rattacher les scènes à leurs sources et garder les notes d’auteur à part. |

## À réception du premier export

1. Déposer le fichier anglais dans `sources/` en gardant son nom et son contenu d’origine. Compléter sa fiche.
2. Dans la chronologie, relever la date à la précision donnée par l’export, les protagonistes et le lieu. Inscrire l’identifiant d’événement s’il existe, sinon un repère de section ou un court extrait anglais qui permette de retrouver le passage.
3. Dans le glossaire, créer une ligne par terme et par langue cible. Garder la forme anglaise même lorsqu’un nom propre est repris à l’identique. Utiliser la référence source pour distinguer les homonymes.
4. Quand commencera l’écriture, copier le modèle dans `manuscrits/fr/01.md`. Inscrire le numéro du chapitre dans la chronologie et distinguer dans les notes les faits attestés, les interprétations et les ajouts romanesques.

Pour une nouvelle langue, créer un dossier frère de `fr/`, par exemple `manuscrits/es/` pour l’espagnol. Reprendre les numéros de chapitre et ajouter les choix de traduction au même glossaire.

Les tableaux CSV utilisent la virgule comme séparateur et l’encodage UTF-8. Ils contiennent uniquement leurs en-têtes au démarrage.
