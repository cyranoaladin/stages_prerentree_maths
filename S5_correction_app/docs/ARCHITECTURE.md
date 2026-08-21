# Architecture

## Le principe

```
Documents distribués (immuables)
        ↓  lecture seule
Correction humaine, critère par critère
        ↓
Stockage structuré (SQLite, points en centièmes entiers)
        ↓
Validation déterministe  ── refuse plutôt que de deviner
        ↓
Analyse déterministe     ── aucun modèle de langage
        ↓
Faits pédagogiques structurés
        ↓
Proposition de bilan     ── générateur déterministe
        ↓
Validation / modification humaine
        ↓
LaTeX → PDF
```

Ce qui est calculé l'est par du code. Un modèle de langage, s'il était un jour activé, ne
pourrait que proposer une rédaction : les points, la note, la ventilation N−1 /
passerelle, les codes d'erreur, la classification des compétences, les pourcentages, la
force de preuve et les priorités ne passent jamais par lui.

## Découpage

```
app/
  config.py        chemins, réseau, garde-fous ; rien n'écrit hors de runtime/
  database.py      moteur SQLite, sessions transactionnelles, PRAGMA
  models.py        le modèle de données
  schemas.py       validation d'entrée (Pydantic)
  security.py      chemins, noms de fichiers, jetons, sous-processus, empreintes
  main.py          application FastAPI, démarrage, contrôle d'immutabilité
  cli.py           ligne de commande

  domain/          tout ce qui calcule, rien qui affiche
    points.py        arithmétique exacte en centièmes
    immutability.py  recalcul des 60 empreintes
    importer.py      import du référentiel V3, avec empreinte des sources
    correction.py    saisie, invariants, machine d'état, révisions
    validation.py    ce qui empêche de valider, formulé pour être corrigeable
    evidence.py      force de preuve, barème publié
    analysis.py      score, deux pools, compétences, erreurs, statuts
    action_plan.py   plan de quatre semaines
    narrative.py     rédaction des blocs (déterministe ; option IA éteinte)
    reports.py       blocs, rendu LaTeX, compilation, manifeste

  routes/          HTTP, rendu, codes de retour
  templates/       Jinja2, échappement automatique
  static/          CSS et JS locaux, aucune ressource distante

latex/             style et gabarits des quatre documents
migrations/        migrations explicites, précédées d'une sauvegarde
tools/             init, import, intégrité, sauvegarde, export, contrôle Git
tests/             une base jetable par module de test
runtime/           base, rapports, exports, sauvegardes — exclu de Git
```

## Le flux d'une saisie

1. Le navigateur envoie un `POST /eleve/{student_id}/critere/{scoring_id}` en JSON.
2. `schemas.ResponseIn` refuse un score négatif, un code inconnu, un statut inconnu.
3. `domain.correction.save_response` applique les invariants métier : score dans le
   barème, pas de code d'erreur sur un critère intégralement réussi, statut cohérent.
4. La modification est journalisée dans `audit_event` avec l'ancienne et la nouvelle
   valeur.
5. La réponse renvoie l'état enregistré et l'avancement ; l'interface affiche l'heure.

Aucune requête SQL n'est construite par concaténation : tout passe par l'ORM.

## Le flux d'une analyse

`analysis.analyse` lit les lignes notées, les regroupe par compétence d'analyse **et par
portée curriculaire**, calcule la force de preuve selon un barème publié, en déduit un
statut pédagogique, puis les priorités. Le résultat est empreinté (`analysis_sha256`) et
conservé dans `analysis_snapshot` : un rapport sait de quelle analyse il est issu.

Les critères mixtes n'existent pas au niveau de la saisie : ce sont leurs sous-critères
analytiques qui sont notés, et leur somme redonne exactement les points du critère
imprimé.

## Le flux d'un rapport

`reports.ensure_report` construit ou met à jour les blocs. Un bloc modifié par un humain
et approuvé n'est jamais remplacé par une régénération : il est conservé, et la
conservation est journalisée. `render_tex` échappe tout texte humain avant de le confier
à LaTeX. `compile_pdf` lance le moteur sans shell, en deux passes, dans un répertoire de
travail dédié ; en cas d'échec, le `.tex` est conservé et le rapport n'est pas déclaré
généré.

## Ce que l'architecture rend impossible

| interdit | mécanisme |
| --- | --- |
| écrire dans un document distribué | aucune ouverture en écriture ; empreintes recalculées au démarrage et avant validation |
| valider une correction incomplète | `validation.validate` liste chaque manque |
| générer un bilan sans correction validée | vérifié dans `reports.ensure_report` et dans la route |
| perdre une version approuvée | nouvelle version, jamais écrasement |
| exécuter une commande construite depuis un nom d'élève | `safe_slug` puis `run_command` sans shell |
| servir un fichier hors des racines autorisées | `resolve_document` résout puis confine |
