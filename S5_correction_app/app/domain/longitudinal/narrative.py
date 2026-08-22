# -*- coding: utf-8 -*-
"""Rédaction déterministe du bilan longitudinal, à partir des seuls faits.

Ce module ne lit ni les documents sources, ni la base : il reçoit
``LONGITUDINAL_FACTS`` et rien d'autre. C'est la garantie que chaque phrase produite
est traçable jusqu'à un fait daté et empreinté.

Trois règles de langue, qui découlent du modèle de preuve :

* on écrit « a fait l'objet d'un travail ciblé en S2 », jamais « a été consolidé
  en S2 ». Un livret prouve ce qui a été proposé, pas ce qui a été acquis ;
* une réussite obtenue juste après le travail sur la notion est présentée comme
  telle, et suivie d'un contrôle à distance. Elle n'est pas annoncée comme
  installée ;
* une notion de l'année à venir n'est jamais un manque. Elle est une passerelle,
  et son échec s'écrit « sera naturellement reprise en classe ».

Les blocs produits sont éditables : l'enseignant peut réécrire n'importe lequel, et
sa version approuvée n'est jamais réécrasée par une régénération.
"""

Block = tuple      # (clé, titre, contenu)

_ORDINAUX = {1: "première", 2: "deuxième", 3: "troisième", 4: "quatrième", 5: "cinquième"}


def _liste(elements, vide="", conjonction="et"):
    elements = [e for e in elements if e]
    if not elements:
        return vide
    if len(elements) == 1:
        return elements[0]
    return "%s %s %s" % (", ".join(elements[:-1]), conjonction, elements[-1])


def _minuscule(label):
    return (label or "").rstrip(".").lower()


# ------------------------------------------------------------------- page 1
def _essentiel(f) -> str:
    prenom = f["student"]["first_name"]
    diag = f["initial_diagnostic"]
    n1 = f["n_minus_1"]

    if diag["available"] and diag["priorities"]:
        depart = ("Le positionnement de pré-rentrée avait signalé %d point%s de "
                  "vigilance et %d point%s d'appui."
                  % (len(diag["priorities"]), "s" if len(diag["priorities"]) > 1 else "",
                     len(diag["strengths"]), "s" if len(diag["strengths"]) > 1 else ""))
    else:
        depart = ("Le dossier disponible ne permet pas de reconstituer un "
                  "positionnement initial complet.")

    domaines_travailles = sorted({d["domain"] for d in f["domains"]
                                  if d["coverage"] in ("MODERATE", "STRONG")})
    axes = ("Le stage a porté principalement sur %s."
            % _liste([d.lower() for d in domaines_travailles[:4]], "les domaines du programme"))

    # Les familles lisent des domaines, pas des intitulés de compétence : la synthèse
    # de première page reste à cette granularité, le détail vient page 3.
    forces = list(dict.fromkeys((s["domain"] or _minuscule(s["label"])).lower()
                                for s in f["strengths"][:5]))[:3]
    priorites = list(dict.fromkeys((p["domain"] or _minuscule(p["label"])).lower()
                                   for p in f["consolidation_priorities"][:4]))[:2]

    if forces:
        etat = ("L'évaluation de clôture apporte des éléments positifs sur %s."
                % _liste(forces))
    else:
        etat = ("L'évaluation de clôture n'apporte pas encore d'élément positif "
                "concordant sur les domaines évalués.")
    etat += (" La part du sujet consacrée aux acquis de l'année précédente est "
             "réussie à %s %%." % _fr(n1["percentage"])) if n1["percentage"] is not None else ""

    if priorites:
        suite = ("La priorité des premières semaines porte sur %s." % _liste(priorites))
    else:
        suite = ("Aucune priorité de rattrapage ne se dégage : les premières semaines "
                 "serviront à entretenir les acquis et à aborder les notions nouvelles.")

    a_confirmer = [_minuscule(x["label"]) for x in f["to_confirm"]]
    reserve = ""
    if a_confirmer:
        reserve = (" %s réussites ont été obtenues juste après un travail sur la notion : "
                   "elles seront revérifiées à distance en deuxième semaine."
                   % ("Certaines" if len(a_confirmer) > 1 else "Une de ces"))

    return "%s a suivi les cinq séances du stage, soit dix heures de travail. %s %s %s %s%s" % (
        prenom, depart, axes, etat, suite, reserve)


