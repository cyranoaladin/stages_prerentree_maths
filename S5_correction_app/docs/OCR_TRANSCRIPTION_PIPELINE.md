# Lecture assistée des copies — téléversement, transcription, revue

Ce document décrit la chaîne qui va de la copie scannée à une transcription
**vérifiée par un humain**. Il ne décrit pas une correction automatique : il n'en
existe pas, et rien ici n'en produit.

> Une mauvaise lecture du signe « − », d'un exposant ou d'une barre de fraction change
> complètement le diagnostic pédagogique. Le système préfère donc afficher
> « caractère incertain — validation humaine requise » plutôt qu'une transcription
> nette, élégante et fausse.

## 1. Principe : l'IA est un lecteur assisté, jamais la source

```
COPIE ORIGINALE  (immuable, sha256, source primaire — ne change jamais)
   ↓ rendu local par poppler
PAGES DÉRIVÉES   (DERIVED, empreintes propres, jamais retouchées)
   ↓ lecture PRIMARY  — modèle vision, sortie structurée
TRANSCRIPTION A + incertitudes explicites
   ↓ lecture BLIND    — second modèle, MÊME image, qui n'a PAS vu A
TRANSCRIPTION B
   ↓ réconciliation locale et déterministe (aucun troisième modèle ne vote)
   ↓ revue humaine, bloc par bloc
   ↓ ATTESTATION DE COMPLÉTUDE, page par page
TRANSCRIPTION VÉRIFIÉE  ← la seule qui fasse foi
   ↓
correction (humaine, inchangée)
```

La source primaire reste la copie originale. Une transcription, même vérifiée, en est
une lecture — pas un remplacement.

## 2. Téléversement

Deux voies, mêmes contrôles :

| voie | usage |
|---|---|
| écran de correction → **Téléverser la copie** | usage courant |
| `make s5-correction-copie ELEVE=… COPIE=…` | administration, lots |

**Un PDF multipage** est le cas principal : la pagination interne du PDF fait foi.
**Plusieurs images** (PNG, JPEG, WEBP, TIFF) sont acceptées, une par page.

L'ordre des pages est arrêté **dans le navigateur, avant l'envoi** : miniatures,
boutons monter/descendre, retrait, puis « Confirmer l'ordre et téléverser ». Tant que
ce bouton n'est pas cliqué, **rien n'a quitté le poste**. Le serveur enregistre
l'ordre reçu et ne le retrie jamais.

Ce choix est délibéré : une zone d'attente serveur pour les envois non confirmés
serait un endroit où des copies d'élèves s'accumuleraient sans statut ni provenance.

### Sécurité

Ni le nom, ni l'extension, ni le `Content-Type` du navigateur ne sont crus. **Seuls
les octets font foi** — un `.pdf` qui commence par `MZ` est refusé.

| contrôle | comportement |
|---|---|
| traversée de chemin, nom dangereux | nom réduit à son basename, caractères filtrés |
| fichier déguisé | type lu dans les octets de tête ; refus |
| fichier vide | refus |
| PDF illisible / 0 page | refus |
| doublon dans un même envoi | refus (ordre indéfendable) |
| PDF + images mélangés, ou plusieurs PDF | refus |
| taille excessive | `NEXUS_S5_UPLOAD_MAX_BYTES`, 120 Mo par défaut |
| pages excessives | `NEXUS_S5_UPLOAD_MAX_PAGES`, 60 par défaut |
| fichiers excessifs | `NEXUS_S5_UPLOAD_MAX_FILES`, 60 par défaut |

Le flux est **temporaire → contrôle → empreinte → ingestion atomique**. En cas
d'échec, le temporaire est détruit et aucune ligne n'est écrite : il n'existe pas
d'état où une copie serait à moitié rattachée.

La pièce ingérée est immuable et privée (`0400`). Un remplacement passe par `SUPERSEDED` :
l'ancienne pièce est conservée, jamais effacée.

## 3. Rendu des pages

`pdftoppm` (poppler), déjà utilisé par la QA PDF du dépôt — aucune dépendance
nouvelle. Les images fournies sont réencodées en PNG **sans recadrage, sans filtre,
sans rehaussement de contraste** : une retouche pourrait effacer un trait de crayon.

Le résultat est une pièce `DERIVED` (`source_kind = DERIVED_PAGE_IMAGES`) rattachée à
l'original par `derived_from_id`, avec son propre `sha256`, ses dimensions et son
`dpi`. L'original n'est pas touché.

### Résolution : 300 dpi — **valeur d'ingénierie par défaut, non démontrée**

Ce qui suit est une mesure de **rendu**, pas une mesure de qualité de lecture.
`make s5-ocr-mesure-dpi PDF=…` rend la taille effective d'une page A4 :

| dpi | pixels | poids page |
|---|---|---|
| 150 | 1240 × 1755 | 8,9 Ko |
| 200 | 1653 × 2339 | 16,3 Ko |
| 250 | 2066 × 2924 | 22,9 Ko |
| **300** | **2480 × 3509** | **33,2 Ko** |

