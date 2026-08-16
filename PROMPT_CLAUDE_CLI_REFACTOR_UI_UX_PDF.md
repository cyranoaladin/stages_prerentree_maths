# Mission Claude CLI — refonte complète, audit pédagogique, UI/UX et production PDF

## 0. Mandat

Tu travailles **dans le dossier courant**, qui est la racine du paquet :

`Nexus_Reussite_Documentation_Stages_Maths_2026/`

Tu es simultanément :

- lead senior en ingénierie documentaire et automatisation de production ;
- architecte d’une documentation statique locale, hors ligne et facilement navigable ;
- expert UI/UX et accessibilité ;
- spécialiste de la production de PDF pédagogiques A4 ;
- professeur agrégé de mathématiques chargé du contrôle de cohérence, de correction et de progressivité ;
- responsable qualité et confidentialité pour des documents concernant des élèves mineurs.

Ta mission n’est pas de faire une retouche superficielle. Tu dois **lire, inventorier, auditer, corriger, restructurer, améliorer, générer, tester et livrer** un paquet réellement exploitable pendant les stages, sans dette documentaire, sans angle mort, sans lien cassé, sans doublon inutile, sans correction visible dans les documents élèves et sans fuite de données nominatives.

Tu dois aller jusqu’à la production effective des fichiers. Ne t’arrête pas à un audit ou à un plan si les corrections sont réalisables localement.

---

# 1. Contexte du paquet à auditer

Le dossier contient quatre niveaux :

- `4e/` — entrée en Quatrième ;
- `3e/` — entrée en Troisième ;
- `2nde/` — entrée en Seconde générale et technologique ;
- `1ere_spe/` — entrée en Première générale, spécialité mathématiques.

Chaque niveau contient actuellement, sous des formes Markdown et HTML :

- un document maître et un index ;
- un guide formateur ;
- un tableau de bord enseignant ;
- cinq séances, chacune avec fiche professeur, fiche élève, supports et cartes d’aide ;
- des évaluations ;
- un portfolio ;
- des dossiers nominatifs ;
- les programmes pédagogiques sources ;
- les tests initiaux et bilans PDF d’origine.

La racine contient notamment :

- `INDEX.md` et `INDEX.html` ;
- `README.md` et `README.html` ;
- `RAPPORT_LIVRAISON.md` et `.html` ;
- `MANIFEST.csv` ;
- `build_all_html.py` ;
- `assets/print.css` ;
- les logos Nexus.

Les onze élèves actuellement documentés sont :

- **4e** : Sinda Chikhaoui, Fares Darghouth ;
- **3e** : Sarah Bargaoui, Selim Mansouri, Amine Mansouri, Fares Laajili ;
- **2nde** : Noa Maniaci, Ahmed Bakir ;
- **1re spécialité** : Donia Khadhrani, Malek Khadhrani, Ahmad Beldi.

Ces noms et les bilans associés sont des données personnelles concernant des mineurs. Leur traitement doit rester strictement local et compartimenté.

---

# 2. Sources de vérité et ordre d’autorité

Applique l’ordre d’autorité suivant.

## 2.1 Sources pédagogiques canoniques

Les quatre fichiers suivants sont les sources principales de la progression, des objectifs, des profils et des choix didactiques :

- `4e/05_SOURCES/stage_prerentree_quatrieme_maths.md` ;
- `3e/05_SOURCES/stage_prerentree_troisieme_maths.md` ;
- `2nde/05_SOURCES/stage_prerentree_seconde_maths.md` ;
- `1ere_spe/05_SOURCES/stage_prerentree_premiere_maths.md`.

Ne modifie jamais silencieusement leur progression, l’ordre des cinq séances, les priorités par élève, les proportions de tronc commun et de différenciation, ni les principes « réussite × confiance ».

## 2.2 Sources nominatives

Les tests initiaux et les bilans PDF élèves/parents constituent les preuves nominatives. Ils peuvent être lus pour vérifier la personnalisation, mais :

- ne jamais modifier les PDF d’origine ;
- ne jamais envoyer leur contenu vers un service externe ;
- ne jamais inclure le bilan d’un élève dans le pack d’un autre ;
- ne jamais exposer ces documents dans un paquet public ou dans une recherche globale non filtrée.

## 2.3 Documents dérivés

Les `.md` opérationnels sont les sources éditables dérivées. Les `.html` et futurs `.pdf` sont des sorties générées. Évite tout système où le même contenu est corrigé indépendamment dans plusieurs formats.

## 2.4 Gestion des écarts

Si une erreur mathématique, une contradiction, une coquille ou une impossibilité d’impression est prouvée dans une source canonique :

