# Contrôle visuel manuel — page d'Inès KEFI

À faire **avant** de saisir la vraie copie. Playwright n'est pas installé sur ce poste :
les parcours sont couverts par `TestClient` et par des contrôles DOM, mais le rendu
réel dans un navigateur ne l'est pas. Ces dix minutes le couvrent.

```bash
make s5-correction-run
```

puis ouvrir `http://127.0.0.1:8765/eleve/ines-kefi`.

## 0. Contrôle de la micro-passe finale (version 1.1.1)

Les quatorze points ci-dessous valident la dernière passe avant la saisie réelle.
Ils se font d'un seul parcours de la page, du haut vers le bas.

- [ ] **1.** L'en-tête annonce « **22 critères du sujet · 0 / 23 lignes analytiques renseignées — 0 %** »
- [ ] **2.** Aucune séquence `\begin{enumerate}`, `\item` ou `\end{enumerate}` n'est visible nulle part sur la page
- [ ] **3.** **B2** affiche une vraie liste numérotée : 1. Développer… 2. Réduire ensuite… 3. Contrôler…
- [ ] **4.** **B3** affiche une vraie liste numérotée (fréquence, puis moyenne)
- [ ] **5.** **C1** affiche une vraie liste numérotée de quatre questions, précédée du titre en gras « L'atelier de peinture. »
- [ ] **6.** **C2** affiche une vraie liste numérotée de deux questions
- [ ] **7.** KaTeX fonctionne : `5(x − 3)`, les fractions et `(−4) × (−7)` sont typographiés, aucun `$` visible
- [ ] **8.** Le PDF reste collant : descendre jusqu'en bas, il est toujours affiché
- [ ] **9.** **B2** montre trois lignes marquées, dans l'ordre : `PASSERELLE N`, `PASSERELLE N`, `N-1`
- [ ] **10.** **A3** montre deux lignes : un sous-critère `N-1` (regroupement des termes en x) et un sous-critère `PASSERELLE N` (écriture réduite complète)
- [ ] **11.** **C2_c2** ne montre **qu'une seule** limite d'interprétation — celle qui cite « A1, A5 et C2 question 1 »
- [ ] **12.** Les raccourcis sont neutralisés dans les zones de saisie (détail en section 8)
- [ ] **13.** Les observations générales sont inchangées : six listes déroulantes et une remarque libre
- [ ] **14.** Le corrigé est masqué tant qu'on n'a pas cliqué « Afficher le corrigé et le barème »

Si le point 11 échoue, la base n'a pas été réimportée depuis la micro-passe :
`python3 tools/init_database.py --force`, puis recharger.

## 1. Mathématiques rendues

- [ ] L'énoncé de **A2** affiche une vraie fraction — barre horizontale, numérateur au-dessus — et non `$\dfrac{5}{8} - \dfrac{1}{4}$`
- [ ] L'énoncé de **A6** affiche `2/3 = …/15` typographié
- [ ] **A4** affiche `37°` avec un vrai symbole degré
- [ ] Aucun `$`, `\frac`, `\dfrac` ou `\circ` visible à l'écran
- [ ] Ouvrir le corrigé de **A1** : la réponse `0` est typographiée
- [ ] Couper le réseau et recharger : le rendu est identique — KaTeX est servi depuis le dépôt

## 2. PDF collant

- [ ] Le sujet distribué s'affiche à gauche au chargement
- [ ] Descendre jusqu'au critère **C2_c2**, tout en bas : le PDF est **toujours visible**
- [ ] Le PDF ne recouvre jamais le bandeau bleu nuit du haut
- [ ] Le PDF reste utilisable : on peut faire défiler ses pages indépendamment de la grille
- [ ] Réduire la fenêtre sous ~1100 px : deux onglets « Sujet » / « Correction » apparaissent, le sticky disparaît

## 3. Premier contact

- [ ] Le bandeau annonce « **23 lignes analytiques restent à renseigner pour les 22 critères du sujet** » — jamais « 22 points »
- [ ] Le compte des lignes (23) et celui des critères du sujet (22) sont tous deux lisibles, et ne se confondent pas
- [ ] Le détail est **replié** : on voit une seule ligne, pas une liste de 23
- [ ] Cliquer « Voir le détail » déplie la liste
- [ ] Cliquer « Valider la correction » sans rien saisir : la page de refus liste les manques, et le retour rouvre le détail automatiquement
- [ ] Dans ce détail, **A3 n'apparaît qu'une fois**, avec ses deux sous-critères imbriqués — le sujet papier ne comportait qu'une question A3

## 4. Panneau de score

- [ ] **B1_c1** propose cinq valeurs : 0 / 0,25 / 0,5 / 0,75 / 1
- [ ] **A1_c1** n'en propose que trois : 0 / 0,5 / 1 — parce que rien ne justifiait les quarts
- [ ] **B3_c3** n'en propose que deux : 0 / 0,3 — l'encadrement est écrit ou il ne l'est pas
- [ ] **A3** apparaît en **deux lignes** notées, l'une marquée `N-1`, l'autre `PASSERELLE N`

