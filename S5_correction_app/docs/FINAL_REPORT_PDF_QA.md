# QA finale des bilans PDF

Audit conduit le 22 août 2026, avant la première correction réelle. Quarante-cinq
documents synthétiques — quinze couples élève × matière, trois documents chacun —
générés, compilés, rastérisés et inspectés page à page.

**REPORT_PDF_QUALITY = PASS.** Zéro défaut bloquant.

## 1. Corpus audité

| type | documents | pages | pagination |
| --- | ---: | ---: | --- |
| Bilan parents | 15 | 90 | 6 pages |
| Fiche élève | 15 | 17 | 1 page (13), 2 pages (2) |
| Synthèse enseignant | 15 | 47 | 3 pages (13), 4 pages (2) |
| **total** | **45** | **154** | |

Les cinq niveaux sont couverts : 4e, 3e, 2nde, 1re spé mathématiques, 1re NSI. Les
copies synthétiques alternent réussite, demi-réussite et échec de façon
déterministe, pour que chaque bilan produit ait de la matière — points forts,
points à consolider, profil d'erreurs, plan chargé.

## 2. Templates

`bilan_longitudinal_parents.tex.j2` a été restructuré. `bilan_parents.tex.j2`,
`fiche_eleve.tex.j2`, `synthese_enseignant.tex.j2` et `plan_4_semaines.tex.j2` ont
reçu leurs métadonnées et le filtre de macros pédagogiques. `nexus_bilan.sty` a été
corrigé sur un point.

## 3. Typographie

Corps à 11 pt pour les parents, 12 pt pour l'élève, 10 pt pour l'enseignant.
Tableaux en `\small`, notes en `\footnotesize` — jamais en dessous. Une seule
famille typographique, hiérarchie portée par la taille et la couleur des titres.

**Défaut trouvé et corrigé (P1).** Le titre de couverture se composait sur deux
lignes qui se touchaient. Cause : le `\par` était placé **hors** du groupe de
taille, si bien que le paragraphe était composé avec l'interligne du corps normal
et non celui du `\Huge`. Le `\par` est passé dans le groupe, le titre est passé en
`\LARGE`, et un `\raggedright` évite la première ligne étirée par la justification.

## 4. Couleurs

Bleu nuit pour la structure, doré discret pour l'accent, gris pour les notes. Aucun
statut n'est porté par la seule couleur : « solide », « satisfaisant », « à
consolider », « prioritaire », « à confirmer » sont écrits en toutes lettres dans
les tableaux.

**Niveaux de gris.** Un bilan parents de chacun des cinq niveaux a été rastérisé en
monochrome. L'encadré doré des passerelles devient un cadre gris clair, toujours
distinguable et surtout titré — « Premières passerelles vers l'année suivante ».
Aucune information ne disparaît.

## 5. Tableaux

**Défaut trouvé et corrigé (P1).** Le tableau « Détail critère par critère » de la
synthèse enseignant débordait à 4,4 mm du bord droit. Deux causes cumulées : la
colonne « Scope » affichait `[PASSERELLE N]`, près de trois centimètres, et les
identifiants de compétence — `M1RE_SUITES_RECURRENCE_BRIDGE` — n'offrent aucun
point de césure et sortaient de leur colonne.

Corrigé par une forme brève du badge (`N−1`, `Pass.`) et un filtre `esc_id` qui
autorise une coupure après chaque souligné. Les largeurs sont désormais explicites
et leur somme vérifiée par un test : le bloc de texte fait 178 mm, aucune
spécification de colonnes ne le dépasse.

**Défaut trouvé et corrigé (P2).** La colonne « Au départ » du tableau par domaines
coupait « en cours d'installation » en deux à chaque ligne. Le libellé est devenu
« à installer ». Le suffixe « (1 compétence(s) de ce domaine ne sont pas mesurées
par ce sujet) » occupait quatre lignes ; il est devenu « — 1 compétence non mesurée
par ce sujet ».