1. ne la corrige pas en silence ;
2. consigne-la dans `reports/SOURCE_ERRATA.md` avec fichier, section, problème, preuve et correction retenue ;
3. applique la correction dans les documents opérationnels ;
4. ne modifie la source canonique elle-même que si cela est nécessaire pour maintenir une source unique cohérente, et trace précisément le changement dans le journal.

Ne complète jamais une information nominative par supposition.

---

# 3. Règles non négociables

1. **Travail local uniquement.** Aucun envoi externe, aucun CDN, aucune police distante, aucune ressource chargée depuis Internet.
2. **Aucune publication.** Ne pousse rien sur GitHub, ne déploie rien, ne partage rien en ligne.
3. **Pas de sudo ni de modification globale de la machine.** Si une dépendance est nécessaire, utilise un environnement virtuel local `.venv/` et des versions épinglées.
4. **Préservation des originaux.** Ne supprime ni ne réécris les tests et bilans PDF d’origine.
5. **Pas de réponse inventée.** Toute correction mathématique doit être vérifiée.
6. **Pas de faux contrôle qualité.** Ne déclare jamais qu’un PDF ou une page a été inspecté si ce n’est pas réellement le cas.
7. **Pas de corrigé dans un document élève.** Vérifie le texte visible, les métadonnées, les commentaires HTML, les attributs `title`, le texte caché et les calques PDF.
8. **Pas de donnée d’un autre élève.** Les packs nominatifs doivent être étanches.
9. **Pas de dépendance à un navigateur connecté.** Le site doit fonctionner hors ligne et, autant que possible, directement en `file://`.
10. **Une seule chaîne de build canonique.** Ne conserve pas plusieurs scripts concurrents produisant des sorties différentes.
11. **Pas de suringénierie.** Préfère une architecture statique, claire, testable, sans framework lourd si du HTML/CSS/JS et Python suffisent.
12. **Aucune modification pédagogique opportuniste.** Les améliorations de fond doivent servir les programmes canoniques, non les remplacer.
13. **La durée de chaque séance reste exactement de 120 minutes.** Toute somme différente est un défaut bloquant.
14. **Le tronc commun doit rester autour de 65–70 % et la différenciation autour de 30–35 %.**
15. **Les dossiers nominatifs sont confidentiels.** Ajoute des avertissements visibles et des métadonnées adaptées.

---

# 4. Sauvegarde et baseline avant modification

Commence par une phase de gel.

## 4.1 Détection Git

- Si le dossier appartient à un dépôt Git :
  - affiche le statut ;
  - vérifie les fichiers non suivis ;
  - crée une branche locale dédiée, sans push, par exemple `refactor/documentation-stages-maths-2026` ;
  - ne détruis aucun travail existant.
- Si le dossier n’est pas un dépôt Git :
  - ne l’initialise pas sans nécessité ;
  - crée `_backup/pre-refactor-YYYYMMDD-HHMMSS/` ;
  - copie uniquement les fichiers qui seront modifiés ;
  - génère une liste SHA-256 des fichiers initiaux.

## 4.2 Baseline obligatoire

Avant toute écriture, mesure et consigne :

- nombre total de fichiers par extension et par niveau ;
- taille totale ;
- nombre de Markdown, HTML et PDF ;
- nombre de liens internes et liens cassés ;
- nombre de fichiers orphelins ;
- nombre de doublons exacts et quasi-doublons ;
- nombre de documents nominatifs ;
- nombre de PDF réellement générés, hors PDF sources ;
- éventuels fichiers vides ;
- erreurs de structure HTML ;
- dépendances et outils disponibles : Python, Pandoc, Chromium/Playwright, WeasyPrint, XeLaTeX, qpdf, pdfinfo, pdftotext, pdffonts, pdftoppm ou mutool.

Écris la baseline dans `reports/AUDIT_INITIAL.md` et `reports/AUDIT_INITIAL.json`.

---

# 5. Audit exhaustif à mener avant la refonte

## 5.1 Inventaire et architecture documentaire

Lis intégralement l’arborescence et détermine pour chaque fichier :

- source, dérivé, actif, obsolète, orphelin ou confidentiel ;
- audience : élève, enseignant, famille, nominatif privé, technique ;
- niveau, séance, type de document, statut de correction ;
- relation avec la source canonique ;
- liens entrants et sortants.

Détecte notamment :

- index écrits à la main qui divergent des fichiers réels ;
- titres Markdown collés à des listes et mal interprétés par Pandoc ;
- documents HTML contenant du CSS dupliqué ou des en-têtes inutiles ;
- liens relatifs fragiles ;
- incohérences de nommage entre `1ere_spe`, `1re`, `Première spécialité`, etc. ;
- fichiers générés non reproductibles ;
- anciens fichiers devenus inutiles ;
- documents dont le type ou l’audience n’est pas identifiable immédiatement.