def _objectifs_du_stage(f) -> str:
    diag = f["initial_diagnostic"]
    if not diag["available"] or not diag["priorities"]:
        return ("Le stage visait la reprise des prérequis du programme de l'année "
                "précédente et une première approche des notions de l'année à venir.")
    return ("Le stage avait pour objet de reprendre les points signalés au "
            "positionnement de pré-rentrée — %s — puis d'ouvrir, lors de la dernière "
            "séance, sur des notions du programme de l'année à venir."
            % _liste([p.rstrip(".").lower() for p in diag["priorities"][:4]]))


def _situation_de_depart(f) -> str:
    diag = f["initial_diagnostic"]
    if not diag["available"]:
        return ("Le dossier disponible ne permet pas de reconstituer un positionnement "
                "initial complet. Aucune comparaison entre le début et la fin du stage "
                "n'est donc proposée dans ce bilan.")
    phrases = []
    instrument = diag.get("instrument") or {}
    phrases.append(
        "Le positionnement de pré-rentrée a été passé le %s : %s, sous la forme d'un %s."
        % (diag.get("date") or "au début du stage",
           diag.get("items_traites") or "l'ensemble des questions a été traité",
           (instrument.get("format") or "questionnaire").lower()))
    if diag.get("strengths"):
        phrases.append("Trois domaines apparaissaient comme des points d'appui : %s."
                       % _liste([s.lower() for s in diag["strengths"]]))
    if diag.get("priorities"):
        phrases.append("Les points de vigilance portaient sur %s."
                       % _liste([p.rstrip(".").lower() for p in diag["priorities"]]))
    if diag.get("confidence_calibration"):
        phrases.append(
            "L'accord entre la réussite et la certitude annoncée était de %s : "
            "certaines réponses fausses étaient données avec une certitude maximale, "
            "ce qui a orienté le travail sur le contrôle du résultat."
            % diag["confidence_calibration"])
    phrases.append(
        "Ce positionnement était qualitatif et par domaine : il ne conservait pas les "
        "réponses question par question. Aucun écart chiffré ne peut donc être établi "
        "entre le début et la fin du stage.")
    return " ".join(phrases)


# ------------------------------------------------------------------- page 2
def _fil_conducteur(f) -> str:
    seances = [s for s in f["stage_trajectory"]["sessions"] if s.get("theme")]
    if len(seances) < 3:
        return ("Le parcours a suivi les thèmes des cinq séances du niveau, en "
                "concentrant le travail personnel sur les points signalés au diagnostic.")
    premiers = [_minuscule(s["theme"]) for s in seances[:2]]
    milieu = _minuscule(seances[2]["theme"]) if len(seances) > 2 else ""
    return ("Le stage a d'abord sécurisé %s, puis a installé %s, avant de mobiliser ces "
            "acquis dans des problèmes mêlant plusieurs domaines lors de la dernière "
            "séance, qui s'est achevée par l'évaluation de clôture."
            % (_liste(premiers), milieu))


def _travail_realise(f) -> str:
    """Ce que le stage a proposé — formulé sans jamais glisser vers l'acquisition."""
    lignes = []
    for seance in f["stage_trajectory"]["sessions"]:
        # Une compétence partagée entre un prérequis et une passerelle apparaît deux
        # fois dans la matrice, sous le même libellé : elle ne doit être citée qu'une.
        cibles = list(dict.fromkeys(_minuscule(c) for c in (seance.get("skills_targeted") or [])))
        if not cibles:
            continue
        lignes.append("en %s, %s" % (seance["session"], _liste(cibles[:3])))
    if not lignes:
        return ("Le détail séance par séance n'est pas disponible dans les documents "
                "consultés.")
    texte = ("Les notions suivantes ont fait l'objet d'un travail ciblé : %s."
             % _liste(lignes))
    if not f["stage_trajectory"]["observations_available_anywhere"]:
        texte += (" Les tableaux d'observation des séances n'ayant pas été renseignés, "
                  "ce bilan ne rend pas compte du déroulement des séances elles-mêmes : "
                  "il rend compte de ce qui a été proposé, et de ce que l'évaluation de "
                  "clôture établit.")
    return texte


# ------------------------------------------------------------------- page 3
def _score_brut(f) -> str:
    brut = f["final_assessment"]["raw_score"]
    if isinstance(brut, dict):
        brut = brut.get("sur_20") or brut.get("earned") or "—"
    return ("Le score brut au sujet de clôture est de %s sur 20. Ce nombre décrit la "
            "copie et rien de plus : le sujet agrège des prérequis de l'année écoulée "
            "et quelques situations de découverte portant sur le programme de l'année à "
            "venir. Les deux parts sont donc présentées séparément ci-dessous, et c'est "
            "la première qui renseigne sur les acquis." % brut)


