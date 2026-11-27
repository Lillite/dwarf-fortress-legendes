# Dossier documentaire de P014

## Choix enregistré

Le 27 novembre 2026, l’utilisateur a choisi [P014](../../../reperes/pistes.md#p014) et demandé « Ecrit P014 ». Nouvelle complète en français sur la branche `legendes/region1-an-100-02-28-story-writer`. La demande reprend le parcours d’Asmel, de son désir d’immortalité en 35 au recrutement de Solon en 96. La version publiée ici est une création propre à cette branche.

## Événements et passages anglais

Les identifiants ci-dessous appartiennent aux `historical_events` du [XML de région 1](../../../sources/README.md). Les [notices de la piste](../../../reperes/index-legends/dossiers/P014.md) donnent les champs complets, les lignes du XML et les liens directs. Les années sans précision intra-annuelle restent à l’année.

| Année et précision (`seconds72`) | Fait vérifié dans l’export | Notice et champs |
| --- | --- | --- |
| 2 et 54, dates intra-annuelles inconnues | Ajout puis retrait d’un lien entre Asmel et Kib. Les fiches individuelles identifient les anciens époux et leurs enfants communs. | 926 et 18636, `hfid` et `hfid_target`. Figures 347 et 352, `hf_link/link_type=former spouse` et `child`. |
| 35, 369600 | Asmel se donne pour but l’immortalité. | 9484, `hfid=352`, `secret_goal=immortality`. |
| 37, 109200 | À Boardhammers, Asmel prend possession de The Fated Tombs et en apprend un secret. | 10137, `artifact_id=76`, `site_id=76`. 10138, `student_hfid=352`, `interaction=SECRET_14`. L’objet et le site appartiennent à deux séries d’identifiants. |
| 46, 159600 | Asmel dépose l’objet à Boardhammers. | 14304, `artifact_id=76`, `hist_figure_id=352`, `site_id=76`. |
| 61, 75600 | À Labortakers, Zuglar et Goden, deux fils de Kib et d’Asmel, sont tués au même instant enregistré. | 24187 et 24200, `hfid=1113` et `1382`, `site_id=150`, `slayer_hfid=170`. Le temps écoulé avant qu’un messager apporte la nouvelle reste ouvert. |
| 61, 218400 | À Blockadedeath, Asmel recrute Kib en lui offrant l’immortalité. | 24323, `site_id=210`, `corruptor_hfid=352`, `target_hfid=347`, `action=bring into network`, `method=offer immortality`, balise `successful`. |
| 62, 386400 | On confronte Asmel à Boardhammers au sujet de son absence de vieillissement. Son installation à Diamondgalley est attribuée à la fuite. | 25208, `reason=ageless`. 25209, `reason=flight`, `state=settled`, `site_id=179`. Même repère horaire. |
| 64, 25200 | Asmel s’établit à Severetrots pour étudier. | 26389, `reason=scholarship`, `site_id=197`. |
| 83, 151200 puis 294000 | Un jaguar tue Kib pendant la bataille de Rockglistened. Plus tard dans l’année, Tun, fille de Kib et d’Asmel, est en visite à Gorgespiraled. | 46051, `slayer_race=JAGUAR`, `site_id=293`, collection 4235. 46404, `hfid=735`, `state=visiting`, `site_id=168`. |
| 96, 134400 | À Boardhammers, Solon Beachedglaze accepte d’entrer dans le réseau d’Asmel à la suite de la seconde offre d’immortalité. | 65164, `target_hfid=350`, `corruptor_hfid=352`, `site_id=76`, `method=offer immortality`, balises `successful` et `failed_judgment_test`. |

## Relations, lacunes et part de fiction

Les notices des figures 347 et 352 nomment Tun (735), Zuglar (1113) et Goden (1382) parmi leurs enfants. Le décès de Kib établit qu’elle pouvait être tuée. Les deux recrutements aboutissent, mais l’export ne décrit aucun effet du secret sur le vieillissement de Kib ou de Solon. L’objet conserve sa désignation originale, *The Fated Tombs*. Sa forme, le contenu du secret et un éventuel procédé de transmission restent inconnus.

Les lettres, le mot rayé, le marché, le témoin aux doigts blessés, la moustache d’encre et les paroles échangées relèvent de la fiction. La visite de Tun à Gorgespiraled est attestée après la mort de sa mère. Le déplacement d’Asmel pour lui annoncer cette mort et la rencontre entre père et fille ont été imaginés. Le lieu où Asmel reçoit la nouvelle découle dans le récit de son installation antérieure à Severetrots. Les conditions pratiques des recrutements et les oignons de Solon relèvent également de la fiction. Sa fiche de figure porte la valeur `associated_type=PLANTER`.

## Texte livré

- [De la main de ton père · nouvelle intégrale](nouvelle.md)
- [Quatrième de couverture](0.md)
- [Chronologie](../../../reperes/chronologie.csv) et [glossaire](../../../reperes/glossaire.csv)

Le texte suit quatre dates dans l’ordre. Le souhait de l’an 35, l’acquisition du secret et le dépôt de l’objet sont racontés par Asmel dans la scène de 61. Les notices mobilisées sont associées à la nouvelle dans la chronologie. Le [suivi de la branche](../../../REPRISE.md) enregistre son achèvement.