Les noms de dossiers existants peuvent être conservés pour ne pas casser les liens. Normalise d’abord les **libellés visibles** et les métadonnées. Toute modification de chemin doit être accompagnée d’une table de correspondance et de liens compatibles.

## 5.2 Audit pédagogique et mathématique

Pour chaque niveau, séance et document :

- comparer la fiche élève et la fiche professeur au programme canonique ;
- vérifier que les objectifs, les contenus, la personnalisation et les traces écrites sont cohérents ;
- vérifier que le déroulé minute par minute totalise 120 minutes ;
- vérifier la présence réelle du tronc commun, des parcours Consolidation, Maîtrise et Approfondissement ;
- vérifier que chaque exercice possède une consigne complète et non ambiguë ;
- vérifier qu’il existe une correction professeur correspondante ;
- recalculer chaque résultat ;
- utiliser SymPy ou un script déterministe lorsque pertinent, puis effectuer une relecture mathématique ;
- vérifier les notations françaises : virgule décimale, espaces insécables, degrés, unités, intervalles, signes, fractions ;
- vérifier que les réponses attendues ne dépendent pas d’une convention non précisée ;
- vérifier qu’aucune question n’a deux réponses possibles ;
- vérifier que les anticipations vers le niveau suivant restent raisonnables ;
- vérifier l’alignement des exercices ciblés avec le diagnostic du bon élève ;
- vérifier la cohérence du barème et du nombre d’items ;
- vérifier la cohérence entre score, confiance, geste pédagogique et plan d’action.

Repère et remplace les contenus purement génériques ou les faux supports, par exemple :

- un « support de manipulation » qui ne contient qu’un titre au lieu d’une figure utilisable ;
- une activité qui demande une droite graduée mais n’en imprime aucune ;
- une carte qui nomme un outil sans le matérialiser ;
- un rituel avec des emplacements vides au lieu de vraies questions ;
- des espaces de réponse insuffisants ;
- des placeholders ou formulations copiées sans adaptation au niveau.

Les supports doivent devenir de vrais objets imprimables : droites graduées, bandes de fractions, repères, triangles, diagrammes, cartes à découper, tableaux, grilles, axes, figures codées, arbres, etc. Utilise des SVG locaux ou des dessins vectoriels générés, pas des images floues.

## 5.3 Audit séparation élève/professeur

Recherche dans tous les documents élèves :

- corrigés ;
- réponses attendues ;
- commentaires pédagogiques réservés au professeur ;
- métadonnées révélant une réponse ;
- liens vers les corrigés ;
- contenu caché par CSS ;
- notes de génération ;
- noms d’autres élèves.

Recherche dans les documents professeur :

- corrigés manquants ;
- barèmes incomplets ;
- points de vigilance trop génériques ;
- absence d’indicateurs de réussite ;
- décalage avec la fiche élève.

## 5.4 Audit confidentialité et PII

Produis une matrice de confidentialité :

- public local non nominatif ;
- enseignant ;
- élève générique ;
- nominatif privé ;
- source sensible.

Vérifie que :

- les index principaux ne dévoilent pas automatiquement les bilans PDF ;
- la recherche globale publique exclut les contenus nominatifs ;
- un mode privé séparé permet la navigation nominative avec un avertissement ;
- les manifests publics ne contiennent pas de noms d’élèves ;
- les logs et rapports techniques ne recopient pas les bilans ;
- les PDF nominatifs portent « Confidentiel — destinataire : [nom] » ;
- les fichiers publics portent `noindex` et ne chargent aucune ressource distante ;
- aucune donnée n’est écrite dans `localStorage` ou un cache navigateur sans nécessité.

## 5.5 Audit UI/UX actuel

Teste la navigation actuelle sur :

- bureau ;
- tablette ;
- mobile 390 px et 320 px ;
- zoom 200 % ;
- clavier seul.

Évalue :

- nombre de clics pour atteindre une fiche de séance ;
- capacité à revenir au niveau et à la racine ;
- compréhension de l’audience ;
- distinction des documents élèves/professeur/confidentiels ;
- recherche et filtrage ;
- cohérence des titres ;
- densité cognitive ;
- lisibilité ;
- focus clavier ;
- contraste ;
- débordement horizontal ;
- comportement hors ligne et en `file://`.

Consigne les défauts dans `reports/UX_AUDIT.md`, avec sévérité P0/P1/P2/P3.

---

# 6. Architecture cible — une seule source de vérité

Après l’audit, mets en place une architecture de production simple et reproductible.

## 6.1 Registre documentaire canonique

Crée un registre unique, par exemple `content/catalog.json`, qui référence tous les documents avec au minimum :

- identifiant stable ;
- titre visible ;
- niveau ;
- séance ;
- audience ;
- type ;
- chemin source Markdown ;
- chemin HTML généré ;
- chemin PDF généré ;
- caractère confidentiel ;
- ordre de navigation ;
- inclusion dans les packs ;
- statut de validation ;
- source pédagogique.

