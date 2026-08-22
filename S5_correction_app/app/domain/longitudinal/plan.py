# -*- coding: utf-8 -*-
"""Plan des quatre premières semaines de l'année, déduit des faits longitudinaux.

Quatre partis pris, tous destinés à produire un plan qu'une famille peut réellement
tenir :

* **peu d'objectifs.** Deux par semaine, trois la dernière. Un plan qui liste huit
  priorités n'est pas suivi ;
* **une charge réaliste.** Quinze à vingt-cinq minutes, deux à quatre fois par
  semaine. Jamais « une heure de mathématiques par jour » : l'élève rentre de
  vacances et reprend une scolarité complète ;
* **un seuil vérifiable.** « Travailler les fractions » n'est pas un objectif :
  « réussir 4 soustractions de fractions sur 5 sans aide » en est un. La famille
  doit pouvoir constater elle-même si l'objectif est atteint ;
* **les passerelles ne sont pas des priorités.** Une notion de l'année à venir
  découverte le jour de l'évaluation ne devient pas un travail de rattrapage.

La semaine 2 porte les contrôles différés : toute compétence réussie immédiatement
après avoir été retravaillée y est revérifiée, sans amorçage.
"""

MAX_P1 = 2


def _liste(elements):
    elements = [e for e in elements if e]
    if not elements:
        return ""
    if len(elements) == 1:
        return elements[0]
    return "%s et %s" % (", ".join(elements[:-1]), elements[-1])

# Forme de chaque semaine : (numéro, objectifs, minutes, fréquence, intention).
WEEK_SHAPES = (
    (1, 2, 15, "3 séances de 15 minutes",
     "stabiliser les prérequis les plus critiques pour démarrer l'année"),
    (2, 2, 15, "3 séances de 15 minutes",
     "réactiver à distance et vérifier ce qui n'a été réussi qu'immédiatement"),
    (3, 2, 20, "2 séances de 20 minutes",
     "mobiliser deux compétences ensemble, dans un même problème"),
    (4, 3, 20, "2 séances de 20 minutes",
     "faire le point sur les quatre semaines"),
)

# Travail concret et seuil, par domaine. Le seuil est toujours une proportion
# constatable sur un petit nombre d'exercices : il doit pouvoir être vérifié à la
# maison, sans matériel ni correction experte.
DOMAIN_WORK = {
    "Nombres relatifs": (
        "4 calculs de somme ou de différence, puis 2 placements sur une droite graduée",
        "réussir 5 exercices sur 6 sans aide, en plaçant les nombres avant de conclure"),
    "Fractions": (
        "4 soustractions de fractions à dénominateurs différents, puis 2 problèmes courts",
        "réussir 5 exercices sur 6 sans aide, en convertissant les deux termes"),
    "Calcul littéral": (
        "4 développements du type k(a - b), puis 2 réductions avec constantes signées",
        "réussir 5 exercices sur 6 sans aide, signes compris"),
    "Géométrie": (
        "3 raisonnements rédigés en donnée–propriété–conclusion",
        "produire 3 raisonnements sur 4 sans ajouter d'hypothèse absente de l'énoncé"),
    "Grandeurs et mesures": (
        "3 calculs d'aire ou de périmètre sur figures composées, unités comprises",
        "réussir 3 exercices sur 4 sans aide, unités écrites"),
    "Proportionnalité": (
        "3 quatrièmes proportionnelles, dont un pourcentage",
        "réussir 3 exercices sur 4 sans aide"),
    "Statistiques": (
        "2 calculs de moyenne suivis d'un contrôle de vraisemblance",
        "réussir 3 exercices sur 4, en vérifiant que la moyenne est bien encadrée"),
}

_DEFAUT = ("une série courte d'exercices gradués sur la notion",
           "réussir 4 exercices sur 5 sans aide")


def _work_and_threshold(ligne):
    return DOMAIN_WORK.get(ligne.get("domain"), _DEFAUT)