Le raisonnement qui motive 300 dpi est **géométrique**, et rien de plus : un chiffre
manuscrit d'environ 6 mm occupe ≈ 71 px à 300 dpi contre ≈ 35 px à 150 dpi ; un
exposant, moitié moins. Plus de pixels donne au modèle plus de matière — c'est
plausible, ce n'est pas démontré.

> **Ce tableau ne mesure pas la précision OCR/HTR.** Aucune donnée présentée ici ne
> permet d'affirmer qu'« en dessous de 250 dpi, un exposant et un chiffre se
> confondent » pour un modèle donné. Cette affirmation, qui figurait dans une version
> antérieure de ce document, était une extrapolation et a été retirée.
>
> **État réel : `300 dpi = engineering default / hypothesis`**, pas « résolution
> optimale démontrée ».

Le vrai arbitrage se mesurera sur des **copies manuscrites réelles**, en comparant au
minimum 200 / 250 / 300 / 400 dpi sur qualité *et* coût — le poids transmis croît
comme le carré de la résolution, et les jetons d'entrée avec lui.

De même, les 33 Ko d'une page synthétique à 300 dpi **ne représentent pas** le poids
d'un vrai scan, avec écriture, bruit de capteur, ombres et compression. Ces chiffres
ne doivent servir à estimer ni la bande passante, ni le coût en jetons, ni la mémoire,
ni la durée d'envoi.

`NEXUS_S5_RASTER_DPI` permet d'ajuster ; `RASTER_MAX_PIXELS` borne les dérapages.

## 4. OpenRouter : configuration et secret

```bash
export OPENROUTER_API_KEY=...          # prioritaire
# ou, fichier local hors Git, mode 600 obligatoire :
runtime/secrets/openrouter.key
```

Réglages disponibles :

