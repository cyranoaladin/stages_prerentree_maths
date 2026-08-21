# -*- coding: utf-8 -*-
"""Génère les livrets LaTeX et les fichiers JSON de la séance S5 de clôture.

Sortie, pour chaque couple élève × matière :

    S5_cloture/<niveau>/<matiere>/<Eleve>/
        S5_TRAVAIL_<NIVEAU>_<ELEVE>.tex          (75 min, aucun corrigé)
        S5_EVALUATION_<NIVEAU>_<ELEVE>.tex       (45 min, aucun corrigé, aucun barème)
        student_learning_profile.json
        evaluation_blueprint.json
        responses_TEMPLATE.json
        post_stage_analysis_schema.json
        four_week_action_plan_TEMPLATE.json
        _ENSEIGNANT/
            S5_ENSEIGNANT_<NIVEAU>_<ELEVE>.tex   (profil, déroulé, corrigés, barème)
            evaluation_manifest.json
            answer_key.json
            README.md

Les fichiers contenant une réponse attendue sont regroupés dans `_ENSEIGNANT/`
(§17 : dossiers enseignants clairement séparés).
"""

import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data import common
from data.levels import LEVELS, LEVEL_ORDER
from data import criteria_map

GENERATED_ON = "2026-08-20"
SCHEMA_PREFIX = "nexus-s5"


# --------------------------------------------------------------------- helpers
STATUT_FR = {
    "acquis": "acquis",
    "en_voie_acquisition": "en voie",
    "fragile": "fragile",
    "non_evalue": "non évalué",
    "non_travaille": "non travaillé",
}

# Espace de réponse élargi pour les phases de consolidation : ces exercices se
# traitent au stylo, avec la relation écrite avant le calcul.
SPACE_UP = {"short": "lines:2", "lines:2": "lines:3", "lines:3": "lines:4",
            "lines:4": "lines:5", "lines:5": "lines:6", "lines:6": "lines:7"}


def space_tex(space):
    if not space:
        return r"\shortlines{1}"
    if space == "short":
        return r"\shortlines{1}"
    if space.startswith("lines:"):
        return r"\worklines{%s}" % space.split(":")[1]
    return r"\shortlines{1}"


def preamble(head_right, foot_left):
    return "\n".join([
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage{nexusS5}",
        r"\setnexusheader{%s}{%s}" % (head_right, foot_left),
        r"\begin{document}",
    ])


# Caractères Unicode mathématiques rencontrés dans les dossiers sources, convertis
# en LaTeX afin qu'aucun document ne dépende d'un moteur Unicode.
TEX_SUBST = {
    "\u222a": r"$\cup$", "\u2229": r"$\cap$", "\u00d7": r"$\times$", "\u00f7": r"$\div$",
    "\u2212": r"$-$", "\u00b2": r"$^2$", "\u00b3": r"$^3$", "\u2075": r"$^5$",
    "\u2074": r"$^4$", "\u207b": r"$^-$", "\u2260": r"$\neq$", "\u2265": r"$\geqslant$",
    "\u2264": r"$\leqslant$", "\u221a": r"$\sqrt{\ }$", "\u211d": r"$\mathbb{R}$",
    "\u2192": r"$\rightarrow$", "\u2264": r"$\leqslant$",
}


def escape(txt):
    """Texte brut issu des dossiers sources vers texte LaTeX sûr."""
    txt = (txt.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
              .replace("#", r"\#"))
    for k, v in TEX_SUBST.items():
        txt = txt.replace(k, v)
    return txt


# ------------------------------------------------------------- livret de travail
def render_travail(st):
    lv = core.level_of(st)
    ph = core.phases(st)
    out = [preamble("%s — Stage de pré-rentrée" % lv["label"],
                    "Séance 5/5 — %s" % st["name"])]
    out.append(r"\nexuscover{SÉANCE 5 --- RÉINVESTIR, CONSOLIDER, PRÉPARER LA RENTRÉE}{Livret de travail}{%s}{%s}{%s --- %s --- 1\,h\,15 de travail, puis 45 minutes d'évaluation dans un document séparé}"
               % (st["name"], st["parcours"], lv["label"], lv["subject"]))

    out.append(r"\begin{goalbox}")
    out.append(r"\textbf{Objectif personnel de cette séance.} %s" % escape(st["objectif"]))
    out.append(r"\par\medskip")
    out.append(r"\textbf{Ce livret couvre uniquement les 75 premières minutes.} L'évaluation finale est remise ensuite, dans un document distinct.")
    out.append(r"\end{goalbox}")

    # le fil des cinq séances
    out.append(r"\begin{methodbox}")
    out.append(r"\textbf{Le fil des cinq séances}")
    out.append(r"\begin{itemize}[leftmargin=13mm,labelsep=3mm,itemsep=1.5pt]")
    for s in ("S1", "S2", "S3", "S4"):
        out.append(r"\item[\textbf{\color{Navy}%s}] %s ;" % (s, lv["sessions"][s]))
    out.append(r"\item[\textbf{\color{Navy}S5}] aujourd'hui : réactiver, consolider deux axes personnels, faire le pont vers la %s, puis mesurer." % lv["year_next"])
    out.append(r"\end{itemize}")
    out.append(r"\end{methodbox}")

    # feuille de route
    out.append(r"\sectiontitle{Feuille de route des 75 minutes}")
    out.append(r"\rowcolors{2}{SoftBlue}{white}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{20mm} X X}")
    out.append(r"\rowcolor{Navy}\color{white}Temps & \color{white}Travail & \color{white}Preuve attendue \\")
    proofs = {
        1: "Cinq réponses écrites et le contrôle utilisé.",
        2: "Trois réussites autonomes sur l'axe prioritaire.",
        3: "Deux réussites autonomes sur le second axe.",
        4: "Une production reliant un acquis de %s à un attendu de %s." % (lv["year_prev"], lv["year_next"]),
        5: "Deux engagements écrits avant l'évaluation.",
    }
    for p in ph:
        out.append(r"%d--%d min & %s & %s \\" % (p["debut"], p["fin"], escape(p["objectif"]), proofs[p["n"]]))
    out.append(r"\end{tabularx}")

    out.append(r"\begin{graybox}\small\textbf{Règle de la séance.} J'écris ma réponse \emph{et} le contrôle qui la rend défendable. "
               r"Une réponse sans contrôle reste une hypothèse. La ligne « Certitude » se remplit \emph{avant} toute vérification.\end{graybox}")

    # ---------------- phase 1
    p = ph[0]
    out.append(r"\par\vspace{2mm}")
    out.append(r"\phasehead{Phase 1 --- Réactivation}{%d--%d min}{%s}" % (p["debut"], p["fin"], escape(lv["phase1"]["objectif"])))
    out.append(lv["phase1"]["consigne"])
    out.append(r"\begin{enumerate}")
    for it in lv["phase1"]["items"]:
        out.append(r"\item %s" % it["tex"])
        out.append(r"\shortlines{2}")
    out.append(r"\end{enumerate}")
    out.append(r"\certline")
    out.append(r"\aideline")

    # ---------------- phases 2 et 3
    for p in (ph[1], ph[2]):
        m = p["module"]
        out.append(r"\needspace{62mm}\par\vspace{3mm}")
        out.append(r"\phasehead{Phase %d --- %s}{%d--%d min}{%s}"
                   % (p["n"], "Consolidation, axe prioritaire" if p["n"] == 2 else "Consolidation, second axe",
                      p["debut"], p["fin"], escape(m["titre"])))
        out.append(m["rappel"])
        if p["avec_exemple"]:
            out.append(r"\begin{graybox}")
            out.append(m["exemple"])
            out.append(r"\end{graybox}")
        out.append(r"\subsectiontitle{À toi}")
        out.append(r"\begin{enumerate}")
        for ex in p["exos"]:
            out.append(r"\needspace{18mm}")
            out.append(r"\item %s" % ex["tex"])
            out.append(space_tex(SPACE_UP.get(ex["space"], ex["space"])))
        out.append(r"\end{enumerate}")
        out.append(r"\begin{successbox}\textbf{Critère de réussite de cette phase :} %s\end{successbox}" % escape(m["reussite"]))
        out.append(r"\certline")

    # ---------------- phase 4
    p = ph[3]
    out.append(r"\needspace{62mm}\par\vspace{3mm}")
    out.append(r"\phasehead{Phase 4 --- Réinvestissement}{%d--%d min}{%s}"
               % (p["debut"], p["fin"], escape(lv["phase4"]["objectif"])))
    out.append(lv["phase4"]["tex"])

    # ---------------- phase 5
    p = ph[4]
    out.append(r"\needspace{62mm}\par\vspace{3mm}")
    out.append(r"\phasehead{Phase 5 --- Avant l'évaluation}{%d--%d min}{Cadrage méthodologique. Aucun contenu de l'évaluation n'est annoncé.}"
               % (p["debut"], p["fin"]))
    out.append(common.PHASE5_TEX)
    out.append(r"\begin{warningbox}\textbf{Fin du livret de travail.} L'évaluation finale est un document séparé, remis par l'enseignant à l'issue de ces 75 minutes.\end{warningbox}")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------- évaluation élève
