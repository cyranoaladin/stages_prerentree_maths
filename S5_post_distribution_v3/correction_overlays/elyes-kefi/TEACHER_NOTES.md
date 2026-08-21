# Notes de correction — Elyes KEFI

**Entrée en Troisième — Mathématiques.** Document de travail enseignant. Il ne remplace aucun livret et ne modifie aucune question.

## Ce que ce dossier change, et ce qu'il ne change pas

Le sujet et l'évaluation ont été imprimés et remis à l'élève. Ils sont figés. Ce qui suit ne porte que sur la correction et sur ce qu'il est légitime d'en conclure.

## Deux décomptes séparés

| | points disponibles |
| --- | ---: |
| consolidation des acquis de l'année N-1 | 18.50 |
| passerelles vers l'année N | 1.50 |
| **score brut au sujet de clôture** | **20.00** |

Le score brut sur 20 n'est pas le diagnostic de consolidation N-1. Une non-réussite sur une passerelle ne produit ni « fragile », ni « non acquis », ni priorité de remédiation.

## Critères de passerelle — à ne jamais lire comme un déficit

- `3E_ELYES_KEFI_B2_c3` (B2, 0.50 pt) — M3_TRIGO_SIN_BRIDGE
  - la question 3 demande le rapport liant le côté opposé et l'hypoténuse : le sinus, qui appartient au programme de Troisième et non à celui de Quatrième.
  - limite : une non-réussite ne documente aucune fragilité sur la trigonométrie de Quatrième, mesurée aux critères 1 et 2 du même item
- `3E_ELYES_KEFI_C2_c1` (C2, 1.00 pt) — M3_LIT_DOUBLE_DISTRIB_BRIDGE
  - (x+4)(x+3) relève du double produit, introduit en phase 4 de la séance. Le skill_id d'origine M3E_LIT_01 porte la distributivité simple k(ax+b), acquis de Quatrième.

## Questions à correction prudente

### B4 — critère `3E_ELYES_KEFI_B4_c2` (0.50 pt)

Consigne réellement imprimée : « Indiquer un contrôle qui aurait détecté cet oubli. »

- accepté : recomptage de l'effectif : cinq valeurs annoncées, quatre utilisées
- accepté : recalcul de la somme et confrontation à la liste source
- accepté : confrontation terme à terme de la série employée et de la série donnée
- refusé comme preuve de détection : l'encadrement de la moyenne entre la plus petite et la plus grande valeur : c'est un contrôle de vraisemblance parfaitement légitime, mais 11,25 appartient à l'intervalle [5 ; 15]. Dans ce cas précis, il ne détecte pas l'omission.
- règle de correction : l'encadrement ne peut jamais être exigé comme preuve qu'une omission a été détectée. Un élève qui le propose comme unique contrôle n'obtient pas ce critère, mais aucun code d'erreur de méthode n'est porté : le contrôle proposé est correct, il est seulement insuffisant ici.
- limite d'interprétation : la distinction entre contrôle de vraisemblance et contrôle détecteur est fine ; la non-réussite ne documente pas une absence de pratique du contrôle

### B4 — critère `3E_ELYES_KEFI_B4_c3` (0.50 pt)

Consigne réellement imprimée : « Expliquer pourquoi l'encadrement de la moyenne entre la plus petite et la plus grande valeur ne l'aurait pas détecté. »

- accepté : toute formulation établissant que 11,25 reste compris entre 5 et 15, donc que l'encadrement est vérifié malgré l'erreur
- règle de correction : la réponse attendue est une explication, pas un calcul ; toute formulation correcte est créditée intégralement.

## Saisie

La saisie se fait critère par critère, dans `responses/responses_v3_TEMPLATE_elyes-kefi.json`. Un code d'erreur ne se porte que sur le critère effectivement échoué.