Les index, menus, packs et manifests doivent être générés depuis ce registre. Aucun index important ne doit rester maintenu manuellement en parallèle.

## 6.2 Chaîne de build canonique

Refactorise `build_all_html.py` ou remplace-le par une seule commande canonique, par exemple :

```bash
python tools/build.py all
```

Elle doit proposer des sous-commandes documentées :

```bash
python tools/build.py audit
python tools/build.py html
python tools/build.py pdf
python tools/build.py packs
python tools/build.py qa
python tools/build.py all
```

Ajoute un `Makefile` ou des scripts simples :

```bash
make audit
make build
make pdf
make qa
make all
make serve
make clean-generated
```

Le nettoyage ne doit jamais supprimer les sources ni les PDF d’origine.

## 6.3 Dépendances

- Détecte d’abord les outils installés.
- Utilise un `.venv` local si nécessaire.
- Épingle les dépendances dans `requirements.txt` ou `requirements.lock`.
- Ne télécharge aucune police.
- Ne crée pas un projet Node complet si du Python et du JavaScript natif suffisent.
- Évite deux moteurs PDF concurrents. Fais un essai comparatif court, choisis le moteur qui rend correctement les mathématiques, puis documente ce choix.

## 6.4 Mathématiques dans HTML et PDF

Le rendu actuel peut contenir des expressions pseudo-LaTeX non interprétées. Normalise les formules dans une syntaxe unique et teste leur rendu.

Contraintes :

- aucune dépendance MathJax distante ;
- MathML natif, KaTeX local ou rendu vectoriel local uniquement ;
- formules lisibles, non coupées, sélectionnables ou vectorielles ;
- cohérence entre HTML et PDF ;
- aucun code LaTeX brut visible dans la version élève.

---

# 7. Refonte UI/UX de la navigation locale

Construis un véritable portail documentaire statique, sobre et premium, cohérent avec Nexus Réussite.

## 7.1 Charte

Utilise comme base :

- bleu nuit Nexus : `#071A3A` ;
- or : `#C9A227` ;
- rouge : `#D71F2B` ;
- fond clair crème/blanc ;
- contraste WCAG AA ;
- aucune information portée uniquement par la couleur.

Utilise les logos locaux dans `assets/`.

## 7.2 Page d’accueil racine

La racine doit proposer :

- un en-tête Nexus clair ;
- quatre cartes de niveau ;
- un résumé « 5 séances × 2 h » ;
- des accès rapides : « Enseignant », « Élève », « Évaluations », « Packs PDF » ;
- un bouton « Ouvrir le dossier confidentiel » distinct, accompagné d’un avertissement ;
- un champ de recherche local ;
- des filtres par niveau, séance, audience et type ;
- un bloc « Documents prêts à imprimer » ;
- un bloc « Dernière génération / état QA » ;
- un lien vers le rapport de build.

## 7.3 Page de niveau

Pour chaque niveau :

- titre, objectifs et élèves concernés ;
- cinq cartes de séance dans l’ordre ;
- pour chaque séance, quatre actions visibles : professeur, élève, supports, aides ;
- accès aux évaluations ;
- accès au pack PDF complet du niveau ;
- accès au pack enseignant ;
- accès aux dossiers nominatifs dans la zone privée seulement ;
- badges explicites : `ÉLÈVE`, `ENSEIGNANT`, `CORRIGÉ`, `CONFIDENTIEL`, `À DÉCOUPER` ;
- liens précédent/suivant ;
- fil d’Ariane.

## 7.4 Navigation dans les documents

Chaque page HTML doit comporter :

- lien d’évitement ;
- en-tête compact ;
- fil d’Ariane ;
- bouton retour au niveau ;
- boutons séance précédente/suivante lorsque pertinent ;
- bouton « Imprimer / PDF » ;
- lien direct vers le PDF correspondant lorsqu’il existe ;
- sommaire interne pour les documents longs ;
- indication de l’audience et de la confidentialité ;
- pied de page avec version et date de build.

## 7.5 Recherche hors ligne

La recherche doit fonctionner sans serveur et sans `fetch` réseau :

- index de recherche généré localement ;
- chargement par fichier JS relatif ou données intégrées ;
- recherche publique excluant les contenus nominatifs ;
- recherche privée séparée ;
- pas de stockage des requêtes ;
- résultats avec niveau, séance, type et audience.

## 7.6 Responsive et accessibilité

Exigences minimales :

