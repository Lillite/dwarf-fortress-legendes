# Clôture de chaque demande

Appliquer cette règle à toute demande sur le projet, y compris une explication, une vérification ou une relecture sans autre modification du dépôt. L’assistant qui traite la demande est responsable de sa clôture.

1. Attribuer un identifiant neuf à la demande. Choisir `main` pour la méthode, la SPEC et les outils communs, ou la branche `legendes/…` du XML pour le travail sur un monde, ses pistes et ses manuscrits.
2. Terminer le travail et les vérifications, puis préparer le texte de la réponse finale. Rassembler uniquement les reçus des appels effectués pour cette demande. Un nouvel échange repart de zéro. Ne reconstituer aucun ancien échange et ne reporter aucun cumul de conversation ou de compte.
3. Si tous les appels ont livré un reçu, consigner leur total. Si seuls certains l’ont livré, consigner le sous-total et laisser le total inconnu. Si le total est inconnu, compter le seul message utilisateur courant et la réponse finale préparée avec `tiktoken` et l’encodage de référence `o200k_base`. Inscrire ces deux nombres comme indication de texte visible. Si ce comptage est lui aussi inaccessible, laisser la mesure absente. Un chiffre inconnu ne vaut jamais zéro.
4. Avant de rendre la main, publier la fiche dans `suivi/usage-llm/<demande>.json` sur `main` ou dans `reperes/usage-llm/<demande>.json` sur la branche du XML. Vérifier la fiche distante ou attendre la réussite du workflow qui la relit. Publier uniquement les métadonnées. Si la publication échoue, la retenter sous le même identifiant et signaler tout échec persistant dans la réponse.
5. Envoyer la réponse préparée. L’écriture de la fiche et ses éventuelles reprises appartiennent à la même demande.

La version de référence de la procédure et du workflow se trouve sur `main`. Le workflow peut écrire la fiche d’un export même si sa branche utilise une version antérieure des outils. [Commandes et format des compteurs](outils/README.md#journal-des-tokens)
