# Notes de correction — Malek KHADHRANI

**Entrée en Première générale — Spécialité mathématiques — Mathématiques.** Document de travail enseignant. Il ne remplace aucun livret et ne modifie aucune question.

## Ce que ce dossier change, et ce qu'il ne change pas

Le sujet et l'évaluation ont été imprimés et remis à l'élève. Ils sont figés. Ce qui suit ne porte que sur la correction et sur ce qu'il est légitime d'en conclure.

## Deux décomptes séparés

| | points disponibles |
| --- | ---: |
| consolidation des acquis de l'année N-1 | 19.50 |
| passerelles vers l'année N | 0.50 |
| **score brut au sujet de clôture** | **20.00** |

Le score brut sur 20 n'est pas le diagnostic de consolidation N-1. Une non-réussite sur une passerelle ne produit ni « fragile », ni « non acquis », ni priorité de remédiation.

## Critères de passerelle — à ne jamais lire comme un déficit

- `1ERE_SPE_MALEK_KHADHRANI_C1_c4` (C1, 1.00 pt) — **critère mixte**
  - « Écrire la relation liant u_(n+1) et u_n, puis calculer u_2 » agrège en un seul critère une notation de Première et un calcul d'évolution successive de Seconde. Le critère imprimé est indivisible ; il est donc éclaté en sous-critères analytiques virtuels, à somme de points strictement égale.
  - sous-critères analytiques virtuels :
    - `1ERE_SPE_MALEK_KHADHRANI_C1_c4_v1` 0.50 pt — bridge_n — relation de récurrence u_(n+1) = 1,04 x u_n correctement écrite
    - `1ERE_SPE_MALEK_KHADHRANI_C1_c4_v2` 0.50 pt — n_minus_1 — u_2 obtenu par application répétée du coefficient multiplicateur, évalué à partir de la relation écrite par l'élève

## Questions à correction prudente

### B2 — critère `1ERE_SPE_MALEK_KHADHRANI_B2_c2` (0.60 pt)

Consigne réellement imprimée : « Soit x un réel tel que 0 < x < 1. Comparer x^2 et x, puis justifier la réponse par un exemple numérique et par un argument valable pour tout x de cet intervalle. »

- niveau demandé : comparaison correcte (x^2 < x) et argument valable pour tout x : signe de x(x-1), ou multiplication de 0 < x < 1 par x > 0.
- preuve renforcée : rédaction formelle du tableau de signes de x(x-1). Valorisée, jamais exigée.
- règle de correction : aucun formalisme non demandé par la consigne imprimée ne conditionne l'attribution des points.
- limite d'interprétation : cet item, seul, ne prouve pas une compétence de démonstration universelle

### C2 — critère `1ERE_SPE_MALEK_KHADHRANI_C2_c2` (1.00 pt)

Consigne réellement imprimée : « L'affirmation « la fonction inverse f(x) = 1/x est croissante sur ]0 ; +infini[ » est-elle exacte ? Répondre par oui ou non, en justifiant à l'aide de deux valeurs bien choisies. »

- accepté : un contre-exemple explicite : 1 < 2 et f(1) = 1 > f(2) = 0,5 ; la totalité des points du critère est acquise
- accepté : tout autre couple de valeurs correctement choisi et correctement comparé
- règle de correction : un contre-exemple suffit à réfuter une affirmation universelle. La consigne imprimée demande deux valeurs bien choisies : rien de plus ne peut être exigé. L'ajout spontané « donc la fonction est décroissante » n'est pas pénalisé, et la décroissance sur tout l'intervalle n'est pas à démontrer.
- limite d'interprétation : cette question ne permet pas de conclure que l'élève sait établir la monotonie d'une fonction sur un intervalle : elle mesure l'usage d'un contre-exemple

## Saisie

La saisie se fait critère par critère, dans `responses/responses_v3_TEMPLATE_malek-khadhrani.json`. Un code d'erreur ne se porte que sur le critère effectivement échoué.
