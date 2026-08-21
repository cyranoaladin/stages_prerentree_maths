---
title: "Supports pratiques S3 - Fonctions, contrats, tests et débogage"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 3 - Supports pratiques</h1>
<div class="subtitle">Fonctions, contrats, tests et débogage</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Fiches de manipulation, traçage et projet</div>
</div><div class="student-only"></div>
## Support 1 - anatomie d’une fonction

```python
def nom_fonction(parametre_1, parametre_2):
    """Description brève du résultat et des préconditions."""
    # calcul local
    return resultat
```

| Élément | Rôle | Exemple personnel |
|---|---|---|
| nom | intention |  |
| paramètre | entrée symbolique |  |
| argument | valeur lors de l’appel |  |
| variable locale | état interne |  |
| `return` | sortie transmise |  |

## Support 2 - cartes « afficher ou renvoyer ? »

<div class="cut-card"><h3>print</h3><p>Affiche pour un humain.</p><p>La valeur affichée n’est pas automatiquement réutilisable.</p></div>
<div class="cut-card"><h3>return</h3><p>Transmet une valeur à l’appelant.</p><p>Met fin à l’exécution de la fonction.</p></div>
<div class="cut-card"><h3>None</h3><p>Valeur obtenue si aucun <code>return</code> explicite n’est exécuté.</p></div>
<div class="cut-card"><h3>assert</h3><p>Vérifie une condition du contrat ou un résultat de test.</p></div>

## Support 3 - fabrique de tests

| Fonction | Cas normal | Cas limite | Cas égalité | Cas invalide | Résultat attendu |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Support 4 - ticket de débogage

1. Symptôme observé : ................................................................................
2. Plus petit exemple qui échoue : ...................................................................
3. Premier état incorrect : ..........................................................................
4. Hypothèse : .........................................................................................
5. Test après correction : ............................................................................
