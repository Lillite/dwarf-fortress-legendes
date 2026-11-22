# SPEC éditoriale — Écrire une nouvelle ou un roman à partir des légendes de Dwarf Fortress

**Version 1.13 · Fiction textuelle · Rédaction originale dans la langue choisie par l’utilisateur**

Toute période documentée par l’export *Legends* peut fournir le sujet d’un livre. Un récit peut se dérouler entièrement dans l’histoire générée à la création du monde, commencer et finir des siècles avant la partie, suivre un peuple, une personne ou un objet à travers plusieurs lieux. Une forteresse peut y tenir la première place, apparaître en chemin ou être entièrement absente.

Le texte doit se suffire à lui-même. Quelqu’un qui ouvre le livre sans connaître le jeu doit pouvoir s’orienter, découvrir quelque chose qui l’intéresse et avoir envie de rester en compagnie de la voix qui raconte. L’exactitude se vérifie dans les sources. Le plaisir de lecture se travaille dans la façon d’entrer dans une scène, de faire entendre une pensée et de choisir l’instant où l’on quitte un personnage.

## 1. Trouver le sujet dans la matière disponible

Commencer par ouvrir le sommaire `reperes/index-legends/README.md` sur la branche du monde. L’index permet de retrouver, par identifiant, les rôles d’une figure dans les événements et les collections qui réunissent ces derniers. Lors d’une reprise, retrouver les identifiants déjà consignés dans le registre ou le plan. Si l’index manque ou correspond à un autre état des sources, le [régénérer](outils/README.md). La lecture ciblée de l’original reste possible pendant cette opération.

Relever ce qui éveille une curiosité précise : deux rencontres éloignées dans le temps, une œuvre qui survit à son auteur, une charge dont plusieurs titulaires connaissent des destins différents, un départ dont on retrouve la trace ailleurs. Revenir aux passages du XML qui soutiennent la proposition et citer les identifiants retenus. Un champ manquant ou un renvoi non résolu laisse une question ouverte. Une rencontre unique peut fournir une meilleure entrée dans le récit que cinquante mentions de la même personne.

### Seconde lecture avant de proposer les pistes

Dès le premier parcours, garder trace des points de départ qui ont produit les pistes et des domaines simplement recensés. Avant de présenter le registre à l’utilisateur, reprendre le fichier par ses domaines les moins explorés, même si plusieurs histoires semblent déjà prometteuses. Une liste de guerres indique combien le monde en a connues. Qui retrouve-t-on d’une bataille à l’autre, et dans quelle position ?

Choisir le point de départ d’après les lacunes du premier parcours. Pour les guerres, ouvrir les batailles rattachées aux conflits et relever, là où le XML les précise, les chefs de chaque camp, leur rôle, leur faction et le lieu. Regrouper les mentions de chaque chef à travers les batailles en conservant le camp qu’il commandait à chaque date. Rechercher ailleurs dans l’export les mentions de ces figures, groupes ou sites par identifiant et par catégorie, y compris dans d’autres conflits. Remettre les occurrences dans l’ordre et comparer les rôles, les alliés, les adversaires ou le sort des lieux. Si les premières pistes venaient surtout de biographies, on peut aussi partir d’une charge, retrouver ses titulaires successifs et chercher ce que chacun a reçu de son prédécesseur.

Ainsi, une générale qui commande l’attaque d’une ville en l’an 57 puis la défense d’une autre en l’an 90 offre un angle de récit. Qu’est-ce que défendre une ville pour quelqu’un qui en a attaqué une ? Les deux notices peuvent attester ce changement de rôle. Un changement d’allégeance, un remords ou une leçon tirée de la première attaque demanderaient d’autres indices pour être tenus pour acquis.

Consigner dans le [registre des pistes](reperes/pistes.md) le domaine repris, le chemin réellement suivi et les références trouvées. Selon la matière, ouvrir une piste, enrichir une piste existante ou noter en une phrase où la recherche s’arrête. Si les renvois manquent, préciser lesquels. Présenter les propositions après cette seconde lecture. Aucun thème n’a de place réservée et le nombre de pistes dépend de ce que les occurrences permettent de raconter.

### Examiner une piste prometteuse

Répondre dans le plan à quatre questions.

