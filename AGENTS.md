# Travailler sur la variante Story Writer

Sur `main-story-writer`, maintenir les instructions communes, la SPEC documentaire, les gabarits, les outils et leurs tests. Consigner les événements, citations, décisions et manuscrits propres à un monde sur sa branche d’export. Ces consignes s’appliquent aussi aux branches d’export créées depuis cette variante.

## Écriture exclusivement avec Story Writer

1. **Préparation documentaire.** L’import, l’index, la chronologie, le glossaire, la recherche de liens, la proposition et la sélection de pistes, le dossier factuel et les vérifications de sources suivent la [SPEC](SPEC_Roman_Dwarf_Fortress.md). Ces opérations peuvent s’exécuter même si Story Writer est absent.
2. **Entrée dans un travail littéraire.** Avant tout plan narratif, essai de scène, rédaction, continuation, dialogue, titre, synopsis, quatrième de couverture, traduction littéraire, critique, relecture stylistique ou réécriture, vérifier que le plugin officiel [Story Writer](https://chatgpt.com/plugins/plugins_6ab235d1cda08191afa7ba8c81fb0429) est disponible dans la session qui réalise le travail. Charger et appliquer sa compétence générale ou la compétence spécialisée appropriée fournie par ce plugin. Un lien, une mention dans la demande ou une installation antérieure ne prouvent pas que la compétence est utilisable dans cette session.
3. **Plugin disponible.** Lui remettre le dossier de la piste, les contraintes de l’utilisateur et les textes concernés. Toute composition ou modification littéraire, même un court extrait proposé en conversation, passe exclusivement par Story Writer. Les outils du dépôt classent les livrables et vérifient leurs références.
4. **Plugin absent ou inutilisable.** Si aucune compétence officielle appropriée ne peut être chargée ou utilisée, arrêter la partie littéraire et afficher exactement le message ci-dessous. Aucun brouillon, extrait, remplacement manuel ou fichier littéraire de substitution. Conserver les livrables antérieurs. Pour une demande mixte, achever la préparation documentaire demandée et indiquer l’étape littéraire bloquée dans le suivi de reprise du monde.

> ERREUR — Story Writer indisponible. Activez le plugin Story Writer dans cette conversation, puis relancez la demande d’écriture.

Les workflows GitHub effectuent des traitements documentaires et techniques. L’accès au plugin se vérifie au moment de la demande dans la session d’écriture.

## Clôture de chaque demande

Appliquer cette règle à toute demande sur le projet, y compris une explication, une vérification ou une relecture sans autre modification du dépôt. L’assistant qui traite la demande est responsable de sa clôture.

1. Attribuer un identifiant neuf à la demande. Choisir `main-story-writer` pour la méthode, la SPEC et les outils communs, ou la branche `legendes/…` du XML pour le travail sur un monde, ses pistes et ses manuscrits.
2. Terminer le travail et les vérifications, puis préparer le texte de la réponse finale. Rassembler uniquement les reçus des appels effectués pour cette demande. Un nouvel échange repart de zéro. Ne reconstituer aucun ancien échange et ne reporter aucun cumul de conversation ou de compte.
3. Si tous les appels ont livré un reçu, consigner leur total. Si seuls certains l’ont livré, consigner le sous-total et laisser le total inconnu. Si le total est inconnu, compter le seul message utilisateur courant et la réponse finale préparée avec `tiktoken` et l’encodage de référence `o200k_base`. Inscrire ces deux nombres comme indication de texte visible. Si ce comptage est lui aussi inaccessible, laisser la mesure absente. Un chiffre inconnu ne vaut jamais zéro.
4. Avant de rendre la main, publier la fiche dans `suivi/usage-llm/<demande>.json` sur `main-story-writer` ou dans `reperes/usage-llm/<demande>.json` sur la branche du XML. Vérifier la fiche distante ou attendre la réussite du workflow qui la relit. Publier uniquement les métadonnées. Si la publication échoue, la retenter sous le même identifiant et signaler tout échec persistant dans la réponse.
5. Envoyer la réponse préparée. L’écriture de la fiche et ses éventuelles reprises appartiennent à la même demande.

La version de référence de la procédure et du workflow se trouve sur `main-story-writer`. Le workflow peut écrire la fiche d’un export même si sa branche utilise une version antérieure des outils. [Commandes et format des compteurs](outils/README.md#journal-des-tokens)
