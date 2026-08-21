# Confidentialité et sécurité

## Ce qui est en jeu

Des corrections nominatives, des observations d'enseignant et des bilans destinés à des
familles. Ce sont des données personnelles d'élèves mineurs. Le dépôt Git peut être
public.

## Où vivent les données

| donnée | emplacement | suivi par Git |
| --- | --- | --- |
| base des corrections | `runtime/corrections.sqlite3` | **non** |
| bilans PDF et LaTeX | `runtime/reports/<élève>/` | **non** |
| exports JSON | `runtime/exports/` | **non** |
| sauvegardes | `runtime/backups/` | **non** |
| code, gabarits, documentation | dans le dépôt | oui |

`.gitignore` exclut `S5_correction_app/runtime/`, toute base SQLite, et les répertoires
`responses_reelles/`, `copies_eleves/`, `bilans_finaux/`, `corrections_reelles/`.

`tools/check_runtime_not_tracked.py` échoue si l'un de ces fichiers est suivi. Le test
`test_aucune_donnee_reelle_n_est_suivie_par_git` le lance à chaque exécution de la suite.

## Réseau

L'application écoute `127.0.0.1:8765`. Elle ne s'expose pas au réseau sans que l'opérateur
ne le demande, et même alors :

```bash
python3 -m app.cli serve --allow-network      # refusé sans NEXUS_S5_PASSWORD
NEXUS_S5_PASSWORD=... python3 -m app.cli serve --allow-network
```

Le mot de passe doit faire au moins douze caractères, il vient d'une variable
d'environnement, et il n'existe **aucune valeur par défaut**. Un avertissement est affiché
avant l'ouverture.

## Chemins de documents

Aucun chemin ne vient du client. Une route demande un élève et une nature de document ; le
serveur reconstruit le chemin depuis la base, puis `security.resolve_document` le résout
avec `realpath` et vérifie qu'il reste sous une racine autorisée. Tout le reste est refusé
en 404 : `..`, ses formes encodées, un chemin absolu, un lien symbolique qui sort, un
répertoire.

Les racines autorisées sont `S5_cloture/` et `S5_post_distribution_v3/` en lecture, et
`runtime/reports/` pour les PDF produits.

## Sous-processus

`security.run_command` est le seul chemin vers un sous-processus. Il refuse un argument
non textuel, impose `shell=False`, fixe un environnement minimal, et applique un délai
maximal. `os.system`, `os.popen` et `subprocess.getoutput` sont absents du code, et un
test le vérifie sur l'arbre syntaxique — pas par recherche de texte, qu'un commentaire
suffirait à tromper.

Les noms de fichiers produits passent par `safe_slug` : ASCII, majuscules, tirets bas.
`safe_slug("rm -rf /; echo")` ne contient ni espace, ni point-virgule, ni barre oblique.

## Injection

Toutes les requêtes passent par l'ORM ou par des paramètres liés ; aucune chaîne SQL n'est
concaténée depuis une donnée utilisateur.

Les gabarits Jinja2 échappent le HTML par défaut. Une observation contenant
`<script>alert('xss')</script>` ressort en `&lt;script&gt;` — c'est testé.

Pour LaTeX, `reports.latex_escape` neutralise `\ { } $ & # _ % ~ ^` avant tout rendu. Un
texte contenant `100 % & <b>sûr</b>` s'imprime littéralement.

## Jetons de formulaire

`security.issue_token` / `check_token` fournissent des jetons signés HMAC, prêts pour une
protection CSRF si l'application est un jour exposée. En mode localhost strict, sans
compte utilisateur, ils ne sont pas exigés — c'est un choix documenté, pas un oubli.

## Modèle de langage

Aucun n'est appelé. `LLMNarrativeGenerator` existe comme réservation d'architecture et
lève une exception tant que `NEXUS_S5_ENABLE_LLM` n'est pas posé **et** qu'un fournisseur
n'est pas câblé. Une méthode `pseudonymise` retire le nom et l'identifiant de l'élève,
prête pour le jour où cette question se posera. Aucune clé n'est inscrite dans le dépôt,
et un test refuse toute chaîne littérale affectée à un nom de secret.

## Immutabilité

Les soixante empreintes des documents distribués sont recalculées au démarrage, avant
chaque validation, avant chaque distribution de paquet élève, et par
`tools/verify_integrity.py`. Si l'une a changé, l'application bascule en lecture seule et
l'affiche sur toutes les pages. Elle ne continue jamais en silence.