def _consolidation(f) -> str:
    n1 = f["n_minus_1"]
    if n1["available_centi"] == 0:
        return "Aucun critère de prérequis n'a été évalué."
    texte = ("Sur la part du sujet consacrée aux acquis de l'année précédente, %s points "
             "sur %s sont obtenus" % (n1["earned"], n1["available"]))
    if n1["percentage"] is not None:
        texte += ", soit %s %%" % _fr(n1["percentage"])
    texte += (". Ce pourcentage décrit le corpus évalué — les compétences que ce sujet "
              "précis a mesurées — et ne se transpose pas en niveau général.")
    return texte


def _passerelles(f) -> str:
    bridge = f["bridge_n"]
    lignes = [l for l in f["skills"] if l["curriculum_scope"] == "bridge_n"]
    if not lignes:
        return ("Le sujet ne comportait pas de question portant sur le programme de "
                "l'année à venir.")
    prometteuses = [_minuscule(l["label"]) for l in lignes
                    if l["trajectory_status"] == "BRIDGE_PROMISING"]
    a_poursuivre = [_minuscule(l["label"]) for l in lignes
                    if l["trajectory_status"] != "BRIDGE_PROMISING"]
    texte = ("Le sujet comportait %s points de découverte portant sur le programme de "
             "l'année à venir. Ces questions ne sont pas des prérequis : elles n'avaient "
             "pas à être maîtrisées." % bridge["available"])
    if prometteuses:
        texte += (" Une première aisance encourageante apparaît sur %s."
                  % _liste(prometteuses))
    if a_poursuivre:
        texte += (" %s %s sera naturellement reprise en classe dans les premières "
                  "semaines de l'année." % ("En revanche," if prometteuses else "",
                                            _liste(a_poursuivre).capitalize()))
    return texte.strip()


def _points_forts(f) -> list:
    sortie = []
    for ligne in f["skills"]:
        if ligne["curriculum_scope"] != "n_minus_1" or not ligne["has_final_evidence"]:
            continue
        if ligne["trajectory_status"] not in ("CONSOLIDATION_OBSERVEE",
                                              "ACQUIS_ACTUELLEMENT_DISPONIBLE",
                                              "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION"):
            continue
        force = ("plusieurs éléments concordants"
                 if ligne["evidence_strength"] in ("MODERATE", "STRONG")
                 else "un nombre encore réduit d'éléments")
        if ligne["initial_status"] in ("fragile", "en_voie_acquisition"):
            phrase = ("%s : signalé au départ, ce point présente aujourd'hui %s."
                      % (ligne["label"], force))
        else:
            phrase = ("%s : l'appui constaté au départ se retrouve en fin de stage, "
                      "sur %s." % (ligne["label"], force))
        sortie.append(phrase)
    # Le §29 borne cette liste : au-delà de trois entrées, elle cesse d'être lue.
    return sortie[:3]


def _points_a_consolider(f) -> list:
    sortie = []
    for p in f["consolidation_priorities"][:3]:
        ligne = next((l for l in f["skills"]
                      if l["label"] == p["label"]
                      and l["curriculum_scope"] == "n_minus_1"), None)
        if ligne is None:
            continue
        if ligne["trajectory_status"] == "FRAGILITE_PERSISTANTE":
            motif = "signalé au départ, ce point reste installé malgré le travail conduit"
        elif ligne["trajectory_status"] == "FRAGILITE_INITIALE_CONFIRMEE":
            motif = "signalé au départ, ce point se retrouve à l'évaluation"
        else:
            motif = "l'évaluation situe cette compétence en deçà du seuil attendu"
        sortie.append("%s : %s." % (ligne["label"], motif))
    return sortie


def _a_confirmer(f) -> list:
    sortie = []
    for ligne in f["skills"]:
        if ligne["trajectory_status"] != "REUSSITE_A_CONFIRMER":
            continue
        sortie.append(
            "%s : réussite obtenue peu après le travail sur la notion ; revérifiée en "
            "deuxième semaine, sans révision préalable." % ligne["label"])
    return sortie[:3]


def _non_evaluees(f) -> list:
    return ["%s : travaillée pendant le stage, mais aucune question du sujet de clôture "
            "ne la mesure ; son état actuel n'est pas documenté." % x["label"]
            for x in f["without_final_evidence"] if x["worked_during_stage"]][:3]


