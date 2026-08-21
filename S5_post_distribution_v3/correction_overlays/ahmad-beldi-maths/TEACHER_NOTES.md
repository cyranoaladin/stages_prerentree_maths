# Notes de correction — Ahmad BELDI

**Entrée en Première générale — Spécialité mathématiques — Mathématiques.** Document de travail enseignant. Il ne remplace aucun livret et ne modifie aucune question.

## Ce que ce dossier change, et ce qu'il ne change pas

Le sujet et l'évaluation ont été imprimés et remis à l'élève. Ils sont figés. Ce qui suit ne porte que sur la correction et sur ce qu'il est légitime d'en conclure.

## Deux décomptes séparés

| | points disponibles |
| --- | ---: |
| consolidation des acquis de l'année N-1 | 17.50 |
| passerelles vers l'année N | 2.50 |
| **score brut au sujet de clôture** | **20.00** |

Le score brut sur 20 n'est pas le diagnostic de consolidation N-1. Une non-réussite sur une passerelle ne produit ni « fragile », ni « non acquis », ni priorité de remédiation.

## Critères de passerelle — à ne jamais lire comme un déficit

- `1ERE_SPE_AHMAD_BELDI_C1_c4` (C1, 1.00 pt) — **critère mixte**
  - « Écrire la relation liant u_(n+1) et u_n, puis calculer u_2 » agrège en un seul critère une notation de Première et un calcul d'évolution successive de Seconde. Le critère imprimé est indivisible ; il est donc éclaté en sous-critères analytiques virtuels, à somme de points strictement égale.
  - sous-critères analytiques virtuels :
    - `1ERE_SPE_AHMAD_BELDI_C1_c4_v1` 0.50 pt — bridge_n — relation de récurrence u_(n+1) = 1,04 x u_n correctement écrite
    - `1ERE_SPE_AHMAD_BELDI_C1_c4_v2` 0.50 pt — n_minus_1 — u_2 obtenu par application répétée du coefficient multiplicateur, évalué à partir de la relation écrite par l'élève
- `1ERE_SPE_AHMAD_BELDI_C2_c1` (C2, 1.00 pt) — M1RE_SUITES_RECURRENCE_BRIDGE
  - l'écriture de u_(n+1) en fonction de u_n est la notation de suite introduite en phase 4 de la séance ; le manifeste marque déjà cet item « not_comparable ».
- `1ERE_SPE_AHMAD_BELDI_C2_c2` (C2, 1.00 pt) — M1RE_SUITES_RECURRENCE_BRIDGE
  - u_2 est ici demandé dans le cadre de la suite ; le classer en N-1 ferait retomber sur la consolidation de Seconde l'échec éventuel d'une notation nouvelle. Le coefficient multiplicateur reste mesuré en N-1 par les deux critères de l'item B3.

## Questions à correction prudente

### B2 — critère `1ERE_SPE_AHMAD_BELDI_B2_c2` (0.60 pt)

Consigne réellement imprimée : « Soit x un réel tel que 0 < x < 1. Comparer x^2 et x, puis justifier la réponse par un exemple numérique et par un argument valable pour tout x de cet intervalle. »

- niveau demandé : comparaison correcte (x^2 < x) et argument valable pour tout x : signe de x(x-1), ou multiplication de 0 < x < 1 par x > 0.
- preuve renforcée : rédaction formelle du tableau de signes de x(x-1). Valorisée, jamais exigée.
- règle de correction : aucun formalisme non demandé par la consigne imprimée ne conditionne l'attribution des points.
- limite d'interprétation : cet item, seul, ne prouve pas une compétence de démonstration universelle

### B4 — critère `1ERE_SPE_AHMAD_BELDI_B4_c1` (0.75 pt)

Consigne réellement imprimée : « Soit x un réel tel que 0 < x < 1. Comparer x^3 et x^2 : donner d'abord un argument valable pour tout x de cet intervalle, puis illustrer par un exemple numérique. »

- niveau demandé : comparaison correcte (x^3 < x^2) assortie d'un argument valable pour tout x de l'intervalle. Tout argument général correct convient : signe de x^2(x-1), multiplication de 0 < x < 1 par x^2 > 0, ou comparaison des facteurs.
- preuve renforcée : rédaction formelle du signe de x^2(x-1) sur ]0 ; 1[. Elle est valorisée qualitativement en observation, jamais exigée pour accorder les points promis par la consigne imprimée.
- règle de correction : la consigne imprimée demande « un argument valable pour tout x », non une démonstration formelle. Aucun élève n'est pénalisé pour l'absence d'un formalisme que la consigne ne réclame pas. L'exemple numérique est rétribué par son propre critère et ne peut pas tenir lieu d'argument général.
- limite d'interprétation : cet item, seul, ne prouve pas une compétence de démonstration universelle : il porte sur un intervalle donné et sur deux puissances voisines

### B4 — critère `1ERE_SPE_AHMAD_BELDI_B4_c2` (0.25 pt)

Consigne réellement imprimée : « …puis illustrer par un exemple numérique. »

- règle de correction : tout exemple numérique cohérent appartenant à ]0 ; 1[ est crédité. Sa présentation comme illustration et non comme preuve est attendue mais n'est pas une condition d'attribution des points.

## Saisie

La saisie se fait critère par critère, dans `responses/responses_v3_TEMPLATE_ahmad-beldi-maths.json`. Un code d'erreur ne se porte que sur le critère effectivement échoué.