def render_evaluation(st):
    lv = core.level_of(st)
    items = core.exam_items(st)
    out = [preamble("%s — Stage de pré-rentrée" % lv["label"],
                    "Évaluation finale — %s" % st["name"])]
    out.append(r"\nexuscover{ÉVALUATION FINALE --- DIAGNOSTIC DE SORTIE}{Durée : 45 minutes}{%s}{%s}{%s --- %s}"
               % (st["name"], lv["label"], lv["subject"], "à traiter individuellement"))
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{22mm} X >{\bfseries}p{16mm} X}")
    out.append(r"\toprule Nom et prénom & \rule{62mm}{0.32pt} & Date & \rule{34mm}{0.32pt} \\ \bottomrule")
    out.append(r"\end{tabularx}")
    out.append(common.EXAM_INSTRUCTIONS_TEX)

    for part in common.EXAM_PARTS:
        part_items = [i for i in items if i["part"] == part["part"]]
        out.append(r"\newpage" if part["part"] == "A" else r"\needspace{68mm}\par\vspace{3mm}")
        out.append(r"\phasehead{Partie %s --- %s}{environ %d min}{%s}"
                   % (part["part"], escape(part["titre"]), part["minutes"],
                      _part_hint(part["part"])))
        out.append(r"\begin{enumerate}")
        for it in part_items:
            out.append(r"\needspace{22mm}")
            out.append(r"\item[\textbf{%s.}] %s" % (it["ref"], it["tex"]))
            sp = it["space"]
            if part["part"] == "A" and (sp == "short" or not sp):
                sp = "lines:2"
            out.append(space_tex(sp))
            out.append(r"\par\vspace{1.2mm}")
        out.append(r"\end{enumerate}")
        if part["part"] == "A":
            out.append(r"\certbox{Certitude sur l'ensemble de la partie A :}")
        elif part["part"] == "B":
            out.append(r"\certbox{Certitude sur la question B2 :}")
        else:
            out.append(r"\certbox{Certitude sur la question C1 :}")
            out.append(r"\brouillon{\dimexpr\textheight/3\relax}")

    out.append(r"\newpage")
    out.append(r"\sectiontitle{Après l'évaluation --- à remplir en deux minutes}")
    out.append(r"\begin{methodbox}Ces trois lignes ne sont pas notées. Elles servent à construire le plan des quatre premières semaines de la rentrée.\end{methodbox}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{62mm} X}")
    out.append(r"\toprule")
    out.append(r"La question que j'ai trouvée la plus sûre & \rule{85mm}{0.32pt} \\")
    out.append(r"La question sur laquelle j'ai le plus hésité & \rule{85mm}{0.32pt} \\")
    out.append(r"Une notion que je veux revoir dès la première semaine & \rule{85mm}{0.32pt} \\")
    out.append(r"\bottomrule\end{tabularx}")
    out.append(r"\vfill")
    out.append(r"\begin{graybox}\small Ce document est un diagnostic de sortie. Il sera analysé compétence par compétence, "
               r"puis comparé au positionnement passé en début de stage lorsque cette comparaison est légitime.\end{graybox}")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def _part_hint(p):
    return {
        "A": "Questions courtes. Écrire le résultat, sans rédaction longue.",
        "B": "Écrire la relation, la propriété ou la règle avant le calcul, puis contrôler.",
        "C": "Reconnaître la notion utile, mobiliser plusieurs acquis, conclure par une phrase.",
    }[p]