1. **Qu’avons-nous réellement ?** Citer les passages qui permettent de suivre la piste. Distinguer ce qui est connu à chaque extrémité et ce qui manque entre les deux.
2. **Par où le lecteur peut-il entrer ?** Trouver une personne, un geste ou une situation à sa portée. Pour raconter une migration ancienne, on peut entrer le matin où quelqu’un doit choisir ce qu’il emporte. Le lecteur découvrira la géographie quand le trajet lui donnera un sens.
3. **Qu’aurait-on plaisir à lire dans cette histoire précise ?** Ce peut être l’intimité d’une amitié, l’ironie d’un témoignage, le mystère d’une disparition, la découverte d’un usage ou l’émotion de voir un geste se transmettre. Nommer l’attrait qui justifierait de revenir au livre le lendemain.
4. **Quel est le plus petit périmètre qui rende justice au sujet ?** Délimiter la période et les figures suivies, puis esquisser une première sélection d’événements, révisable au fil de l’écriture. Une vie peut tenir dans une nouvelle racontée depuis son dernier matin. Une rencontre peut ouvrir un roman si ses conséquences transforment plusieurs existences.

### Évaluer si la piste a assez de matière

Avant d’arrêter le format, résumer la piste en quelques phrases en utilisant seulement ce que l’export permet d’établir. Retirer provisoirement les dialogues, les motivations supposées et les péripéties imaginées. Que reste-t-il de singulier à raconter sur ce monde ? Une entrée détaillée peut contenir une situation entière. Le même transfert d’objet mentionné dans les notices de trois personnes reste un seul événement, même si les trois notices permettent de mieux en comprendre les circonstances.

Pour chaque moment décisif envisagé, noter dans le plan **le passage source, ce qu’il apporte de distinct et ce que l’auteur devra imaginer**. Examiner en particulier le milieu du récit. Deux dates éloignées peuvent offrir une ouverture et une fin magnifiques tout en laissant entièrement indéterminé ce qui les relie.

| Ce que l’examen de l’export permet d’établir | Décision éditoriale |
| --- | --- |
| Un nom, une date ou une mention isolée, sans situation particulière à faire comprendre. | Garder la piste en réserve. Chercher dans le même export les personnes, lieux ou objets associés. Si rien ne l’éclaire, choisir un autre sujet. |
| Un épisode concret peut être mis en scène, mais il prend surtout son sens dans l’histoire de quelqu’un d’autre. | L’intégrer comme scène ou épisode secondaire d’un récit mieux documenté. |
| Une situation précise porte un récit autonome. On peut dire qui elle touche, ce qui change ou se révèle, et pourquoi le texte peut s’achever là. | Retenir la nouvelle. Un seul événement riche peut suffire, même si le fichier renseigne peu le reste de cette vie. |
| Plusieurs étapes distinctes, reliées par un personnage, un groupe, un objet ou une transformation, éclairent aussi le milieu du récit. Chacune renouvelle ce que le lecteur attend ou comprend. | Retenir le roman si ces étapes gagnent à être vécues en scène. Une série de faits répétitifs peut tenir en quelques lignes, quelle que soit sa longueur dans l’export. |

Une lacune peut nourrir un récit : on peut raconter ce que l’ignorance du sort d’un disparu fait à ses proches, si l’export donne prise sur leur histoire. En revanche, si l’on doit inventer la disparition, la recherche et les retrouvailles pour que la piste tienne, chercher un autre angle. **Le format est retenu lorsque le plan peut le justifier par des passages précis et par l’expérience de lecture qu’ils rendent possible.**

**Décision à consigner.** Noter dans le plan le matériau retenu et la forme envisagée. Au besoin, esquisser ce que le lecteur découvrira en entrant dans l’histoire et ce qui pourrait lui rester à la fin. Si ces lignes pourraient convenir à des dizaines d’autres mondes, y faire entrer un détail propre à cet export.

### Laisser chaque histoire trouver sa forme

Les outils de cette SPEC servent à résoudre des problèmes d’écriture quand ils se présentent. Choisir la voix, l’ordre des révélations et l’allure à partir de ce qui attire dans cette légende. Une histoire peut prendre la forme d’une lettre qui reste sans réponse, suivre une journée presque en temps réel ou laisser les décennies passer entre trois repas de famille. Le plan peut consigner cette intuition en une phrase et se préciser en écrivant.

**Inviter l’utilisateur à donner une direction.** Si son goût peut éclairer un choix, poser une question à laquelle on peut répondre par un mot, une image, un thème, une humeur ou une préférence précise. Pour une histoire de ville rebaptisée, on pourrait demander « Qu’aimerais-tu retrouver de l’ancienne ville en lisant ? » Une réponse comme « Peut-être les noms que les vieux continuent à employer… et quelque chose d’assez drôle » suffit pour écrire. Essayer par exemple une scène où deux voisins donnent au même visiteur des adresses différentes et se proposent tous deux de l’accompagner. Cette scène imaginée explore le souhait exprimé. La cause du changement de nom, le personnage principal et le dénouement peuvent se découvrir plus tard. Garder le « peut-être » dans les notes pour se souvenir de la liberté laissée.

