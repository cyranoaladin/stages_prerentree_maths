# Génération des bilans

## Quatre documents

| type | fichier produit | destinataire | ton |
| --- | --- | --- | --- |
| `BILAN_PARENTS` | `BILAN_PARENTS_<ÉLÈVE>.pdf` | familles | professionnel, accessible, orienté action |
| `SYNTHESE_ENSEIGNANT` | `SYNTHESE_ENSEIGNANT_<ÉLÈVE>.pdf` | enseignant | technique, vocabulaire complet |
| `PLAN_RENTREE` | `PLAN_RENTREE_4_SEMAINES_<ÉLÈVE>.pdf` | familles et élève | opérationnel, une page |
| `FICHE_ELEVE` | `FICHE_ELEVE_<ÉLÈVE>.pdf` | élève | langage simple, aucun jargon |

Lorsqu'une personne suit plusieurs matières, la matière est ajoutée au nom du fichier :
Ahmad BELDI ne peut pas produire deux fichiers de même nom.

## Blocs, provenance, approbation

Un rapport est une suite de **blocs** nommés. Chaque bloc porte :

- son `source` : `deterministic`, `human`, ou `llm_suggestion` ;
- son `approved` : vrai dès que vous avez cliqué sur « Conserver ce texte ».

Une **régénération** ne remplace jamais un bloc `human` ou approuvé. Elle le conserve, et
consigne la conservation dans l'historique. L'ancienne version d'un bloc remplacé est
gardée dans `report_block_history`.

Une régénération après **approbation** du rapport ne modifie pas la version approuvée :
elle crée une version `v2`, en y reportant les blocs que vous aviez modifiés. La `v1`
approuvée reste consultable et son PDF reste sur le disque.

## Le générateur déterministe suffit

`DeterministicNarrativeGenerator` produit la totalité des textes, sans réseau, sans clé,
sans aléa. C'est le générateur utilisé. Il ne calcule rien : il met en phrases des faits
déjà établis par l'analyse, et recopie les nombres.

`LLMNarrativeGenerator` est une réservation d'architecture, désactivée. L'activer exigerait
`NEXUS_S5_ENABLE_LLM=1`, un fournisseur configuré par variable d'environnement, une
confirmation avant transmission, et la journalisation du fournisseur. Un générateur de
texte ne touche jamais un score.

## Ce que les textes ne diront jamais

Vérifié par les tests, sur le PDF réellement compilé :

- aucune progression chiffrée, aucun « +N % », aucun « a progressé de N niveaux » ;
- aucune notion de passerelle qualifiée de « lacune » ou de « non acquise » ;
- aucun identifiant technique — `skill_id`, `criterion_id`, `mastery_delta`,
  `n_minus_1`, `bridge_n`, `analysis_sha256` — dans un document destiné aux familles ou à
  l'élève ;
- aucune accolade JSON échappée dans le rendu.

La phrase de limite scientifique figure au contraire explicitement dans le bilan parents.

## LaTeX

`latex/nexus_bilan.sty` est **autonome** : il ne dépend pas de `nexusS5.sty`, qui
accompagne les documents distribués et n'est pas modifié. Il reprend les mêmes couleurs,
les mêmes encadrés et la même typographie, pour que les bilans ne détonnent pas à côté des
livrets.

Les gabarits Jinja2 emploient des délimiteurs adaptés à LaTeX — `\VAR{ }`, `\BLOCK{ }`,
`\#{ }` — pour ne pas entrer en conflit avec les accolades. Tout texte humain traverse
`latex_escape` avant d'y entrer.

## Compilation

```
runtime/build/<NOM>_v<version>/     répertoire de travail, recréé à chaque fois
runtime/reports/<élève>/            .tex, .pdf et .manifest.json conservés
```

Le moteur est lancé sans shell, avec un environnement minimal, `SOURCE_DATE_EPOCH` fixé
pour un rendu reproductible, deux passes pour résoudre `\pageref{LastPage}`, et un délai
maximal. La sortie est décodée en tolérant les octets non UTF-8 d'un journal LaTeX : une
erreur de compilation ne doit pas être perdue à cause d'un problème d'encodage.

En cas d'échec : le `.tex` est conservé, l'erreur et la fin du journal sont renvoyées, le
rapport **n'est pas** marqué généré, et l'échec est journalisé.

## Manifeste

Chaque PDF produit s'accompagne d'un manifeste :

```json
{
  "document_id": "BILAN_PARENTS-v1-asm-ines-kefi",
  "student_id": "ines-kefi",
  "assessment_id": "asm-ines-kefi",
  "report_type": "BILAN_PARENTS",
  "correction_revision": 1,
  "analysis_sha256": "…",
  "template_version": "1.0.0",
  "generated_at": "2026-08-21T19:32:11+01:00",
  "pdf_sha256": "…"
}
```

On peut ainsi dire, d'un PDF donné, de quelle révision de correction et de quelle analyse
il est issu.

## Génération en lot

« Générer tous les bilans validés » ne produit rien pour une correction non validée : ces
élèves sont **listés** dans la réponse, avec la raison. L'export de clôture range ensuite
les documents par type, écrit les analyses JSON, et empreinte chaque fichier dans
`MANIFEST_SHA256.json`.