| variable | défaut |
|---|---|
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` |
| `OCR_MODEL_PRIMARY` | `google/gemini-3.1-pro-preview` |
| `OCR_MODEL_VERIFY` | `meta-llama/llama-4-maverick` — modèle de la lecture aveugle |
| `OCR_MODEL_BASELINE` | `mistralai/mistral-medium-3.1` — **repère de benchmark seulement**, voir §25 |
| `OPENROUTER_TIMEOUT` | 180 s |
| `OPENROUTER_MAX_RETRIES` | 4 |
| `OCR_MAX_COST_PER_COPY_USD` | 3,00 $ |

La clé **n'est jamais** : dans Git, en base, envoyée au navigateur, journalisée,
affichée. Le frontend appelle notre serveur ; notre serveur appelle OpenRouter.
L'interface n'affiche que `OpenRouter : configuré` ou `OpenRouter : clé absente`.
Un fichier de clé lisible par d'autres utilisateurs est **refusé** avec le `chmod` à
appliquer. Toute exception sortante passe par `redact()`.

## 5. Confidentialité — non négociable

Ce sont des copies d'élèves mineurs. Chaque appel porte, sans exception :

```json
"provider": {
  "data_collection": "deny",
  "zdr": true,
  "require_parameters": true,
  "allow_fallbacks": false
}
```

Si aucun endpoint conforme n'existe pour le modèle demandé, **l'appel échoue**
(`NoCompliantEndpointError`). Il n'est jamais rerouté vers un fournisseur qui
conserverait les données, et aucun repli vers un modèle non conforme n'est tenté —
y compris après une erreur transitoire.

Ces contraintes ne sont pas paramétrables depuis l'interface : les assouplir demande
de modifier `app/domain/openrouter.py`, ce qui laisse une trace dans Git.

### Ce que ZDR ne dit pas

`ZDR` signifie « l'endpoint ne conserve pas les données ». Il ne signifie **rien
d'autre** :

* **ZDR ≠ résidence géographique.** Un endpoint ZDR peut se trouver n'importe où. Si
  une exigence de résidence européenne apparaît, ce sera une politique distincte, à
  traiter comme telle.
* **ZDR ≠ conformité juridique.** Ce document n'écrit ni « conforme RGPD », ni
  équivalent : une telle qualification demande une analyse juridique indépendante que
  ni ce code ni cette documentation ne fournissent.
* **ZDR ≠ absence de cache.** Voir la section sur les trois caches.
* **ZDR ≠ absence de journalisation côté compte.** Voir ci-dessous.

### Ce que l'application ne peut pas vérifier

OpenRouter peut conserver prompts et réponses si une fonction de journalisation ou
d'observabilité est activée **au niveau du compte**. Aucune API n'expose cette
configuration : l'application ne sait ni la lire, ni l'empêcher.

Elle ne prétend donc jamais l'avoir vérifiée. `ACCOUNT_PRIVACY_POLICY` vaut :

| valeur | signification |
|---|---|
| `UNKNOWN` | défaut — le code ne sait rien de la configuration du compte |
| `OPERATOR_ATTESTED` | l'opérateur déclare avoir vérifié ; c'est une déclaration humaine, pas une preuve |
| `VERIFIED` | **inatteignable** : le code refuse de le produire, faute de pouvoir le démontrer |

Un test vérifie qu'une tentative de forcer `VERIFIED` retombe sur `UNKNOWN`.

**Recommandations opérationnelles**, à décider hors application :

* activer le ZDR au niveau du compte ou d'un garde-fou, lorsque l'offre le permet ;
* utiliser une **clé OpenRouter dédiée à S5**, avec un *spending limit* côté
  fournisseur. `OCR_MAX_COST_PER_COPY_USD` est un plafond applicatif : il ne connaît
  que les coûts que l'API lui rend, et ne remplace pas un plafond fournisseur ;
* ne pas activer la journalisation des prompts sur ce compte.

### Garde-fou d'envoi d'une copie réelle

```bash
ALLOW_REAL_STUDENT_REMOTE_OCR=0   # défaut : aucune copie d'élève ne part
```

Une pièce `REAL_STUDENT_COPY` non marquée synthétique n'est envoyée à aucun
fournisseur tant que ce drapeau vaut 0. Ce n'est pas un bouton d'interface : la
décision se prend hors application, en connaissance de ce que l'image contient. Les
fixtures synthétiques du contrôle de chaîne n'en dépendent pas.

Le journal des prompts et réponses côté OpenRouter n'est jamais activé
automatiquement par l'application.

### Les trois caches, à ne jamais confondre

| cache | qui le contrôle | ce que nous faisons |
|---|---|---|
| *prompt caching* du fournisseur | le fournisseur | rien ; optimisation interne au modèle |
| *response caching* d'OpenRouter | le compte, éventuellement à notre insu | `X-OpenRouter-Cache: false` **à chaque appel** |
| cache applicatif local | nous | `runtime/ocr_cache/`, mode 0600, ne quitte jamais le poste |

`provider.zdr` porte sur le **routage**, pas sur le cache de la passerelle : c'est
pourquoi l'en-tête part systématiquement, quel que soit le préréglage du compte. Un
test vérifie sa présence sur la requête HTTP réellement émise, et un test négatif
vérifie qu'on ne peut pas l'écraser depuis le corps de requête.

### Endpoint contrôlé

Un mauvais `OPENROUTER_BASE_URL` exfiltrerait les copies. Seul HTTPS vers
`openrouter.ai` est accepté ; tout autre hôte exige
`NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1`, réservé au développement. La vérification TLS
n'est jamais désactivée — un test parcourt le code à la recherche de `verify=False`.

**Stockage distant** : les copies ne sont **pas** déposées sur `/files` d'OpenRouter.
L'original probant est déjà stocké localement ; les pages partent en base64, le temps
de l'appel. Si un mécanisme `/files` devait apporter un avantage, il ferait l'objet
d'une décision explicite avant tout usage en production.

**Données personnelles — ce qui part réellement.** La partie *textuelle* de la
requête ne contient ni nom, ni classe, ni historique, ni identifiant d'évaluation :
un test le vérifie par mot entier sur la charge utile réelle.

> **Mais l'image, elle, est la copie.** Elle porte très probablement le nom de
> l'élève, écrit ou imprimé en tête de page, et tout ce que l'élève y a écrit.
> Affirmer « aucune donnée personnelle n'est envoyée » sur la foi d'un contrôle du
> JSON textuel serait faux. Ce qui part au fournisseur, c'est **la copie d'un élève
> identifiable**.

C'est précisément pourquoi l'envoi d'une copie réelle exige
`ALLOW_REAL_STUDENT_REMOTE_OCR=1` (§ ci-dessous) : la décision est prise en
connaissance de cause, pas par un clic.

Une dérivation `REDACTED_FOR_REMOTE_OCR` — masquage de la seule zone administrative
du sujet, dont la position est connue et garantie sans réponse — est **envisageable**
et non implémentée. Si elle l'était : aucun masquage heuristique, aucun risque
d'effacer du travail scolaire, original intact, provenance du recadrage enregistrée.

## 6. Stratégie de lecture : chaque page est vue

Le parsing PDF documentaire (Mistral OCR et équivalents) est excellent pour du texte
imprimé et de la structure. Il **n'est pas** le lecteur de notre cas critique, pour
deux raisons : notre matière est manuscrite et mathématique, et les pipelines PDF
plafonnent le nombre d'images effectivement remontées au modèle — une page non vue
serait une page silencieusement absente de la transcription.

La stratégie principale envoie donc **chaque page rendue** à un modèle vision, une
page par appel. `OCR_MODEL_BASELINE` reste disponible comme repère documentaire, pas
comme preuve.

Trois vocabulaires, distingués dans le code et la documentation :

* **OCR** — texte imprimé ;
* **HTR** — *Handwritten Text Recognition*, écriture manuscrite ;
* **transcription mathématique** — notation mathématique manuscrite.

## 7. Ce que la consigne interdit

Consignes versionnées : `handwriting_transcription_v1`, `math_verification_v1`
(`app/domain/ocr_prompts.py`). Chaque campagne enregistre sa `prompt_version` : deux
transcriptions divergentes à deux dates doivent pouvoir s'expliquer.

**Ne jamais corriger.** Si la copie porte `-5 - (-5) = -10`, la transcription porte
`-5 - (-5) = -10`. Pas `0`. Cela vaut pour les signes faux, les fractions mal formées,
les expressions inachevées, les unités oubliées.

**Aucune solution n'est montrée au modèle.** Ni réponse attendue, ni barème, ni
corrigé, ni diagnostic historique. Le modèle peut recevoir les énoncés imprimés et les
références A1…C2, uniquement pour rattacher les réponses aux questions. Un modèle à
qui l'on montre la bonne réponse normalise l'écriture vers elle, et transcrirait une
copie fausse en copie juste.

Attention explicite portée dans la consigne : signe moins / tiret / barre de fraction,
`×` / `x` / `*`, `÷` / `/`, numérateur et dénominateur, parenthèses et crochets,
exposants et indices, racines et leur portée, `=` `≠` `≈` `<` `>` `≤` `≥`, virgule
décimale, lettres `x` `y` `n` contre chiffres, unités, degrés, pourcentages, flèches,
coordonnées, ratures.

## 8. Sortie structurée

`response_format: json_schema`, `strict: true`, schéma `ocr-page-v1`. La réponse est
**revalidée localement** : le drapeau strict du fournisseur ne dispense pas de
vérifier. Un modèle qui n'honore pas le contrat est signalé comme inadapté — on ne
rafistole pas un JSON approximatif.

Par bloc : `block_id`, `item_ref` (nullable), `origin`
(`PRINTED` | `HANDWRITTEN` | `DIAGRAM_ANNOTATION`), `kind` (`TEXT` | `MATH` | `MIXED`),
`status` (`ACTIVE` | `CROSSED_OUT` | `OVERWRITTEN` | `AMBIGUOUS`), `verbatim`, `latex`,
`uncertainty` (`LOW` | `MEDIUM` | `HIGH`), `alternatives[]`, `notes`, `bbox`.

`bbox` est facultatif à dessein : les modèles vision généralistes ne fournissent pas
de coordonnées fiables, et prétendre le contraire donnerait une fausse précision
spatiale.

**Deux représentations.** `verbatim` restitue ce qui est écrit ; `latex` rend la même
expression lisible. Le LaTeX ne change jamais la valeur : si le verbatim porte une
égalité fausse, le LaTeX porte la même égalité fausse.

**Ratures.** Une rature est une donnée, pas du bruit. Le texte barré n'est jamais
jeté : il devient un bloc `CROSSED_OUT` à côté du bloc `ACTIVE`.

**Incertitude.** « Je ne sais pas » est une réponse utile. `uncertainty` +
`alternatives` (« 3 ou 8 », « signe moins ou barre de fraction ») ; `[illisible]` pour
une zone qui l'est vraiment. L'incertitude déclarée par un modèle est une aide, **pas
une probabilité calibrée**, et le système ne la traite pas comme telle.

## 9. Double lecture **aveugle** et réconciliation locale

`PASS 1 — PRIMARY` lit chaque page.

`PASS 2 — BLIND` relit **la même image**, avec un second modèle, **la même consigne et
le même schéma** — et sans jamais voir la transcription produite par PRIMARY.

> **Pourquoi aveugle.** Montrer la transcription candidate à un second modèle produit
> un biais de confirmation : acquiescer lui coûte moins que relire. Une version
> antérieure de ce pipeline faisait exactement cela et appelait le résultat un
> « consensus ». Ce n'en était pas un.

La comparaison des deux lectures est ensuite **locale et déterministe** : appariement
par texte identique, puis par (item, nature) ; ce qui ne s'apparie pas reste
`UNMATCHED` plutôt que d'être rapproché de force.

| situation | réconciliation |
|---|---|
| une seule lecture | `AI_SINGLE_READING` |
| deux lectures identiques, incertitude basse, même item | `AI_TWO_BLIND_READINGS_IDENTICAL` |
| lectures différentes | `HUMAN_REVIEW_REQUIRED` |
| bloc vu par une seule des deux lectures | `HUMAN_REVIEW_REQUIRED` (`UNMATCHED`) |
| incertitude `HIGH`, même en accord | `HUMAN_REVIEW_REQUIRED` |
| même texte, item différent | `HUMAN_REVIEW_REQUIRED` |

**Aucun troisième modèle ne vote.** Le désaccord entre deux lecteurs indépendants est
précisément l'information qui doit remonter à l'humain.

**`AI_TWO_BLIND_READINGS_IDENTICAL` n'est pas « correct ».** Deux modèles peuvent se
tromper de la même manière. Le nom dit ce qui a été observé — deux lectures, le même
résultat — et rien de plus. Un mode `SECOND_LOOK`, où l'on montrerait la candidate au
modèle pour éclairer un humain, reste possible ; son schéma existe et est testé, mais
il ne serait **jamais** appelé « lecture indépendante ».

### L'angle mort : l'omission

Une revue « par bloc » ne peut pas révéler une zone que **les deux** lectures ont
omise : l'écran ne montre que ce que les modèles ont vu. Une pile de blocs tous
acceptés ne prouve donc rien sur la complétude.

Deux mécanismes y répondent :

1. **les zones vues par une seule lecture** remontent en `UNMATCHED`, affichées à part
   sur l'écran de revue — la seconde lecture révèle les omissions de la première, et
   réciproquement ;
2. **l'attestation humaine de complétude**, page par page, obligatoire : un humain
   déclare avoir comparé la page originale et la transcription, et que tout contenu
   manuscrit ou mathématique visible est représenté ou explicitement marqué.

L'attestation porte sur des **octets précis** (`page_sha256`) : re-rendre la page à
une autre résolution la rend périmée, et la transcription redevient inexploitable.

## 10. Revue humaine

Écran `/eleve/<id>/transcription` : la page rendue à gauche (zoom, rotation
d'affichage, pagination, miniatures), la transcription à droite.

Par bloc : item, verbatim, **source LaTeX et rendu KaTeX côte à côte**, incertitudes,
alternatives, et la divergence PRIMARY / VERIFY quand elle existe.

Actions : **Accepter**, **Modifier**, **Illisible**, **Rejeter**, **Relancer OCR**.

Une décision humaine **s'ajoute** à la proposition de l'IA :

```
verbatim        ← ce que la machine a lu, conservé tel quel
human_verbatim  ← ce que l'humain retient
reviewed_at / reviewed_by_role
```

`AI_PROPOSED → HUMAN_VERIFIED`. Rien n'est écrasé silencieusement, et une relecture
ultérieure ne piétine jamais un bloc déjà tranché par un humain.

## 11. Machine d'état

`NOT_STARTED → RUNNING → AI_PROPOSED → REVIEW_REQUIRED → HUMAN_VERIFIED`, plus
`FAILED`.

**Un invariant unique**, `transcription_is_usable()`, centralise tout ce qui interdit
d'exploiter une transcription. Une garde posée sur une seule route ne protégerait rien
— un autre chemin appellerait le moteur directement. Elle exige, ensemble :

* une pièce source **courante** (ni remplacée, ni périmée) dont l'empreinte se vérifie ;
* des pages rendues dont l'empreinte se vérifie ;
* l'état `HUMAN_VERIFIED` : tous les blocs tranchés, tous les désaccords résolus ;
* la **complétude attestée** pour chaque page, sur les octets courants ;
* aucune campagne encore `RUNNING`, aucune campagne périmée.

Chacune de ces conditions a son test négatif isolé.

**Une copie scannée ne permet pas de déduire** l'autonomie, le rythme, la fréquence
d'aide ou l'attitude. Ces champs restent humains, et rien dans cette chaîne ne les
renseigne.

## 12. Provenance

Chaque bloc répond, sans ambiguïté :

| question | où |
|---|---|
| quelle page ? | `transcription_block.page_index` + `ocr_page.page_sha256` |
| quel original ? | `source_copy_id` → `source_copy` (ORIGINAL) |
| quel sha256 ? | `source_copy_file.sha256`, original et page rendue |
| quel modèle ? | `ocr_run.model_id`, `provider_name` |
| quel run ? | `primary_run_id`, `verify_run_id` |
| quelle consigne ? | `ocr_run.prompt_version`, `schema_version` |
| modifié par un humain ? | `review_state`, `human_verbatim` |
| quand, par qui ? | `reviewed_at`, `reviewed_by_role` |

Cette couche est **séparée de la correction** : rien n'écrit dans
`criterion_response`, et un test le vérifie.

## 13. Cache, coût, reprises

**Cache** — clé = `sha256(page) + modèle + prompt_version + schema_version + paramètres`,
paramètres incluant le **rang de la page** : la consigne porte « page N sur M », donc
deux pages aux octets identiques (deux pages blanches d'un même scan) envoient deux
requêtes différentes et ne peuvent pas partager un résultat. « Relancer » contourne le
cache, explicitement.

**Coût** — `usage: {include: true}` ; jetons, coût, modèle et durée sont enregistrés
par appel et par campagne. `OCR_MAX_COST_PER_COPY_USD` borne la dépense par copie :
au-delà, la campagne s'arrête. Aucune donnée de coût n'entre dans la correction
pédagogique.

**Reprises** — recul croissant borné sur 408/409/429/5xx et les échecs réseau ;
`Retry-After` respecté. **Jamais** de reprise sur 400/401/402/403/404/413/422, jamais
de reprise infinie, jamais de repli vers un modèle non conforme.

## 14. Sauvegarde

`make s5-correction-backup` inclut : l'original, les pages rendues, le cache de
lecture, et la base — qui porte les campagnes, les résultats bruts par page, les
versions de consigne, les blocs et les vérifications humaines.

`make s5-correction-backup-verify` restaure dans un temporaire et recontrôle chaque
empreinte : `RESTORE VERIFIED` ou `RESTORE FAILURE`.

> **Les archives ne sont pas chiffrées.** L'empreinte garantit l'**intégrité** ; elle
> ne dit rien de la **confidentialité**. L'archive est créée en `0600` — lisible par
> son seul propriétaire — et le répertoire des sauvegardes en `0700`. C'est tout.
> Une archive sortie de cette machine (clé USB, cloud, courriel) doit être chiffrée
> par ailleurs : elle contient des copies d'élèves, leurs transcriptions et les
> décisions humaines.

Le répertoire `runtime/secrets/` n'est **jamais** inclus dans une sauvegarde. Un test
dépose une clé sentinelle, produit une archive, et cherche cette sentinelle dans
**tous les octets** de l'archive — compressés comme décompressés.

### Droits de fichiers

L'immutabilité et la confidentialité sont deux propriétés distinctes. Un mode `0444`
est en lecture seule *et* lisible par tous : sur un poste partagé, la copie d'un élève
serait exposée à tous les comptes.

| élément | mode |
|---|---|
| copies originales et pages rendues | `0400` |
| cache de lecture | `0600` |
| archives de sauvegarde | `0600` |
| fichier de clé | `0600` (refusé sinon) |
| `source_copies/`, `ocr_cache/`, `backups/`, `secrets/` | `0700` |

L'intégrité vient du hachage, pas des droits. `make s5-correction-fsck` signale tout
fichier plus ouvert que prévu.

### Cohérence base ↔ fichiers

SQLite et les fichiers ne forment pas une transaction unique.
`make s5-correction-fsck` réconcilie les deux, en **lecture seule** : base référençant
un fichier absent, fichier orphelin, empreinte divergente, droits trop ouverts, pièce
dérivée sans original, rang de page dupliqué, plusieurs pièces courantes, campagne sur
pièce remplacée, campagne bloquée en `RUNNING`, attestation périmée, temporaire
résiduel. Aucune réparation n'est automatique, et une pièce correctement rattachée
n'est jamais supprimée par cet outil.

## 15. Modèles : configurables, et mesurés

```bash
make s5-ocr-modeles     # catalogue OpenRouter du jour, vision + sorties structurées
make s5-ocr-smoke       # chaîne de bout en bout, FIXTURE SYNTHÉTIQUE, clé requise
make s5-ocr-bench ELEVE=<id> [MODELES="a b"] [REFERENCE=ref.json]
```

Les défauts actuels ont été retenus après interrogation du catalogue réel (vision +
sorties structurées confirmées pour les trois). Ils sont **provisoires** : rien ne
démontre encore qu'ils lisent bien une écriture d'élève.

`ocr_benchmark.py` mesure deux régimes, sans les confondre :

* **sans référence humaine** — latence, coût par page, blocs, blocs mathématiques,
  ratures, incertitudes, rattachement aux items, et accord entre modèles. *L'accord
  n'est pas la justesse : deux modèles peuvent se tromper de la même manière.*
* **avec référence humaine** — CER, exactitude des expressions mathématiques, signes
  mathématiques erronés, omissions, blocs non appariés.

**Aucune métrique de qualité n'est produite sans référence humaine.** Le harness le
dit explicitement dans son rapport.

## 16. Ce qui reste à démontrer

Les tests logiciels ne valident pas la reconnaissance d'écriture manuscrite. Les
fixtures sont typographiques ; la plomberie est éprouvée, la lecture ne l'est pas.

Quand une vraie copie sera fournie, la première opération sera :

1. ingestion ;
2. rendu des pages ;
3. lecture PRIMARY ;
4. lecture BLIND (aveugle) ;
5. revue humaine complète ;
6. constitution d'une transcription de référence ;
7. mesure des erreurs des deux modèles.

`HANDWRITING_TRANSCRIPTION_GATE` ne peut pas être déclaré PASS avant cette mesure.

## 17. Ce que les défauts de modèle sont, et ne sont pas

> **Note de disponibilité — observation datée, pas vérité durable.**
> Au moment du premier test live, ces modèles ont été **refusés** par la politique de
> routage imposée (ZDR + `data_collection=deny` + `require_parameters` + pas de
> repli) : `anthropic/claude-opus-4.8`, `qwen/qwen3-vl-32b-instruct`,
> `openai/gpt-5.4-mini`, `mistralai/mistral-medium-3.1`.
>
> Ce refus **n'est pas** un jugement de qualité, et il n'est pas définitif : la
> compatibilité d'un fournisseur change dans le temps. Ces modèles restent des
> candidats légitimes du benchmark. La politique, elle, n'a pas été assouplie pour
> en retenir un — et ne doit jamais l'être.

`OCR_MODEL_PRIMARY` et `OCR_MODEL_VERIFY` sont des **valeurs de pilote**, pas des
choix de production. Elles ont passé une porte live sur **fixture synthétique** à une
date donnée — vision, sortie structurée, erreur volontaire conservée — et rien de
plus : aucune ne s'est encore mesurée sur une écriture d'élève.

`google/gemini-3.1-pro-preview` est de surcroît un modèle *preview*. Il ne doit pas
devenir PRIMARY de production par inertie.

`app/config.py` est **l'unique autorité** de ces valeurs. Les outils, les scripts, le
Makefile et cette documentation les lisent ; aucun ne les redéfinit. Un test le
vérifie sur l'arbre syntaxique.

Le benchmark réel devra interroger le catalogue **du jour** et comparer au minimum,
sous réserve de ZDR + image + sorties structurées :

* un modèle frontier généraliste ;
* un modèle vision rapide de la génération courante ;
* au moins un Qwen3-VL, orienté OCR et document AI ;
* un modèle de vérification fort ;
* une baseline économique.

### Critères de sélection, arrêtés *avant* de regarder les résultats

| critère | pourquoi |
|---|---|
| omissions | une zone non lue est invisible dans une revue par blocs |
| hallucinations | un bloc inventé pollue la correction |
| signes mathématiques erronés | un « − » lu « / » change la réponse |
| transcription mathématique exacte | c'est la mesure utile, pas le CER global |
| rattachement d'item correct | lire juste et rattacher faux est aussi grave |
| ratures correctement typées | une rature est une donnée |
| illisible correctement signalé | mieux vaut « je ne sais pas » qu'une invention |
| fiabilité des sorties structurées | une vision excellente avec un JSON douteux ne convient pas |
| latence | 60 pages × 2 lectures |
| coût par page | il se mesure sur de vrais scans, pas sur des fixtures |

Un modèle n'est pas promu parce qu'il « semble mieux » a posteriori.

## 18. Portes et leur état

| porte | ce qu'elle couvre |
|---|---|
| `make s5-full-gate` | statique, intégrité, tests, fsck, sauvegarde/restauration, état du jour — **sans clé, sans coût** |
| `make s5-ocr-live-gate` | catalogue + contrôle de chaîne réel sur **fixture synthétique** — clé requise, coût réel |

`OPENROUTER_IMPLEMENTATION_GATE`, `OPENROUTER_LIVE_CONNECTIVITY_GATE`,
`OPENROUTER_PRIVACY_ROUTING_GATE` et `HANDWRITING_REAL_ACCURACY_GATE` sont **quatre
portes distinctes**. Que l'implémentation soit complète et testée hors ligne ne dit
rien de la connectivité réelle, ni du routage effectivement obtenu, ni de la qualité
de lecture manuscrite.


## 19. Mode de données, authentification et transport

Le mode par défaut est **REAL** : un poste qui oublie de se déclarer est protégé, pas
exposé.

| | `S5_DATA_MODE=REAL` (défaut) | `S5_DATA_MODE=SYNTHETIC` |
|---|---|---|
| authentification | exigée, **y compris sur 127.0.0.1** | non exigée |
| mot de passe | `NEXUS_S5_PASSWORD`, ≥ 12 caractères | inutile en local |
| réseau en clair | **refus de démarrer** | autorisé, mais mot de passe exigé |
| ce qu'il contient | copies d'élèves réelles | fixtures uniquement |

Pourquoi l'authentification même en local : tout processus du poste capable d'ouvrir
un navigateur pourrait autrement lire les copies.

**HTTP Basic ne chiffre rien.** Exposer des données réelles au réseau en clair
laisserait circuler le mot de passe *et* les copies. Deux issues, et deux seulement :

```bash
# TLS direct
python3 -m app.cli serve --allow-network --ssl-certfile cert.pem --ssl-keyfile cle.pem