# ------------------------------------------------------------ dossier enseignant
def render_enseignant(st):
    lv = core.level_of(st)
    ph = core.phases(st)
    items = core.exam_items(st)
    tot = core.exam_totals(items)
    rows = core.skill_table(st)
    out = [preamble("Dossier enseignant — confidentiel",
                    "S5 — %s — usage enseignant" % st["name"])]
    out.append(r"\nexuscover{SÉANCE 5 --- DOSSIER ENSEIGNANT}{Profil, déroulé, corrigés et barème}{%s}{%s}{%s --- %s}"
               % (st["name"], lv["label"], lv["subject"], st["parcours"]))
    cr = lv["curriculum_reference"]
    prog = cr["programme_applique_a_l_eleve"]
    ref = " ".join(x for x in (prog.get("BO"), prog.get("NOR")) if x)
    out.append(r"\begin{methodbox}\small\textbf{Programme de référence.} %s%s. "
               r"Transition visée : %s.%s\end{methodbox}"
               % (escape(prog["texte"]), (" --- " + escape(ref)) if ref else "",
                  escape(cr["transition"]),
                  (r" \textbf{Attention :} " + escape(prog["remarque"]))
                  if prog.get("remarque") else ""))
    out.append(r"\begin{keybox}\textbf{DOCUMENT CONFIDENTIEL --- USAGE ENSEIGNANT.} Contient les corrigés, le barème "
               r"et des données nominatives. Ne pas remettre à l'élève ni le laisser visible pendant la séance.\end{keybox}")

    # ---- 1. profil
    out.append(r"\sectiontitle{1. Profil synthétique}")
    b = st["baseline"]
    out.append(r"\begin{methodbox}")
    out.append(r"\textbf{Diagnostic initial.} %s. %s%s" % (
        escape(b["items"]), escape(b["summary"]),
        "" if not b["calibration"] else r" Calibration réussite-confiance : \textbf{%s}." % escape(b["calibration"])))
    if b["date"]:
        out.append(r"\par Date du bilan : %s." % b["date"])
    out.append(r"\end{methodbox}")
    out.append(r"\subsectiontitle{Points d'appui documentés}")
    out.append(r"\begin{itemize}" + "".join(r"\item %s" % escape(x) for x in b["appuis"]) + r"\end{itemize}")
    out.append(r"\subsectiontitle{Difficultés documentées}")
    out.append(r"\begin{itemize}" + "".join(r"\item %s" % escape(x) for x in b["priorites"]) + r"\end{itemize}")
    if b["observations"]:
        out.append(r"\subsectiontitle{Lecture détaillée du diagnostic}")
        out.append(r"\rowcolors{2}{SoftGray}{white}")
        out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{32mm} p{28mm} X}")
        out.append(r"\rowcolor{Navy}\color{white}Domaine & \color{white}Statut initial & \color{white}Observation issue du bilan \\")
        for d, s, o in b["observations"]:
            out.append(r"%s & %s & %s \\" % (escape(d), escape(s), escape(o)))
        out.append(r"\end{tabularx}")
    out.append(r"\begin{warningbox}\textbf{Limite de la reconstruction.} Les tableaux d'observation séance par séance du "
               r"dossier individuel sont vierges : il n'existe aucune preuve documentée entre le diagnostic initial et "
               r"aujourd'hui. Tout statut porté ci-dessous décrit un \emph{état de départ}, jamais une acquisition constatée."
               r"\end{warningbox}")

    # ---- 2. compétences
    out.append(r"\newpage\sectiontitle{2. Matrice de trajectoire --- état avant la séance 5}")
    out.append(r"\rowcolors{2}{SoftBlue}{white}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\ttfamily\scriptsize}p{27mm} X >{\scriptsize}p{16mm} >{\scriptsize}p{20mm} >{\scriptsize\centering\arraybackslash}p{9mm}}")
    out.append(r"\rowcolor{Navy}\color{white}\scriptsize skill\_id & \color{white}Compétence & \color{white}Travaillée en & \color{white}Statut avant S5 & \color{white}Prio. \\")
    for r in rows:
        star = r"$\bullet$ " if r["cible_s5"] else ""
        out.append(r"%s & %s%s & %s & %s & %s \\" % (
            r["skill_id"].replace("_", r"\_"), star, escape(r["label"]),
            ", ".join(r["sessions_travaillees"]) or "---",
            STATUT_FR[r["statut_avant_s5"]], r["priorite_provisoire"]))
    out.append(r"\end{tabularx}")
    out.append(r"\par\vspace{1mm}\small\textbf{Lecture de la colonne « Statut avant S5 » :} elle décrit "
               r"l'état constaté au \emph{positionnement initial}, jamais une acquisition constatée depuis. "
               r"« acquis » signifie « acquis au positionnement initial » ; « en voie » signifie « en voie "
               r"d'acquisition ».")
    out.append(r"\par\small$\bullet$ compétence ciblée par les phases 2 et 3 de la séance. "
               r"La colonne « Prio. » est \emph{provisoire} : la priorité définitive est produite par "
               r"\code{tools/analyze_s5.py} après la correction.")
    remed = [r for r in rows if core.retention_context(st, r["skill_id"])["recommended_delayed_check"]]
    if remed:
        out.append(r"\begin{warningbox}\textbf{Effet de récence.} Les compétences suivantes sont "
                   r"retravaillées pendant cette séance, puis évaluées moins d'une heure plus tard : "
                   + ", ".join(r"\code{%s}" % r["skill_id"] for r in remed) + r". "
                   r"Une réussite y mesure une \emph{performance immédiate}, pas une consolidation "
                   r"durable. Le plan de rentrée prévoit pour elles un contrôle différé en semaine 1 "
                   r"ou 2 ; aucun bilan ne doit écrire « acquis durablement » sur cette seule preuve."
                   r"\end{warningbox}")

    # ---- 3. justification
    out.append(r"\sectiontitle{3. Pourquoi ces activités, pour cet élève}")
    m1, m2 = ph[1]["module"], ph[2]["module"]
    out.append(r"\begin{goalbox}\textbf{Objectif de la séance :} %s\end{goalbox}" % escape(st["objectif"]))
    out.append(r"\subsectiontitle{Axe prioritaire (phase 2, %d min) --- %s}" % (ph[1]["minutes"], escape(m1["titre"])))
    out.append(escape(m1["pourquoi"]))
    out.append(r"\par\vspace{1mm}\textbf{Compétence visée :} \code{%s}." % ph[1]["skill"])
    out.append(r"\subsectiontitle{Second axe (phase 3, %d min) --- %s}" % (ph[2]["minutes"], escape(m2["titre"])))
    out.append(escape(m2["pourquoi"]))
    out.append(r"\par\vspace{1mm}\textbf{Compétence visée :} \code{%s}." % ph[2]["skill"])
    out.append(r"\subsectiontitle{Équilibre commun / individuel}")
    commun = sum(p["minutes_objectifs_communs"] for p in ph)
    indiv = sum(p["minutes_individualisees"] for p in ph)
    out.append(r"Sur les 75 minutes : \textbf{%d min} (%d\,\%%) relèvent des objectifs communs du niveau et "
               r"\textbf{%d min} (%d\,\%%) ciblent le profil individuel. Sur l'évaluation : \textbf{%g points} "
               r"de noyau commun (%s\,\%%) et \textbf{%g points} individualisés (%s\,\%%)."
               % (commun, round(100 * commun / 75), indiv, round(100 * indiv / 75),
                  tot["points_commun"], tot["part_commun_pct"], tot["points_individuel"], tot["part_individuel_pct"]))

    # ---- 4. déroulé
    out.append(r"\newpage\sectiontitle{4. Déroulé minute par minute}")
    out.append(r"\rowcolors{2}{SoftGray}{white}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{18mm} p{34mm} X X}")
    out.append(r"\rowcolor{Navy}\color{white}Temps & \color{white}Phase & \color{white}Conduite & \color{white}Indicateur observable \\")
    conduites = {
        1: ("Individuel, sans carte de rappel pendant 7 minutes, puis 3 minutes de mise en commun.",
            "Au moins 4 réponses exactes sur 5 ; la certitude est renseignée avant toute vérification."),
        2: ("Rappel bref, exemple guidé au tableau, puis exercices en autonomie. Aide donnée seulement après une tentative écrite.",
            "Trois réussites consécutives sans aide sur la compétence visée."),
        3: ("Pas d'exemple guidé : l'élève démarre seul. Intervention uniquement sur demande.",
            "Deux réussites autonomes ; le contrôle est écrit sans qu'on le demande."),
        4: ("Travail écrit, correction collective courte à la fin. Ne pas transformer ce temps en cours magistral.",
            "L'élève relie explicitement un acquis de l'année écoulée à un attendu de l'année à venir."),
        5: ("Lecture des cinq règles, puis remise de l'évaluation. Aucune information sur son contenu.",
            "Les deux engagements sont écrits."),
    }
    for p in ph:
        c, i = conduites[p["n"]]
        out.append(r"%d--%d min & %s & %s & %s \\" % (p["debut"], p["fin"], escape(p["objectif"][:60]), c, i))
    out.append(r"%d--%d min & Évaluation finale & Individuel, sans document. Partie A environ 10 min, B environ 20 min, C environ 15 min. & Somme des durées cibles : %d min, marge de %d min. \\"
               % (common.WORK_MINUTES, common.WORK_MINUTES + common.EXAM_MINUTES,
                  tot["minutes"], common.EXAM_MINUTES - tot["minutes"]))
    out.append(r"\end{tabularx}")

    # ---- 5. corrigé du travail
    out.append(r"\newpage\sectiontitle{5. Corrigé du livret de travail}")
    out.append(r"\subsectiontitle{Phase 1 --- réactivation}")
    out.append(r"\begin{enumerate}")
    for it in lv["phase1"]["items"]:
        out.append(r"\item \code{%s} --- %s" % (it["skill"], it["corrige"]))
    out.append(r"\end{enumerate}")
    for p in (ph[1], ph[2]):
        out.append(r"\subsectiontitle{Phase %d --- %s}" % (p["n"], escape(p["module"]["titre"])))
        out.append(r"\begin{enumerate}")
        for ex in p["exos"]:
            out.append(r"\item %s" % ex["corrige"])
        out.append(r"\end{enumerate}")
        out.append(r"\minititle{Erreurs probables}")
        out.append(r"\begin{itemize}")
        for e in p["module"]["erreurs"]:
            out.append(r"\item \textsc{%s} --- %s" % (e["code"], e["desc"]))
        out.append(r"\end{itemize}")
    out.append(r"\subsectiontitle{Phase 4 --- pont vers %s}" % lv["year_next"])
    out.append(lv["phase4"]["corrige"])

    # ---- 6. corrigé de l'évaluation
    out.append(r"\newpage\sectiontitle{6. Corrigé de l'évaluation et barème analytique}")
    out.append(r"\begin{keybox}\textbf{Total : %g points sur %d.} Noyau commun %g pts (%s\,\%%), "
               r"items individualisés %g pts (%s\,\%%). Somme des durées cibles : %d minutes."
               r"\end{keybox}" % (tot["points"], common.EXAM_TOTAL_POINTS, tot["points_commun"],
                                  tot["part_commun_pct"], tot["points_individuel"],
                                  tot["part_individuel_pct"], tot["minutes"]))
    for it in items:
        out.append(r"\itemhead{%s --- \code{%s} --- %s}{%g}{%g}"
                   % (it["ref"], it["skill"], "noyau commun" if it["kind"] == "commun" else "item individualisé",
                      it["points"], it["minutes"]))
        out.append(r"\begin{graybox}\small\textbf{Réponse attendue :} %s\end{graybox}" % it["answer"])
        out.append(r"\minititle{Étapes significatives}")
        out.append(r"\begin{enumerate}" + "".join(r"\item %s" % s for s in it["steps"]) + r"\end{enumerate}")
        out.append(r"\minititle{Barème par critère --- la saisie se fait critère par critère}")
        out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\ttfamily\scriptsize}p{9mm} >{\bfseries}p{9mm} >{\ttfamily\scriptsize}p{24mm} >{\scriptsize}p{18mm} X}")
        out.append(r"\toprule \scriptsize critère & Pts & \scriptsize compétence & \scriptsize preuve & Ce qui est exigé \\ \midrule")
        for c in it["criteria"]:
            out.append(r"%s & %g & %s & %s & %s \\" % (
                c["criterion_id"].rsplit("_", 1)[1], c["points"],
                c["skill_id"].replace("_", r"\_"), c["evidence_type"], c["desc"]))
        out.append(r"\bottomrule\end{tabularx}")
        if it.get("methodes_alternatives_acceptees"):
            out.append(r"\begin{successbox}\small\textbf{Méthodes différentes acceptées, sans perte de points :} "
                       + " ".join(escape(m) for m in it["methodes_alternatives_acceptees"]) + r"\end{successbox}")
        out.append(r"\minititle{Erreurs probables et codes}")
        out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\ttfamily\small}p{26mm} X}")
        out.append(r"\toprule Code & Description \\ \midrule")
        for e in it["errors"]:
            out.append(r"%s & %s \\" % (e["code"], e["desc"]))
        out.append(r"\bottomrule\end{tabularx}")
        out.append(r"\par\vspace{1mm}\small\textbf{Rôle pour la rentrée :} %s" % escape(it["role_rentree"]))
        out.append(r"\par\vspace{2mm}")

    # ---- 7. correspondance
    out.append(r"\newpage\sectiontitle{7. Correspondance diagnostic initial $\leftrightarrow$ évaluation finale}")
    out.append(r"\rowcolors{2}{SoftBlue}{white}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{9mm} >{\ttfamily\scriptsize}p{25mm} >{\ttfamily\scriptsize}p{22mm} >{\ttfamily\scriptsize}p{16mm} X}")
    out.append(r"\rowcolor{Navy}\color{white}Item & \color{white}\scriptsize skill\_id & \color{white}\scriptsize baseline & \color{white}\scriptsize comparaison & \color{white}Lecture \\")
    comp_label = {
        "indicative_skill_comparison": "confrontation indicative seulement : un énoncé parallèle existe au positionnement initial, mais la réponse de l'élève à cet énoncé n'a pas été conservée",
        "post_only": "état final seul : aucune question du positionnement initial ne porte sur cette compétence",
        "not_comparable": "non comparable : contenu introduit pendant la séance 5 elle-même",
        "parallel_measures": "deux mesures nominatives appariées disponibles : un écart chiffré serait légitime",
    }
    for it in items:
        bl = it["baseline_item"]
        if not bl and it["baseline_skill_refs"]:
            bl = "+".join(r["baseline_items"][0] for r in it["baseline_skill_refs"][:2]) + "..."
        out.append(r"%s & %s & %s & %s & %s \\" % (
            it["ref"], it["skill"].replace("_", r"\_"),
            (bl or "---").replace("_", r"\_"),
            it["comparison_status"].replace("_", r"\_"),
            comp_label[it["comparison_status"]]))
    out.append(r"\end{tabularx}")
    out.append(r"\begin{keybox}\textbf{Aucun écart chiffré ne sera calculé.} Les réponses de l'élève aux "
               r"18 questions du positionnement initial n'ont pas été conservées : le dossier n'en garde qu'un "
               r"statut par domaine. Un statut qualitatif n'est pas une mesure : le convertir en score pour en "
               r"soustraire un autre produirait un chiffre sans valeur. Le script d'analyse impose donc "
               r"\code{mastery_delta = null} pour toutes les compétences, et se limite à une confrontation "
               r"\emph{indicative} entre le statut initial et l'état final.\end{keybox}")

    # ---- 8. interprétation
    out.append(r"\sectiontitle{8. Clés d'interprétation après correction}")
    out.append(r"\subsectiontitle{Échelle de maîtrise par compétence}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{10mm} X}")
    out.append(r"\toprule Niveau & Signification \\ \midrule")
    for k in sorted(common.MASTERY_SCALE):
        out.append(r"%s & %s \\" % (k, common.MASTERY_SCALE[k]))
    out.append(r"\bottomrule\end{tabularx}")
    out.append(r"\subsectiontitle{Croiser réussite et certitude}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{40mm} X}")
    out.append(r"\toprule Situation & Conduite à tenir \\ \midrule")
    out.append(r"Juste, certitude 3--4 & acquis disponible : faire transférer sur une situation nouvelle. \\")
    out.append(r"Juste, certitude 1--2 & presque acquis : faire expliciter la procédure, puis réutiliser. \\")
    out.append(r"Faux, certitude 1--2 & notion à installer ou procédure à reprendre pas à pas. \\")
    out.append(r"Faux, certitude 3--4 & priorité absolue : confronter la conviction avant toute reprise technique. \\")
    out.append(r"\bottomrule\end{tabularx}")
    out.append(r"\subsectiontitle{Distinguer les niveaux d'erreur}")
    out.append(r"Une erreur de \textsc{CALCUL} isolée, non reproduite sur les items voisins de même compétence, "
               r"ne vaut pas non-maîtrise conceptuelle. La chaîne à reconstituer est : "
               r"\textbf{connaissance} $\rightarrow$ \textbf{choix de méthode} $\rightarrow$ \textbf{exécution} "
               r"$\rightarrow$ \textbf{justification} $\rightarrow$ \textbf{contrôle}. Les codes d'erreur du barème "
               r"situent l'écart sur cette chaîne.")

    # ---- 9. observation
    out.append(r"\sectiontitle{9. Points d'observation propres à cet élève}")
    out.append(r"\begin{itemize}" + "".join(r"\item %s" % escape(w) for w in st["watch"]) + r"\end{itemize}")
    out.append(r"\subsectiontitle{Grille de saisie de la séance}")
    out.append(r"\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{26mm} X X X}")
    out.append(r"\toprule Phase & Aide maximale utilisée & Réussite autonome & Observation \\ \midrule")
    for p in ph[:4]:
        out.append(r"Phase %d & & & \\[6mm]" % p["n"])
    out.append(r"\bottomrule\end{tabularx}")

    out.append(r"\begin{warningbox}\textbf{Avant d'écrire quoi que ce soit sur les acquis de cet élève :} tant que "
               r"l'évaluation n'est pas corrigée et analysée par \code{tools/analyze_s5.py}, aucune formulation du type "
               r"« maîtrise désormais », « forte progression » ou « objectif atteint » ne doit être employée. "
               r"Les formulations admises sont : « à vérifier lors de l'évaluation finale », « observé en séance, à confirmer », "
               r"« hypothèse de consolidation ».\end{warningbox}")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------ JSON
