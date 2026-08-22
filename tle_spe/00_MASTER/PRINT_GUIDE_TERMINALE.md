# Guide d'impression et de distribution — stages Terminale

Ce guide couvre les deux modules, `tle_spe` (mathématiques) et `tle_nsi` (NSI).

## 1. Produire les PDF

```bash
make terminale        # régénère d'abord les documents Markdown nominatifs
make terminale-pdf    # puis les assemble en PDF A4
```

Les fichiers sont écrits sous `dist/terminale/`, avec un inventaire dans
`MANIFEST_TERMINALE.csv`.

**Les PDF ne sont pas versionnés.** Leur contenu binaire dépend de la version de WeasyPrint
et des polices installées : deux machines ne produisent pas deux fichiers identiques. Le
Markdown, lui, est versionné et fait foi.

Dépendances : `pandoc` et `weasyprint`. `make terminale-pdf-list` liste ce qui serait produit
sans rien rendre — utile pour vérifier la composition avant d'imprimer.

## 2. Ce qui est produit

| Dossier | Contenu | Destinataire |
|---|---|---|
| `eleves/` | Un dossier par élève et par matière : livret individuel et plan de remédiation | L'élève et sa famille |
| `seances/` | Une fiche par séance (S1 à S5) et le pack des cinq séances | À photocopier pour le groupe |
| `enseignant/seances/` | Une préparation par séance : fiche professeur, supports, cartes d'aide | L'enseignant seul |
| `enseignant/` | Les corrigés nominatifs, les tableaux de bord, les packs complets | L'enseignant seul |

**Les deux niveaux de granularité coexistent volontairement.** Le pack des cinq séances sert
à photocopier tout le stage d'un coup ; les fichiers `S1` à `S5` servent à préparer et à
imprimer une séance à la fois, ce qui est l'usage réel. Préparer la séance 3 ne doit pas
obliger à imprimer un pack de cent pages.

| Fichier | Contenu | Pages |
|---|---|---:|
| `seances/Tle_SPE_S3_FICHE_ELEVE.pdf` | L'activité élève de la séance 3 | 5 |
| `enseignant/seances/Tle_SPE_S3_PREPARATION_ENSEIGNANT.pdf` | Fiche professeur, supports, cartes d'aide | 12 |

**Un dossier `eleves/` ne contient jamais de corrigé.** Ce n'est pas une convention de
nommage : `tools/build_terminale_pdf.py` refuse d'assembler un pack élève contenant un
document marqué `PROF`, `Corrige`, `Tableau_Bord` ou `Guide_Formateur`, et l'assemblage
échoue plutôt que de produire un fichier douteux.

## 3. Réglages d'impression

| Réglage | Valeur |
|---|---|
| Format | A4 |
| Recto-verso | Oui, reliure bord long |
| Couleur | Recommandée pour la page de garde et les tableaux ; le noir et blanc reste lisible |
| Mise à l'échelle | **100 %, sans ajustement** — les marges sont déjà calculées |
| Agrafage | Coin supérieur gauche pour les dossiers élèves ; reliure spirale pour les packs enseignants |

La page de garde est en aplat marine plein page. Sur une imprimante à jet d'encre, elle
consomme beaucoup d'encre : imprimer les couvertures en une seule passe sur une laser, ou
supprimer la première page si l'encre est comptée — le livret reste complet sans elle.

## 4. Volumétrie

À l'impression recto-verso, pour une cohorte de neuf élèves :

| Lot | Exemplaires | Pages par exemplaire | Feuilles |
|---|---:|---:|---:|
| Dossiers élèves (maths) | 10 | 5 à 25 | ~90 |
| Dossiers élèves (NSI) | 5 | 15 à 25 | ~55 |
| Fiche d'une séance, maths | 9 | 5 | ~23 |
| Fiche d'une séance, NSI | 5 | 5 à 7 | ~15 |
| Préparation d'une séance | 1 | 11 à 14 | ~7 |
| Packs enseignants complets | 2 | 100 et 98 | ~100 |

Imprimer séance par séance est plus économe : cinq tirages de 5 pages pour un élève de maths
valent 23 feuilles en recto-verso, contre 17 pour le pack de 34 pages — mais on n'imprime que
ce qui sert le jour même, et les fiches non utilisées ne sont pas gaspillées.

Le manifeste donne le compte exact après chaque génération.

## 5. Distribution

1. **Vérifier avant de distribuer.** Chaque dossier élève porte le nom de son élève sur la
   couverture. Un dossier remis au mauvais élève est une fuite de données personnelles.
2. **Ne jamais joindre un corrigé à un dossier élève**, même à la demande d'une famille : le
   plan de remédiation est conçu pour être tenté avant d'être corrigé.
3. **Les packs enseignants et les tableaux de bord ne sortent pas du dossier pédagogique.**
   Ils contiennent les diagnostics de plusieurs élèves.
4. **Après le stage**, remettre à la famille le livret complété, et archiver le portfolio.

## 6. Cas particuliers de cette cohorte

- **Deux élèves n'ont pas passé le positionnement en mathématiques.** Leur dossier ne compte
  que 5 pages et porte la mention « Diagnostic à établir » : il organise la passation en
  séance 1 au lieu d'annoncer des résultats. Prévoir deux jeux du positionnement papier.
- **Deux élèves suivent l'option mathématiques expertes.** Elles reçoivent un second dossier,
  distinct, marqué `EXPERTES` dans le nom du fichier. Ne pas le confondre avec leur dossier
  de spécialité.
- **Une élève du groupe 2 ne suit que les mathématiques.** Son livret le précise ; elle ne
  reçoit aucun document NSI ni physique-chimie.
- **Une homonymie existe avec un élève entrant en Première NSI.** Vérifier le niveau indiqué
  sur la couverture avant de remettre un dossier.