L’utilisateur peut aussi répondre « surprends-moi », choisir entre des options ou en mêler plusieurs. S’il souhaite découvrir l’histoire en la lisant, parler de l’expérience qu’il aimerait vivre et réserver les péripéties, le résultat d’un tirage et la fin aux notes de travail et au manuscrit. Poursuivre dès que la réponse permet d’essayer une scène. Revenir sur la même question seulement si une décision qu’il a voulu garder reste en suspens ou si deux de ses consignes sont incompatibles.

Au moment de choisir une piste, « quelque chose sur l’exil » permet de rapprocher sa préférence des pistes du registre. Si plusieurs conviennent, lui proposer celles-ci en quelques mots. « Choisis une histoire d’exil pour moi, en français » permet déjà de retenir une piste documentée et de commencer la recherche. Vérifier la langue si elle reste à déterminer. Une délégation vaut pour le choix confié.

**Quand tirer au sort.** « Surprends-moi » laisse l’auteur choisir comment s’y prendre. « Au hasard » demande un tirage. Délimiter ce qui est confié au hasard, par exemple la voix qui racontera une scène, et tirer parmi des possibilités compatibles avec l’export et les préférences exprimées. Pour départager deux témoins, attribuer une face de pièce à chacun, tirer à pile ou face, puis écrire l’instant tel que le témoin désigné a pu le vivre. Un tirage peut aussi décider si un détail apparaît dès ce récit ou attend un autre livre. S’il s’agissait d’un essai et que la scène appelle un autre choix, noter la raison de la reprise. Une question restée sans réponse demeure en attente lorsque la décision appartient encore à l’utilisateur.

**Quand décider en écrivant.** L’auteur peut commencer en sachant ce qui attire le lecteur et découvrir en écrivant jusqu’où le conduira cette attente. Pour reprendre le travail, consigner dans le plan les mots de l’utilisateur, la part confiée à l’auteur ou au hasard et les décisions prises qui engagent la suite. Une possibilité encore ouverte peut le rester jusqu’à la scène où elle comptera.

**À la relecture**, si d’autres histoires de cette branche existent, rapprocher leurs premières pages ou leurs fins. Retrouve-t-on par habitude le même témoin qui raconte longtemps après les faits, la même révélation au même endroit, la même dernière phrase qui explique l’émotion ? Essayer un autre traitement là où la répétition affaiblit la singularité de la légende. Un motif récurrent peut aussi être un choix heureux, notamment dans un recueil.

## 2. Choisir entre la nouvelle et le roman

À partir de la matière établie dans le plan, choisir la forme qui donne à chaque moment la place qu’il mérite. Les repères suivants aident à construire la nouvelle ou le roman une fois le sujet retenu.

| Question | Nouvelle | Roman |
| --- | --- | --- |
| Où se trouve le centre ? | Dans une rencontre, une découverte, une décision ou une image qui change de sens. | Dans une transformation dont plusieurs étapes méritent d’être vécues : une relation se noue, se compromet, puis oblige à choisir autrement. |
| Où commencer ? | Près du moment décisif. Le passé entre par les détails qui changent la lecture du présent. | Au premier moment qui crée un attachement ou ouvre une attente capable d’évoluer. Des conséquences ultérieures justifieront de revenir sur le passé. |
| Que développer ? | Accorder de la place au geste, au dialogue ou à la perception qui donne son effet au récit. Quelques lignes peuvent franchir un siècle. | Développer les décisions et leurs conséquences. Un fil secondaire peut faire découvrir un autre milieu, éclairer le conflit depuis une position adverse ou mener sa propre vie en marge de l’intrigue. |
| Où finir ? | Au moment où le lecteur perçoit pleinement ce qui vient de changer. Une prise de conscience, un apaisement ou une image juste peuvent suffire. | Quand le lecteur peut éprouver ce qu’est devenue la question principale. Une réponse peut avoir un prix. Une incertitude peut désormais peser autrement sur les êtres qu’il a suivis. |
| Comment vérifier le choix ? | Si le récit continue après sa phrase la plus juste pour expliquer l’émotion, essayer de finir plus tôt. | Si le milieu répète la même situation avec d’autres dates, essayer une forme plus courte. Si le résumé escamote plusieurs choix dont dépend la fin, développer ces étapes. |

## 3. Respecter les événements et écrire dans les silences de l’export

