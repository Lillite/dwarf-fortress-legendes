# Index de l’export Legends

Consulter un relevé selon la question posée. Les numéros renvoient aux notices du XML de ce monde.

| Relevé | Ce qu’il permet de retrouver |
| --- | --- |
| [Routes commerciales](routes.csv) | Transactions par marchand, site de départ et destination. |
| [Successions](successions.csv) | Renversements groupés par entité et profil local de charge. |
| [Parcours des artefacts](objets.csv) | Notices de possession, perte ou dépôt pour le même objet. |
| [Rencontres répétées](rencontres.csv) | Paires de figures citées dans plusieurs notices de confrontation, intrigue, enlèvement ou apprentissage. |
| [Types d’événements](types-evenements.csv) | 57526 événements dans 96 types. Un exemple par type pour explorer d’autres domaines. |
| [Batailles](commandements.csv) | 203 batailles. Camp et chef pour chaque notice d’attaque ou de bataille en rase campagne. |
| [Chefs ayant attaqué et défendu](chefs-attaque-defense.csv) | 8 figures. Les deux événements donnés en exemple renvoient au relevé des batailles. |
| [Œuvres et exemplaires](oeuvres.csv) | 2186 textes. Chaque ligne relie auteurs, composition et objets porteurs documentés. |
| [Histoire des lieux](lieux.csv) | 451 mentions de fondation, destruction, reprise, occupation ou abandon, classées par site. |
| [Installations encadrant une destruction](retours.csv) | 8 rapprochements où une même figure s’installe au même site avant et après une destruction datée. |
| [Références à vérifier](references-a-verifier.csv) | 21379 observations groupées par champ et raison. Le détail est dans la table SQLite `issues`. |

Une même notice peut documenter plusieurs histoires. Un rôle militaire indique la position dans la bataille. Une nouvelle installation atteste deux présences, le trajet et ses raisons restent à établir. Les dates à l’année et les mentions simultanées conservent leur précision d’origine. Une valeur vide ou `-1` dans un relevé de commandement marque une donnée non renseignée.

## Sources indexées

- region1-00100-02-28-legends.xml · SHA-256 `b6c4315398494c30bce5ce6d491bc24e7fa64a8a6ee9a17af7ff55ee02fdfbfc`

[Dossiers par piste, contrôles et relecture](dossiers/README.md)
