# Terminale Spécialité Mathématiques — Séance 2 — Fiche professeur
## Fonction exponentielle : exposants, équations, vers le logarithme

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance en deuxième position

La fonction exponentielle est le **domaine le plus faible du groupe** : 57,1 % de réussite
moyenne, trois élèves porteurs d'une certitude erronée, deux élèves à 0 % de réussite.

L'enjeu pour la Terminale est direct : la fonction logarithme est introduite comme
réciproque de l'exponentielle. Toute erreur sur les règles d'exposants se transpose telle
quelle aux règles sur ln. Les équations différentielles $y' =$ ay + b et le calcul de
primitives reposent également sur ces manipulations.

## Objectifs de la séance

1. Appliquer sans erreur $\exp(a) \times \exp(b) = \exp(a+b)$ et $\exp(a)/\exp(b) = \exp(a - b)$.
2. Maintenir la parenthèse autour de l'exposant soustrait.
3. Utiliser la stricte positivité de l'exponentielle pour conclure sur une équation ou une
   inéquation.
4. Faire apparaître le lien avec le logarithme, sans le traiter.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Question de contrôle sur la séance 1 : sens de variation de $v_n = 4 \times 0{,}7^n$ | Répond, déclare sa certitude |
| 20 min | Confrontation | Écrit $e^{2x}/e^{x - 1}$ au tableau ; recueille les réponses **avant** commentaire | Propose une simplification, la teste en $x = 1$ |
| 25 min | Reconstruction | Établit les quatre règles à partir de la relation fonctionnelle ; établit la stricte positivité | Prend la trace écrite |
| 30 min | Entraînement différencié | Distribue les trois parcours ; circule | Traite son parcours, note l'aide utilisée |
| 20 min | Ouverture Terminale | Introduit ln comme réciproque ; montre le passage d'une règle à l'autre | Observe, note la correspondance |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Écrire au tableau : « Simplifier $e^{2x} / e^{x - 1}$. » Demander une réponse écrite et une
   certitude, sans discussion.
2. Recueillir les propositions. Les deux réponses attendues sont $e^{3x - 1}$ — erreur
   d'addition des exposants — et $e^{x+1}$.
3. **Test numérique**, à faire faire par les élèves, en $x = 1$ :
   - $e^{2 \times 1} / e^{1 - 1} = e^2 / e^0 = e^2 \approx 7{,}39$ ;
   - $e^{3 \times 1 - 1} = e^2 \approx 7{,}39$ — l'erreur ne se voit pas en $x = 1$.
   Refaire en **$x = 2$** :
   - $e^4 / e^1 = e^3 \approx 20{,}09$ ;
   - $e^{3 \times 2 - 1} = e^5 \approx 148{,}4$. La contradiction apparaît.
4. Faire verbaliser : diviser, c'est soustraire les exposants.
5. Faire écrire la parenthèse : $2x - (x - 1) = 2x - x + 1 = x + 1$. Insister : sans la
   parenthèse on obtient $2x - x - 1 = x - 1$, qui est faux.

**Point de vigilance.** Le choix de la valeur de test n'est pas neutre : $x = 1$ ne discrimine
pas les deux réponses. C'est une occasion de faire réfléchir les élèves au choix d'un
contre-exemple, geste qu'ils réutiliseront toute l'année.

## Reconstruction

**Les quatre règles**, toutes déduites de $\exp(a + b) = \exp(a) \times \exp(b)$ :

| Règle | Écriture |
|---|---|
| Produit | $\exp(a) \times \exp(b) = \exp(a + b)$ |
| Quotient | $\exp(a) / \exp(b) = \exp(a - b)$ |
| Inverse | $\exp( - a) = 1 / \exp(a)$ |
| Puissance | $(\exp(a))^n = \exp$(na) |

**Stricte positivité.** Pour tout réel x, $\exp(x) > 0$. Démonstration courte à conduire :
$\exp(x) = \exp(x/2 + x/2) = (\exp(x/2))^2$, qui est un carré, donc positif ou nul ; et
$\exp(x) \times \exp( - x) = \exp(0) = 1$, donc $\exp(x)$ ne peut pas être nul.

Conséquences à écrire au tableau :

- $\exp(u(x)) = 0$ n'a **jamais** de solution ;
- $\exp(u(x)) > 0$ est vraie pour tout x du domaine ;
- dans une factorisation, on peut simplifier par $\exp(x)$ sans perdre de solution.

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Ceux dont le livret porte « Fonction exponentielle » en priorité | Exercices 1 à 4, exemple résolu fourni |
| Maîtrise | Réussite hésitante sur le domaine | Exercices 3 à 6, justification écrite exigée |
| Approfondissement | Domaine acquis avec certitude | Exercices 6 à 8, dont la démonstration de la stricte positivité |

## Ouverture sur la Terminale — 20 minutes

Présenter le logarithme népérien comme la fonction qui « défait » l'exponentielle :
$\ln(\exp(x)) = x$ et $\exp(\ln(x)) = x$ pour $x > 0$.

Faire construire, par les élèves, le tableau de correspondance :

| Règle sur exp | Règle sur ln |
|---|---|
| $\exp(a + b) = \exp(a) \times \exp(b)$ | ln(ab) $= \ln a + \ln b$ |
| $\exp(a - b) = \exp(a) / \exp(b)$ | $\ln(a/b) = \ln a - \ln b$ |
| exp(na) $= (\exp(a))^n$ | $\ln(a^n) = n \ln$ a |
| $\exp(x) > 0$ pour tout x | ln x n'existe que pour $x > 0$ |

Faire énoncer la conclusion : *une erreur commise sur exp se retrouvera à l'identique sur
ln.* C'est l'argument qui justifie la séance.

Ne pas faire résoudre d'équation avec ln pendant le stage.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Exposants additionnés dans une division | Test numérique en $x = 2$ ; réécriture avec la parenthèse |
| Parenthèse oubliée dans l'exposant soustrait | Faire écrire les deux calculs côte à côte |
| Une solution attribuée à $\exp(x) = 0$ | Rappeler la stricte positivité ; faire tracer l'allure de la courbe |
| $\exp(a + b)$ écrit $\exp(a) + \exp(b)$ | Test numérique avec $a = b = 1$ : $e^2 \approx 7{,}39$ contre $2e \approx 5{,}44$ |
| $\exp(x^2)$ confondu avec $(\exp(x))^2$ | Faire calculer les deux en $x = 2$ : $e^4$ contre $e^4$ — puis en $x = 3$ : $e^9$ contre $e^6$ |

## Indicateurs de fin de séance

- L'élève écrit la parenthèse spontanément.
- L'élève teste sa formule sur une valeur numérique avant de déclarer une certitude de 4.
- L'élève sait dire pourquoi $\exp(x) = 0$ n'a pas de solution.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