# TLS terminé par un proxy DÉCLARÉ
NEXUS_S5_TRUSTED_PROXY_TLS=1 NEXUS_S5_TRUSTED_PROXY_HOSTS=10.0.0.1 …
```

`X-Forwarded-Proto: https` n'est lu **que** si un proxy de confiance est déclaré et
que la connexion vient de lui. Aucun certificat n'est généré automatiquement : un
certificat non maîtrisé ne résout rien.

Un mot de passe est également exigé pour toute exposition réseau, **quel que soit le
mode déclaré** : `S5_DATA_MODE` est une déclaration d'opérateur, et une erreur de
déclaration ne doit pas suffire à ouvrir un serveur sans authentification.

### CSRF

Deux barrières indépendantes sur toute méthode mutante : un **jeton signé**
(cookie `nexus_csrf`, `SameSite=Strict`, `Secure` dès que le transport l'est, renvoyé
en `X-CSRF-Token`) et un **contrôle d'origine**. Un site tiers ne peut ni lire le
cookie, ni falsifier `Origin`. Chaque barrière a son test négatif.

### En-têtes

`Cache-Control: no-store` sur toute route sensible, `Referrer-Policy: no-referrer`,
`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, et une CSP
`script-src 'self'` — qui interdit tout script inline. Aucune copie ne transite par
`localStorage`, `IndexedDB` ou un service worker ; les aperçus d'envoi libèrent leurs
URL d'objet.

