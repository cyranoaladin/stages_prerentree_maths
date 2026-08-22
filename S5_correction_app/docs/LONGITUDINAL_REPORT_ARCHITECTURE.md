# Architecture du pipeline de bilan longitudinal

## L'ordre des étapes est la garantie

```
sources → normalisation → faits structurés → calcul déterministe
        → règles pédagogiques → LONGITUDINAL_FACTS.json → rédaction
```

Aucune rédaction ne commence avant que les faits ne soient figés et empreintés. Un
générateur de texte — déterministe aujourd'hui, éventuellement assisté demain —
n'accède jamais aux documents sources : il reçoit les faits, et seulement eux.
C'est ce qui rend chaque phrase du bilan traçable jusqu'à un document daté.

## Modules

| module | rôle |
| --- | --- |
| `longitudinal/sources.py` | retrouve les documents déclarés, les empreinte en SHA-256, **nomme les absents** |
| `longitudinal/dossier.py` | lit le dossier individuel : objectifs personnalisés par séance, état des tableaux de suivi |
| `longitudinal/evidence_levels.py` | hiérarchie de preuve A/B/C/D, statuts de trajectoire, couverture |
| `longitudinal/trajectory.py` | matrice longitudinale, une ligne par compétence |
| `longitudinal/plan.py` | plan des quatre semaines, seuils mesurables, plafond de deux P1 |
| `longitudinal/facts.py` | assemble et empreinte `LONGITUDINAL_FACTS` |
| `longitudinal/narrative.py` | rédaction déterministe, à partir des faits seuls |
| `longitudinal/guard.py` | contrôle du texte **avant** compilation |
| `longitudinal/render.py` | contexte du gabarit, compilation, manifeste |
| `longitudinal/service.py` | orchestration, verrous d'entrée, péremption |

## Ce que le pipeline consomme

Le socle existait déjà : la couche de clôture produit pour chaque élève un
`student_learning_profile.json` qui porte le diagnostic initial par compétence, les
séances où chaque compétence a été ciblée, les questions du test initial qui lui
correspondent, et le contexte de récence. L'import de l'application en retenait
seulement le statut initial et sa preuve ; la version 3 du schéma conserve le reste.

| source | rôle | niveau de preuve |
| --- | --- | --- |
| `4e/03_EVALUATIONS/4e_Test_Initial.pdf` | instrument du positionnement | A (via le profil) |
| `student_learning_profile.json` | diagnostic normalisé par compétence | A |
| `4e_Dossier_Individuel_<Élève>.md` | objectifs personnalisés par séance, suivi | C (B si le suivi est rempli) |
| `4e_Remediation_Ciblee_<Élève>_*.md` | exercices prescrits par domaine | C |
| `4e/02_SEANCES/S1..S5/` | matériel de niveau | C |
| dossiers de séance personnalisés | livrets remis à l'élève | C |
| correction validée dans l'application | critères notés sur la copie réelle | A |

## Schéma de données (version 3)

`baseline_status` gagne sept colonnes (questions du test initial, séances de
travail, ciblage en séance 5, état de la preuve de séance, priorité provisoire,
domaine, importance). Quatre tables sont créées : `longitudinal_facts`,
`skill_trajectory`, `action_plan_item`, `report_source`.

Les sections éditables du bilan restent portées par `report_block`, qui possède déjà
`source` (`deterministic` / `llm` / `human`) et `approved` : une version approuvée par
l'enseignant n'est jamais réécrasée par une régénération.

## Verrous

* **correction validée exigée.** Un brouillon peut encore changer ; un bilan remis à
  une famille, non ;
* **péremption.** Les faits sont liés à une révision de correction. Rouvrir la copie
  crée une nouvelle correction : le bilan antérieur devient périmé et le système le
  dit. La recherche de péremption porte sur l'évaluation, pas sur l'identifiant de
  correction, précisément parce que celui-ci change à la réouverture ;
* **contrôle avant compilation.** Un texte refusé n'est jamais compilé : sous forme
  de PDF, il serait déjà transmissible.

## Immutabilité

Aucun document distribué n'est lu en écriture. Les bilans sont des artefacts
nouveaux, écrits sous `runtime/`, hors de Git.
