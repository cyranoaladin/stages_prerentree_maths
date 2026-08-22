# Dettes techniques

Ce qui reste à faire, ou ce qui a été fait avec une limite connue. Rien n'est caché ici :
une dette non écrite est une dette qui se paie deux fois.

## 1. Aucune copie réelle n'a été corrigée

**Portée** : la seule qui compte vraiment.

Le pipeline est éprouvé sur des jeux synthétiques. La justesse pédagogique des seuils de
statut, la lisibilité des bilans et l'ergonomie réelle de la saisie ne se vérifient qu'en
corrigeant une copie. C'est l'objet du pilote, et c'est pour cela que le statut est
`READY_FOR_PILOT` et non « validé ».

## 2. Aucun test dans un vrai navigateur

**Portée** : raccourcis clavier, rendu du PDF dans l'`iframe`, ergonomie à 1366×768.

Playwright n'est pas installé sur ce poste, et la livraison ne doit pas dépendre de
l'installation d'un navigateur complet. Le test est écrit et s'exécutera si Playwright
apparaît. En attendant, ces trois points sont à vérifier à la main pendant le pilote.

## 3. Pas d'authentification

**Portée** : le mode `--allow-network`.

En localhost strict, sans compte utilisateur, c'est un choix assumé pour cette première
version. Le mode réseau refuse de démarrer sans `NEXUS_S5_PASSWORD`, mais il n'y a pas
encore de session, de connexion ni de gestion de comptes. Tant que l'application reste
locale, ce n'est pas un problème ; le jour où elle serait exposée, il faudrait le traiter
avant, pas après.

Les jetons CSRF existent (`security.issue_token`) mais ne sont pas exigés : sans session,
ils protégeraient peu.

## 4. La reprise après changement du référentiel V3 est manuelle

**Portée** : le cas où un fichier de `S5_post_distribution_v3/` change après l'import.

La dérive est détectée et affichée, jamais résorbée en silence — c'est voulu. Mais la
reprise consiste à réimporter dans une base vierge et à **ressaisir** les corrections
depuis l'export. Un migrateur qui rapprocherait les anciens critères des nouveaux
n'existe pas, et serait délicat à écrire correctement.

En pratique, le référentiel ne devrait plus bouger : il décrit des documents distribués.

## 5. La restauration d'une sauvegarde n'est pas testée automatiquement

**Portée** : le manuel décrit la procédure, aucun test ne la rejoue.

Écrire ce test suppose de manipuler la base pendant qu'elle est ouverte, ou de démarrer un
second processus. Faisable, mais pas fait.

## 6. Un seul moteur LaTeX essayé

**Portée** : `pdflatex` sur cette machine.

Les gabarits n'ont pas été compilés avec `lualatex` ni `xelatex`, ni sur une autre
distribution TeX. Le style n'emploie que des paquets courants, mais rien ne le garantit
ailleurs.

## 7. Le générateur assisté par modèle de langage n'est qu'une réservation

**Portée** : `LLMNarrativeGenerator`.

La classe existe, refuse de fonctionner, et porte une méthode de pseudonymisation. Aucun
fournisseur n'est câblé. C'est délibéré : la génération déterministe produit la totalité
des documents, et rien n'oblige à ajouter une dépendance réseau à un outil qui manipule des
données d'élèves.

## 8. Le champ « durée observée » n'est pas exploité

**Portée** : `correction.observed_duration_minutes` est saisissable et exporté, mais aucun
calcul ne s'en sert.

Il est là pour recueillir des mesures réelles, qui serviront un jour à calibrer les
estimations de durée. Tant qu'il n'y a pas de données, mieux vaut ne rien en tirer.

## 9. Pas de reprise de correction à plusieurs

**Portée** : deux enseignants corrigeant en même temps le même élève.

SQLite en WAL supporte des lecteurs concurrents, et l'écriture est transactionnelle, mais
rien ne signale à l'un que l'autre vient de modifier le même critère. Pour un usage
mono-poste, ce n'est pas un problème.

## 10. La vue de groupe n'agrège rien

**Portée** : `/groupe` affiche des chiffres élève par élève.

C'est volontaire : les corpus de critères diffèrent d'un élève à l'autre, une moyenne de
classe n'aurait pas de sens, et le tableau porte l'avertissement. Mais un enseignant
pourrait souhaiter une lecture par compétence à l'échelle du groupe. Elle n'existe pas.

## 11. La revue curriculaire ne couvre qu'Inès KEFI

**Portée** : les 315 critères des 14 autres élèves.

La passe corrective du 21 août a établi, contre les attendus officiels, que développer
`k(a − b)` est un attendu de Quatrième et non de Cinquième. Pour Inès, cela a fait passer
`B2_c1` et `B2_c2` en passerelle et `A3_c1` en mixte. **`A3` et `B2` sont des items du
noyau commun de Quatrième** : Fares DARGHOUTH et Sinda CHIKHAOUI ont exactement les mêmes.
Leur classement n'a pas été modifié, la mission l'interdisant, mais la question est
ouverte. Voir `FUTURE_CURRICULUM_REVIEW.md`.

Les autres élèves portent par ailleurs encore la justification générée automatiquement
« aucune notion du programme de l'année N n'est requise », qui est une affirmation et non
une source.

## 12. Rubriques et suggestions limitées aux 22 critères d'Inès

**Portée** : les 315 autres critères.

Ils conservent l'échelle de score arithmétique — sans règle d'attribution — et affichent
encore les erreurs probables de l'item sous chacun de leurs critères. Le mécanisme est en
place et générique (`app/data/criterion_overlays.py`) ; seul le contenu manque, et il ne
peut être écrit qu'élève par élève.

## Ce qui n'est pas une dette

- l'absence de progression chiffrée : c'est une décision scientifique, documentée ;
- l'absence de framework front : le rendu serveur suffit et l'application fonctionne hors
  ligne ;
- l'échelle de scores restreinte : le serveur accepte plus large que les boutons, c'est
  documenté dans `CORRECTION_RULES.md`.