# ------------------------------------------------------------------- page 4
def _conseil(f) -> str:
    priorites = [_minuscule(p["label"]) for p in f["consolidation_priorities"][:2]]
    diag = f["initial_diagnostic"]
    calibration = diag.get("confidence_calibration")
    phrases = []
    if priorites:
        phrases.append("Les quatre premières semaines gagnent à rester courtes et "
                       "régulières : quinze à vingt minutes, deux à trois fois par "
                       "semaine, valent mieux qu'une longue séance hebdomadaire.")
        phrases.append("La priorité porte sur %s." % _liste(priorites))
    else:
        phrases.append("Aucun rattrapage n'est nécessaire. Quinze minutes deux fois par "
                       "semaine suffisent à entretenir les automatismes pendant que la "
                       "classe installe les notions nouvelles.")
    if calibration:
        phrases.append("Un point mérite une attention particulière : nommer la propriété "
                       "utilisée avant de calculer, puis vérifier que le résultat est "
                       "plausible. C'est ce geste qui rend les erreurs visibles à l'élève "
                       "lui-même.")
    phrases.append("Les seuils indiqués dans le plan sont là pour être constatés à la "
                   "maison : ils permettent de savoir quand une notion est acquise, sans "
                   "attendre le premier contrôle.")
    return " ".join(phrases)


def _fr(valeur):
    """Pourcentage arrondi à l'unité, pour un document destiné aux familles.

    Une décimale suggérerait une exactitude que quarante-cinq minutes
    d'évaluation ne portent pas. La synthèse enseignant conserve la précision
    technique là où elle sert au diagnostic.
    """
    if valeur is None:
        return "—"
    return "%d" % round(float(valeur))


# --------------------------------------------------------------------- API
def parent_blocks(f) -> list:
    """Blocs du bilan destiné aux familles, dans l'ordre des quatre pages."""
    blocs = [
        ("essentiel", "L'essentiel", _essentiel(f)),
        ("objectifs_stage", "Objectifs du stage", _objectifs_du_stage(f)),
        ("situation_depart", "Situation de départ", _situation_de_depart(f)),
        ("fil_conducteur", "Fil conducteur du parcours", _fil_conducteur(f)),
        ("travail_realise", "Travail réalisé pendant le stage", _travail_realise(f)),
        ("score_brut", "Score brut au sujet de clôture", _score_brut(f)),
        ("consolidation", "Consolidation des prérequis", _consolidation(f)),
        ("passerelles", "Premières passerelles vers l'année suivante", _passerelles(f)),
    ]
    forts = _points_forts(f)
    if forts:
        blocs.append(("points_forts", "Points forts actuels",
                      "\n".join("— %s" % p for p in forts)))
    consolider = _points_a_consolider(f)
    if consolider:
        blocs.append(("points_consolider", "Points à consolider",
                      "\n".join("— %s" % p for p in consolider)))
    confirmer = _a_confirmer(f)
    if confirmer:
        blocs.append(("a_confirmer", "Réussites à confirmer dans la durée",
                      "\n".join("— %s" % p for p in confirmer)))
    non_evaluees = _non_evaluees(f)
    if non_evaluees:
        blocs.append(("non_evaluees", "Notions travaillées que l'évaluation ne mesure pas",
                      "\n".join("— %s" % p for p in non_evaluees)))
    blocs.append(("conseil", "Conseil Nexus Réussite", _conseil(f)))
    return blocs


def student_blocks(f) -> list:
    """Fiche de l'élève : langage simple, deuxième personne, aucun jargon."""
    forts = [_minuscule(s["label"]) for s in f["strengths"][:4]]
    priorites = [_minuscule(p["label"]) for p in f["consolidation_priorities"][:3]]
    objectifs = []
    for semaine in f["four_week_plan"]["weeks"][:3]:
        for objectif in semaine["objectives"][:1]:
            objectifs.append("Semaine %d — %s" % (semaine["week"], objectif["objective"]))
    return [
        ("sais_faire", "Ce que je sais déjà bien faire",
         "\n".join("— %s" % x for x in forts)
         or "Le sujet de clôture ne permet pas encore de le dire précisément."),
        ("a_consolider", "Ce que je dois encore consolider",
         "\n".join("— %s" % x for x in priorites)
         or "Rien de particulier : il s'agit d'entretenir ce qui est déjà en place."),
        ("objectifs", "Mes trois objectifs prioritaires",
         "\n".join("— %s" % o for o in objectifs) or "—"),
        ("preuve", "Comment je saurai que j'ai progressé",
         "\n".join("— %s" % s["success_threshold"]
                   for w in f["four_week_plan"]["weeks"]
                   for s in w["objectives"][:1])),
    ]
