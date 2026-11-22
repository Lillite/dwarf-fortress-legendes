# Nouvelles et romans des légendes de Dwarf Fortress

Ce projet transforme des épisodes d’un export *Legends* anglais en œuvres de fiction textuelles. Le récit peut suivre toute période documentée, y compris des siècles d’histoire antérieurs à la partie. L’utilisateur choisit la piste et la langue d’écriture.

**Pour reprendre une histoire, sélectionner sa branche d’export dans la [liste des branches](https://github.com/Lillite/dwarf-fortress-legendes/branches), puis ouvrir le [suivi de reprise](REPRISE.md) sur cette branche.** Les critères de sélection du sujet, de suffisance de la matière, d’écriture et de relecture sont réunis dans la [SPEC éditoriale](SPEC_Roman_Dwarf_Fortress.md).

## Une branche permanente par export

`main` contient la méthode commune, la SPEC et les modèles. Avant de déposer un nouvel export *Legends*, créer depuis la version courante de `main` une branche nommée `legendes/<monde>-<export>`. Utiliser un nom lisible et un repère qui distingue l’export, par exemple `legendes/monde-des-brumes-an-250`. Si le même monde est exporté à nouveau, lui donner une nouvelle branche. Les fichiers complémentaires issus de la même opération d’export vont ensemble.

Conserver sur cette branche l’original anglais, les fiches, toutes les pistes, les nouvelles, les romans, leurs traductions et le journal de reprise. Pour une deuxième histoire tirée du même export, sélectionner cette même branche et ouvrir un nouveau dossier de manuscrit. Pour reprendre un export déjà enregistré, retrouver sa branche et vérifier la [fiche de source](sources/README.md).

**Chaque branche d’export est conservée, même après la dernière relecture. Elle ne doit jamais être fusionnée dans `main` ni dans une autre branche.** La fin d’une histoire se consigne dans le journal de sa branche.

## Du fichier anglais au manuscrit relu

| Étape | Travail | Trace à conserver dans le dépôt |
| --- | --- | --- |
| 1. Créer la branche et ajouter l’export | Créer la branche permanente de cet export depuis `main`, puis y déposer l’original anglais dans `sources/` sous son nom d’origine. Identifier le monde, les fichiers associés et la période connue. | Nom exact de la branche et chemin de l’export dans la [fiche de source](sources/README.md) et dans le suivi de cette branche. |
| 2. Lire et proposer | Parcourir l’export, y compris les époques anciennes. Repérer les histoires possibles. Pour chaque piste, citer les passages, expliquer l’intérêt pour un lecteur et évaluer la matière réellement disponible. Présenter les options à l’utilisateur avec leurs identifiants. | [Registre des pistes](reperes/pistes.md). Si la lecture se fait en plusieurs séances, indiquer les sections parcourues et la prochaine section. |
| 3. Recueillir le choix | L’utilisateur désigne la piste et la langue. Consigner ses mots, la date, l’identifiant, la langue et toute contrainte de couverture. Tant que le choix reste ouvert, garder les pistes disponibles et le suivi à l’étape 3. | Registre des pistes et [suivi de reprise](REPRISE.md). Une fois le choix exprimé, ouvrir le plan de cette histoire. |
| 4. Rechercher les liens et préparer l’histoire | Repartir des identifiants, des alias et des passages de la piste. Suivre les renvois pertinents dans les deux sens, puis ceux des éléments découverts. Situer chaque lien dans le temps, noter sa source, les incertitudes et son effet possible sur le récit. Réévaluer le format à la lumière de l’enquête. | Dossier de recherche dans le [modèle de plan](manuscrits/fr/plan.md), [chronologie](reperes/chronologie.csv), [glossaire](reperes/glossaire.csv) et, au besoin, notes de format dans la fiche de source. |
| 5. Rédiger dans la langue choisie | Préparer les faits de chaque scène dans cette langue, puis écrire directement le texte littéraire. Appliquer la SPEC au point de vue, aux dialogues et au rythme. À la fin de chaque chapitre, contrôler les faits dans l’original anglais. | Plan, [chapitre ou nouvelle](modeles/chapitre.md), références aux scènes et dernier passage rédigé. |
| 6. Relire et corriger | Relire la nouvelle d’une traite ou plusieurs chapitres consécutifs du roman. Corriger continuité, voix, rythme et clarté. Vérifier ensuite le texte corrigé contre les événements retenus. | Manuscrit corrigé et bilan de relecture dans le plan. Consigner les passages revus, les corrections et les questions encore ouvertes. |

## Classer les fichiers pour retrouver une histoire

- Attribuer à chaque piste un identifiant unique dans le registre, par exemple `P001`. La référence complète d’une piste est le nom de sa branche d’export accompagné de son identifiant dans le registre.
- Après le choix, copier le [modèle de plan](manuscrits/fr/plan.md) dans `manuscrits/<langue>/<piste>/plan.md`. Par exemple, `manuscrits/fr/P001/` accueillerait un récit français. Une nouvelle peut tenir dans `nouvelle.md`. Pour un roman, utiliser `01.md`, `02.md`, etc. Le [modèle de chapitre](modeles/chapitre.md) convient aux deux formes.
- Dans la chronologie, inscrire la destination complète d’un événement, par exemple `manuscrits/fr/P001/01.md`. Dans le glossaire, conserver la forme anglaise, la langue cible et la référence qui distingue deux homonymes. Les deux CSV utilisent la virgule et l’encodage UTF-8.
- Pour une traduction ultérieure, reprendre le manuscrit original stabilisé. Placer l’édition dans le dossier de sa langue avec le même identifiant de piste, et conserver les références communes à l’export.

À la fin de chaque étape ou séance interrompue, enregistrer sur la branche de l’export les fichiers de travail et actualiser le [suivi](REPRISE.md) dans le même commit. À la reprise, ouvrir l’élément indiqué à la ligne « Prochaine action ».