def _objective_sentence(ligne) -> str:
    """Objectif formulé pour une famille : ce qu'il faut savoir faire, pas un statut."""
    label = (ligne.get("label") or "").rstrip(".")
    if ligne["curriculum_scope"] == "bridge_n":
        return ("se familiariser avec « %s », qui sera reprise en classe dès les "
                "premières semaines" % label.lower())
    return "rendre disponible sans aide « %s »" % label.lower()


def _candidates(trajectoire):
    """Compétences éligibles au plan, dans l'ordre où elles comptent.

    Une compétence sans preuve finale n'entre pas dans les priorités : on ne peut
    pas prioriser ce qu'on n'a pas mesuré. Elle reste visible dans la matrice et,
    si elle a été ciblée pendant le stage, dans les notions à revoir.
    """
    ordre = {"P1": 0, "P2": 1, "P3": 2}
    pool = [l for l in trajectoire
            if l["curriculum_scope"] == "n_minus_1"
            and l["has_final_evidence"]
            and l["priority_rank"] in ordre]
    pool.sort(key=lambda l: (ordre[l["priority_rank"]],
                             l["importance_n"] != "critique",
                             l["success_rate"] if l["success_rate"] is not None else 1.0))
    return pool


def _maintenance_pool(trajectoire):
    """Repli lorsqu'aucune priorité ne se dégage.

    Un élève qui réussit l'ensemble des prérequis n'a pas besoin d'un plan de
    rattrapage — mais il a besoin d'un plan. On bascule alors en entretien, sur
    les compétences les plus critiques pour l'année à venir, en le disant.
    """
    pool = [l for l in trajectoire
            if l["curriculum_scope"] == "n_minus_1" and l["has_final_evidence"]]
    pool.sort(key=lambda l: (l["importance_n"] != "critique",
                             l["success_rate"] if l["success_rate"] is not None else 1.0))
    return pool


def _cap_p1(pool):
    """Ramène le nombre de priorités de rang 1 à deux au plus.

    Le moteur d'analyse partagé tolère davantage de P1 : il décrit l'état des
    compétences, sans se soucier de ce qu'une famille peut tenir. Le plan, lui,
    est un engagement de travail : au-delà de deux priorités simultanées, il n'est
    pas suivi. Les suivantes deviennent P2 et restent visibles, avec le motif.
    """
    p1 = [l for l in pool if l["priority_rank"] == "P1"]
    if len(p1) <= MAX_P1:
        return []
    p1.sort(key=lambda l: (l["importance_n"] != "critique",
                           l["success_rate"] if l["success_rate"] is not None else 1.0))
    retrogradees = []
    for ligne in p1[MAX_P1:]:
        ligne["priority_rank"] = "P2"
        ligne["priority_downgraded_by_plan"] = True
        retrogradees.append({"analysis_skill_id": ligne["analysis_skill_id"],
                             "label": ligne["label"],
                             "reason": "au-delà de deux priorités simultanées, un plan "
                                       "de rentrée n'est pas tenu ; cette compétence "
                                       "reste au plan, en second rang"})
    return retrogradees