Chaque nouvel export anglais ouvre une branche permanente depuis `main`, selon le [processus du dépôt](README.md). Identifier cette branche et l’export dans la fiche de `sources/`. Toutes les histoires et éditions tirées de cet export se travaillent sur cette même branche. La branche est conservée et ne doit jamais être fusionnée dans une autre branche.

### Choisir ce qui entre dans l’histoire

Le nombre d’éléments repérés pour une piste découle de l’analyse des occurrences et des renvois du XML, sans minimum, plafond ni cible par histoire. Plusieurs notices peuvent éclairer le même événement sous des angles différents : conserver leurs apports et compter le fait une seule fois. Cette première sélection forme une réserve de matière. Pendant l’écriture, l’auteur peut en retrancher, y ajouter un élément découvert plus tard ou en garder un pour un autre récit du même monde. Le bon dosage s’entend sur la page. Un enfant qui réclame toujours le quignon brûlé peut avoir sa place au repas de famille pour le simple plaisir de l’y rencontrer. Ce goût peut rester son seul trait connu, même à la dernière page du livre.

Un détail peut aussi passer discrètement dans le récit actuel et prendre de l’importance dans un autre roman. On peut tout aussi bien le garder dans les notes pour que le prochain livre ait le plaisir de le faire découvrir. Si un rapprochement mérite d’être retrouvé, noter dans le plan ce que le lecteur a effectivement vu, ou ce qui est resté hors texte, puis renvoyer vers la piste future dans le [registre de la branche](reperes/pistes.md) si elle existe déjà. Une reprise ultérieure reste une possibilité.

À la relecture, juger l’accumulation sur quelques pages. Si cinq noms nouveaux au milieu d’un repas font perdre le fil de la conversation, essayer d’en retirer, d’en déplacer ou d’en laisser un seul au détour d’une réplique. Si la version raccourcie perd la saveur du repas, rétablir ce qui manque. Une demande explicite de couverture intégrale demeure applicable à l’ensemble précis désigné par l’utilisateur.

Dans `reperes/chronologie.csv`, garder les références utiles aux faits exploités ou nécessaires pour vérifier la continuité. Un fait peut servir de repère de travail sans apparaître dans le livre. Une notice sans intérêt pour la piste peut être laissée de côté sans entrée ni justification individuelle. Lors d’une coupe, vérifier ce que sauront encore le lecteur et les personnages : si l’objet a changé de mains entre deux scènes, un détail à sa réapparition peut suffire à rendre ce passage intelligible.

### Relier et enrichir les notices brèves

Deux notices peuvent désigner le même lieu, la même personne ou le même objet. Vérifier les identifiants et les rôles, puis choisir ce qui rend leur rapprochement lisible : une conséquence établie, le retour d’un objet, deux souvenirs divergents, ou une simple ellipse. Une proximité de dates permet de situer deux épisodes. Une affirmation sur leur cause demande un appui distinct. Une motivation imaginée peut vivre dans la voix d’un personnage. Une rencontre inventée, un dialogue ou un détail sensoriel peuvent donner corps au passage dès lors qu’ils respectent les faits et le point de vue.

**Exemple fictif.** Une artisane grave une coupe. Des années plus tard, sa fille la rend à sa mère. Entre ces deux notices, l’export mentionne aussi la nomination d’un dignitaire local. Le récit peut passer directement aux retrouvailles. Autre possibilité, la fille a enveloppé la coupe dans un vieil avis de nomination. Sa mère reconnaît le nom sur le papier froissé. Un autre roman pourra un jour raconter l’histoire de ce dignitaire. En attendant, nous savons dans quoi la fille a transporté la coupe. La fille passe le pouce dans une rainure avant de lâcher l’objet : ce geste inventé donne à la mère le temps de reconnaître son travail. Si l’export tait la manière dont la fille a obtenu la coupe, le récit peut laisser ce trajet dans l’ombre. Dans les notes de scène, conserver les références de la gravure et de la restitution et signaler les inventions qui engagent la suite.

Pour qualifier ces raccords, utiliser les distinctions suivantes.

| Dans les notes de rédaction | Dans le texte destiné au lecteur |
| --- | --- |
| **Fait attesté.** Le fichier indique une action, un acteur, un lieu ou une date. | Respecter les éléments précisés et l’ordre établi. Deux faits datés de la même année peuvent rester d’ordre inconnu. |
| **Interprétation.** Une motivation ou un lien entre deux faits paraît plausible. | Donner à cette interprétation un point de vue identifiable. Une personne peut croire qu’un départ est une trahison alors que le lecteur dispose d’indices pour en douter. |
| **Ajout romanesque.** Un geste, un échange, une habitude ou un lien intime a été imaginé. | L’écrire avec la précision nécessaire à la scène. Vérifier sa compatibilité avec les faits, puis noter les ajouts qui engagent la suite. |

