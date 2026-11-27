# Préparer les événements et les pistes d’un export Legends

**Version 2.0 · Variante Story Writer · Préparation documentaire**

Cette SPEC couvre l’import du monde, l’organisation des événements, la proposition de pistes et le dossier remis à Story Writer. Toute période attestée de l’histoire du monde peut être explorée, y compris avant la partie. Le passage à l’écriture suit la [règle Story Writer](AGENTS.md#écriture-exclusivement-avec-story-writer).

## Identifier le monde et ses sources

Créer la branche de l’export depuis `main-story-writer`. Y conserver dans `sources/` l’original anglais et les éventuels compléments de la même opération. Renseigner la [fiche de source](sources/README.md) avec leurs chemins, le monde, la version connue du jeu et la période couverte. Pour reprendre un monde, ouvrir le [journal de reprise](REPRISE.md) de sa branche.

Ouvrir le sommaire `reperes/index-legends/README.md` de l’export. Les empreintes du manifeste permettent de vérifier quels fichiers ont été indexés. Si l’index manque ou que les sources ont changé, le [régénérer](outils/README.md). Pendant ce temps, l’original reste consultable.

## Organiser et recouper les événements

- Pour chaque fait utile, conserver le fichier, la catégorie et l’identifiant de la notice, ainsi que le champ ou le passage anglais qui l’établit. En l’absence d’identifiant, relever la section et un extrait repérable. Les noms identiques se départagent par les identifiants et les rôles. [Guide du XML](sources/guide-xml.md)
- Suivre les renvois dans les deux sens. Relever selon le cas les personnes et groupes, leurs rôles, les lieux, objets, œuvres, fonctions et collections d’événements. Identifier le camp et la fonction à la date de chaque occurrence. Un changement de rôle peut relier deux notices éloignées.
- Classer les faits à la précision fournie par le XML. Conserver les égalités et les ordres indéterminés. Distinguer un événement repris dans plusieurs fichiers, une collection et les événements qu’elle regroupe. Citer les sources complémentaires d’un même fait une seule fois dans la chronologie avec leurs références.
- Distinguer fait attesté, rapprochement à vérifier et information manquante. Une date commune ne suffit pas à établir une rencontre ou une causalité. Consigner les variantes, les contradictions et les recherches sans résultat.
- Tenir à jour la [chronologie](reperes/chronologie.csv) et le [glossaire](reperes/glossaire.csv). Conserver les formes anglaises et la langue de la forme retenue. Si un manuscrit existe, sa destination dans la chronologie permet de retrouver les passages liés à une notice.

## Seconde lecture avant de proposer les pistes

Noter les domaines qui ont produit les premières pistes et reprendre ceux qui restent peu explorés. Par exemple, partir d’un conflit et suivre les chefs de chaque camp dans d’autres batailles, d’un lieu et rechercher qui y revient après sa destruction, ou d’une œuvre et identifier ses détenteurs successifs. Vérifier chaque rapprochement dans les notices originales. La sélection des parcours dépend des sections réellement présentes.

Dans le [registre des pistes](reperes/pistes.md), noter le point de départ, les renvois suivis, les références trouvées et le résultat. Une recherche peut ouvrir une piste, enrichir une piste existante ou s’arrêter sur une lacune précise. Si la séance s’interrompt, noter le prochain renvoi dans `REPRISE.md`.

## Présenter et choisir les pistes

Attribuer à chaque piste un identifiant local stable de la forme `P001`. Indiquer en quelques lignes le sujet, la période, les acteurs ou objets concernés, ce qui change dans les faits et les notices qui permettent de le vérifier. Signaler ce qui manque entre les étapes documentées. Pour une mention isolée, préciser quelle recherche permettrait de la développer. Conserver les pistes en réserve et les liens entre pistes. Le nombre de propositions dépend des découvertes.

Présenter les pistes avec leurs identifiants. Consigner le choix ou la délégation de l’utilisateur, sa date, la langue, le périmètre demandé et les questions ouvertes. Si le choix reste en attente, conserver le registre et le point de reprise.

## Constituer le dossier à remettre à Story Writer

Copier le [modèle de dossier](manuscrits/fr/plan.md) dans `manuscrits/<langue>/<piste>/plan.md`. Y réunir les faits retenus dans la langue demandée, les passages anglais et leurs identifiants, les relations documentées et les incertitudes. Pour les notices détaillées, utiliser la fiche générée `reperes/index-legends/dossiers/<piste>.md`. Si le monde utilise `reperes/occurrences.csv`, y conserver les associations entre piste et événement avant même qu’un chapitre existe. [Outils et formats](outils/README.md)

Le dossier est prêt à transmettre lorsque le périmètre choisi, les preuves et les lacunes sont repérables. Remettre à Story Writer le dossier, les contraintes formulées par l’utilisateur et, pour une reprise, les fichiers littéraires déjà produits. Les choix de narration et tout travail sur le texte relèvent exclusivement du plugin. Les contrôles du dépôt portent sur les références, les fichiers et la correspondance avec l’export. En cas d’écart, consigner le fait et sa source pour que Story Writer reprenne le passage.