def build_profile(st):
    lv = core.level_of(st)
    items = core.exam_items(st)
    tot = core.exam_totals(items)
    ph = core.phases(st)
    return {
        "schema": SCHEMA_PREFIX + "-learning-profile-v1",
        "generated_on": GENERATED_ON,
        "student": {
            "id": st["id"], "name": st["name"],
            "level": lv["label"], "level_key": lv["key"], "subject": lv["subject"],
            "year_prev": lv["year_prev"], "year_next": lv["year_next"],
            "parcours": st["parcours"],
        },
        "sources": [{"path": p, "exists": core.source_exists(p)} for p in core.student_sources(st)],
        "baseline": {
            "available": st["baseline"]["available"],
            "instrument": lv["baseline_instrument"],
            "date": st["baseline"]["date"],
            "items_traites": st["baseline"]["items"],
            "confidence_scale": common.CONFIDENCE_SCALE,
            "confidence_calibration": st["baseline"]["calibration"],
            "summary": st["baseline"]["summary"],
            "strengths": st["baseline"]["appuis"],
            "priorities": st["baseline"]["priorites"],
            "domain_observations": [{"domain": d, "status": s, "observation": o}
                                    for d, s, o in st["baseline"]["observations"]],
            "item_level_results_available": False,
            "item_level_results_note": "Les dossiers restituent des statuts par domaine, non les réponses aux 18 items. La comparaison initial/final est conduite au niveau de la compétence.",
            "skills": [dict(row, retention=core.retention_context(st, row["skill_id"]))
                       for row in core.skill_table(st)],
            "mesure_initiale_nominative_disponible": False,
            "mesure_initiale_note": ("les réponses item par item du diagnostic initial ne sont "
                                     "pas conservées : aucun score initial nominatif n'existe. "
                                     "Aucun delta de maîtrise ne peut donc être calculé."),
        },
        "trajectory": {
            "S1": {"theme": lv["sessions"]["S1"], "documented_evidence": None},
            "S2": {"theme": lv["sessions"]["S2"], "documented_evidence": None},
            "S3": {"theme": lv["sessions"]["S3"], "documented_evidence": None},
            "S4": {"theme": lv["sessions"]["S4"], "documented_evidence": None},
            "note": "Aucune observation de séance n'a été saisie dans le dossier individuel : « travaillé » ne vaut pas « acquis ».",
        },
        "session5": {
            "work_minutes": common.WORK_MINUTES,
            "exam_minutes": common.EXAM_MINUTES,
            "objective": st["objectif"],
            "priority_skills": [st["p1"], st["p2"]],
            "activities": [
                {"phase": p["n"], "title": p["objectif"], "minutes": p["minutes"],
                 "start": p["debut"], "end": p["fin"], "type": p["type"],
                 "skill": p.get("skill"),
                 "minutes_common_objectives": p["minutes_objectifs_communs"],
                 "minutes_individualised": p["minutes_individualisees"]}
                for p in ph
            ],
            "differentiation": {
                "work_common_minutes": sum(p["minutes_objectifs_communs"] for p in ph),
                "work_individual_minutes": sum(p["minutes_individualisees"] for p in ph),
                "work_common_pct": round(100.0 * sum(p["minutes_objectifs_communs"] for p in ph) / common.WORK_MINUTES, 1),
            },
        },
        "assessment": {
            "duration_minutes": common.EXAM_MINUTES,
            "target_minutes": tot["minutes"],
            "total_points": tot["points"],
            "common_points": tot["points_commun"],
            "individual_points": tot["points_individuel"],
            "common_share_pct": tot["part_commun_pct"],
            "items": [{"item_id": i["item_id"], "ref": i["ref"], "part": i["part"],
                       "kind": i["kind"], "skill_id": i["skill"],
                       "skills": core.item_skills(i),
                       "skills_extra": i.get("skills_extra", []),
                       "points": i["points"],
                       "estimated_minutes": i["minutes"],
                       "time_estimate": i["time_estimate"],
                       "criteria": [{"criterion_id": c["criterion_id"], "points": c["points"],
                                     "skill_id": c["skill_id"],
                                     "evidence_type": c["evidence_type"],
                                     "subpart": c["subpart"]} for c in i["criteria"]],
                       "task": i["task"], "difficulty": i["difficulty"],
                       "baseline_item_id": i["baseline_item"],
                       "baseline_skill_refs": i["baseline_skill_refs"],
                       "comparability": i["comparability"],
                       "comparison_status": i["comparison_status"],
                       "confidence_probe": bool(i.get("confidence"))}
                      for i in items],
        },
        "post_stage": {"status": "awaiting_assessment",
                       "note": "Aucun résultat final n'est renseigné avant la passation."},
    }