## 20. Rotation réelle des pages

Tourner l'affichage ne change pas ce que voit le modèle. Une rotation demandée par
l'opérateur produit une pièce dérivée :

```
ORIGINAL → DERIVED_PAGE_IMAGES → DERIVED_ROTATED_PAGES → lecture
```

0, 90, 180 ou 270 degrés ; toute autre valeur est refusée. La page tournée porte son
propre `sha256`, ses dimensions et son angle. **L'humain et le modèle voient la même
image** : la visionneuse sert la page effective, rotation comprise. Comme l'empreinte
change, la clé de cache change et la page est relue — automatiquement.

## 21. Preuves non textuelles et programmes

`kind` couvre `TEXT`, `MATH`, `MIXED`, `CODE`, `DIAGRAM`, `GRAPH`, `TABLE`,
`GEOMETRY`, `OTHER_NON_TEXT`.

**Une absence de texte n'est jamais une absence de réponse.** Une figure, une droite
graduée annotée ou un tableau peuvent constituer la réponse entière. Une preuve non
textuelle exige une description, et tant qu'un humain ne s'est pas prononcé sur elle,
la transcription n'est pas exploitable.

**Programmes** (`CODE`, déjà nécessaire pour la 1re NSI) : `verbatim_code` conserve
l'indentation espace par espace, la casse, la ponctuation, les guillemets, les
commentaires et les lignes vides. Aucun formatage, aucune réparation, aucune
conversion en Markdown. Une indentation fausse ou un `=` au lieu d'un `==` sont
l'information la plus utile de la copie.

