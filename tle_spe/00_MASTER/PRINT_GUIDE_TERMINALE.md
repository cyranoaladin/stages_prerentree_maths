# Guide d'impression et de distribution — stages Terminale

Ce guide couvre les trois modules : `tle_spe` (mathématiques), `tle_nsi` (NSI) et
`tle_pc` (physique-chimie).

**Nexus Réussite** — centre d'accompagnement scolaire. Chaque stage dure 10 heures, à raison
de 2 heures par jour pendant 5 jours consécutifs, **du 24 au 28 août 2026**. Les documents
doivent donc être prêts avant le 24 août.

## 1. Produire les PDF

```bash
make terminale        # régénère d'abord les documents Markdown nominatifs
make terminale-pdf    # puis les assemble en PDF A4
```

Les fichiers sont écrits sous `dist/terminale/`, avec un inventaire dans
`MANIFEST_TERMINALE.csv`.

```bash
make terminale-livraison   # écrit dist/terminale/NOTE_DE_REMISE.md
```

**La note de remise est le document à imprimer pour la personne qui distribue.** Elle
est produite à partir du registre de la cohorte, et non écrite à la main : elle ne peut
pas décrire une remise différente de ce qui a été fabriqué. Elle donne, élève par élève,
ce qui lui revient et en combien de pages ; séance par séance, ce qui se photocopie et
en combien d'exemplaires ; et la liste de ce qui ne sort pas du dossier pédagogique.
Le même outil échoue si un document nominatif se trouve dans la liasse collective.

**Les PDF ne sont pas versionnés.** Leur contenu binaire dépend de la version de LuaLaTeX
et des polices installées : deux machines ne produisent pas deux fichiers identiques. Le
Markdown, lui, est versionné et fait foi.

Dépendances : `pandoc`, `lualatex` et `latexmk`. `make terminale-pdf-list` liste ce qui serait produit
sans rien rendre — utile pour vérifier la composition avant d'imprimer.

## 2. Ce qui est produit

| Dossier | Contenu | Destinataire |
|---|---|---|
| `eleves/` | Par élève et par matière : le **cahier des cinq séances**, et un dossier réunissant livret individuel et plan de remédiation | L'élève et sa famille |
| `seances/` | Une fiche par séance (S1 à S5) et le pack des cinq séances | À photocopier pour le groupe |
| `enseignant/seances/` | Une préparation par séance : fiche professeur, supports, cartes d'aide | L'enseignant seul |
| `enseignant/` | Les corrigés nominatifs, les tableaux de bord, les packs complets | L'enseignant seul |

**Les deux niveaux de granularité coexistent volontairement.** Le pack des cinq séances sert
à photocopier tout le stage d'un coup ; les fichiers `S1` à `S5` servent à préparer et à
imprimer une séance à la fois, ce qui est l'usage réel. Préparer la séance 3 ne doit pas
obliger à imprimer un pack de cent pages.

| Fichier | Contenu | Pages |
|---|---|---:|
| `seances/Tle_SPE_S3_FICHE_ELEVE.pdf` | L'activité élève de la séance 3 | 6 |
| `enseignant/seances/Tle_SPE_S3_PREPARATION_ENSEIGNANT.pdf` | Fiche professeur, supports, cartes d'aide | 9 |

**Le cahier des cinq séances est le document de travail.** C'est celui que l'élève apporte
chaque jour : il porte sa progression, ses automatismes, ses exercices — et seulement les
siens, ceux de sa piste. Un élève en remédiation n'y trouve pas les problèmes destinés à
ceux qui n'ont rien à reprendre, et réciproquement. Il fait de 17 à 24 pages selon le profil,
et c'est la seule chose à imprimer en recto verso agrafé.

Le **dossier individuel**, lui, se conserve : il restitue le positionnement, sert à l'entretien
avec la famille et porte la page de signature de l'enseignant. On l'imprime une fois, on ne le
réimprime pas.

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

La note de remise (`dist/terminale/NOTE_DE_REMISE.md`, produite par
`make terminale-livraison`) donne le compte exact, élève par élève et séance par
séance, à partir du registre. Les ordres de grandeur, pour la cohorte de neuf élèves —
huit en mathématiques, quatre en NSI, trois en physique-chimie :

| Lot | Exemplaires | Pages par exemplaire | Feuilles |
|---|---:|---:|---:|
| Cahiers des cinq séances (maths) | 8 | 17 à 23 | ~85 |
| Cahiers des cinq séances (NSI) | 4 | 21 à 23 | ~45 |
| Cahiers des cinq séances (physique-chimie) | 3 | 23 à 24 | ~36 |
| Dossiers individuels (les trois matières) | 15 | 4 à 17 | ~95 |
| Fiche d'une séance, maths | 8 | 5 à 6 | ~24 |
| Fiche d'une séance, NSI | 4 | 6 à 7 | ~16 |
| Fiche d'une séance, physique-chimie | 3 | 6 | ~9 |
| Préparation d'une séance | 1 | 9 à 14 | ~7 |
| Packs enseignants complets | 3 | 96 à 114 | ~160 |

Imprimer séance par séance coûte un peu plus de papier : les cinq fiches de mathématiques
font 5, 5, 6, 6 et 6 pages, soit 15 feuilles en recto-verso, contre 14 pour le pack de
33 pages tiré d'un bloc. On n'imprime en revanche que ce qui sert le jour même, et une
séance qui se déroule autrement que prévu ne rend pas caduque une liasse déjà tirée.

Le manifeste et la note de remise donnent le compte exact après chaque génération.

## 5. Distribution

1. **Vérifier avant de distribuer.** Chaque dossier élève porte le nom de son élève sur la
   couverture. Un dossier remis au mauvais élève est une fuite de données personnelles.
2. **Ne jamais joindre un corrigé à un dossier élève**, même à la demande d'une famille : le
   plan de remédiation est conçu pour être tenté avant d'être corrigé.
3. **Les packs enseignants et les tableaux de bord ne sortent pas du dossier pédagogique.**
   Ils contiennent les diagnostics de plusieurs élèves.
4. **Après le stage**, remettre à la famille le livret complété, et archiver le portfolio.

## 6. Cas particuliers de cette cohorte

- **Une élève n'a pas passé le positionnement en mathématiques.** Son dossier ne compte que
  4 pages et porte la mention « Diagnostic à établir » : il organise la passation en séance 1
  au lieu d'annoncer des résultats. Prévoir un jeu du positionnement papier.
- **Deux élèves suivent l'option mathématiques expertes.** Elles ne reçoivent **pas** de
  dossier séparé : l'option figure dans leur livret de mathématiques, section « Option
  annuelle », et leurs exercices d'option sont à la fin de leur feuille de remédiation. Leur
  dossier est donc plus épais que celui des autres.
- **Trois élèves suivent le stage de physique-chimie**, dont une qui ne suit que celui-là.
  **Deux ne suivent que les mathématiques.** Chaque livret annonce les spécialités réelles :
  ne pas se fier au nom du groupe pour savoir quoi remettre — le tableau 1 de la note de
  remise fait foi.