## 5. Rubrique compréhensible

- [ ] Sous les boutons, « Règle d'attribution des points » est déjà ouverte
- [ ] Sur **B1_c1**, la ligne 0,75 dit précisément : « les deux calculs exacts, une unité manquante ou erronée »
- [ ] La question « pourquoi 0,5 plutôt que 0,75 ? » trouve sa réponse sans ouvrir le corrigé
- [ ] Après avoir cliqué un score, la ligne correspondante de la rubrique se surligne en vert

## 6. Corrigé fermé

- [ ] Le titre de **A1_c1** dit « Somme algébrique de relatifs, avec soustraction d'un négatif » — **pas** « résultat 0 exact »
- [ ] Le titre de **A2_c1** ne montre pas `3/8`
- [ ] Restent visibles sans ouvrir : la portée (`N-1` / `PASSERELLE N`), la compétence, le type de preuve, le maximum
- [ ] Ouvrir « Afficher le corrigé et le barème » : la réponse attendue, les étapes, la rubrique, le classement curriculaire et **la source officielle** apparaissent

## 7. Erreurs propres au critère

- [ ] **B1_c1** (aire) : les suggestions sont `CONCEPT`, `NOTATION`, `CALCUL` — et « prix calculé à partir du périmètre » n'y figure **pas**
- [ ] **B1_c2** (prix) : la suggestion `METHODE` dit bien « prix calculé à partir du périmètre »
- [ ] **B2_c1** (développement) : « distributivité appliquée au seul premier terme »
- [ ] **B2_c2** (réduction) : « termes en x et constantes additionnés ensemble »
- [ ] **B2_c3** (contrôle) : `CONTROLE`, « aucun contrôle mené » — et rien sur la distributivité
- [ ] Aucune suggestion n'est cochée d'avance
- [ ] « Autre code d'erreur que ceux suggérés » donne accès aux codes restants

## 8. Raccourcis sûrs

Les tests automatisés vérifient que les raccourcis sont neutralisés dans `input`,
`textarea`, `select`, `button`, les éléments `contenteditable` et les rôles ARIA
interactifs. Ce qu'ils ne voient pas, c'est le comportement réel du navigateur.
Ce contrôle est donc **à faire à la main**, deux fois.

**Essai A — « Observation sur ce critère ».** Cliquer dans la zone d'observation
d'un critère quelconque, puis taper exactement :

```
F N E O 0 1 2 3 4 5
```

- [ ] le score du critère est **inchangé**
- [ ] le critère courant est **inchangé** — la page n'a pas défilé vers un autre
- [ ] **aucun panneau** ne s'est ouvert (ni corrigé, ni rubrique, ni codes d'erreur)
- [ ] **aucun code d'erreur** n'a été activé
- [ ] le texte `F N E O 0 1 2 3 4 5` est **intégralement présent** dans la zone

**Essai B — « Remarque libre ».** Descendre aux observations générales, cliquer
dans la grande zone « Remarque libre », taper la même séquence :

- [ ] les cinq mêmes constats, à l'identique

**Contre-épreuve.** Cliquer en dehors de tout champ de saisie :

- [ ] `F` met le plein score et passe au critère suivant — les raccourcis
      fonctionnent donc toujours là où ils doivent fonctionner
- [ ] Même essai dans un `select` des observations générales : rien ne bouge

## 9. Observations générales compactes

- [ ] Six listes déroulantes — autonomie, méthode, rythme, rédaction, contrôle, attitude face à l'erreur
- [ ] Chacune a un commentaire facultatif d'une ligne
- [ ] Une seule grande zone reste : « Remarque libre »
- [ ] La durée observée est saisissable et annoncée comme n'entrant dans aucun calcul
- [ ] « Enregistrer les observations » affiche une heure d'enregistrement

## 10. Validation

- [ ] Renseigner les 23 lignes notées avec des valeurs de test
- [ ] L'indicateur passe à « 22 critères du sujet · 23 / 23 lignes analytiques renseignées — 100 % »
- [ ] « Valider la correction » aboutit et bascule vers l'analyse
- [ ] L'analyse affiche **17,5** points d'acquis N−1 et **2,5** points de passerelle

> **Après ce contrôle, remettre la base à zéro** avant la vraie saisie :
> `python3 tools/init_database.py --force` (une sauvegarde est prise automatiquement).
> Les valeurs de test ne doivent pas se mélanger à la correction réelle.

## Ce que ce contrôle ne remplace pas

La justesse pédagogique des rubriques et des statuts ne se juge qu'en corrigeant une
vraie copie. C'est l'objet de `PILOT_REAL_COPY_VALIDATION.md`.