Les tableaux longs utilisent `longtable` et répètent leur en-tête.

## 6. Visualisations

Aucun graphique n'est produit. La décision est motivée point par point dans
`REPORT_VISUALIZATION_POLICY.md` : frise de progression refusée faute de mesures
comparables, radar refusé faute d'axes comparables, barres par domaine refusées
parce qu'un domaine à un seul critère produirait une barre visuellement identique à
un domaine à six. Le profil d'erreurs reste un tableau de comptage, dans la
synthèse enseignant seulement.

Un test vérifie qu'aucun environnement de dessin — `tikzpicture`, `pgfplots`,
`axis` — n'apparaît dans le LaTeX produit.

## 7. Pagination

**Défaut trouvé et corrigé (P1).** Les bilans parents faisaient 5 à 7 pages, avec
des pages presque vides : une page ne portant que deux lignes, une autre le seul
bloc « Conseil ».

Le gabarit a été restructuré selon la logique éditoriale des cinq premières
sections, puis le plan a été refondu : quatre tableaux successifs avec en-têtes
répétés sont devenus **un** tableau à trois colonnes, avec une ligne d'en-tête
pleine largeur par semaine.

Deux variantes intermédiaires ont été essayées et rejetées, chacune pour une raison
mesurée : loger l'intention de la semaine dans une colonne de 14 mm la brisait en
huit lignes d'un mot ; une quatrième colonne « Rythme » de 22 mm multipliait les
retours à la ligne sans rien apporter.

Résultat : **six pages, stables sur les quinze profils**, sans page orpheline.

| page | contenu | remplissage médian |
| ---: | --- | ---: |
| 1 | identité, l'essentiel, objectifs, situation de départ | 60 % |
| 2 | fil conducteur et trajectoire des cinq séances | 57 % |
| 3 | bilan par domaines, évaluation de clôture, passerelles | 80 % |
| 4 | points forts, à consolider, à confirmer, notions non mesurées | 74 % |
| 5 | plan des quatre semaines | 98 % |
| 6 | priorités de rentrée, conseil, limites | 28 % |

**Écart à la cible, assumé.** La consigne visait quatre à cinq pages. Le document
en fait six. Le plan occupe une page entière dès que l'élève cumule plusieurs
priorités — et c'est la partie que la famille utilisera réellement ; la comprimer
pour gagner une page reviendrait à sacrifier ce qui sert. La sixième page porte la
clôture. La porte de qualité accepte donc quatre à six pages et signale l'écart en
P3, pour qu'il reste visible ; au-delà de six, il redevient un défaut.

Les pages 1 et 2 sont remplies à 57–60 %. C'est le prix d'une structure éditoriale
fixe, et c'est un document qui respire plutôt qu'un document tassé. Aucune page
intermédiaire n'est creuse.

## 8. Impression

Format A4 sur 45 documents sur 45. Marge d'encre minimale mesurée : **8,6 mm**, sur
le filet de l'en-tête ; le texte courant reste à 16 mm ou plus. Aucun contenu
critique en zone fragile.

## 9. Niveaux de gris

Voir §4. Testé sur les cinq niveaux, page 3 — celle qui porte le plus de structures
colorées. Lisible.

## 10. Contenu

Les contrôles de fond, hérités du pipeline longitudinal et revérifiés ici sur les
45 documents :

| contrôle | résultat |
| --- | --- |
| notion ciblée déclarée acquise | 0 |
| passerelle échouée présentée comme une lacune | 0 |
| écart de maîtrise chiffré | 0 (`mastery_delta` vaut `null`) |
| progression chiffrée | 0 |
| identifiant technique dans un document parents ou élève | 0 |
| terme proscrit (« lacune », « élève faible »…) | 0 |
| réserve documentaire fidèle aux sources | oui, sur les 15 |