def build_blueprint(st):
    lv = core.level_of(st)
    items = core.exam_items(st)
    tot = core.exam_totals(items)
    by_skill = core.points_per_skill(st, items)
    return {
        "schema": SCHEMA_PREFIX + "-evaluation-blueprint-v1",
        "generated_on": GENERATED_ON,
        "student_id": st["id"], "level_key": lv["key"], "subject": lv["subject"],
        "duration_minutes": common.EXAM_MINUTES,
        "estimated_minutes": tot["minutes"],
        "estimation_model": "data/timing.py — lecture, traitement, rédaction, par niveau",
        "margin_minutes": round(common.EXAM_MINUTES - tot["minutes"], 2),
        "total_points": tot["points"],
        "scale": "note sur 20 + maîtrise par compétence de 0 à 4",
        "design_rules": {
            "common_core_pct_target": "70 % environ",
            "individual_pct_target": "30 % environ",
            "common_core_pct_actual": tot["part_commun_pct"],
            "individual_pct_actual": tot["part_individuel_pct"],
            "equity_note": "Le noyau commun est strictement identique pour tous les élèves du même niveau, ce qui rend les copies comparables.",
        },
        "parts": [
            {"part": p["part"], "title": p["titre"], "minutes_budget": p["minutes"],
             "points": sum(i["points"] for i in items if i["part"] == p["part"]),
             "estimated_minutes": round(sum(i["minutes"] for i in items if i["part"] == p["part"]), 2),
             "items": [i["ref"] for i in items if i["part"] == p["part"]]}
            for p in common.EXAM_PARTS
        ],
        "points_per_skill": by_skill,
        "max_share_one_skill_pct": round(100.0 * max(by_skill.values()) / tot["points"], 1),
        "points_per_skill_note": "les points d'un item mobilisant plusieurs compétences sont répartis à parts égales entre elles",
        "comparability_summary": {
            c: len([i for i in items if i["comparability"] == c]) for c in common.COMPARABILITY
        },
        "comparison_status_summary": {
            c: len([i for i in items if i["comparison_status"] == c])
            for c in ("item_level", "skill_level", "not_comparable")
        },
        "confidence_probes": [i["ref"] for i in items if i.get("confidence")],
        "error_codes": common.ERROR_CODES,
        "mastery_scale": common.MASTERY_SCALE,
    }