## 22. Continuation entre pages

`continues_from` / `continues_to` proposés par le modèle, `human_continues_from` /
`human_continues_to` décidés par l'humain. La réponse n'est **jamais dupliquée** :
deux preuves physiques, un ensemble logique. Et le système ne rattache jamais une
suite à la question dont elle est physiquement la plus proche.

## 23. Profil de développement

Le parcours navigateur n'est pas facultatif : `make s5-full-gate` s'arrête si le
profil est incomplet, plutôt que de passer au vert avec un test critique ignoré.

```bash
pip install --user playwright        # dépendance de DÉVELOPPEMENT
python3 -m playwright install chromium
make s5-full-gate                    # inclut le navigateur et l'échelle 60 pages
make s5-browser-gate                 # parcours navigateur seul
make s5-debt-gate                    # verdict de dette, calculé
```

L'application de production ne dépend pas de Playwright.

## 24. Échelle mesurée — 60 pages

Mesures réelles, hors ligne, sur le plafond annoncé :

| grandeur | valeur |
|---|---|
| rastérisation, 60 pages à 300 dpi | 14,5 s (≈ 0,24 s/page) |
| campagne simulée, 120 appels | 0,4 s |
| blocs enregistrés | 480 |
| pages OCR | 120 |
| base (WAL compris) | 1,9 Mo |
| fichiers stockés | 2,0 Mo |
| reprise après interruption | 0,2 s, 0 appel refacturé |
| sauvegarde + restauration vérifiée | 0,05 s |
| réconciliation `fsck` | 0,04 s |
| affichage page 1 / page 60 | 4 ms / 3 ms |

Aucune croissance quadratique : la dernière page ne coûte pas plus que la première, et
l'écran n'en charge qu'une à la fois. **La latence et le coût des fournisseurs ne se
déduisent pas de ces chiffres** — le client est simulé, et une fixture ne pèse pas ce
que pèse un vrai scan.


## 25. Rôle du modèle BASELINE

`OCR_MODEL_BASELINE` est un **repère de comparaison**, employé par
`tools/ocr_benchmark.py` et par rien d'autre.

Il **ne lit jamais une copie**. À la date du dernier test live, il n'a d'ailleurs pas
d'endpoint compatible avec la politique imposée : le présenter comme un lecteur
disponible serait faux.

L'invariant est imposé par le code, pas seulement par la convention : `run_reading()`
n'accepte que les rôles `PRIMARY` et `BLIND`, et refuse explicitement tout autre —
`BASELINE` compris. Un test négatif le vérifie.

Si un jour ce modèle passe une porte live sous la politique en vigueur, il pourra
redevenir un candidat de lecture. Pas avant, et pas par inertie.
