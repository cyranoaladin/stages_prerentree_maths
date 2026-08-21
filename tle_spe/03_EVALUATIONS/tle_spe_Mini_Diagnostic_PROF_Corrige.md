# Terminale Spécialité Mathématiques — Mini-diagnostic complémentaire (Corrigé enseignant)

## Objet

Le positionnement initial couvre cinq domaines : second degré, dérivation, fonction
exponentielle, suites numériques, produit scalaire. Il ne couvre **ni les probabilités de
Première, ni les compétences transversales** (justification, contrôle, lecture de programme).

Ce mini-diagnostic comble ce manque. Il est proposé en début de séance 1 et dépouillé
pendant l'entraînement différencié de la même séance : les résultats orientent la conduite
de la séance 5.

## Corrigé et lecture

### Exercice 1 — Probabilité conditionnelle

a) **P(NSI ∩ expertes) = P(NSI) × P_NSI(expertes) = 0,6 × 0,8 = 0,48**, soit 48 %.

b) Propriété : P(A ∩ B) = P(A) × P_A(B).

*Erreur attendue :* multiplier 0,6 par 0,8 sans savoir pourquoi, ou additionner. Une réponse
juste sans propriété écrite compte comme « réussite hésitante ».

### Exercice 2 — Indépendance

a) **Oui.** Le résultat du premier lancer n'influence pas le second : P_A(B) = P(B) = 0,5.

b) **Non.** Ils peuvent se produire ensemble : obtenir pile deux fois est possible, de
probabilité 0,25.

*Erreur attendue :* confondre les deux notions, ou déclarer les événements incompatibles
parce qu'ils sont « différents ». C'est la confusion la plus fréquente ; elle est traitée en
séance 5 avec les cartes de tri.

### Exercice 3 — Variable aléatoire

a) 0,2 + 0,5 + 0,3 = 1, et chaque probabilité est comprise entre 0 et 1 : c'est bien une loi
de probabilité.

b) **E(X) = (−1) × 0,2 + 0 × 0,5 + 2 × 0,3 = −0,2 + 0 + 0,6 = 0,4.**

*Erreur attendue :* calculer la moyenne des valeurs (−1 + 0 + 2)/3 sans pondérer.

### Exercice 4 — Justification écrite

Il manque **l'étude du signe de f'**. La rédaction correcte :

> f'(x) = 2x − 4 = 2(x − 2), qui s'annule en 2, est négatif avant et positif après. Donc f
> est décroissante sur ]−∞ ; 2] et croissante sur [2 ; +∞[.

La conclusion de l'élève est de surcroît **fausse** : f n'est pas croissante sur ℝ.

*Lecture.* Cet exercice mesure moins une connaissance qu'une habitude. Un élève qui repère le
manque sans savoir le combler est en bonne position ; un élève qui valide la rédaction est à
suivre de près en séance 4.

### Exercice 5 — Contrôle de vraisemblance

a) La **somme** des racines doit valoir −b/a = 7 ; or 2 + 6 = 8. Le **produit** doit valoir
c/a = 10 ; or 2 × 6 = 12. Les deux contrôles échouent.

b) Δ = 49 − 40 = 9, √Δ = 3 : les racines sont (7 − 3)/2 = **2** et (7 + 3)/2 = **5**.

*Lecture.* C'est l'exercice le plus discriminant du mini-diagnostic. Un élève qui ne dispose
d'aucun contrôle validera toute racine plausible. Le contrôle somme/produit est imposé dès la
séance 3.

### Exercice 6 — Python

a) `mystere(4)` renvoie **6** : range(4) produit 0, 1, 2, 3, dont la somme vaut 6.

b) **4 tours de boucle.**

*Erreur attendue :* répondre 10 (somme de 1 à 4) en oubliant que range commence à 0, ou 5
tours en incluant la borne.

## Grille de dépouillement

À remplir pour l'ensemble du groupe, une croix par élève et par ligne.

| Compétence | Pas encore | Avec aide | Seul | Peut expliquer |
|---|:---:|:---:|:---:|:---:|
| Probabilité conditionnelle (ex. 1) | | | | |
| Indépendance / incompatibilité (ex. 2) | | | | |
| Espérance (ex. 3) | | | | |
| Justification avant conclusion (ex. 4) | | | | |
| Contrôle de vraisemblance (ex. 5) | | | | |
| Lecture d'un programme (ex. 6) | | | | |

## Décisions à prendre à l'issue du dépouillement

| Constat | Décision |
|---|---|
| Plus de la moitié du groupe échoue aux exercices 1 à 3 | Porter le temps « probabilités » de la séance 5 de 20 à 30 minutes, en réduisant Python |
| Confusion indépendance / incompatibilité généralisée | Introduire les cartes de tri dès la séance 4, en fin de séance |
| Exercice 4 majoritairement validé comme correct | Rendre obligatoire l'écriture de la propriété dans **toutes** les fiches élèves |
| Exercice 5 non traité par plus de deux élèves | Imposer la fiche de contrôle somme/produit dès la séance 1 |
| Exercice 6 échoué par le groupe 1 | Signaler au module `tle_nsi` : la séance 3 y reprend `range` et les bornes |

---
_Document enseignant. Ne pas diffuser aux élèves avant dépouillement._