def build_manifest(st):
    lv = core.level_of(st)
    items = core.exam_items(st)
    return {
        "schema": SCHEMA_PREFIX + "-evaluation-manifest-v1",
        "generated_on": GENERATED_ON,
        "confidential": True,
        "student_id": st["id"], "level_key": lv["key"], "subject": lv["subject"],
        "items": [{
            "item_id": i["item_id"], "ref": i["ref"], "part": i["part"], "kind": i["kind"],
            "skill_id": i["skill"], "skills_extra": i.get("skills_extra", []),
            "skill_label": lv["skills"][i["skill"]]["label"],
            "objective": lv["skills"][i["skill"]]["label"],
            "prerequisites": lv["skills"][i["skill"]]["sessions"],
            "task_type": i["task"], "difficulty": i["difficulty"],
            "statement": i["tex"],
            "target_minutes": i["minutes"],
            "time_estimate": i["time_estimate"],
            "points": i["points"],
            "expected_answer": i["answer"],
            "significant_steps": i["steps"],
            "likely_errors": i["errors"],
            "error_codes": sorted({e["code"] for e in i["errors"]}),
            "grading_criteria": i["criteria"],
            "criteria_total_points": round(sum(c["points"] for c in i["criteria"]), 4),
            "evidence_types": sorted({c["evidence_type"] for c in i["criteria"]}),
            "methodes_alternatives_acceptees": i.get("methodes_alternatives_acceptees", []),
            "retention": {sid: core.retention_context(st, sid) for sid in core.item_skills(i)},
            "baseline_item_id": i["baseline_item"],
            "baseline_item_text": lv["baseline_items"].get(i["baseline_item"]) if i["baseline_item"] else None,
            "baseline_skill_refs": i["baseline_skill_refs"],
            "comparability": i["comparability"],
            "comparison_status": i["comparison_status"],
            "linked_sessions": lv["skills"][i["skill"]]["sessions"],
            "role_for_september": i["role_rentree"],
            "confidence_probe": bool(i.get("confidence")),
        } for i in items],
    }


def build_answer_key(st):
    items = core.exam_items(st)
    return {
        "schema": SCHEMA_PREFIX + "-answer-key-v1",
        "generated_on": GENERATED_ON,
        "confidential": True,
        "student_id": st["id"],
        "total_points": core.exam_totals(items)["points"],
        "answers": [{
            "item_id": i["item_id"], "ref": i["ref"], "skill_id": i["skill"],
            "skills": core.item_skills(i),
            "points": i["points"],
            "expected_answer": i["answer"],
            "steps": i["steps"],
            "methodes_alternatives_acceptees": i.get("methodes_alternatives_acceptees", []),
            "criteria": i["criteria"],
        } for i in items],
    }


def build_responses_template(st):
    items = core.exam_items(st)
    return {
        "schema": SCHEMA_PREFIX + "-responses-v1",
        "generated_on": GENERATED_ON,
        "student_id": st["id"],
        "status": "awaiting_assessment",
        "assessed_on": None,
        "instructions": {
            "saisie": "la saisie se fait CRITERE PAR CRITERE, jamais au niveau de l'item : "
                      "chaque critère porte une compétence, et c'est de là que viennent les "
                      "scores par compétence.",
            "criteria[].score": "points attribués à ce critère, entre 0 et criteria[].max_points ; "
                                "un crédit partiel est admis lorsque le critère le permet",
            "confidence": "1 à 4, uniquement pour les items marqués confidence_probe ; null sinon",
            "error_codes": "liste de codes issus de evaluation_blueprint.json ; liste vide si aucune erreur",
            "observation": "note libre facultative de l'enseignant",
        },
        "responses": [{
            "item_id": i["item_id"], "ref": i["ref"], "skill_id": i["skill"],
            "skills": core.item_skills(i),
            "max_points": i["points"],
            "criteria": [{"criterion_id": c["criterion_id"], "skill_id": c["skill_id"],
                          "evidence_type": c["evidence_type"], "subpart": c["subpart"],
                          "max_points": c["points"], "score": None,
                          "desc": c["desc"]} for c in i["criteria"]],
            "confidence": None,
            "confidence_probe": bool(i.get("confidence")),
            "error_codes": [],
            "observation": None,
        } for i in items],
        "session_observations": {
            "phase_1": {"aide_max": None, "reussite_autonome": None, "note": None},
            "phase_2": {"aide_max": None, "reussite_autonome": None, "note": None},
            "phase_3": {"aide_max": None, "reussite_autonome": None, "note": None},
            "phase_4": {"aide_max": None, "reussite_autonome": None, "note": None},
        },
    }


