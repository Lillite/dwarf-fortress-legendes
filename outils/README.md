# Indexer et interroger un export Legends

## Dans GitHub Actions

Créer la branche du monde depuis `main`, puis pousser le XML dans `sources/`. Le workflow **Indexer un export Legends** récupère les sources du commit, exécute Python et publie les rapports dans `reperes/index-legends/` sur la branche du monde. Ouvrir d’abord le `README.md` de ce dossier. Les changements du registre, de la chronologie, du glossaire, de la copie de la SPEC ou des manuscrits relancent les dossiers éditoriaux. La base et les relevés factuels sont réutilisés sur cache valide, ou reconstruits si le cache a expiré. Aucun modèle de langage, service externe d’analyse ou clé d’API n’intervient dans cette étape.

Pour un monde déjà présent ou pour réappliquer les outils de `main`, ouvrir [Indexer un export Legends](https://github.com/Lillite/dwarf-fortress-legendes/actions/workflows/indexer-legendes.yml) dans Actions. Cliquer sur **Run workflow**, choisir **main** comme branche d’exécution et saisir le nom complet de la branche du monde dans **branche**. Les anciennes branches peuvent ainsi être indexées même si elles ne possèdent pas encore le workflow. Pour leurs futurs déclenchements automatiques sur push, il faut y intégrer le workflow de `main`.

Le sommaire, les CSV et le manifeste des empreintes SHA-256 restent sur la branche. Après une indexation à froid ou un lancement manuel, la base complète est téléchargeable sous **Artifacts** dans l’exécution correspondante, sous le nom `legendes-sqlite-<commit source>-<tentative>`. Après l’expiration de l’artefact, une relance le reconstitue. La publication nécessite le droit d’écriture du jeton Actions sur la branche du monde. Un nouveau commit de chapitre intervenu pendant le calcul est conservé. Si une entrée utilisée pour ces rapports a changé entre-temps, le workflow ne publie pas les résultats de l’ancien XML.

Réserver `reperes/index-legends/` aux fichiers générés. Les décisions éditoriales se consignent dans le registre des pistes et dans le plan du manuscrit. Si le dernier XML est retiré, le workflow retire les rapports générés. En cas d’erreur d’import, l’exécution échoue et les derniers rapports valides gardent les empreintes de leurs sources.

## En local

Utiliser Python 3.10 ou ultérieur, avec la bibliothèque standard. Dans les commandes suivantes, remplacer les chemins par ceux de l’export. La branche peut contenir le XML standard et son complément DFHack `*-legends_plus.xml` issus de la même opération. Les fichiers standard et complémentaires sont identifiés par leur nom usuel ou leur racine. Les champs observés dans chacun restent disponibles avec le nom de fichier et le numéro de ligne d’origine.

```sh
python3 outils/analyser_legendes.py --sources sources --base build/legendes.sqlite --rapports build/rapports
python3 outils/dossier_legendes.py build/legendes.sqlite historical_figure 400 --sortie build/figure-400.md
python3 -m unittest discover -s tests -v
```

La deuxième commande est un exemple utilisant la figure 400 de région 1. Remplacer sa catégorie et son identifiant pour interroger un autre monde, une œuvre, un événement, un site ou une collection. Le dossier indique qui cite la notice, ce qu’elle cite elle-même, les champs des rôles et les lignes à lire dans les sources. Un dossier se construit à partir de la base existante en quelques requêtes.

Si le monde possède déjà un relevé éditorial `reperes/occurrences.csv`, on peut le comparer à la même base. La première commande liste les types d’événement et leur couverture dans ce CSV. La seconde isole les événements déjà associés à une piste. Le CSV se lit sur la branche du monde et peut évoluer indépendamment de la base.

```sh
python3 outils/lire_pistes.py build/legendes.sqlite reperes/occurrences.csv
python3 outils/lire_pistes.py build/legendes.sqlite reperes/occurrences.csv --piste P014
```

## Lire les résultats

| Question | Relevé à ouvrir |
| --- | --- |
| Quelles familles d’événements explorer ? | `types-evenements.csv` indique leur effectif, leurs années et une notice de départ. |
| Qui commande dans plusieurs batailles ? | `commandements.csv` relie guerre, bataille, événement, site, camps, chefs et issue. `chefs-attaque-defense.csv` isole les figures observées dans les deux rôles. |
| Par où suivre un texte ? | `oeuvres.csv` rattache une œuvre à ses auteurs, à ses notices de composition et à ses exemplaires matériels lorsqu’ils sont documentés. |
| Qui retrouve-t-on dans une ville après sa destruction ? | `lieux.csv` et `retours.csv` donnent les notices du site et les figures pour lesquelles deux installations encadrent une destruction. Les trois dates doivent pouvoir être ordonnées. |
| Quel rapprochement demande une vérification directe ? | `references-a-verifier.csv` regroupe les champs dont la cible manque ou l’interprétation reste ouverte. La table SQLite `issues` contient les observations individuelles. |

Dans SQLite, `records` identifie une notice par **catégorie et identifiant**. `fields` conserve les occurrences et valeurs brutes, y compris les balises vides. `refs` donne le champ du rôle, l’origine et la cible de chaque renvoi reconnu. Les structures internes à un site s’identifient par **site et numéro local**. `sections` inventorie les sections rencontrées, y compris celles qui sont vides. Le manifeste `manifest.json` et la table `sources` permettent de retrouver l’empreinte de l’original utilisé.

Les rapports thématiques couvrent les formes de notices reconnues. Un autre type reste consultable dans l’inventaire et les champs bruts. Un rapprochement par personne, lieu ou date constitue un point de départ pour la [seconde lecture éditoriale](../SPEC_Roman_Dwarf_Fortress.md#seconde-lecture-avant-de-proposer-les-pistes). Vérifier les liens décisifs dans l’original avant de leur attribuer un lien de causalité ou une signification narrative.


## Dossiers de piste et mise à niveau

Ouvrir `reperes/index-legends/dossiers/README.md` sur la branche du monde. Chaque fiche regroupe les événements du registre et ceux rattachés aux chapitres dans la chronologie. Les numéros locaux de la fiche renvoient au répertoire des participants et des objets. Les motifs de sélection identiques sont écrits une fois. Les notices détaillées conservent les champs, les rôles et les lignes du XML. Une scène a son propre dossier avec les notices associées et les passages du plan ou des notes qui mentionnent leurs identifiants. Suivre les renvois vers ces documents pour les décisions exprimées en prose libre.

Les autres événements partageant au moins deux références figurent dans un CSV distinct. Les relevés `routes.csv`, `successions.csv`, `rencontres.csv` et `objets.csv` ouvrent des parcours supplémentaires. La couverture dépend des champs que contient chaque export.

Le rapport `controles.md` compare la structure des manuscrits à la SPEC des outils de main et vérifie les références structurées. `relecture.md` rassemble les ouvertures et les paragraphes identiques. `dependances.csv` associe les références aux pistes et aux chapitres. L’artefact **comparaison** indique les dépendances modifiées par rapport à l’état publié au point de comparaison. Un push fournit le SHA précédent. Pour une relecture depuis une révision précise, saisir son SHA complet dans le champ facultatif **depuis** du lancement manuel. Le diff des manuscrits est joint lorsque deux commits distincts sont comparés. Lors du premier calcul, le rapport indique que la référence est en cours de constitution.

Pour produire ces dossiers en local dans un répertoire vide :

```sh
python3 outils/dossiers_pistes.py build/legendes.sqlite --monde . --sortie build/dossiers
```

Les liens des fiches sont préparés pour leur emplacement publié sous `reperes/index-legends/dossiers/`. Les analyses automatiques produisent des documents de travail. Les textes du manuscrit, le titre et la quatrième de couverture gardent leur édition Markdown.

## Journal des tokens

Une demande peut comporter plusieurs appels. Employer le même identifiant pour ses appels et un nouvel identifiant pour la demande suivante. À la fin du travail sur un monde, consigner les compteurs dans `reperes/usage-llm/<demande>.json` sur sa branche. L’interface de conversation peut ne fournir aucune mesure par demande. Dans ce cas, consigner « indisponible ». La CI Python/SQLite effectue ses calculs sans appel LLM. Un commit Git ou un temps d’exécution ne fournit aucune mesure de la conversation.

Le workflow **[Journal des tokens d’une demande](https://github.com/Lillite/dwarf-fortress-legendes/actions/workflows/journal-tokens.yml)** se lance depuis main. Indiquer la branche du monde, l’identifiant de demande et éventuellement sa piste. Laisser les reçus vides en l’absence de compteurs. En cas d’appels API, fournir uniquement les objets minimaux `id`, `model` et `usage`, en tableau JSON si plusieurs appels. Cocher **Tous les appels** seulement si la liste est exhaustive. Le workflow publie directement le journal dans la branche choisie. GitHub reçoit les entrées du lancement : y saisir exclusivement ces métadonnées, jamais la conversation ni une clé.

Depuis un checkout de la branche du monde, l’équivalent local est :

```sh
python3 outils/journal_tokens.py --demande reprise-001 --piste P014
python3 outils/journal_tokens.py --demande reprise-002 --recu appel-1.json --recu appel-2.json --complet
```

Inclure ensuite uniquement le JSON produit dans le commit de la séance. Les états sont **indisponible**, **partiel** et **mesuré**. Un reçu rejoué pour la même demande compte une fois. Les compteurs de cache et de raisonnement sont des sous-ensembles du total. Le programme ne copie ni les prompts ni les réponses dans le journal. Les champs `total_demande` et `sous_total_appels_mesurés` distinguent une consommation intégrale d’une somme connue sur quelques appels. [Compteurs officiels](https://help.openai.com/en/articles/10478918-reviewing-api-usage-and-costs)

Pour comparer la taille de deux fiches ou mesurer le seul texte visible d’une demande, installer localement le module optionnel `tiktoken`, puis utiliser par exemple `--texte fiche.md --encodage o200k_base` avec le journal local. Chaque mesure conserve le nom de l’encodage, l’empreinte du texte et sa longueur en tokens pour cet encodage. Ce comptage reste indépendant des reçus et du quota ChatGPT. La première utilisation d’un encodage peut télécharger son vocabulaire.
