# Fiche de l’export Legends de région 1

| Repère | Valeur vérifiée |
| --- | --- |
| Branche permanente | `legendes/region1-an-100-02-28-story-writer` |
| Original | [region1-00100-02-28-legends.xml](region1-00100-02-28-legends.xml) |
| Chemin dans le dépôt | `sources/region1-00100-02-28-legends.xml` |
| Repère du monde | Le XML ne donne aucun nom global au monde. `region1` vient du nom du fichier. Orbliving et Earthlenses sont deux forteresses distinctes, respectivement les sites 90 et 676. |
| Date portée par le nom du fichier | An 100, mois 02, jour 28. Des événements sont enregistrés pour chacune des années 1 à 100. Certaines naissances sont antérieures à l’an 1. |
| Langues rencontrées | Balises, rôles, types et descriptions de formes en anglais. Plusieurs titres d’œuvres et les noms d’ères sont en français, parfois mêlé d’anglais. Les graphies citées sont conservées. |
| Version du jeu et compléments | Version non renseignée. Un seul fichier reçu. |
| Empreinte de l’original | 50 320 459 octets. SHA-256 `b6c4315398494c30bce5ce6d491bc24e7fa64a8a6ee9a17af7ff55ee02fdfbfc`. Objet Git `90718a486aeadf84e93cfd249068c17de2f15fbc`. |

## Inventaire des quinze sections

| Section sous `df_world` | Entrées |
| --- | ---: |
| `regions` | 779 |
| `underground_regions` | 405 |
| `sites` | 692 |
| `world_constructions` | 0 |
| `artifacts` | 470 |
| `historical_figures` | 12 132 |
| `entity_populations` | 243 |
| `entities` | 1 031 |
| `historical_events` | 57 526 |
| `historical_event_collections` | 5 952 |
| `historical_eras` | 3 |
| `written_contents` | 2 186 |
| `poetic_forms` | 78 |
| `musical_forms` | 95 |
| `dance_forms` | 88 |

Les événements se répartissent entre 96 types. Les collections comprennent notamment 44 guerres. Les identifiants d’événements sont discontinus, de 0 à 72672. Les trois notices d’ère portent successivement « Age du mythe » (`start_year=-1`), « Age légendaire » (75) et « Age du mythe » (76).

## Lire et vérifier le fichier

- L’original déclare CP437 et utilise des fins de ligne CRLF. Les douze premières notices d’artefacts contiennent chacune un octet 0x11 avant le nom de l’objet et un octet 0x10 après. Un analyseur XML 1.0 strict s’arrête sur le premier à la ligne 12 801. Pour la lecture, décoder les octets en CP437, rendre ces deux signes par ◄ et ► dans une copie en mémoire, puis adapter la déclaration d’encodage à UTF-8 avant l’analyse. Cette opération conserve les textes et les numéros de ligne. Le fichier déposé garde ses octets d’origine.
- Les renvois sont propres à chaque catégorie. La fiche du livre physique 61 renvoie par `item/page_written_content_id=47` à un texte. Le numéro de structure 3 de la Chapelle symétrique n’a de sens qu’à l’intérieur du site 159. Les champs répétés, tels les `expelled_hfid` de l’événement 18759, désignent plusieurs personnes.
- Les identifiants de personnes portent plusieurs noms selon le rôle. L’événement 29454 distingue la personne rançonnée, celle qui demande la rançon et celle qui paie. Les liens `hf_link` d’une fiche de figure permettent de vérifier la parenté.
- Les valeurs `-1` s’interprètent selon le champ. Pour la précision intra-annuelle, `seconds72=-1` laisse seulement l’année connue. Deux événements au même instant peuvent documenter des aspects différents d’une même scène. Une création d’œuvre, sa mise en objet et son dépôt peuvent ainsi former un seul épisode.
- Les balises vides portent parfois l’information décisive. L’événement 43587 contient à la fois `<wrongful_conviction/>` et `<death_penalty/>`. La notice de création 11973 contient `<name_only/>`, qui invite à distinguer la nomination de l’objet de sa fabrication.
- Une collection peut préciser le contexte. Le duel 2498 est rattaché à la bataille 2497 et celle-ci à la guerre 2496. La section vide `world_constructions` coexiste avec des événements de type `created world construction`.

Les pistes, les noms de travail et les passages à vérifier figurent dans le [registre documentaire](../reperes/pistes.md).
