# Des légendes de Dwarf Fortress aux manuscrits avec Story Writer

`main-story-writer` sert de point de départ aux mondes dont les textes sont confiés exclusivement à [Story Writer](https://chatgpt.com/plugins/plugins_6ab235d1cda08191afa7ba8c81fb0429). La [SPEC](SPEC_Roman_Dwarf_Fortress.md) organise l’enquête dans les sources et les pistes à proposer. Les [instructions du projet](AGENTS.md#écriture-exclusivement-avec-story-writer) définissent comment vérifier le plugin et quelle erreur renvoyer s’il est indisponible.

## Commencer ou reprendre un export

1. Créer depuis `main-story-writer` une branche permanente `legendes/<monde>-<export>` portant un nom disponible. Pour explorer avec Story Writer un export déjà traité sur une autre branche, utiliser un nom distinct. Conserver sur cette branche les originaux anglais, les relevés, les pistes, les manuscrits et leurs traductions. Les branches d’export restent séparées.
2. Déposer dans `sources/` les fichiers d’un même export, remplir la [fiche de source](sources/README.md) et le [suivi](REPRISE.md). Le push du XML déclenche l’indexation. Pour la déclencher manuellement, lancer **Indexer un export Legends** depuis `main-story-writer` et choisir la branche de l’export comme cible. [Guide des outils](outils/README.md)
3. Explorer l’index et les notices, recouper les événements, puis reprendre les domaines peu explorés. Présenter le [registre des pistes](reperes/pistes.md). Y inscrire la piste et la langue choisies ainsi que la date, les contraintes ou la délégation de l’utilisateur.
4. Préparer le [dossier documentaire](manuscrits/fr/plan.md) de la piste. L’index, la préparation des événements, les vérifications factuelles et la proposition de pistes fonctionnent sans plugin.
5. Dès qu’une demande porte sur un plan narratif, un texte littéraire ou sa révision, vérifier l’accès réel à Story Writer dans la session. Lui confier cette partie avec le dossier et les consignes de l’utilisateur. Si Story Writer est indisponible, appliquer l’erreur prévue dans [AGENTS.md](AGENTS.md#écriture-exclusivement-avec-story-writer).

Pour reprendre un travail, ouvrir le `REPRISE.md` de la branche concernée. À chaque interruption ou fin d’étape, y inscrire l’état réel et la prochaine action.

## Classer les fichiers

| Fichier sur la branche d’export | Contenu |
| --- | --- |
| `reperes/pistes.md` | Pistes et décisions de sélection. L’identifiant complet associe la branche et l’ID local. |
| `reperes/chronologie.csv`, `reperes/glossaire.csv` | Dates, faits, noms, références anglaises et correspondances avec les fichiers produits. CSV en UTF-8 avec séparateur virgule. |
| `manuscrits/<langue>/<piste>/plan.md` | Dossier de recherche transmis à Story Writer, puis références des livrables. |
| `manuscrits/<langue>/<piste>/0.md` | Titre et quatrième de couverture produits par Story Writer. [Gabarit de fichier](modeles/0.md) |
| `manuscrits/<langue>/<piste>/nouvelle.md` ou `01.md`, `02.md`, etc. | Texte produit par Story Writer. Les chapitres séparés portent leur en-tête numéroté dans la langue de l’édition. [Gabarit de chapitre](modeles/chapitre.md) |
| `REPRISE.md` | Étape active, dernière action et point de reprise. |

Chaque histoire du même export conserve son identifiant et son dossier. Une traduction utilise le même identifiant dans le répertoire de sa langue et le manuscrit stabilisé comme référence.

## Journal des demandes

Consigner les demandes relatives à cette variante dans `suivi/usage-llm/` sur `main-story-writer`. Pour un monde, utiliser `reperes/usage-llm/` sur sa branche. [Règle de clôture](AGENTS.md#clôture-de-chaque-demande) · [Commandes](outils/README.md#journal-des-tokens)
