# Indexer et interroger un export Legends

## Dans GitHub Actions

Créer la branche du monde depuis `main-story-writer`, puis pousser le XML dans `sources/`. Le workflow **Indexer un export Legends** récupère les sources du commit, exécute Python et publie les rapports dans `reperes/index-legends/` sur la branche du monde. Ouvrir d’abord le `README.md` de ce dossier. Les changements du registre, de la chronologie, du glossaire, de la copie de la SPEC ou des manuscrits relancent les dossiers éditoriaux. La base et les relevés factuels sont réutilisés sur cache valide, ou reconstruits si le cache a expiré. Aucun modèle de langage, service externe d’analyse ou clé d’API n’intervient dans cette étape.

Pour un monde de cette variante déjà présent ou pour réappliquer les outils de `main-story-writer`, ouvrir [Indexer un export Legends](https://github.com/Lillite/dwarf-fortress-legendes/actions/workflows/indexer-legendes.yml) dans Actions. Cliquer sur **Run workflow**, choisir **main-story-writer** comme branche d’exécution et saisir le nom complet de la branche du monde dans **branche**. Le déclenchement manuel utilise les outils de cette variante. Les futurs exports qui en dérivent héritent du déclenchement automatique.

Le sommaire, les CSV et le manifeste des empreintes SHA-256 restent sur la branche. Après une indexation à froid ou un lancement manuel, la base complète est téléchargeable sous **Artifacts** dans l’exécution correspondante, sous le nom `legendes-sqlite-<commit source>-<tentative>`. Après l’expiration de l’artefact, une relance le reconstitue. La publication nécessite le droit d’écriture du jeton Actions sur la branche du monde. Un nouveau commit de chapitre intervenu pendant le calcul est conservé. Si une entrée utilisée pour ces rapports a changé entre-temps, le workflow ne publie pas les résultats de l’ancien XML.

Réserver `reperes/index-legends/` aux fichiers générés. Les décisions éditoriales se consignent dans le registre des pistes et dans le plan du manuscrit. Si le dernier XML est retiré, le workflow retire les rapports générés. En cas d’erreur d’import, l’exécution échoue et les derniers rapports valides gardent les empreintes de leurs sources.

## En local

Utiliser Python 3.10 ou ultérieur, avec la bibliothèque standard. Dans les commandes suivantes, remplacer les chemins par ceux de l’export. La branche peut contenir le XML standard et son complément DFHack `*-legends_plus.xml` issus de la même opération. Les fichiers standard et complémentaires sont identifiés par leur nom usuel ou leur racine. Les champs observés dans chacun restent disponibles avec le nom de fichier et le numéro de ligne d’origine. Pour la commande de consultation, affecter à `CATEGORIE` et `ID_NOTICE` la catégorie et l’identifiant d’une notice présente dans la base. Le relevé `build/rapports/types-evenements.csv` donne un identifiant de départ pour chaque type d’événement observé, dans la catégorie `historical_event`.

```sh
python3 outils/analyser_legendes.py --sources sources --base build/legendes.sqlite --rapports build/rapports
python3 outils/dossier_legendes.py build/legendes.sqlite "$CATEGORIE" "$ID_NOTICE" --sortie build/notice.md
python3 -m unittest discover -s tests -v
```

Le dossier indique qui cite la notice, ce qu’elle cite elle-même, les champs des rôles et les lignes à lire dans les sources. Un dossier se construit à partir de la base existante en quelques requêtes.

Si le monde possède déjà un relevé éditorial `reperes/occurrences.csv`, on peut le comparer à la même base. La première commande liste les types d’événement et leur couverture dans ce CSV. La seconde isole les événements déjà associés à une piste. Le CSV se lit sur la branche du monde et peut évoluer indépendamment de la base. Affecter à `PISTE` l’identifiant voulu dans le registre de cette branche.

```sh
python3 outils/lire_pistes.py build/legendes.sqlite reperes/occurrences.csv
python3 outils/lire_pistes.py build/legendes.sqlite reperes/occurrences.csv --piste "$PISTE"
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

Les rapports thématiques couvrent les formes de notices reconnues. Un autre type reste consultable dans l’inventaire et les champs bruts. Un rapprochement par personne, lieu ou date constitue un point de départ pour la [seconde lecture documentaire](../SPEC_Roman_Dwarf_Fortress.md#seconde-lecture-avant-de-proposer-les-pistes). Vérifier les liens décisifs dans l’original avant de leur attribuer un lien de causalité.


## Dossiers de piste et mise à niveau

Ouvrir `reperes/index-legends/dossiers/README.md` sur la branche du monde. Chaque fiche regroupe les événements du registre et ceux rattachés aux chapitres dans la chronologie. Les numéros locaux de la fiche renvoient au répertoire des participants et des objets. Les motifs de sélection identiques sont écrits une fois. Les notices détaillées conservent les champs, les rôles et les lignes du XML. Une scène a son propre dossier avec les notices associées et les passages du plan ou des notes qui mentionnent leurs identifiants. Suivre les renvois vers ces documents pour les décisions exprimées en prose libre.

Les autres événements partageant au moins deux références figurent dans un CSV distinct. Les relevés `routes.csv`, `successions.csv`, `rencontres.csv` et `objets.csv` ouvrent des parcours supplémentaires. La couverture dépend des champs que contient chaque export.

Le rapport `controles.md` vérifie le classement des fichiers et leurs références structurées. `relecture.md` rassemble les ouvertures et les paragraphes identiques. `dependances.csv` associe les références aux pistes et aux chapitres. L’artefact **comparaison** indique les dépendances modifiées par rapport à l’état publié au point de comparaison. Un push fournit le SHA précédent. Pour une relecture depuis une révision précise, saisir son SHA complet dans le champ facultatif **depuis** du lancement manuel. Le diff des manuscrits est joint lorsque deux commits distincts sont comparés. Lors du premier calcul, le rapport indique que la référence est en cours de constitution.

Pour produire ces dossiers en local dans un répertoire vide :

```sh
python3 outils/dossiers_pistes.py build/legendes.sqlite --monde . --sortie build/dossiers
```

Les liens des fiches sont préparés pour leur emplacement publié sous `reperes/index-legends/dossiers/`. Les analyses automatiques produisent des documents de travail. Les textes du manuscrit, le titre et la quatrième de couverture gardent leur édition Markdown.

## Journal des tokens

Une fiche correspond à une demande utilisateur. Choisir un identifiant unique, par exemple une date suivie d’un sujet et d’un suffixe si nécessaire. Réutiliser cet identifiant uniquement pour les tentatives ou les appels de cette même demande. Sur `main-story-writer`, le journal se trouve dans `suivi/usage-llm/<demande>.json`. Sur `legendes/<monde>-<export>`, il se trouve dans `reperes/usage-llm/<demande>.json`. Les anciens échanges restent hors du calcul. La publication de la fiche fait partie de la clôture de la demande. [Consignes de clôture](../AGENTS.md)

| Donnée disponible à la clôture | Ce qui est enregistré |
| --- | --- |
| Reçus API de tous les appels effectués pour cette demande | `statut: mesuré` et somme dans `total_demande`. Un identifiant de réponse compte une fois. Les tokens de cache et de raisonnement sont déjà inclus dans les compteurs correspondants. |
| Reçus d’une partie des appels | `statut: partiel`, somme dans `sous_total_appels_mesurés` et `total_demande: null`. |
| Aucun reçu de consommation | `statut: indisponible` et `total_demande: null`. |
| Total inconnu et texte visible accessible | `indication_visible` donne l’encodage, la taille du seul message utilisateur courant, celle de la réponse finale préparée et leur somme. Cette mesure exclut les messages précédents, les pièces jointes, les outils et le travail interne. |

Un reçu peut inclure du contexte relu par le modèle lors de cet appel. Utiliser le reçu tel quel. Les reçus des demandes antérieures, les compteurs de session et le quota du compte n’entrent jamais dans le calcul. [Documentation des compteurs API](https://help.openai.com/en/articles/10478918-reviewing-api-usage-and-costs)

### Publier avant de répondre

Depuis le dépôt avec un accès en écriture à `origin`, utiliser le script de `main-story-writer`. Pour une conversation dont le total est inconnu, préparer la réponse définitive et copier uniquement les deux textes dans des fichiers UTF-8 temporaires hors du dépôt. Installer le module Python `tiktoken` pour ce comptage. Le premier chargement de l’encodage peut télécharger son vocabulaire. Dans les commandes suivantes, affecter à `DEMANDE` un identifiant neuf pour la demande courante.

```sh
python3 outils/journal_tokens.py --publier --branche main-story-writer --demande "$DEMANDE" \
  --message-utilisateur /tmp/demande.txt --reponse-finale /tmp/reponse.txt --encodage o200k_base
```

Pour un monde, affecter à `BRANCHE_EXPORT` le nom complet de sa branche et à `PISTE` l’identifiant concerné, si la demande porte sur une piste. Avec des compteurs API, fournir les reçus du tour. Ajouter `--complet` lorsque tous les appels sont couverts.

```sh
python3 outils/journal_tokens.py --publier --branche "$BRANCHE_EXPORT" --demande "$DEMANDE" \
  --piste "$PISTE" --recu /tmp/appel-1.json --recu /tmp/appel-2.json --complet
```

`--publier` écrit uniquement la fiche sur la branche distante et vérifie sa présence et ses compteurs. En mode local, omettre `--publier` et `--branche` pour préparer le JSON sur la branche courante. On peut alors publier cette fiche via le connecteur GitHub et relire le fichier sur la branche cible. L’option distincte `--texte fiche.md --encodage o200k_base` permet aussi de mesurer un document de travail.

Le workflow **Journal des tokens d’une demande** se lance depuis `main-story-writer`, pour cette variante et ses branches d’export. Renseigner la branche cible et l’identifiant de la demande. Les entrées facultatives acceptent les reçus minimaux (`id`, `model`, `usage`) et les compteurs visibles déjà calculés localement, par exemple `{"encodage":"o200k_base","message_utilisateur":20,"reponse_finale":80}`. Attendre la réussite de l’exécution. GitHub ne reçoit que les métadonnées. La CI ne voit pas les conversations ChatGPT et n’appelle aucun LLM pour cette opération. [Ouvrir le workflow](https://github.com/Lillite/dwarf-fortress-legendes/actions/workflows/journal-tokens.yml)
