# Saisie des corrections — V3

Un gabarit par élève : `responses_v3_TEMPLATE_<student_id>.json`.

Pour corriger, copier le gabarit sous un nom daté, puis le renseigner :

```
cp responses/responses_v3_TEMPLATE_elyes-kefi.json \
   responses/responses_elyes-kefi_2026-08-28.json
```

Trois règles, et elles ne souffrent pas d'exception.

1. La saisie se fait **critère par critère**. Le script refuse un fichier incomplet
   plutôt que de compléter une valeur manquante.
2. Un **code d'erreur appartient au critère qui a échoué**, et à aucun autre. Il ne
   se propage ni aux autres critères de l'item, ni aux autres compétences.
3. Une **méthode mathématiquement correcte n'est jamais une erreur**. Cocher
   `accepted_alternative_method` et écrire l'observation.

Puis :

```
python3 tools/analyze_s5_post_distribution.py \
    --student elyes-kefi \
    --responses responses/responses_elyes-kefi_2026-08-28.json
```
