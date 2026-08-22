# Audit visuel des bilans PDF

Quarante-cinq documents synthétiques, rastérisés à 150 dpi, **toutes leurs pages**
inspectées : mesures automatiques, planches contact, et relecture humaine des
planches. Aucun résultat d'élève réel n'y figure.

## Corpus

| type | documents | pages | pages/doc |
| --- | ---: | ---: | --- |
| Eleve | 15 | 17 | 1 p (×13), 2 p (×2) |
| Enseignant | 15 | 47 | 3 p (×13), 4 p (×2) |
| Parents | 15 | 90 | 6 p (×15) |
| **total** | **45** | **154** | |

## Mesures automatiques

| contrôle | résultat |
| --- | --- |
| format papier | 45 / 45 en A4 (595,276 × 841,89 pts) |
| pages blanches | 0 |
| marge d'encre minimale | 8.6 mm (seuil 8 mm) |
| texte sélectionnable | 45 / 45 |
| métadonnées renseignées | 45 / 45 titrés |
| alertes P0 / P1 / P2 | 0 / 0 / 0 |

## Remplissage des pages

Mesuré **dans le bloc de texte**, en écartant l'en-tête et le pied de page
courants. Sans cette précaution la mesure donnait 93 % sur toutes les pages, y
compris les plus vides : elle ne mesurait que la présence de la garniture.

| document | page | remplissage médian | lecture |
| --- | ---: | ---: | --- |
| Eleve | 1 | 96 % | fiche complète |
| Eleve | 2 | 22 % | suite, page de clôture |
| Enseignant | 1 | 92 % | synthèse et compétences |
| Enseignant | 2 | 96 % | détail critère par critère |
| Enseignant | 3 | 79 % | profil d'erreurs et conclusions |
| Enseignant | 4 | 19 % | page de clôture |
| Parents | 1 | 61 % | identité, l'essentiel, situation de départ — aérée à dessein |
| Parents | 2 | 57 % | trajectoire des cinq séances |
| Parents | 3 | 80 % | domaines et évaluation de clôture |
| Parents | 4 | 74 % | ce que l'évaluation établit |
| Parents | 5 | 98 % | plan des quatre semaines — page pleine, c'est la partie utilisée |
| Parents | 6 | 28 % | clôture : priorités, conseil, limites |

Aucune page intermédiaire n'est creuse. Les pages de clôture — dernière page de
chaque document — sont volontairement peu remplies : elles portent la conclusion,
pas du contenu à tasser.

## Ce que l'automatisation n'établit pas

Les mesures ci-dessus disent qu'aucune page n'est blanche, qu'aucune encre
n'approche le bord, qu'aucun tableau ne déborde et qu'aucune page intermédiaire
n'est creuse. Elles ne disent **pas** si la hiérarchie se lit, si un tableau est
compréhensible, ou si une formulation convient à une famille.

Ces jugements ont été portés en regardant les planches contact, document par
document, et ils sont consignés dans `FINAL_REPORT_PDF_QA.md` avec les défauts
trouvés et corrigés. Un script ne remplace pas cette lecture ; il la rend
possible en écartant ce qui est mesurable.

## Reproduire cet audit

```bash
python3 tools/synthetic_pipeline_check.py --keep     # 45 PDF synthétiques
python3 tools/pdf_visual_qa.py ../tmp/tests/synthetic_reports \
        --dpi 150 --json /tmp/visualqa.json          # mesures + planches contact
python3 tools/check_report_pdf_quality.py ../tmp/tests/synthetic_reports \
        --allow-test-markers                          # porte de qualité
```

Les planches contact sont écrites dans le répertoire de travail indiqué en fin
d'exécution. Elles ne sont jamais versionnées.