- navigation utilisable à 320 px sans débordement ;
- zoom 200 % sans perte de contenu ;
- clavier complet ;
- focus visible ;
- structure sémantique `header/nav/main/footer` ;
- `lang="fr"` ;
- textes alternatifs ;
- tableaux avec en-têtes ;
- boutons suffisamment grands ;
- aucun piège clavier ;
- aucun contraste insuffisant ;
- préférence de mouvement réduit respectée ;
- interface imprimable sans les contrôles de navigation.

---

# 8. Refonte des documents imprimés

## 8.1 Règles communes A4

Tous les documents produits doivent respecter :

- format A4 portrait, sauf support nécessitant explicitement le paysage ;
- marges minimales de 15 mm ;
- police de corps d’au moins 11 pt pour les fiches élèves ;
- zones de réponse réellement suffisantes ;
- numéros de page ;
- en-tête avec niveau, séance et type ;
- pied de page discret Nexus ;
- titres non orphelins ;
- paragraphes avec veuves/orphelines contrôlées ;
- lignes de tableau jamais scindées ;
- listes non détachées de leur titre ;
- nombres avec espaces insécables ;
- unités attachées à leur valeur ;
- absence de pages quasi vides ;
- impression correcte en niveaux de gris ;
- métadonnées PDF en français.

## 8.2 Documents élèves

Ils doivent être autonomes et contenir :

- consigne ;
- espace de réponse ;
- degré de certitude ;
- parcours clairement identifié ;
- trace écrite à compléter ;
- auto-évaluation ;
- exit ticket ;
- aucune correction, même cachée.

Les exercices doivent être répartis de façon lisible. Ne tasse pas douze exercices sur une seule page au détriment de l’écriture.

## 8.3 Documents professeur

Ils doivent contenir :

- déroulé exact ;
- consignes orales ;
- objectifs ;
- matériel ;
- corrigés complets ;
- barème lorsque pertinent ;
- erreurs attendues ;
- gestes de remédiation ;
- indicateurs de réussite ;
- décision de passage entre parcours ;
- correspondance avec le document élève.

Les réponses ne doivent pas dépendre uniquement d’une couleur : ajoute `RÉPONSE`, `VIGILANCE`, `JUSTIFICATION` ou une icône textuelle.

## 8.4 Supports de manipulation

Génère les supports réels, aux dimensions utilisables :

- cartes avec pointillés de découpe et marges de sécurité ;
- droites graduées ;
- bandes fractionnaires ;
- figures géométriques précises ;
- repères ;
- grilles ;
- tableaux ;
- diagrammes de Venn ;
- arbres pondérés ;
- cartes d’aide A–E ;
- cartes « données / propriété / contrôle / conclusion ».

Privilégie SVG et dessin vectoriel. Vérifie les dimensions après impression à 100 %.

## 8.5 Documents nominatifs

Chaque PDF nominatif doit comporter :

- nom de l’élève ;
- niveau ;
- mention « Confidentiel » ;
- diagnostic fidèle ;
- plan d’action ;
- suivi des cinq séances ;
- exercices ciblés ;
- bilan final ;
- aucune donnée d’un autre élève.

Ne mets pas automatiquement les bilans parents d’origine dans le pack remis à l’élève. Conserve-les dans les sources privées et distingue :

- pack de travail élève nominatif ;
- dossier enseignant confidentiel ;
- sources nominatives originales.

---

# 9. Production PDF obligatoire

Le paquet actuel contient surtout des HTML imprimables et des PDF sources. Tu dois générer tous les PDF opérationnels.

## 9.1 Arborescence cible

Crée une arborescence explicite, par exemple :

```text
dist/
├── site-public/
├── site-private/
├── pdf/
│   ├── 4e/
│   │   ├── eleves/
│   │   ├── enseignants/
│   │   ├── evaluations/
│   │   ├── supports/
│   │   └── nominatifs-prives/
│   ├── 3e/
│   ├── 2nde/
│   └── 1ere_spe/
├── packs/
│   ├── eleves/
│   ├── enseignants/
│   └── nominatifs-prives/
└── manifests/
```

Adapte si nécessaire, mais conserve une séparation claire.

## 9.2 PDF individuels à produire pour chaque niveau

Au minimum :

- guide formateur ;
- tableau de bord enseignant ;
- 5 fiches professeur ;
- 5 fiches élève ;
- 5 jeux de supports ;
- 5 jeux de cartes d’aide ;
- mini-diagnostic élève ;
- mini-diagnostic corrigé ;
- évaluation finale élève ;
- évaluation finale corrigée/barème ;
- portfolio ;
- document maître, si son volume reste exploitable ;
- dossiers nominatifs ;
- remédiations ciblées élève ;
- corrigés de remédiation enseignant.

Le test initial original reste la source officielle et doit être copié ou référencé sans altération.

## 9.3 Packs combinés

Produis aussi :

### Par niveau