def build(trajectoire) -> dict:
    """Construit le plan des quatre semaines à partir de la matrice longitudinale."""
    pool = _candidates(trajectoire)
    mode = "consolidation" if pool else "entretien"
    if not pool:
        pool = _maintenance_pool(trajectoire)
    retrogradees = _cap_p1(pool)
    pool = _candidates(trajectoire) or pool     # retri après rétrogradation

    # Contrôles différés : compétences réussies juste après avoir été retravaillées.
    differes = [l for l in trajectoire
                if l["recommended_delayed_check"] and l["has_final_evidence"]]

    # Passerelles à revoir : jamais des priorités, seulement un signalement.
    passerelles = [l for l in trajectoire
                   if l["curriculum_scope"] == "bridge_n" and l["has_final_evidence"]]

    curseur, semaines = 0, []
    for numero, taille, minutes, frequence, intention in WEEK_SHAPES:
        objectifs = []

        if numero == 2 and differes:
            for rang, ligne in enumerate(differes[:2], start=1):
                travail, _ = _work_and_threshold(ligne)
                objectifs.append({
                    "rank": rang,
                    "analysis_skill_id": ligne["analysis_skill_id"],
                    "label": ligne["label"],
                    "objective": "vérifier à distance « %s », sans révision juste avant"
                                 % (ligne["label"] or "").rstrip(".").lower(),
                    "work": "mini-test de 15 minutes reprenant %s" % travail,
                    "duration_minutes": 15,
                    "frequency": "une fois dans la semaine",
                    "success_threshold":
                        "obtenir le même résultat qu'en fin de stage, sans aide et "
                        "sans avoir revu la notion le jour même",
                    "is_delayed_check": True,
                    "kind": "n_minus_1",
                })

        # La semaine 4 ne prend pas de nouvel objectif : elle réévalue ce qui a été
        # posé en priorité, puis fait le point. Y ajouter le vivier ferait dépasser
        # les trois objectifs, et un plan qu'on ne tient pas ne sert à rien.
        while numero != 4 and len(objectifs) < taille and curseur < len(pool):
            ligne = pool[curseur]
            curseur += 1
            travail, seuil = _work_and_threshold(ligne)
            if numero == 3 and objectifs:
                # Semaine de transfert : le second objectif mêle deux compétences.
                precedent = objectifs[0]
                objectifs.append({
                    "rank": len(objectifs) + 1,
                    "analysis_skill_id": ligne["analysis_skill_id"],
                    "label": ligne["label"],
                    "objective": "mobiliser ensemble « %s » et « %s » dans un même problème"
                                 % ((precedent["label"] or "").rstrip(".").lower(),
                                    (ligne["label"] or "").rstrip(".").lower()),
                    "work": "2 problèmes courts mêlant les deux notions",
                    "duration_minutes": 20,
                    "frequency": "2 séances de 20 minutes",
                    "success_threshold":
                        "mener 2 problèmes sur 3 jusqu'au bout, en nommant la propriété "
                        "utilisée avant de calculer",
                    "is_delayed_check": False,
                    "kind": "n_minus_1",
                })
                continue
            objectifs.append({
                "rank": len(objectifs) + 1,
                "analysis_skill_id": ligne["analysis_skill_id"],
                "label": ligne["label"],
                "objective": (_objective_sentence(ligne) if mode == "consolidation"
                              else "entretenir « %s », qui sera sollicitée dès les "
                                   "premiers chapitres"
                                   % (ligne.get("label") or "").rstrip(".").lower()),
                "work": travail,
                "duration_minutes": minutes,
                "frequency": frequence,
                "success_threshold": seuil,
                "is_delayed_check": False,
                "kind": "n_minus_1" if mode == "consolidation" else "maintenance",
            })

        if numero == 3 and len(objectifs) < 2:
            # Le vivier de priorités peut être plus court que le plan. La semaine de
            # transfert garde tout de même son objet : mêler deux compétences déjà
            # travaillées. On les reprend parmi celles des semaines précédentes.
            deja = [o for sem in semaines for o in sem["objectives"]
                    if o["analysis_skill_id"]]
            deja += [o for o in objectifs if o["analysis_skill_id"]]
            noms = list(dict.fromkeys((o["label"] or "").rstrip(".").lower()
                                      for o in deja if o["label"]))
            if len(noms) >= 2:
                objectifs.append({
                    "rank": len(objectifs) + 1, "analysis_skill_id": None,
                    "label": "Transfert",
                    "objective": "mobiliser ensemble « %s » et « %s » dans un même problème"
                                 % (noms[0], noms[1]),
                    "work": "2 problèmes courts mêlant les deux notions",
                    "duration_minutes": 20, "frequency": "2 séances de 20 minutes",
                    "success_threshold":
                        "mener 2 problèmes sur 3 jusqu'au bout, en nommant la propriété "
                        "utilisée avant de calculer",
                    "is_delayed_check": False, "kind": "transfer",
                })

        if numero == 4:
            # Réévaluation explicite de ce qui a été posé en priorité, puis des
            # réussites qui restaient à confirmer.
            # Deux réévaluations au plus : la troisième place revient au bilan
            # cumulatif, qui clôt les quatre semaines.
            a_revoir = [l for l in pool if l.get("priority_rank") in ("P1", "P2")][:2]
            for ligne in a_revoir:
                _, seuil = _work_and_threshold(ligne)
                objectifs.append({
                    "rank": len(objectifs) + 1,
                    "analysis_skill_id": ligne["analysis_skill_id"],
                    "label": ligne["label"],
                    "objective": "réévaluer « %s », posée en priorité à la rentrée"
                                 % (ligne["label"] or "").rstrip(".").lower(),
                    "work": "reprendre la série de la semaine correspondante, sans aide",
                    "duration_minutes": 20, "frequency": "une fois dans la semaine",
                    "success_threshold": seuil,
                    "is_delayed_check": False, "kind": "review",
                })
            # Bilan cumulatif : on réévalue ce qui a été travaillé, pas autre chose.
            revues = [o["label"] for s in semaines for o in s["objectives"]]
            objectifs.append({
                "rank": len(objectifs) + 1,
                "analysis_skill_id": None,
                "label": "Bilan cumulatif des quatre semaines",
                "objective": "reprendre en une seule série les notions travaillées "
                             "depuis la rentrée",
                # Le champ est lu dans un tableau étroit : on nomme au plus deux
                # notions, le reste est déjà détaillé semaine par semaine au-dessus.
                "work": "6 exercices mêlant %s"
                        % (_liste(list(dict.fromkeys(l.rstrip(".").lower()
                                                     for l in revues if l))[:2])
                           or "les notions des trois semaines précédentes"),
                "duration_minutes": 20,
                "frequency": "une fois dans la semaine",
                "success_threshold": "réussir 4 exercices sur 6 sans aide ; en dessous, "
                                     "reprendre la semaine correspondante",
                "is_delayed_check": False,
                "kind": "review",
            })

        semaines.append({
            "week": numero, "intention": intention, "duration_minutes": minutes,
            "frequency": frequence, "objectives": objectifs,
        })

    p1 = [l for l in pool if l["priority_rank"] == "P1"]
    return {
        "mode": mode,
        "mode_note": ("le plan porte sur les priorités dégagées par l'évaluation"
                      if mode == "consolidation" else
                      "l'évaluation ne dégage aucune priorité de consolidation : le "
                      "plan porte sur l'entretien des compétences les plus sollicitées "
                      "en début d'année, et sur les notions de l'année à venir"),
        "weeks": semaines,
        "priorities": [{"analysis_skill_id": l["analysis_skill_id"], "label": l["label"],
                        "domain": l["domain"], "priority_rank": l["priority_rank"]}
                       for l in pool[:3]],
        "delayed_checks": [{"analysis_skill_id": l["analysis_skill_id"],
                            "label": l["label"]} for l in differes],
        "bridge_follow_up": [{"analysis_skill_id": l["analysis_skill_id"],
                              "label": l["label"], "action": l["bridge_action"]}
                             for l in passerelles],
        "p1_count": len(p1),
        "p1_cap": MAX_P1,
        "p1_within_cap": len(p1) <= MAX_P1,
        "p1_downgraded_by_plan": retrogradees,
        "total_weekly_minutes": [s["duration_minutes"] * _seances(s["frequency"])
                                 for s in semaines],
    }


def _seances(frequence: str) -> int:
    for mot, valeur in (("3 séances", 3), ("2 séances", 2), ("une fois", 1)):
        if frequence.startswith(mot):
            return valeur
    return 2
