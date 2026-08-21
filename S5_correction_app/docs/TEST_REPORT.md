# Rapport de tests

```
92 tests passés, 1 ignoré, 0 échec
```

Exécution : `make s5-correction-test`, soit `python3 -m pytest -q` depuis
`S5_correction_app/`.

## Isolation

Chaque module de test travaille sur **sa propre base**, dans un répertoire temporaire.
Aucun test n'écrit dans la base de l'enseignant, aucun n'hérite de l'état laissé par un
autre, et l'ordre d'exécution n'a pas d'influence. Aucun test n'ouvre en écriture un
document distribué.

## Couverture par module

| module | tests | ce qui est vérifié |
| --- | ---: | --- |
| `test_points.py` | 6 | arithmétique exacte en centièmes, refus d'un montant plus fin, absence de flottant, affichage français, échelle de scores |
| `test_import_and_model.py` | 7 | 15 couples, 14 personnes, homonymie Ahmad BELDI, 180 items, 337 critères, 6 sous-critères, portée sur chaque critère, alias cosinus/sinus, 20 points par élève |
| `test_correction_rules.py` | 10 | invariant erreur/réussite, observation sur un critère réussi, zéro sans cause, score hors barème, code inconnu, validation incomplète, non-propagation d'un code, verrouillage et réouverture, certitude non prévue, somme d'un critère mixte |
| `test_analysis_rules.py` | 9 | score brut à 20, absence de double comptage, **scénario passerelles toutes ratées**, erreur limitée à une compétence, `mastery_delta` nul, `SOLIDE` refusé sur preuve faible, récence et contrôle différé, trois blocs de conclusion, plan à 2–3 objectifs |
| `test_delicate_cases.py` | 7 | Sinda, Elyes, Ahmad, Malek, liste vide NSI hors barème, test de C1 légitimement au barème, méthode alternative acceptée |
| `test_reports.py` | 12 | quatre gabarits, échappement LaTeX, refus sans validation, provenance des blocs, survie d'une modification humaine, générateur déterministe, pseudonymisation, absence de shell, assainissement des noms, **compilation des quatre PDF et absence de fuite**, non-écrasement d'un bilan approuvé, langage de la fiche élève |
| `test_web.py` | 15 | dashboard, 404, PDF distribué affiché, badges non fondés sur la seule couleur, service du PDF, **quatre traversées de chemin refusées**, échappement XSS, analyse refusée sans validation, parcours complet, pages de service, historique, absence de ressource distante |
| `test_privacy_and_integrity.py` | 10 | export d'un seul élève, vocabulaire V3, `.gitignore`, données non suivies par Git, absence de secret littéral, écoute locale, mot de passe exigé en mode réseau, sauvegarde, export de clôture, **immutabilité après tout l'usage** |
| `test_regression_v3.py` | 3 | accord chiffré avec l'analyseur V3 de référence, même couverture de critères, refus commun de toute progression chiffrée |
| `test_documentation.py` | 8 | les cinq clarifications scientifiques sont dans la documentation enseignant et **pas** dans les textes élèves, limite scientifique affichée |
| `test_batch_and_ux.py` | 6 | génération de lot restreinte aux corrections validées, aucun bilan pour une correction non validée, vue de groupe non classante, bouton « suivant », compteurs |

## Les tests exigés par le cahier des charges

| exigence | test |
| --- | --- |
| immutabilité, 60 artefacts, 0 modifié | `test_zzz_aucun_artefact_distribue_n_a_change` |
| total brut de 20, pas de double comptage | `test_le_score_brut_vaut_vingt_quand_tout_est_reussi`, `test_aucun_double_comptage_entre_les_deux_pools` |
| passerelles toutes ratées | `test_un_echec_total_sur_les_passerelles_ne_degrade_pas_les_acquis` |
| erreur attachée au seul critère échoué | `test_une_erreur_reste_sur_le_critere_echoue`, `test_le_code_erreur_ne_touche_qu_une_competence` |
| validation impossible si incomplète | `test_une_correction_incomplete_ne_peut_pas_etre_validee` |
| réouverture avec révision | `test_validation_puis_verrouillage_puis_reouverture` |
| PDF sans JSON, sans delta, sans « lacune » | `test_les_quatre_pdf_compilent_et_ne_fuient_rien` |
| quatre cas délicats | `test_delicate_cases.py` |
| liste vide NSI hors barème | `test_nsi_le_cas_de_la_liste_vide_reste_hors_bareme` |
| clarifications côté enseignant | `test_documentation.py` |
| runtime non suivi par Git | `test_aucune_donnee_reelle_n_est_suivie_par_git` |
| export d'un élève sans autre élève | `test_l_export_d_un_eleve_ne_contient_que_cet_eleve` |
| traversée de chemin | `test_les_traversees_de_chemin_sont_refusees` |
| pas de `shell=True` | `test_la_compilation_n_utilise_jamais_un_shell` |
| routes web, codes de retour | `test_web.py` |
| parcours navigateur | `test_parcours_navigateur` — **ignoré** |

## Le test ignoré, et pourquoi

`test_parcours_navigateur` demande Playwright, qui n'est pas installé sur ce poste. Il est
écrit, il s'exécutera si Playwright apparaît, et la livraison n'en dépend pas : les mêmes
parcours sont couverts par `TestClient`, qui traverse la même pile applicative sans le
rendu du navigateur.

Ce qu'un test navigateur apporterait en plus, et qui n'est donc **pas** couvert
automatiquement : le comportement réel des raccourcis clavier, le rendu du PDF dans
l'`iframe`, et l'ergonomie à 1366×768. Ces trois points sont à vérifier à la main pendant
le pilote.

## Ce qui n'est pas testé automatiquement

- la justesse pédagogique d'une correction humaine — c'est l'objet du pilote ;
- la lisibilité typographique des PDF ;
- le comportement sous une autre distribution LaTeX ;
- la restauration d'une sauvegarde, qui est décrite dans le manuel mais non rejouée par un
  test.