Si le matériau rapporte une croyance, une tradition ou un récit d’origine, préciser dans les notes **qui raconte quoi**. Le fait établi peut être qu’un peuple transmet une version de ses origines. Cette nuance ouvre une possibilité littéraire : montrer ce que cette version signifie pour la personne qui la reçoit. En cas de témoignages divergents, conserver leurs références et donner au lecteur les moyens de reconnaître quelle voix il entend.

### De l’export anglais à la langue du récit

Une fois la piste et la langue choisies, préparer pour chaque scène une courte fiche de faits dans la langue du manuscrit. Conserver les références anglaises et inscrire les noms récurrents dans le glossaire. Refermer ensuite la source et composer la scène directement dans cette langue, en choisissant ce que le personnage remarque, sa manière de parler et le rythme du passage. Un premier jet intégral en anglais est utile si l’anglais est la langue retenue.

À la fin du chapitre, rouvrir l’export et contrôler notamment les acteurs, les dates et les causes que suggèrent les mots de liaison. Relire ensuite le texte seul pour juger la voix et la fluidité. Pour une édition dans une autre langue, traduire le manuscrit stabilisé et conserver l’export comme référence factuelle commune.

## 4. Donner vie aux personnages et à l’intrigue

**Trouver le fil conducteur.** Dans le plan, dire en une ou deux phrases ce que le lecteur espère, redoute ou cherche à comprendre, même quand le récit change de lieu ou de voix. Le but d’un personnage peut porter ce fil. S’il obtient ce qu’il voulait, que lui en coûte-t-il, ou à quoi s’est-il engagé ? Le lecteur peut aussi se poser une question qui échappe au personnage. Dans l’exemple de la coupe rendue après l’exil, la voyageuse veut simplement remettre l’objet. Celui qui le reçoit, en voyant la poche raccommodée, commence à comprendre les années pendant lesquelles elle l’a porté. Ce déplacement peut suffire à une nouvelle. Pour un roman, chercher où l’attente se renouvelle au fil des épisodes. L’ordre des scènes et la fin peuvent évoluer au cours de la rédaction.

**Choisir le regard qui a le plus à nous faire découvrir.** La personne qui règne connaît peut-être déjà l’issue d’une négociation. Celle qui attend à la porte peut en reconnaître le résultat à la façon dont on lui rend son manteau. Choisir la voix en fonction de cet accès singulier aux faits. Préciser ce que le personnage désire, ce qu’il ignore, à qui il tient et ce qu’il aurait du mal à s’avouer. Une même méthode convient à un récit à la première personne, à la troisième personne ou à plusieurs voix.

**Donner une conséquence aux épisodes.** Entre deux scènes majeures, chercher ce que la première a changé pour la seconde. Après ce qui vient d’arriver, qu’est-ce que quelqu’un peut encore faire, espérer ou croire ? Une promesse peut rendre une décision plus difficile. Un deuil peut donner un sens neuf à une invitation ancienne. Lorsque l’export ne relie pas deux faits, on peut les rapprocher par un contraste ou un écho : la même coutume vécue librement à une époque et comme une obligation à une autre. Rendre ce rapprochement lisible sans lui inventer une cause historique.

**Faire une place à la vie ordinaire.** Le plaisir peut venir du caractère de quelqu’un, d’un détail drôle, d’une attention inattendue ou du fonctionnement étrange d’un usage. Accorder à ces moments assez de place pour qu’ils existent par eux-mêmes. Savoir de quoi deux amis riaient ensemble donne du poids à la première conversation où l’un d’eux cesse de rire.

**Rendre le temps sensible.** Pour franchir plusieurs générations, choisir ce qui passe de l’une à l’autre et montrer ce qu’il devient entre de nouvelles mains. Une date situe l’ellipse. Une personne qui hésite à utiliser l’outil que son aïeule maniait familièrement en fait sentir la durée. Vérifier séparément quand un événement survient, quand chaque personnage l’apprend et quand le lecteur le comprend.

### Faire vivre un événement décisif

Pour un moment dont dépend le livre, entrer assez tôt pour que le personnage ait encore quelque chose à faire, à espérer ou à redouter. Que voulait-il dans la minute qui précède ? Quel geste l’événement interrompt-il ? Qui devra vivre avec ce qui vient d’arriver ? Ces questions aident à trouver la scène. Selon le sujet, elle pourra tenir dans trois lignes ou prendre tout un chapitre.

