# Lire un export Legends pour préparer une histoire

Partir d’une question de récit, par exemple « Qui a porté cette coupe avant sa restitution ? » Le fichier anglais de la branche est la référence pour ce monde. Commencer par relever sa version si elle est connue, sa racine et les sections présentes. Le guide du wiki décrit notamment une structure sous `df_world` et signale que sa description, héritée de versions antérieures, peut différer du fichier reçu. [Dwarf Fortress Wiki — XML dump](https://dwarffortresswiki.org/index.php/XML_dump)

## Retrouver les entrées utiles

| Section à chercher | Question de lecture |
| --- | --- |
| `historical_events/historical_event` | Quelle action est enregistrée ? Lire son type, sa date et les champs de participants ou de lieu présents pour ce type. |
| `historical_figures/historical_figure` et `entities/entity` | Quel personnage ou quel groupe un événement désigne-t-il ? Vérifier le rôle indiqué dans la notice. |
| `sites/site` et `artifacts/artifact` | S’agit-il bien du même lieu ou du même objet dans deux notices ? Retrouver son entrée et son identifiant. |
| `historical_event_collections/historical_event_collection` | Le fichier regroupe-t-il déjà certains événements, par exemple dans une guerre ? Examiner les épisodes qui éclairent la piste. Leur appartenance au même ensemble laisse ouverte la question de leurs causes. |

Ces chemins sont des repères à confirmer sur le fichier reçu. [Description des sections](https://dwarffortresswiki.org/index.php/XML_dump#Contents_of_the_vanilla_legends.XML_file)

## Exemple de parcours par identifiant

1. Retrouver l’objet par son nom dans la section des artefacts et relever son `id`. Distinguer les homonymes. Pour citer l’entrée, conserver le fichier, la section et l’identifiant.
2. Dans une notice de création qui contient `artifact_id`, suivre la valeur vers l’entrée de l’objet. Si la notice désigne aussi un créateur ou un site, vérifier le libellé du champ avant de résoudre chaque renvoi dans sa propre section. Dans une version ancienne documentée, ces deux champs sont `hist_figure_id` et `site_id`. [Exemple de notice de création, wiki v0.31](https://dwarffortresswiki.org/index.php/v0.31:XML_dump#artifact_created)
3. Rechercher les autres événements qui mentionnent cet objet. Par exemple, sur un fichier utilisant cette structure, la requête XPath `/df_world/historical_events/historical_event[artifact_id='42']` retrouve les notices qui portent précisément ce champ pour l’artefact 42. Le numéro est fictif. Pour les autres types de notices, vérifier comment la référence est écrite. Un nombre identique dans un champ de site ou de personnage désigne une autre catégorie.
4. Ordonner les résultats à la précision connue et noter dans le dossier de recherche ce que chaque notice établit. Deux mentions éloignées d’un objet peuvent justifier un rapprochement littéraire, tout en laissant inconnus ses détenteurs intermédiaires. Garder le trajet ouvert ou le traiter comme une invention dans les notes de travail.

## Export standard et complément DFHack

L’export standard suffit pour commencer. Si le même export comprend un fichier `legends_plus.xml` produit par DFHack, chercher si ce complément précise une notice utile au sujet. Recouper les entrées par monde, catégorie et identifiant, conserver les deux références quand elles se complètent, et ne compter qu’une fois le même événement. Si une référence reste introuvable, consigner cette limite dans la [fiche de l’export](README.md). [Documentation DFHack — exportlegends](https://docs.dfhack.org/en/stable/docs/tools/exportlegends.html)

## Suivre un lien dans l’index du monde

Partir du sommaire `reperes/index-legends/README.md` sur la branche d’export. Si le rapport du domaine ne répond pas à la question, consulter la base SQLite à partir de la catégorie et de l’identifiant. Pour un personnage, la recherche inverse retrouve les notices dont un champ reconnu désigne cette figure. Lire le nom de ce champ : dans une rançon, la personne enlevée, la personne qui exige le paiement et celle qui paie occupent trois rôles différents.

Pour tout fait décisif, revenir à la notice citée, dans le fichier qui la porte. Si un renvoi est signalé comme incomplet ou si un domaine est peu couvert, examiner les champs de l’original avant de conclure qu’une mention manque. Le [mode d’emploi de l’index](../outils/README.md) précise comment reconstruire et interroger la base.