- `[niveau]_PACK_ELEVE_COMPLET.pdf` ;
- `[niveau]_PACK_ENSEIGNANT_COMPLET.pdf` ;
- `[niveau]_PACK_EVALUATIONS_ELEVE.pdf` ;
- `[niveau]_PACK_EVALUATIONS_CORRIGE.pdf`.

### Par séance

- `[niveau]_S1_PACK_ELEVE.pdf` à `[niveau]_S5_PACK_ELEVE.pdf` ;
- `[niveau]_S1_PACK_ENSEIGNANT.pdf` à `[niveau]_S5_PACK_ENSEIGNANT.pdf`.

### Par élève

- `[niveau]_[Nom_Prenom]_PACK_TRAVAIL_PERSONNALISE.pdf` ;
- `[niveau]_[Nom_Prenom]_DOSSIER_ENSEIGNANT_CONFIDENTIEL.pdf`.

Le pack élève ne doit jamais contenir les corrigés professeur ni les données d’un autre élève.

## 9.4 Nommage

Conserve une nomenclature stable, ASCII pour les chemins et libellé français dans les métadonnées. Exemple :

```text
4e_S1_ELEVE_Activite.pdf
4e_S1_PROF_Fiche_Corrigee.pdf
4e_S1_SUPPORTS_Manipulation.pdf
4e_S1_AIDES_Cartes.pdf
4e_Sinda_Chikhaoui_PACK_TRAVAIL_PERSONNALISE.pdf
```

## 9.5 Métadonnées PDF

Chaque PDF doit avoir :

- titre ;
- auteur : `Nexus Réussite` ;
- sujet ;
- mots-clés ;
- langue française ;
- version ;
- niveau ;
- type d’audience ;
- signet ou plan pour les packs longs lorsque l’outil le permet.

Les PDF doivent être ouvrables, non chiffrés, imprimables et sans ressource distante.

---

# 10. Contrôles qualité obligatoires

## 10.1 QA HTML et navigation

Automatise :

- validation de tous les liens relatifs ;
- détection des ancres manquantes ;
- détection des fichiers orphelins ;
- détection des références à des assets inexistants ;
- absence de chargements HTTP externes ;
- absence d’erreurs JavaScript ;
- vérification des titres et `lang` ;
- vérification des breadcrumbs ;
- vérification des liens PDF ;
- test hors ligne ;
- test `file://` ou documentation claire du serveur local si une fonction ne peut pas fonctionner autrement.

## 10.2 QA accessibilité

Si Axe ou Lighthouse est disponible localement, utilise-le. Sinon effectue au minimum des contrôles statiques et Playwright :

- labels ;
- landmarks ;
- ordre des titres ;
- contraste ;
- focus ;
- clavier ;
- images alternatives ;
- tableaux ;
- zoom ;
- débordement mobile.

Aucune violation critique ou sérieuse non documentée ne doit subsister.

## 10.3 QA PDF structurelle

Pour chaque PDF :

- `qpdf --check` ou équivalent ;
- `pdfinfo` : format A4 et nombre de pages ;
- `pdffonts` : polices incorporées ou justification documentée ;
- `pdftotext` : texte extractible et absence de correction dans les documents élèves ;
- absence de page blanche involontaire ;
- absence de fichier vide ;
- taille raisonnable ;
- liens internes/externes valides lorsque présents ;
- pas de chiffrement ;
- metadata cohérentes ;
- aucune PII croisée.

## 10.4 Inspection visuelle exhaustive

Rasterise **toutes les pages de tous les PDF générés** à 120 ou 150 dpi avec `pdftoppm`, `mutool draw` ou équivalent.

Inspecte réellement les images page par page avec l’outil de vision disponible. Vérifie :

- pas de texte coupé ;
- pas de formule cassée ;
- pas de ligne de tableau scindée ;
- pas de titre orphelin ;
- pas de liste sans contexte ;
- pas de nombre coupé ;
- pas de bloc qui déborde ;
- pas de chevauchement ;
- pas de page quasi vide sans raison ;
- espaces de réponse suffisants ;
- cases à cocher non ambiguës ;
- cartes découpables ;
- figures nettes ;
- lecture correcte en niveaux de gris.

Si tu ne disposes pas réellement d’un moyen d’inspection visuelle, ne prétends pas l’avoir faite : produis les planches-contact et marque ce gate comme bloquant.

Crée `reports/PDF_VISUAL_QA.md` avec une ligne par PDF et, pour les packs longs, une ligne par page : `OK` ou défaut précis.

## 10.5 QA mathématique

Crée des tests ou scripts vérifiant les calculs automatisables. Pour chaque correction :

- valeur correcte ;
- domaine de définition ;
- unités ;
- arrondi ;
- cohérence graphique ou géométrique ;
- non-ambiguïté.

Crée `reports/MATH_CONTENT_AUDIT.md` avec :

