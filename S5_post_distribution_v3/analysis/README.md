# Analyses

Vide tant qu'aucune correction n'a été saisie. C'est normal, et c'est voulu : rien n'est
produit ici avant que les scores ne soient renseignés critère par critère.

`tools/analyze_s5_post_distribution.py` écrit, par élève, dans `analysis/<student_id>/` :

| fichier | contenu |
| --- | --- |
| `post_stage_analysis_v3.json` | score brut, consolidation N−1, disponibilité sur les passerelles, compétences, profil d'erreurs, rétention, contrôles différés, entrées du plan |
| `four_week_action_plan_v3.json` | plan de quatre semaines, consolidation et passerelles séparées |
| `bilan_facts_v3.json` | les seuls faits qu'un bilan écrit a le droit de citer |

Les trois sorties sont validées par `schemas/post_stage_analysis_v3.schema.json` pour la
première, et suivent le même modèle pour les deux autres.
