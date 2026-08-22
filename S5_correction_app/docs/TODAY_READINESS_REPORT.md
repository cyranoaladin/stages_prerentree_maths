# Mise en service — rapport de contrôle

Contrôle conduit le 22 août 2026, avant la première correction réelle. Aucune copie
d'élève n'a été saisie : toutes les vérifications reposent sur des fixtures
synthétiques, dans des bases jetables, détruites après usage.

## Portes

| Gate | Résultat | Détail |
| --- | --- | --- |
| 15 élèves × matières | **PASS** | 15 élèves, 15 évaluations reconnus |
| Sources longitudinales | **PASS** | 0 bloqué, 15 prêts avec réserve documentaire |
| Web renderer | **PASS** | 0 séquence LaTeX brute sur les 15 pages, 0 repli nécessaire |
| NSI | **PASS** | `lstlisting` et `tabularx` convertis ; 31 tests dédiés |
| Correction | **PASS** | 15/15 copies synthétiques saisies et validées |
| Analyse | **PASS** | 15/15 analyses déterministes produites |
| Parents PDF | **PASS** | 15/15 compilés |
| Élève PDF | **PASS** | 15/15 compilés |
| Enseignant PDF | **PASS** | 15/15 compilés |
| Plan 4 semaines | **PASS** | P1 ≤ 2 partout, ≤ 3 objectifs par semaine, charge 15–20 min |
| Immutabilité | **PASS** | 60/60, `changed = 0`, `missing = 0` |
| Confidentialité | **PASS** | aucune donnée réelle suivie par Git (4 359 fichiers contrôlés) |
| DB safety | **PASS** | réinitialisation destructrice refusée, base intacte |

**TODAY_READINESS = PASS**

## Ce qui a été levé

### Le blocker NSI

Deux couples — Ahmad BELDI (NSI) et Ahmed BENHADJ SALEM — avaient des énoncés
comportant du code Python et un tableau d'état. L'interface affichait
`\begin{lstlisting}` en toutes lettres, ce qui rendait la correction pénible.

`lstlisting` devient un bloc de code inerte, indentation conservée — en Python elle
porte le sens — et contenu échappé. `tabularx` devient un tableau lorsque sa forme
est celle du corpus, et un renvoi au PDF distribué sinon.

**Un test a trouvé un défaut que l'inventaire n'avait pas vu.** Le balayage des pages
réelles a révélé que `\code{...}` s'affichait brut dans **deux blocs de suggestions
d'erreur** — pas seulement dans les énoncés. Onze champs du référentiel passent
désormais par le renderer, et un filtre distinct sert les attributs HTML, où des
balises n'ont rien à faire.

Le balayage final ne trouve **aucune** des séquences `\begin{`, `\end{`, `\item`,
`\code{`, `\textbf{`, `\emph{`, `\hline` sur les quinze pages.

### La compilation des 45 documents

Le premier passage a produit 29 PDF sur 45. La cause : des caractères typographiques
que le moteur LaTeX refuse.

La première correction, fondée sur une liste devinée, a porté le score à 39/45 — et
c'était la mauvaise méthode. La seconde a relevé **tous** les caractères non-ASCII
réellement présents dans le corpus, les a soumis un par un à une compilation d'essai,
et n'a traité que les six qui échouaient : `−` (106 occurrences), `∪`, `⁵`, `≥`, `⁻`,
`⁴`. Les neuf autres — `« » ° ² ³ × ÷ — …` — passent et ne sont pas touchés.

S'y ajoute un filet de sécurité : un caractère imprévu est décomposé en ASCII, ou
retiré. Perdre un glyphe exotique vaut mieux que perdre le document.

Résultat : **45/45**.

### Deux défauts trouvés par les tests

1. **La semaine 4 du plan produisait cinq objectifs** lorsque l'élève cumulait les
   priorités : les réévaluations s'ajoutaient au vivier au lieu de le remplacer. La
   semaine 4 ne puise plus dans le vivier — elle réévalue au plus deux priorités,
   puis clôt par le bilan cumulatif.
2. **La garde de base n'existait pas.** `init_database.py --force` détruisait sans
   sommation. Elle refuse désormais dès qu'une correction non synthétique porte un
   score ou une observation, sort en code 3, et laisse la base **intacte au bit près**
   — vérifié par empreinte avant et après.

## État des quinze

Aucun couple n'est bloqué. Les quinze sont `READY_WITH_DOCUMENTARY_WARNING`, et la
raison est la même pour tous : **les tableaux d'observation de séance des dossiers
individuels sont des formulaires vierges**. Le bilan pourra donc écrire « cette
notion a fait l'objet d'un travail ciblé en S2 », jamais « l'élève l'a réussie en
S2 ». C'est exactement ce que le niveau de preuve C signifie.

S'y ajoutent, selon les dossiers :

* des **dossiers de séance personnalisés absents** — cinq pour les trois élèves de
  première spécialité, un ou deux ailleurs. Le thème de la séance reste connu par le
  matériel de niveau ; la personnalisation ne l'est pas, et rien n'est inventé ;
* pour **onze profils sur quinze**, un diagnostic initial sans observation rédigée
  par domaine. Les statuts par compétence sont présents partout, donc la trajectoire
  reste calculable ; seule la page « situation de départ » sera plus brève.

Le détail élève par élève est dans `LONGITUDINAL_READINESS_15.md`, et le manifeste
complet de chacun sous `runtime/readiness/<élève>/`.

`READY_FOR_CORRECTION` n'est atteint par personne aujourd'hui. Ce n'est pas un
défaut du système : c'est l'état réel de la documentation, et l'état existe pour
être atteignable le jour où les grilles d'observation seront renseignées.

## Tests

| suite | tests |
| --- | ---: |
| suite projet | 25 |
| post-distribution V3 | 98 (4 ignorés) |
| application correction | **250** (1 ignoré) |
| dont bilan longitudinal | 39 |
| dont rendu NSI | 31 |
| dont mise en service | 26 |
| dont micro-passe Inès | 34 |
| dont pilote Inès | 28 |
| harness `test_analyze_s5` | 48 |

Aucun échec, aucun test supprimé, aucun `FAIL` transformé en `skip`.

## Dettes assumées

Elles ne bloquent pas la mise en service et sont documentées comme telles :

* Playwright absent — le rendu navigateur se contrôle à la main ;
* bilan parents en **cinq pages**, format accepté ;
* séances sans dossier personnalisé, documentées dans chaque bilan ;
* aucun LLM branché — le générateur déterministe suffit ;
* pas d'authentification en local.

## Prochaine action humaine

```bash
make s5-correction-backup
make s5-correction-run
```

Corriger réellement Inès KEFI, valider, ouvrir le bilan longitudinal, générer les
trois documents, et les faire relire **avant** de traiter les quatorze autres.

Le statut reste `READY_FOR_LONGITUDINAL_PILOT`. Il ne passera à
`OPERATIONALLY_VALIDATED` qu'après confirmation humaine que l'analyse est cohérente,
le bilan fidèle, le plan pertinent et les PDF corrects.