def build_post_schema(st):
    """Schéma canonique v2 de la sortie de tools/analyze_s5.py.

    Il décrit la sortie réellement produite, et il est vérifié par jsonschema dans
    les tests : aucune livraison ne peut passer si la sortie ne s'y conforme pas.
    """
    criterion = {
        "type": "object",
        "required": ["criterion_id", "skill_id", "evidence_type", "points", "max_points"],
        "properties": {
            "criterion_id": {"type": "string"},
            "item_ref": {"type": "string"},
            "item_id": {"type": "string"},
            "skill_id": {"type": "string"},
            "evidence_type": {"enum": list(criteria_map.EVIDENCE_TYPES)},
            "subpart": {"type": "string"},
            "points": {"type": "number", "minimum": 0},
            "max_points": {"type": "number", "exclusiveMinimum": 0},
            "difficulty": {"type": "string"},
            "part": {"type": "string"},
            "kind": {"enum": ["commun", "individuel"]},
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "%s-post-stage-analysis-v2" % SCHEMA_PREFIX,
        "title": "Diagnostic de sortie — sortie de tools/analyze_s5.py",
        "type": "object",
        "required": ["schema", "student_id", "level_key", "status", "scoring_model",
                     "baseline_measure_available", "score", "items", "criteria",
                     "skills", "confidence", "errors", "priorities", "warnings"],
        "properties": {
            "schema": {"const": SCHEMA_PREFIX + "-post-stage-analysis-v2"},
            "student_id": {"type": "string"},
            "student_name": {"type": "string"},
            "level_key": {"type": "string"},
            "subject": {"type": "string"},
            "analysed_on": {"type": ["string", "null"]},
            "status": {"enum": ["awaiting_assessment", "analysed"]},
            "scoring_model": {"type": "string",
                              "description": "les scores par compétence proviennent des critères, "
                                             "jamais d'une répartition uniforme"},
            "baseline_measure_available": {
                "type": "boolean",
                "description": "faux tant que les réponses item par item du diagnostic initial "
                               "ne sont pas conservées"},
            "score": {
                "type": "object",
                "required": ["total_points", "max_points", "note_sur_20", "success_rate",
                             "by_part", "common_core_points", "individual_points"],
                "properties": {
                    "total_points": {"type": "number", "minimum": 0},
                    "max_points": {"type": "number", "exclusiveMinimum": 0},
                    "note_sur_20": {"type": "number", "minimum": 0, "maximum": 20},
                    "success_rate": {"type": "number", "minimum": 0, "maximum": 1},
                    "by_part": {"type": "object"},
                    "common_core_points": {"type": "number"},
                    "individual_points": {"type": "number"},
                },
            },
            "items": {
                "type": "array", "minItems": 12, "maxItems": 12,
                "items": {
                    "type": "object",
                    "required": ["item_id", "ref", "part", "kind", "skill_id", "skills",
                                 "points", "max_points", "criteria", "comparison_status"],
                    "properties": {
                        "item_id": {"type": "string"},
                        "ref": {"type": "string"},
                        "part": {"enum": ["A", "B", "C"]},
                        "kind": {"enum": ["commun", "individuel"]},
                        "skill_id": {"type": "string"},
                        "skills": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                        "difficulty": {"enum": ["socle", "standard", "transfert"]},
                        "task_type": {"type": "string"},
                        "points": {"type": "number", "minimum": 0},
                        "max_points": {"type": "number", "exclusiveMinimum": 0},
                        "success_rate": {"type": ["number", "null"]},
                        "criteria": {"type": "array", "minItems": 1, "items": criterion},
                        "error_codes": {"type": "array", "items": {"type": "string"}},
                        "confidence": {"type": ["integer", "null"], "minimum": 1, "maximum": 4},
                        "comparison_status": {"enum": list(core.COMPARISON_VALUES)},
                    },
                },
            },
            "criteria": {"type": "array", "minItems": 1, "items": criterion},
            "skills": {
                "type": "array", "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["skill_id", "label", "importance_n", "points", "max_points",
                                 "success_rate", "baseline_status_qualitative",
                                 "baseline_mastery", "baseline_measure_available",
                                 "post_mastery", "mastery_delta", "delta_blocked_reason",
                                 "comparison_status", "evidence_strength",
                                 "post_test_context", "retention_status",
                                 "recommended_delayed_check"],
                    "properties": {
                        "skill_id": {"type": "string"},
                        "label": {"type": "string"},
                        "domain": {"type": "string"},
                        "importance_n": {"enum": ["critique", "importante", "utile"]},
                        "items": {"type": "array", "items": {"type": "string"}},
                        "criteria": {"type": "array", "items": {"type": "string"}},
                        "evidence_types": {"type": "array",
                                           "items": {"enum": list(criteria_map.EVIDENCE_TYPES)}},
                        "points": {"type": "number", "minimum": 0},
                        "max_points": {"type": "number", "exclusiveMinimum": 0},
                        "success_rate": {"type": "number", "minimum": 0, "maximum": 1},
                        "baseline_status_qualitative": {"enum": common.PRE_STATUS},
                        "baseline_mastery": {
                            "type": "null",
                            "description": "toujours null : un statut qualitatif de domaine n'est "
                                           "pas une mesure et ne peut pas être converti en score"},
                        "baseline_measure_available": {"const": False},
                        "post_mastery": {"type": "integer", "minimum": 0, "maximum": 4},
                        "post_mastery_capped_by_transfer": {"type": "boolean"},
                        "mastery_delta": {
                            "type": "null",
                            "description": "toujours null tant qu'aucune mesure initiale "
                                           "nominative appariée n'existe"},
                        "delta_blocked_reason": {"type": "string"},
                        "comparison_status": {"enum": list(core.COMPARISON_VALUES)},
                        "evidence_strength": {"enum": ["faible", "moyenne", "forte"]},
                        "evidence_strength_score": {"type": "integer"},
                        "evidence_strength_detail": {"type": "array"},
                        "post_test_context": {"enum": ["immediate_after_remediation",
                                                       "first_worked_in_session_5",
                                                       "introduced_in_session_5",
                                                       "no_remediation_in_session"]},
                        "retention_status": {"enum": ["not_yet_verified", "not_measured",
                                                      "verified"]},
                        "recommended_delayed_check": {"type": "boolean"},
                        "retention_reason": {"type": "string"},
                        "errors": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "confidence": {
                "type": "object",
                "required": ["confidence_before", "confidence_after", "calibration_cells"],
                "properties": {
                    "confidence_before_reported": {"type": ["string", "null"]},
                    "confidence_before": {"type": "null"},
                    "confidence_after": {"type": ["number", "null"]},
                    "calibration_cells": {
                        "type": "object",
                        "required": ["juste_confiance_haute", "juste_confiance_basse",
                                     "faux_confiance_basse", "faux_confiance_haute",
                                     "partiel_non_classe"],
                        "additionalProperties": {"type": "integer", "minimum": 0},
                    },
                    "note": {"type": "string"},
                },
            },
            "errors": {
                "type": "object",
                "required": ["error_profile_after", "dominant_codes"],
                "properties": {
                    "error_profile_before": {"type": ["object", "null"]},
                    "error_profile_after": {"type": "object"},
                    "dominant_codes": {"type": "array", "items": {"type": "string"}},
                },
            },
            "priorities": {
                "type": "array", "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["skill_id", "priority_rank", "reason"],
                    "properties": {
                        "skill_id": {"type": "string"},
                        "label": {"type": "string"},
                        "priority_rank": {"enum": ["P1", "P2", "P3", "OK"]},
                        "reason": {"type": "string"},
                        "post_mastery": {"type": "integer"},
                        "success_rate": {"type": "number"},
                        "importance_n": {"type": "string"},
                        "dominant_error_codes": {"type": "array"},
                    },
                },
            },
            "warnings": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        },
    }


def build_action_plan_template(st):
    lv = core.level_of(st)
    return {
        "schema": SCHEMA_PREFIX + "-four-week-plan-v1",
        "generated_on": GENERATED_ON,
        "student_id": st["id"], "level_key": lv["key"], "subject": lv["subject"],
        "status": "awaiting_assessment",
        "source_of_truth": "tools/analyze_s5.py — le plan ne se remplit qu'à partir des priorités calculées",
        "design_rules": [
            "deux ou trois compétences prioritaires par semaine, jamais plus",
            "objectif mesurable, non « revoir ses cours »",
            "durée compatible avec une rentrée scolaire",
            "un critère explicite d'atteinte de l'objectif",
            "un exercice de contrôle identifiable",
        ],
        "weeks": [
            {"week": n, "skills": [], "objective": None, "work_type": None,
             "frequency": None, "duration_minutes": None,
             "success_criterion": None, "control_exercise": None}
            for n in (1, 2, 3, 4)
        ],
        "follow_up_recommendation": {"proposed": None, "justification": None,
                                     "note": "à ne renseigner que si les données calculées le justifient"},
    }


TEACHER_README = """# Dossier enseignant — {name} ({level}, {subject})

**Confidentiel.** Ce répertoire contient les seuls fichiers de la séance S5 qui
révèlent une réponse attendue :

| Fichier | Contenu |
|---|---|
| `S5_ENSEIGNANT_*.tex` / `.pdf` | profil, déroulé minute par minute, corrigés, barème, clés d'interprétation |
| `evaluation_manifest.json` | métadonnées complètes des 12 items, dont la réponse attendue |
| `answer_key.json` | corrigé structuré et critères de correction |

Les documents remis à l'élève se trouvent dans le répertoire parent et ne
contiennent ni corrigé, ni barème, ni code d'erreur.

## Après la passation

1. Saisir les points dans `../responses_TEMPLATE.json` (copie renommée, par exemple
   `responses_2026-08-28.json`).
2. Lancer :

   ```
   python3 S5_cloture/tools/analyze_s5.py --student {sid} --responses <fichier>
   ```

3. Le script produit `post_stage_analysis.json` conforme à
   `../post_stage_analysis_schema.json`. Toute affirmation chiffrée du bilan doit
   provenir de ce fichier.
"""


# ------------------------------------------------------------------------ main
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    n = 0
    for st in core.all_students():
        d = core.student_output_dir(st)
        td = os.path.join(d, "_ENSEIGNANT")
        lv = core.level_of(st)
        write(os.path.join(d, core.doc_basename("TRAVAIL", st) + ".tex"), render_travail(st))
        write(os.path.join(d, core.doc_basename("EVALUATION", st) + ".tex"), render_evaluation(st))
        write(os.path.join(td, core.doc_basename("ENSEIGNANT", st) + ".tex"), render_enseignant(st))
        write_json(os.path.join(d, "student_learning_profile.json"), build_profile(st))
        write_json(os.path.join(d, "evaluation_blueprint.json"), build_blueprint(st))
        write_json(os.path.join(d, "responses_TEMPLATE.json"), build_responses_template(st))
        write_json(os.path.join(d, "post_stage_analysis_schema.json"), build_post_schema(st))
        write_json(os.path.join(d, "four_week_action_plan_TEMPLATE.json"), build_action_plan_template(st))
        write_json(os.path.join(td, "evaluation_manifest.json"), build_manifest(st))
        write_json(os.path.join(td, "answer_key.json"), build_answer_key(st))
        write(os.path.join(td, "README.md"), TEACHER_README.format(
            name=st["name"], level=lv["label"], subject=lv["subject"], sid=st["id"]))
        n += 1
    # blueprints de niveau
    for key in LEVEL_ORDER:
        lv = LEVELS[key]
        write_json(os.path.join(core.S5_ROOT, "_common", "blueprints", "blueprint_%s.json" % key), {
            "schema": SCHEMA_PREFIX + "-level-blueprint-v1",
            "generated_on": GENERATED_ON,
            "level_key": lv["key"], "label": lv["label"], "subject": lv["subject"],
            "year_prev": lv["year_prev"], "year_next": lv["year_next"],
            "curriculum_reference": lv["curriculum_reference"],
            "baseline_instrument": lv["baseline_instrument"],
            "sessions": lv["sessions"],
            "skills": lv["skills"],
            "baseline_items": lv["baseline_items"],
            "critical_prerequisites": lv["critical_prereqs"],
            "bridges_to_year_n": lv["n_bridges"],
            "session5_architecture": {
                "work_minutes": common.WORK_MINUTES,
                "exam_minutes": common.EXAM_MINUTES,
                "phases": [{"n": a, "title": b, "minutes": c,
                            "minutes_common": d, "minutes_individual": e}
                           for a, b, c, d, e in common.PHASE_PLAN],
            },
            "exam_common_core": {
                iid: {"skill_id": it["skill"], "points": it["points"],
                      "task": it["task"], "difficulty": it["difficulty"],
                      "baseline_item_id": it["baseline_item"],
                      "comparability": it["comparability"]}
                for iid, it in lv["eval_common"].items()
            },
            "phase1_items": [{"skill_id": i["skill"], "text": i["tex"]} for i in lv["phase1"]["items"]],
            "phase4": {"title": lv["phase4"]["titre"], "objective": lv["phase4"]["objectif"],
                       "skills_prev": lv["phase4"]["skills_prev"],
                       "skills_next": lv["phase4"]["skills_next"]},
        })
    print("généré : %d dossiers élèves, %d blueprints de niveau" % (n, len(LEVEL_ORDER)))


if __name__ == "__main__":
    main()