- nombre d’exercices vérifiés ;
- erreurs détectées ;
- corrections appliquées ;
- éléments nécessitant une validation humaine.

## 10.6 QA confidentialité

Scanne les fichiers distribuables :

- aucun autre nom d’élève ;
- aucun bilan parent ;
- aucune correction cachée ;
- aucun chemin local personnel ;
- aucune adresse ou secret technique ;
- aucune source privée dans le site public.

Crée un manifest public et un manifest privé distincts.

## 10.7 Reproductibilité

Effectue un build propre deux fois.

- Le nombre et les noms des fichiers doivent être identiques.
- Utilise `SOURCE_DATE_EPOCH` ou des métadonnées déterministes si l’outil le permet.
- Si les hash PDF diffèrent uniquement à cause de métadonnées temporelles, documente-le précisément.
- Aucun fichier manuel ne doit être requis après `make all`.

---

# 11. Améliorations complémentaires à inclure

Ajoute les éléments suivants s’ils ne sont pas déjà couverts :

1. `README.md` réécrit pour un utilisateur non technique.
2. `QUICK_START.md` : ouvrir le portail, reconstruire, imprimer, retrouver un élève.
3. `PRINT_GUIDE.md` : recto/verso, papier conseillé, ordre d’impression, quantités.
4. `PRINT_CHECKLIST.csv` : niveau, séance, document, audience, quantité, pages, couleur/N&B, assemblage.
5. `CHANGELOG.md` détaillé.
6. `reports/CONTENT_GAPS.md` : lacunes qui nécessitent un arbitrage humain.
7. `reports/DEAD_FILES_AND_DUPLICATES.md`.
8. `reports/ACCESSIBILITY_QA.md`.
9. `reports/NAVIGATION_QA.md`.
10. `reports/FINAL_DELIVERY_REPORT.md`.
11. `MANIFEST_PUBLIC.csv` et `MANIFEST_PRIVATE.csv` avec SHA-256.
12. Une commande locale simple : `make serve`, affichant l’URL locale.
13. Une page « Préparer la séance du jour » donnant en un écran : documents à imprimer, matériel, élèves à suivre, objectif et liens.
14. Une page « Packs prêts à imprimer ».
15. Une page privée « Suivi nominatif » clairement séparée.
16. Des planches-contact PDF pour contrôle visuel, hors packs de distribution.
17. Un contrôle des quantités de documents : aucune séance, aucun niveau et aucun élève manquant.
18. Des liens de téléchargement vers les PDF depuis le portail.
19. Des boutons d’impression masqués lors de l’impression.
20. Des feuilles de style distinctes `site.css` et `print.css`, sans duplication incontrôlée.
21. Un inventaire des documents qui doivent être imprimés en couleur et de ceux qui restent lisibles en noir et blanc.
22. Une stratégie de version : par exemple `2026.1` et date de build, visible sans alourdir les pages.

---

# 12. Critères de qualité et gates de sortie

Ne déclare le paquet final prêt que si tous les critères suivants sont satisfaits.

## 12.1 Contenu

- quatre niveaux présents ;
- cinq séances par niveau ;
- tous les déroulés totalisent 120 minutes ;
- toutes les fiches élèves sont complètes ;
- tous les corrigés professeur sont complets ;
- les trois parcours sont visibles ;
- les plans nominatifs correspondent aux bons élèves ;
- aucune erreur mathématique connue ;
- aucun placeholder involontaire ;
- aucune contradiction entre versions.

## 12.2 Navigation

- zéro lien cassé ;
- zéro fichier actif orphelin ;
- racine → niveau → séance → document en trois actions maximum ;
- retour et fil d’Ariane partout ;
- recherche locale fonctionnelle ;
- filtres fonctionnels ;
- accès PDF évident ;
- mobile, zoom et clavier validés.

## 12.3 PDF

- tous les PDF attendus existent ;
- tous passent le contrôle structurel ;
- toutes les pages sont visuellement contrôlées ;
- aucune coupure ou fuite de corrigé ;
- packs élève, enseignant et nominatifs correctement séparés ;
- métadonnées et page A4 conformes ;
- manifest et empreintes générés.

## 12.4 Confidentialité

- site public sans source nominative ;
- site privé séparé ;
- manifests séparés ;
- aucune contamination croisée ;
- avertissements de confidentialité ;
- aucun envoi réseau.

## 12.5 Reproductibilité

- une commande canonique reconstruit l’ensemble ;
- la documentation de build est exacte ;
- le second build produit la même liste de fichiers ;
- aucun bricolage manuel post-build.

---

# 13. Méthode de travail attendue

Tu peux utiliser des sous-agents, mais garde un intégrateur unique. Répartition conseillée :

