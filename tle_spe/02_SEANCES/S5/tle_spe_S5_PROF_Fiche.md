# Terminale Spécialité Mathématiques — Séance 5 — Fiche professeur
## Produit scalaire vers l'espace, probabilités, Python, évaluation de synthèse

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance

Trois objets sont réunis dans la dernière séance parce qu'ils demandent peu de
reconstruction et beaucoup de mise en perspective :

- le **produit scalaire** est acquis pour quatre élèves sur sept (71,4 %) ; l'enjeu n'est
  pas le calcul mais l'usage du critère u·v = 0 comme outil de preuve ;
- les **probabilités** de Première n'ont pas été évaluées par le positionnement ; elles sont
  réactivées sans diagnostic préalable, car elles conditionnent la loi binomiale ;
- **Python** est réactivé sur un cas d'usage mathématique, ce qui prolonge la séance 1.

La séance se referme sur l'évaluation de synthèse et le plan de septembre.

## Objectifs de la séance

1. Utiliser le critère d'orthogonalité pour démontrer et pour déterminer un paramètre.
2. Réactiver probabilité conditionnelle, arbre pondéré, indépendance et espérance.
3. Écrire une boucle Python calculant les termes d'une suite et cherchant un seuil.
4. Mesurer les progrès et fixer le plan de travail de septembre.

## Déroulé minuté

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 4 : signe de f' et variations de f |
| 20 min | Produit scalaire | Calcul par les coordonnées ; critère d'orthogonalité ; détermination d'un paramètre ; annonce de l'espace |
| 20 min | Probabilités | Arbre pondéré ; probabilité conditionnelle ; indépendance ; espérance ; annonce de la loi binomiale |
| 20 min | Python | Termes d'une suite par une boucle ; recherche du premier rang dépassant un seuil |
| 35 min | Évaluation finale | Épreuve de synthèse, cinq exercices, certitude déclarée |
| 15 min | Bilan | Restitution, plan de septembre, portfolio |

## Produit scalaire — 20 minutes

**Rappel.** En repère orthonormé, u·v = x_u x_v + y_u y_v. Le résultat est un **nombre**.
Faire redire ce point : l'erreur la plus fréquente est d'annoncer un vecteur.

**Le critère comme outil.** Faire traiter deux usages :

1. *Démontrer.* u(−2 ; 5) et v(4 ; 1) : u·v = −8 + 5 = −3 ≠ 0, donc les vecteurs ne sont pas
   orthogonaux.
2. *Déterminer un paramètre.* u(3 ; m) et v(−2 ; 6) orthogonaux : −6 + 6m = 0, donc m = 1.

Le second usage est celui qui manque : le critère se lit comme une **équation** dont
l'inconnue est un paramètre.

**Annonce de la Terminale.** Écrire au tableau le même critère avec trois coordonnées :
u·v = x_u x_v + y_u y_v + z_u z_v. Puis :

> Un vecteur **normal** à un plan est un vecteur orthogonal à deux vecteurs directeurs de ce
> plan. Si n(a ; b ; c) est normal au plan P et si A(x₀ ; y₀ ; z₀) appartient à P, alors P a
> pour équation cartésienne a(x − x₀) + b(y − y₀) + c(z − z₀) = 0.
>
> Autrement dit : l'équation d'un plan **est** un produit scalaire nul. Tout le chapitre de
> géométrie dans l'espace repose sur le critère que vous connaissez déjà.

## Probabilités — 20 minutes

Ce contenu n'a pas été diagnostiqué : le conduire en observation, sans présumer du niveau.

**Arbre pondéré.** Faire construire l'arbre d'une situation simple : une urne contient 3
boules rouges et 2 boules noires ; on tire deux boules successivement sans remise.

Faire écrire sur les branches les probabilités conditionnelles, puis établir :

> P(A ∩ B) = P(A) × P_A(B)
> P(B) = P(A) × P_A(B) + P(Ā) × P_Ā(B)  *(formule des probabilités totales)*

**Indépendance.** Deux événements sont indépendants lorsque P_A(B) = P(B). Faire distinguer
de l'incompatibilité : deux événements incompatibles de probabilités non nulles ne sont
jamais indépendants. C'est une confusion classique, à provoquer et à traiter.

**Variable aléatoire.** Loi de probabilité sous forme de tableau ; espérance
E(X) = Σ x_i P(X = x_i), interprétée comme la moyenne des valeurs sur un grand nombre de
répétitions.

**Annonce de la Terminale.**

> Quand on répète n fois, de façon indépendante, une même épreuve à deux issues, on obtient
> un **schéma de Bernoulli**. Le nombre de succès suit alors la **loi binomiale** de
> paramètres n et p, dont l'espérance vaut np. La loi des grands nombres viendra ensuite
> justifier pourquoi la moyenne observée se rapproche de l'espérance.

## Python — 20 minutes

Objectif : écrire une boucle qui calcule les termes d'une suite et cherche un seuil. Le
lien avec la séance 1 doit être explicite.

```python
# Suite arithmetique u(n+1) = u(n) + r
def terme_arithmetique(u0, r, n):
    u = u0
    for _ in range(n):
        u = u + r
    return u

# Suite geometrique v(n+1) = q * v(n)
def terme_geometrique(v0, q, n):
    v = v0
    for _ in range(n):
        v = q * v
    return v

# Premier rang pour lequel la suite depasse un seuil
def premier_rang_depassement(v0, q, seuil):
    v = v0
    n = 0
    while v <= seuil:
        v = q * v
        n = n + 1
    return n
```

**Points à faire travailler.**

- `range(n)` produit n valeurs : la boucle effectue bien n pas, pas n + 1.
- La boucle `while` ne termine que si la suite dépasse effectivement le seuil : demander aux
  élèves ce qui se passe si q < 1 et si le seuil est supérieur à v₀. C'est une occasion de
  relier au sens de variation de la séance 1.
- Faire tester `terme_geometrique(2, 3, 4)` : le résultat 162 doit coïncider avec le calcul
  à la main.

**Pour le groupe 1**, qui suit également la spécialité NSI : signaler que ces mêmes boucles
sont retravaillées en séance 3 du module `tle_nsi`, sous l'angle de la spécification et des
tests.

## Évaluation finale — 35 minutes

Distribuer `03_EVALUATIONS/tle_spe_Evaluation_Finale_ELEVE.md`. Cinq exercices, un par
domaine, avec certitude déclarée à chaque question. Aucune note n'est attribuée : la copie
est relue avec la matrice réussite × confiance et comparée au positionnement initial.

## Bilan — 15 minutes

1. Restituer à chaque élève la comparaison entre sa carte initiale et son résultat final.
2. Faire remplir le plan de travail de septembre dans le livret individuel (quatre semaines).
3. Faire compléter le portfolio et l'auto-évaluation finale.
4. Faire formuler à chacun, à voix haute, **une** phrase : « ce que j'ai corrigé pendant ce
   stage, c'est… »

## Erreurs à surveiller

| Erreur observée | Réponse |
|---|---|
| Vecteur annoncé comme résultat d'un produit scalaire | Faire souligner le résultat et écrire « c'est un nombre » |
| P(A ∩ B) confondu avec P_A(B) | Faire replacer chacune sur l'arbre : la conditionnelle est **sur** la branche |
| Indépendance confondue avec incompatibilité | Faire chercher deux événements incompatibles et calculer P_A(B) = 0 ≠ P(B) |
| Bornes de boucle décalées | Faire afficher les valeurs successives avec `print` |

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