**Rechercher le pourquoi.** Distinguer ce qui provoque l’événement, ce qui amène le personnage à cet endroit et ce que voulait l’auteur de l’acte. « Tué par une boule de feu » donne la cause immédiate du décès. Pour savoir qui l’a lancée ou ce que cette personne cherchait à faire, remonter aux notices associées. Si un mobile est attesté, choisir quand et par qui le lecteur pourra le découvrir. Si le mobile demeure inconnu, le romancier peut laisser ouverte cette question et donner au héros une raison intime d’être là. Il peut également prêter une intention plausible à un personnage, en veillant à ce que cette invention respecte ses actes connus. Consigner les choix importants dans les notes : dans la prose, écrire la scène pleinement, sans interrompre le lecteur pour commenter sa fabrication.

Deux outils d’écriture éclairent ce travail.

- **La focalisation.** Choisir à quelle expérience le lecteur a accès. Un ancien adversaire pourrait reconnaître le héros à sa façon de rire tout en ignorant ce qui l’amène à se battre. En racontant depuis cet adversaire, on peut rendre leur rencontre très intime et laisser le reste de la bataille hors de sa vue. [Burkhard Niederhoff, « Focalization », *The Living Handbook of Narratology*](https://www-archiv.fdm.uni-hamburg.de/lhn/node/18.html)
- **La vraisemblance de l’action.** Aristote invite à penser ce qu’une personne peut vraisemblablement faire dans une situation donnée et comment une action en appelle une autre. À la relecture, chercher le détail qui rend un geste crédible. Quelqu’un qui revient chercher un ancien ennemi peut hésiter à lui offrir la main, puis lui présenter l’épaule. Ces quelques secondes donnent au lecteur le temps de mesurer ce qu’il lui en coûte. [Aristote, *Poétique*, chapitre IX](https://beta.perseus.tufts.edu/urn:cts:greekLit:tlg0086.tlg034.butcher1911-eng2:9/)

### Exemple fictif — le héros et la boule de feu

**Données de départ.** Le héros a combattu trois adversaires. Il est mort frappé par une boule de feu. Dans cet exercice, l’origine du projectile, un éventuel mobile et l’intervalle entre les combats et la mort sont inconnus.

> L’homme qui se penchait sur Senn avait une dent de devant cassée en biais. Senn la lui avait cassée lui-même. Il ramena le menton contre sa poitrine et attendit le coup.
>
> — Si tu veux que je te relève, dit l’homme, il va falloir lâcher ma manche.
>
> Senn desserra les doigts. L’autre s’assit à côté de lui sur la marche, passa son épaule sous son bras et attendit qu’il soit prêt. C’était cette patience qui embarrassait Senn. Il aurait préféré qu’on le tire d’un coup, quitte à lui faire mal.
>
> Ils venaient de se mettre debout quand Senn vit leur ombre monter le long du mur. En tournant la tête, il aperçut dans l’embrasure une boule de feu, à hauteur d’homme. Elle frappa son compagnon dans le dos. Ils retombèrent sur la marche. Cette fois, Senn eut beau lui rendre l’épaule, il ne parvint pas à le rasseoir.
>
> Une femme les rejoignit. Elle posa la main contre le cou de l’homme et la retira.
>
> — Il est mort. Tu le connaissais ?
>
> Senn aurait su lui dire de quel côté la dent était cassée. Ce fut elle qui lui apprit qu’il s’appelait Orim.

**Choix de l’auteur.** Senn incarne ici l’un des trois adversaires. La dent cassée, la blessure de Senn et le secours que lui porte le héros sont imaginés. La dent paraît d’abord annoncer un règlement de comptes. À la fin, elle dit combien Senn savait peu de celui qui l’a aidé. Ce fil justifie de raconter la mort depuis sa place. Le lecteur comprend pourquoi le héros se trouvait sur la marche au moment de l’impact, tandis que l’intention à l’origine du feu reste ouverte. Les deux autres combats pourront trouver leur place ailleurs si leur souvenir éclaire une scène.

**Question de relecture.** Une fois refermé le dossier de l’export, que reste-t-il de cette page au-delà de l’information « le héros meurt » ? Ici, c’est le moment où Senn essaie de rendre à cet homme l’épaule qu’il vient de lui offrir. Chercher pour chaque scène importante le geste, la parole ou le silence que le lecteur pourra emporter avec lui.

## 5. Écrire un texte agréable à lire

| Élément | Consigne de rédaction ou de reprise |
| --- | --- |
| Première page | Donner assez d’indices pour que le lecteur puisse se représenter ce qui se passe et sentir pourquoi cela compte pour quelqu’un. On peut entrer en pleine action ou prendre le temps d’installer le cadre. Vérifier l’effet obtenu à la [relecture autonome de compréhension](#relecture-autonome-de-compréhension). |
| Noms et histoire ancienne | Faire place aux noms selon l’attention que le passage peut leur accorder. Un nom entrevu peut rester en arrière-plan. Pour retrouver quelqu’un après une longue absence, rappeler le lien qui comptait dans la scène précédente. Garder les variantes linguistiques et les homonymes dans le glossaire de travail. |
| Scènes et transitions | Développer les minutes dont le lecteur a besoin pour croire à une décision. Résumer les années dont seul l’effet compte. Après une ellipse, choisir un repère qui indique où, quand et auprès de qui nous reprenons le fil. |
| Voix et dialogue | Demander ce que chacun espère obtenir en parlant et ce qu’il préfère taire. Relire le passage en masquant les incises : si les répliques semblent interchangeables, revoir le vocabulaire, les détours ou les silences de chacun. |
| Phrase et rythme | Relire un passage à voix haute pour repérer une syntaxe qui oblige à revenir en arrière, des attaques de phrases identiques ou trois explications de la même émotion. Varier l’allure avec l’expérience du personnage. Une hésitation mérite parfois une phrase longue. Un mot bref peut clore la scène. |
| Dernière page | Choisir le geste, l’image ou la phrase qui fait éprouver le chemin parcouru. Essayer la fin avec et sans son dernier paragraphe. Garder la version qui laisse au lecteur la place de comprendre et de ressentir par lui-même. |

**Fiche de scène facultative.** Dans les notes du chapitre ou de la nouvelle, indiquer le moment et le lieu, le regard suivi, ce qui intéresse le lecteur à l’entrée, ce qui change avant la sortie et les références utiles. Garder une scène contemplative si sa disparition nous prive d’une façon singulière d’habiter ce monde.

## 6. Exemple de travail — un objet transmis pendant un exil

Cet exercice reprend le motif de l’objet passé de main en main, déjà présent dans les notes éditoriales du projet. Les circonstances ci-dessous sont imaginées pour illustrer la méthode. Pour un manuscrit, les personnes, les lieux et les transmissions seraient d’abord à vérifier dans l’export choisi.

**Avant d’en faire un livre.** Si l’export mentionne seulement l’existence de l’objet, la scène de restitution ci-dessous reste un exercice d’écriture. S’il documente le départ de sa détentrice avec l’objet et sa remise à son créateur, ces deux faits offrent déjà un point d’appui pour une nouvelle. Pour développer les années d’exil en roman, chercher ce que d’autres passages permettent d’y raconter. Des notices répétant que l’objet est en sa possession justifient la continuité de sa garde. Une transmission contestée en cours de route, si elle est consignée, donne un épisode avec un enjeu propre.

**En nouvelle.** Entrer le jour où une personne qui a porté un objet pendant son exil vient le rendre à son créateur. Pour l’un, cette journée répare une perte. Pour l’autre, elle en ouvre une. Le voyage entier peut tenir dans l’usure qu’il découvre sur l’objet. Le centre de la nouvelle est l’instant où il comprend ce que signifie pour elle « rendre ».

> Il chercha du pouce l’entaille qu’il avait laissée sur le bord. Elle avait presque disparu.
>
> — Ça accrochait la doublure, dit-elle.
>
> Il imagina d’abord une lime. Puis il vit la poche au creux de son manteau, reprise avec du fil de trois couleurs. Il avait souvent pensé à l’endroit où se trouvait son ouvrage. Jamais à ce qu’il en coûtait de le porter.

**En roman.** Cette même restitution pourrait conclure un récit commencé bien avant l’exil. Il faudrait alors trouver dans le matériau de quoi soutenir les étapes intermédiaires. Qui a confié l’objet à cette personne ? Quand a-t-elle eu une raison sérieuse de s’en séparer ? Quelle relation a-t-elle engagée en le gardant ? Si plusieurs de ces étapes ont des conséquences distinctes, chacune peut mériter une scène. Si toute l’émotion se concentre dans la poche raccommodée et le retour, la nouvelle possède déjà sa juste ampleur.

## 7. Décider si le texte est prêt

### Relecture autonome de compréhension

Dès le premier jet, reprendre l’ouverture et les passages où le cadre peut prêter à confusion : changement d’époque ou de point de vue, rêve, spectacle, jeu de rôles ou récit raconté par un personnage. Lire le manuscrit dans l’ordre en laissant de côté le plan, le XML et les notes d’auteur. À chaque passage, s’en tenir à ce que le lecteur a déjà pu apprendre, y compris dans les chapitres précédents. Une explication donnée plus loin aura son effet au moment où il la lira.

À la première pause naturelle, répondre par écrit ou mentalement à deux questions : **« Quelle scène concrète puis-je imaginer avec ces mots ? »** et **« Qu’est-ce qui compte pour quelqu’un ici, et qu’ai-je envie de découvrir ? »** Appuyer les réponses sur les mots du passage. Chercher une autre interprétation plausible dans ce monde. Si elle entretient le mystère ou l’humour voulu, la laisser jouer. Si elle masque ce qui se passe ou pourquoi on s’y intéresserait, avancer le plus petit indice qui éclaire la scène : un geste, un mot précis, la raison d’une visite. Relire ensuite depuis l’entrée du passage pour vérifier l’effet de la correction.

**Exemple du roi de pâte.** Dans un monde fantastique, un petit roi que l’on soulève et dont on soutient le menton peut se lire comme un souverain vivant et fragile. Dire qu’Odda joue la reine éclaire son rôle à elle. Montrer Buh qui pose sur la table le roi qu’elle a *modelé* rend la figurine immédiatement identifiable. Avancer la promesse du poème pour le souper des laveuses répond à l’autre question : on comprend pourquoi Buh tient à réussir sa petite représentation. On peut alors laisser au lecteur le plaisir de découvrir ce qu’Odda a fait du caillou.

### Lecture du manuscrit entier

Relire ensuite le texte d’une traite. Les questions ci-dessous servent à la révision autonome. Si une lecture humaine est souhaitée avant la finalisation ou l’export EPUB, elles peuvent aussi recueillir ce qu’une personne a effectivement compris et ressenti. La rédaction et les reprises courantes avancent sans validation scène par scène.

- **« À quel moment as-tu eu envie de continuer ? »** La réponse aide à voir si le véritable début du récit se trouve plusieurs pages après son ouverture.
- **« Quel passage as-tu pris plaisir à lire, et où ton attention a-t-elle baissé ? »** Distinguer un ralentissement apprécié d’une accumulation de noms, d’explications ou d’épisodes qui se répètent.
- **« Qu’as-tu compris de son choix, et qu’as-tu ressenti à la fin ? »** Accueillir les interprétations différentes. Reprendre le texte si un élément indispensable pour comprendre ce qui arrive manque sur la page.
- **« Quelle image, quelle personne ou quelle phrase t’est restée ? »** S’en servir pour identifier ce que le texte fait particulièrement bien et préserver cette qualité lors des coupes.

Reprendre le fil du livre en s’appuyant uniquement sur le manuscrit. Qu’attendait-on à l’ouverture ? Quel passage a fait évoluer cette attente ? Après la dernière page, quel geste du début comprend-on autrement, ou quelle question reste avec nous ? Si des épisodes majeurs semblent interchangeables, imaginer leur ordre inversé et repérer ce qui perd de sa force ou devient plus clair. Appliquer cet essai là où l’intérêt retombe. Une conversation dont on aime la compagnie peut garder tout son temps.

Faire ensuite une lecture de contrôle. Vérifier les faits racontés contre l’export, puis relire les passages qui encadrent une ellipse pour repérer un personnage, un savoir ou un objet qui apparaîtrait sans explication. Vérifier aussi les éventuels événements expressément demandés. Suivre les déplacements, les changements de détenteur, les savoirs des personnages et les noms d’une scène à l’autre. Pour une autre langue, `reperes/glossaire.csv` relie les formes d’origine et les formes retenues. La traduction doit aussi retrouver la voix et le rythme propres au livre.

Avant de valider la longueur définitive, reprendre la justification du format dans le plan. Si plusieurs chapitres répètent la même information ou si les épisodes inventés portent désormais toute l’intrigue, resserrer le récit autour des passages les plus féconds et vérifier que les coupes laissent les transitions compréhensibles.

Le manuscrit est prêt pour la validation éditoriale lorsque les faits racontés respectent la source, que les événements expressément demandés sont couverts, que le lecteur peut suivre le récit de façon autonome et que la forme choisie donne à ses meilleurs moments la place qu’ils méritent.

**Documents de travail du projet** — [Processus éditorial](README.md) · [Suivi de reprise](REPRISE.md) · [Fiche de l’export](sources/README.md) · [Pistes](reperes/pistes.md) · [Chronologie](reperes/chronologie.csv) · [Glossaire](reperes/glossaire.csv) · [Modèle de plan](manuscrits/fr/plan.md) · [Modèle de chapitre](modeles/chapitre.md)
