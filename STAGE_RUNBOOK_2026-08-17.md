# STAGE RUNBOOK — Nexus Réussite (Stages Pré-rentrée 2026-2027)
**Guide d'utilisation opérationnel pour l'enseignant**

---

## 1. Avant l'arrivée des élèves (H - 30 min)

1. Ouvrir le dossier de livraison :
   `~/Documents/Nexus_Reussite/LIVRAISON_STAGES_2026-08-17_V3_FINAL`
2. Consulter le document de démarrage rapide :
   `00_COMMENCER_ICI/COMMENCER_ICI.html`
3. Vérifier les impressions de la Séance 1 :
   - Fichiers dans `01_IMPRESSION_URGENTE/SEANCE_1/`
   - Déjà répartis par sous-dossiers : `01_ELEVES`, `02_PROFESSEUR`, `03_SUPPORTS`.

---

## 2. Impression et Préparation des Documents (H - 20 min)

- **4e Maths (3 élèves)** : Imprimer 3 ex. activité élève + 1 ex. fiche prof + 3 ex. supports.
- **3e Maths (5 élèves)** : Imprimer 5 ex. activité élève + 1 ex. fiche prof + 5 ex. supports.
- **2nde Maths (2 élèves)** : Imprimer 2 ex. activité élève + 1 ex. fiche prof + 2 ex. supports.
- **1re Spé Maths (3 élèves)** : Imprimer 3 ex. activité élève + 1 ex. fiche prof + 3 ex. supports.
- **1re NSI (2 élèves)** : Imprimer 2 ex. activité élève + 1 ex. fiche prof + 2 ex. supports.
- **Format d'impression** : Impression **Recto Simple obligatoire**.

---

## 3. Lancement de la Tablette Enseignant (H - 10 min)

Pour enseigner avec une tablette sur le réseau Wi-Fi de la salle :

```bash
# Dans le terminal du dépôt :
make tablet-serve-private
```
- L'adresse IP locale s'affiche automatiquement dans le terminal (ex: `http://192.168.x.x:8000`).
- Ouvrir cette URL sur le navigateur de la tablette.
- Accéder au **Mode Séance du Jour** en 1 clic.

---

## 4. Pendant la Séance (H0 à H+2h)

- Utiliser `04_TABLETTE_ENSEIGNANT/SEANCE_DU_JOUR.html` pour naviguer entre :
  - **Activité élève**
  - **Fiche professeur (durée & déroulé)**
  - **Supports & Manipulations**
  - **Cartes d'aide**
- Ne jamais laisser l'écran de la tablette visible par un élève lorsqu'un corrigé ou dossier nominatif privé est ouvert.

---

## 5. Fin de Séance & Fermeture (H+2h)

1. Récupérer les productions et auto-évaluations des élèves.
2. Arrêter le serveur tablette (`CTRL+C` dans le terminal).
3. Les dossiers confidentiels restent sécurisés sous pli dans `06_DOSSIERS_NOMINATIFS_CONFIDENTIELS/`.