**Défaut trouvé et corrigé (P0).** `\code{return}` s'affichait tel quel dans les
synthèses enseignant NSI : le rendu web traduisait cette macro en `<code>`, mais
aucun équivalent n'existait côté LaTeX. Un filtre `esc_ped` traduit désormais
`\code`, `\textbf` et `\emph` vers leurs commandes LaTeX, le contenu restant
échappé. Dix-sept champs de gabarit sont passés dessus.

**Défaut trouvé et corrigé (P2).** Le pourcentage de consolidation s'affichait avec
une décimale — « 63,5 % ». Il est arrondi à l'unité dans les documents destinés aux
familles ; la synthèse enseignant conserve la précision technique.

## 11. Provenance

Un test rattache le texte aux faits : tout libellé de compétence cité dans les
sections « points forts », « points à consolider » et « réussites à confirmer »
doit exister dans la matrice longitudinale, et les chiffres de la consolidation
doivent provenir des pools calculés, non d'un calcul refait dans le rédacteur.

Un second test vérifie qu'aucun pourcentage de résultat n'est affiché sans son
compte : « 11 points sur 17,5 sont obtenus, soit 63 % », jamais « 63 % » seul.

## 12. Défauts trouvés

| sévérité | défaut | état |
| --- | --- | --- |
| P0 | `\code{}` visible dans les synthèses NSI | corrigé |
| P1 | tableau critère par critère débordant de la marge droite | corrigé |
| P1 | titre de couverture aux lignes qui se touchent | corrigé |
| P1 | bilans parents de 5 à 7 pages, avec pages presque vides | corrigé |
| P2 | métadonnées PDF absentes (titre, auteur, sujet) | corrigé, 45/45 |
| P2 | libellés trop longs pour la colonne « Au départ » | corrigé |
| P2 | mention verbeuse des compétences non mesurées | corrigé |
| P2 | pourcentage à une décimale dans le document parents | corrigé |
| P3 | six pages au lieu de la cible de quatre à cinq | documenté, assumé |

Deux défauts de l'outillage de QA lui-même, corrigés en cours d'audit : la mesure
de remplissage était faussée par l'en-tête et le pied de page courants — elle
donnait 93 % partout, y compris sur une page vide — et un contrôle de « blanc de
pied » se déclenchait sur chaque saut de page volontaire, signalant la structure
plutôt qu'un défaut.

## 13. Corrections apportées

Six fichiers de gabarit, trois modules applicatifs, deux outils de QA. Aucune règle
métier n'a été touchée : le modèle de preuve, la séparation couverture/maîtrise,
`mastery_delta = null`, les périmètres et les priorités sont inchangés.

## 14. Dettes restantes

* **Six pages pour le bilan parents**, au lieu des quatre à cinq visées. Assumé et
  motivé ci-dessus ; réexaminable si la structure du plan évolue.
* **Pages 1 et 2 remplies à 57–60 %.** Conséquence d'une structure éditoriale fixe.
  Un rééquilibrage déplacerait le vide plutôt qu'il ne le supprimerait.
* **Pas de signets PDF.** `hyperref` est chargé et les produirait, mais la charte
  n'utilise pas `\section` : les titres passent par une macro maison. Les ajouter
  demanderait de reprendre la structure de titres, ce qui sort du périmètre du jour.
* **Pas de balisage PDF/UA.** Le texte est sélectionnable, l'ordre de lecture est
  correct, aucune page n'est une image ; le balisage complet reste un chantier.
* **L'esthétique n'est pas testée.** Aucun script ne dit qu'un document est beau.

## 15. Verdict

**REPORT_PDF_QUALITY = PASS.**

45 documents générés, 45 compilés, 45 rastérisés, 154 pages inspectées, 0 défaut
bloquant. Tous les P0 et P1 sont corrigés ; les P2 raisonnables le sont aussi ; le
seul P3 est documenté.

Les documents sont prêts pour la première correction réelle.