- agent 1 : inventaire, liens, doublons et architecture ;
- agent 2 : audit mathématique 4e/3e ;
- agent 3 : audit mathématique 2nde/1re ;
- agent 4 : UI/UX, accessibilité et navigation ;
- agent 5 : pipeline PDF, impression et QA ;
- agent 6 : confidentialité et packs nominatifs.

Les sous-agents d’audit ne doivent pas modifier les mêmes fichiers simultanément. Centralise les corrections.

Procède par phases avec gates :

1. baseline et sauvegarde ;
2. audit ;
3. architecture et plan écrit ;
4. correction du contenu ;
5. refonte du portail ;
6. génération HTML ;
7. génération PDF ;
8. packs ;
9. QA automatisée ;
10. inspection visuelle ;
11. second build propre ;
12. rapport final.

Ne demande une décision propriétaire que si une ambiguïté réelle empêche une correction sûre. Pour les choix d’ergonomie, de structure et de build, prends des décisions raisonnables et documentées.

---

# 14. Rapport final obligatoire

À la fin, réponds avec un rapport factuel contenant au minimum :

## Baseline

- chemin racine ;
- état Git ou sauvegarde ;
- nombre initial de fichiers ;
- défauts principaux reproduits.

## Corrections de fond

- erreurs mathématiques corrigées ;
- contenus génériques remplacés ;
- supports réellement générés ;
- cohérence des cinq séances ;
- personnalisation vérifiée.

## Refonte UI/UX

- architecture ;
- pages générées ;
- recherche ;
- filtres ;
- breadcrumbs ;
- responsive ;
- accessibilité ;
- résultats des tests.

## PDF

- moteur choisi ;
- nombre de PDF par niveau et audience ;
- nombre de packs ;
- nombre total de pages ;
- contrôles structurels ;
- inspection visuelle ;
- défauts résiduels.

## Confidentialité

- séparation public/privé ;
- scans PII ;
- contamination croisée ;
- manifests.

## Reproductibilité

- commandes exactes ;
- résultat du second build ;
- dépendances.

## Inventaire final

- fichiers créés ;
- fichiers modifiés ;
- fichiers archivés ;
- fichiers supprimés, s’il y en a, avec justification.

## Compteurs obligatoires

```text
LEVEL_COUNT=
SESSION_COUNT=
STUDENT_COUNT=
ACTIVE_DOCUMENT_COUNT=
GENERATED_HTML_COUNT=
GENERATED_PDF_COUNT=
GENERATED_STUDENT_PDF_COUNT=
GENERATED_TEACHER_PDF_COUNT=
GENERATED_PRIVATE_PDF_COUNT=
COMBINED_PACK_COUNT=
TOTAL_GENERATED_PDF_PAGE_COUNT=
BROKEN_LINK_COUNT=
ORPHAN_ACTIVE_FILE_COUNT=
DUPLICATE_ACTIVE_FILE_COUNT=
MATH_ERROR_REMAINING_COUNT=
STUDENT_CORRECTION_LEAK_COUNT=
CROSS_STUDENT_PII_LEAK_COUNT=
EXTERNAL_RESOURCE_COUNT=
HTML_CRITICAL_A11Y_COUNT=
HTML_SERIOUS_A11Y_COUNT=
PDF_STRUCTURAL_FAILURE_COUNT=
PDF_VISUAL_DEFECT_COUNT=
MISSING_EXPECTED_DOCUMENT_COUNT=
BUILD_REPRODUCIBILITY_MISMATCH_COUNT=
```

## Statut final

Utilise exactement l’un des statuts :

- `DOCUMENTATION_PACKAGE_GO_LIVE_READY` ;
- `DOCUMENTATION_PACKAGE_READY_WITH_NON_BLOCKING_DEBT` ;
- `BLOCKED_BY_CONTENT_VALIDATION` ;
- `BLOCKED_BY_PDF_VISUAL_QA` ;
- `BLOCKED_BY_PRIVACY_RISK` ;
- `BLOCKED_BY_TOOLING`.

Ne choisis `DOCUMENTATION_PACKAGE_GO_LIVE_READY` que si tous les gates bloquants sont réellement verts.

---

# 15. Première action à exécuter maintenant

Commence immédiatement par :

1. afficher le chemin courant ;
2. inventorier l’arborescence ;
3. lire `README.md`, `INDEX.md`, `RAPPORT_LIVRAISON.md`, `MANIFEST.csv`, `build_all_html.py`, `assets/print.css` ;
4. lire intégralement les quatre programmes canoniques ;
5. analyser un exemple complet de chaque type de document dans chaque niveau ;
6. vérifier les index HTML ;
7. établir la baseline sans modifier les fichiers ;
8. produire `reports/AUDIT_INITIAL.md` ;
9. poursuivre ensuite l’implémentation sans attendre une validation intermédiaire, sauf blocage réel de contenu ou de confidentialité.
