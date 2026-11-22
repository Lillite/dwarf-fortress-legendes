# Indexer et interroger un export Legends

## Dans GitHub Actions

Créer la branche du monde depuis `main`, puis pousser le XML dans `sources/`. Le workflow **Indexer un export Legends** récupère les sources du commit, exécute Python et publie les rapports dans `reperes/index-legends/` sur la branche du monde. Ouvrir d’abord le `README.md` de ce dossier. Une modification du manuscrit seul ne déclenche aucun calcul. Aucun modèle de langage, service externe d’analyse ou clé d’API n’intervient dans cette étape.

Pour un monde déjà présent ou pour réappliquer les outils de `main`, ouvrir [Indexer un export Legends](https://github.com/Lillite/dwarf-fortress-legendes/actions/workflows/indexer-legendes.yml) dans Actions. Cliquer sur **Run workflow**, choisir **main** comme branche d’exécution et saisir le nom complet de la branche du monde dans **branche**. Les anciennes branches peuvent ainsi être indexées même si elles ne possèdent pas encore le workflow. Pour leurs futurs déclenchements automatiques sur push, il faut y intégrer le workflow de `main`.

Le sommaire, les CSV et le manifeste des empreintes SHA-256 restent sur la branche. La base complète est téléchargeable sous **Artifacts** dans l’exécution correspondante, sous le nom `legendes-sqlite-<commit source>-<tentative>`. Après l’expiration de l’artefact, une relance le reconstitue. La publication nécessite le droit d’écriture du jeton Actions sur la branche du monde. Un nouveau commit de chapitre intervenu pendant le calcul est conservé. Si le XML a changé entre-temps, le workflow ne publie pas les résultats de l’ancien XML.

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
