# Validation opérationnelle sur la première copie réelle

## Où en est le système

```
Statut actuel : READY_FOR_PILOT
```

Le pipeline a été éprouvé de bout en bout sur des **jeux synthétiques** : 92 tests
passent, les quatre PDF compilent, les invariants tiennent, les soixante documents
distribués sont intacts. Ce n'est pas la même chose qu'avoir corrigé une copie réelle.

Le système ne passera à `OPERATIONALLY_VALIDATED` qu'après la correction complète d'une
première copie par un enseignant, et la revue humaine du bilan produit.

**Aucune correction réelle n'a été saisie par l'outil de développement.** Les quinze
grilles sont vierges.

## Élève pilote recommandé

**Ines KEFI — Entrée en Quatrième — Mathématiques** (`ines-kefi`).

Pourquoi celle-ci : 22 critères, un seul critère de passerelle (le produit de relatifs en
C2), plusieurs compétences marquées « réussite immédiate après remédiation », et aucun
critère mixte. Le cas est représentatif sans être le plus complexe — c'est ce qu'on
attend d'un pilote.

Si la copie d'Ines KEFI n'est pas disponible, prendre **Sarah BARGAOUI** (`sarah-bargaoui`,
3e), de structure comparable.

## Déroulé

### 1. Avant de commencer

- [ ] `make s5-correction-qa` rend `PASS` et `immutable_artifacts_changed = 0`
- [ ] La copie papier de l'élève est sous les yeux
- [ ] Le sujet distribué s'affiche bien dans la colonne de gauche

### 2. Correction

- [ ] Les 22 critères sont saisis, un par un
- [ ] Chaque code d'erreur porte sur le critère effectivement échoué, et sur lui seul
- [ ] Aucun critère intégralement réussi ne porte de code d'erreur
- [ ] Les zéros sans cause identifiable sont marqués « non répondu » ou « cause non
      identifiée », pas affublés d'un code inventé
- [ ] Les méthodes correctes mais différentes du corrigé sont cochées comme telles
- [ ] La certitude est saisie là où le sujet la demandait, et nulle part ailleurs
- [ ] L'indicateur d'enregistrement affiche bien une heure après chaque geste

### 3. Contrôle humain de la saisie

- [ ] Le score brut affiché correspond au total recompté à la main sur la copie
- [ ] Les points des acquis N−1 et des passerelles s'additionnent bien à 20
- [ ] Un rechargement de la page ne perd rien

### 4. Validation

- [ ] « Valider la correction » aboutit
- [ ] Si des points sont signalés, ils sont compréhensibles et corrigeables sans deviner

### 5. Analyse — la comparaison humaine

C'est l'étape décisive. Lire l'écran d'analyse **en tenant la copie**, et vérifier :

- [ ] Le statut de chaque compétence correspond à ce que la copie montre réellement
- [ ] Aucune compétence classée `SOLIDE` ne repose sur un critère isolé
- [ ] Les compétences « à confirmer » sont bien celles retravaillées pendant la séance
- [ ] Le profil d'erreurs ne contient que des codes réellement saisis
- [ ] Le critère de passerelle n'a dégradé aucun statut d'acquis N−1
- [ ] Les trois blocs de conclusion sont défendables devant un collègue

Si un désaccord apparaît entre le jugement de l'enseignant et le statut calculé :
**ne pas modifier le score pour faire coïncider les deux**. Noter le désaccord, et le
signaler : c'est une règle à discuter, pas une note à ajuster.

### 6. Génération

- [ ] Les quatre documents se génèrent
- [ ] Aucun ne contient d'identifiant technique ni d'accolade

### 7. Revue du bilan parents

Lire le bilan comme le lira une famille :

- [ ] Le score sur 20 n'est pas le titre du document
- [ ] La distinction acquis / découvertes est compréhensible sans explication
- [ ] Aucune phrase ne laisse croire à une progression mesurée
- [ ] Le plan de quatre semaines est réaliste
- [ ] Le ton est juste : ni alarmiste, ni complaisant
- [ ] Les textes modifiés à la main sont bien ceux qui figurent dans le PDF

### 8. Décision

- [ ] Le bilan est approuvé
- [ ] `python3 tools/verify_integrity.py` rend toujours `PASS`
- [ ] Une sauvegarde est prise

Si tout est coché :

```
Statut : OPERATIONALLY_VALIDATED
```

à inscrire dans `docs/QA_FINAL.md`, avec la date et le nom de l'élève pilote.

## Ce qu'il faut noter pendant le pilote

| question | réponse à consigner |
| --- | --- |
| Durée réelle de correction d'une copie | |
| Gestes manqués ou pénibles dans l'interface | |
| Statuts calculés en désaccord avec le jugement enseignant | |
| Phrases du bilan à reformuler systématiquement | |
| Champs manquants | |

Ces notes valent plus qu'un test automatique de plus : elles disent si l'outil sert
réellement.
