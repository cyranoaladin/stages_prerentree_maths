# -*- coding: utf-8 -*-
"""Rédaction des blocs de rapport. Le déterministe suffit ; l'IA est une option éteinte.

Un générateur ne calcule rien. Il met en phrases des faits déjà établis par
``analysis.py``. Les nombres qu'il écrit sont recopiés, jamais recalculés.

Interdits tenus par construction, et vérifiés par les tests :

* aucune progression chiffrée ;
* aucun « non acquis », « lacune » ou « fragile » sur une notion de passerelle ;
* aucun « maîtrise désormais » adossé à une preuve faible ;
* aucune « consolidation durable » après une remédiation immédiate ;
* aucun identifiant technique dans un texte destiné aux parents ou à l'élève.
"""

import os
from typing import List, Tuple

from . import points

Block = Tuple[str, str, str]          # (clé, titre, contenu)


def de(name: str) -> str:
    """« de Sarah », mais « d'Ines ». L'élision compte dans un document lu par une famille."""
    first = (name or "").strip()
    if first and first[0].lower() in "aeiouyéèêàâîïôöûü":
        return "d'%s" % first
    return "de %s" % first


def _join(labels: List[str], vide: str = "") -> str:
    labels = [l for l in labels if l]
    if not labels:
        return vide
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + " et " + labels[-1]


class NarrativeGenerator:
    """Contrat commun. Un générateur reçoit des faits ; il ne les modifie pas."""

    name = "abstract"

    def blocks(self, kind: str, ctx: dict) -> List[Block]:
        raise NotImplementedError


class DeterministicNarrativeGenerator(NarrativeGenerator):
    """Le générateur par défaut, et le seul nécessaire. Aucun réseau, aucune clé, aucun aléa."""

    name = "deterministic"

    def blocks(self, kind: str, ctx: dict) -> List[Block]:
        builder = getattr(self, "_%s" % kind.lower(), None)
        if builder is None:
            raise ValueError("type de rapport inconnu : %s" % kind)
        return builder(ctx)

    # ------------------------------------------------------------ bilan parents
    def _bilan_parents(self, ctx) -> List[Block]:
        a, plan = ctx["analysis"], ctx["plan"]
        n1, bridge = a["n_minus_1_consolidation"], a["bridge_n_readiness"]
        raw = a["raw_assessment_score"]
        out = []

        out.append(("synthese", "Synthèse",
                    "%s a suivi les cinq séances du stage de pré-rentrée, soit dix heures de "
                    "travail, en %s. La séance de clôture a comporté soixante-quinze minutes "
                    "de travail puis une évaluation de quarante-cinq minutes. Ce bilan rend "
                    "compte de ce que cette évaluation permet d'établir, et de ce qu'elle ne "
                    "permet pas."
                    % (ctx["first_name"], ctx["subject_phrase"])))

        baseline = [s for s in a["skills"]
                    if s["curriculum_scope"] == "n_minus_1"
                    and s["baseline_status_qualitative"] in ("fragile", "en_voie_acquisition")]
        if baseline:
            texte = ("Le diagnostic de début de stage signalait des points de vigilance sur : "
                     "%s. Ce diagnostic était qualitatif, domaine par domaine : il ne "
                     "conservait pas les réponses question par question."
                     % _join([s["label"].lower() for s in baseline[:5]]))
        else:
            texte = ("Le diagnostic de début de stage ne signalait pas de fragilité majeure "
                     "sur les domaines couverts par l'évaluation de clôture. Il était "
                     "qualitatif, domaine par domaine.")
        out.append(("situation_depart", "Situation de départ", texte))

        out.append(("travail_realise", "Travail réalisé pendant le stage",
                    "Les quatre premières séances ont porté sur les domaines identifiés au "
                    "diagnostic. La cinquième a repris les deux axes prioritaires %s, puis a "
                    "ouvert sur des notions de l'année à venir, avant l'évaluation finale."
                    % de(ctx["first_name"])))

        out.append(("score_brut", "Score brut au sujet de clôture",
                    "Le score brut est de %s sur 20. Ce nombre décrit la copie ; il ne mesure "
                    "pas à lui seul les acquis de l'année précédente, car le sujet comportait "
                    "aussi des questions de découverte portant sur le programme de l'année à "
                    "venir. Les deux parts sont donc présentées séparément ci-dessous."
                    % raw["sur_20"]))

        pct = n1["percentage"]
        out.append(("consolidation", "Acquis de l'année précédente",
                    "Sur les %s points du sujet qui portent sur les acquis attendus à "
                    "l'entrée dans l'année, %s ont été obtenus%s. %s"
                    % (n1["available"], n1["earned"],
                       (", soit %s %%" % ("%.0f" % pct).replace(".", ",")) if pct is not None
                       else "",
                       self._consolidation_comment(a))))

        if bridge["available_centi"]:
            out.append(("passerelles", "Premières passerelles vers l'année à venir",
                        "Le sujet comportait %s points portant sur des notions découvertes "
                        "pendant la séance et appartenant au programme de l'année à venir ; "
                        "%s ont été obtenus. %s"
                        % (bridge["available"], bridge["earned"],
                           self._bridge_comment(a))))
        else:
            out.append(("passerelles", "Premières passerelles vers l'année à venir",
                        "Le sujet de clôture ne comportait pas de question de découverte : il "
                        "portait intégralement sur les acquis attendus à l'entrée dans "
                        "l'année."))

        forts = [s for s in a["skills"] if s["curriculum_scope"] == "n_minus_1"
                 and s["status"] in ("SOLIDE", "SATISFAISANT")]
        out.append(("points_forts", "Points forts",
                    ("Les éléments suivants sont aujourd'hui réussis : %s."
                     % _join([s["label"].lower() for s in forts[:6]])) if forts
                    else "L'évaluation ne fait pas ressortir de domaine solidement installé ; "
                         "le plan ci-dessous porte donc sur les prérequis essentiels."))

        a_consolider = [s for s in a["skills"] if s["curriculum_scope"] == "n_minus_1"
                        and s["status"] in ("PRIORITAIRE", "A_CONSOLIDER")]
        out.append(("points_consolider", "Points à consolider",
                    ("Le travail de rentrée portera d'abord sur : %s."
                     % _join([s["label"].lower() for s in a_consolider[:6]])) if a_consolider
                    else "Aucune fragilité de prérequis n'est documentée par cette "
                         "évaluation."))

        confirmer = [s for s in a["skills"] if s["recommended_delayed_check"]]
        out.append(("a_confirmer", "Réussites à confirmer dans la durée",
                    ("Certaines réussites ont été obtenues moins d'une heure après que la "
                     "notion venait d'être retravaillée : %s. C'est une réussite réelle, mais "
                     "elle ne dit pas encore si l'acquis tient à distance. Un court contrôle "
                     "est prévu en deuxième semaine pour le vérifier."
                     % _join([s["label"].lower() for s in confirmer[:6]])) if confirmer
                    else "Aucune réussite de l'évaluation ne dépend d'un effet de récence "
                         "immédiat."))

        lignes = []
        for week in plan["weeks"]:
            if not week["objectives"]:
                continue
            lignes.append("Semaine %d — %s : %s."
                          % (week["week"], week["focus"],
                             _join([o["label"].lower() for o in week["objectives"]])))
        out.append(("plan", "Plan des quatre premières semaines",
                    " ".join(lignes) if lignes
                    else "Aucune priorité de consolidation n'est identifiée ; les quatre "
                         "premières semaines peuvent être consacrées au réinvestissement."))

        out.append(("suivi", "Recommandation de suivi",
                    "%s %s" % (plan["follow_up"]["proposed"].capitalize() + ".",
                               plan["follow_up"]["justification"])))

        out.append(("limites", "Ce que ce bilan ne dit pas",
                    "Les réponses initiales question par question n'étant pas disponibles, "
                    "aucune progression chiffrée entre le début et la fin du stage n'est "
                    "calculée : ce serait un chiffre sans mesure derrière lui. Le diagnostic "
                    "initial est donc rappelé de façon qualitative, et l'évaluation finale "
                    "décrite pour elle-même."))
        return out

    def _consolidation_comment(self, a) -> str:
        weak = [s for s in a["skills"] if s["curriculum_scope"] == "n_minus_1"
                and s["evidence_strength"] in ("INSUFFICIENT", "LOW")]
        if weak:
            return ("Ce pourcentage décrit les questions posées, qui sont peu nombreuses sur "
                    "certains domaines : il se lit avec le détail par compétence, non seul.")
        return ("Ce pourcentage décrit les questions posées ; il se lit avec le détail par "
                "compétence.")

    def _bridge_comment(self, a) -> str:
        good = [s for s in a["skills"] if s["curriculum_scope"] == "bridge_n"
                and s["status"] in ("PROMISING", "FIRST_EXPOSURE")]
        if good:
            return ("Ces questions portaient sur des notions rencontrées pour la première "
                    "fois : le résultat obtenu montre une première aisance encourageante, et "
                    "ne constitue pas un jugement sur les acquis antérieurs.")
        return ("Ces questions portaient sur des notions rencontrées pour la première fois. "
                "Le résultat ne constitue donc pas un jugement sur les acquis antérieurs : "
                "ces notions seront enseignées et reprises en classe dès la rentrée.")

    # ------------------------------------------------------ synthèse enseignant
    def _synthese_enseignant(self, ctx) -> List[Block]:
        a = ctx["analysis"]
        out = [("cadre", "Cadre d'interprétation",
                "Analyse déterministe de la correction, révision %d. Les scores sont saisis "
                "critère par critère ; les codes d'erreur sont attachés au seul critère "
                "échoué. %s"
                % (a["correction_revision"], a["delta_blocked_reason"]))]
        etayees = a["conclusions"]["etayees"]
        prudentes = a["conclusions"]["prudentes"]
        limites = a["conclusions"]["limites"]
        out.append(("conclusions_etayees", "Conclusions suffisamment étayées",
                    "\n".join("— " + c for c in etayees) or "— aucune."))
        out.append(("conclusions_prudentes", "Conclusions prudentes",
                    "\n".join("— " + c for c in prudentes) or "— aucune."))
        out.append(("limites_analyse", "Limites de l'analyse",
                    "\n".join("— " + c for c in limites) or "— aucune."))
        return out

    # ------------------------------------------------------------- plan rentrée
    def _plan_rentree(self, ctx) -> List[Block]:
        plan = ctx["plan"]
        return [("cadre", "Comment lire ce plan",
                 "Deux à trois objectifs par semaine, pas davantage. Les notions de "
                 "découverte figurent à part : elles n'ont pas encore été enseignées en "
                 "classe et ne constituent pas un retard."),
                ("suivi", "Suivi proposé", plan["follow_up"]["proposed"].capitalize() + ". "
                 + plan["follow_up"]["justification"])]

    # ------------------------------------------------------------- fiche élève
    def _fiche_eleve(self, ctx) -> List[Block]:
        a = ctx["analysis"]
        forts = [s for s in a["skills"] if s["curriculum_scope"] == "n_minus_1"
                 and s["status"] in ("SOLIDE", "SATISFAISANT")]
        travail = [s for s in a["priorities"] if s["priority_rank"] in ("P1", "P2")][:2]
        bridge = [s for s in a["skills"] if s["curriculum_scope"] == "bridge_n"
                  and s["status"] in ("PROMISING", "FIRST_EXPOSURE")]
        out = [("sais_faire", "Ce que je sais bien faire",
                ("Tu réussis maintenant : %s."
                 % _join([s["label"].lower() for s in forts[:4]])) if forts
                else "Tu as travaillé sérieusement pendant les cinq séances : c'est le point "
                     "de départ.")]
        if bridge:
            out.append(("decouverte", "Ce que j'ai découvert",
                        "Tu as abordé pour la première fois : %s. Tu t'en es bien sorti alors "
                        "que ce n'était pas encore au programme de ton année : c'est "
                        "encourageant."
                        % _join([s["label"].lower() for s in bridge[:3]])))
        out.append(("consolider", "Ce que je dois consolider",
                    ("Deux choses à travailler en priorité : %s."
                     % _join([s["label"].lower() for s in travail])) if travail
                    else "Continue à t'entraîner régulièrement : rien ne demande une reprise "
                         "urgente."))
        out.append(("objectif", "Mon objectif pour septembre",
                    ("En quatre semaines, je veux réussir sans aide trois exercices de suite "
                     "sur : %s. Je note à chaque fois le contrôle que j'ai fait."
                     % _join([s["label"].lower() for s in travail]))
                    if travail else
                    "En quatre semaines, je veux garder l'habitude de vérifier chaque "
                    "résultat avant de passer à la question suivante."))
        out.append(("methode", "Ma méthode",
                    "J'écris la règle ou la relation avant les calculs. Je vérifie mon "
                    "résultat autrement que par le même calcul. Si je bloque, je note ce que "
                    "je ne comprends pas plutôt que de laisser vide."))
        return out


class LLMNarrativeGenerator(NarrativeGenerator):
    """Réservation d'architecture. Désactivé, et il le reste tant qu'on ne l'active pas.

    Rien n'est transmis sans activation explicite, sans configuration par variable
    d'environnement et sans confirmation. Aucune clé n'est inscrite dans le dépôt, et un
    générateur de texte ne touche jamais un score.
    """

    name = "llm_suggestion"

    def __init__(self, provider: str = None):
        self.provider = provider or os.environ.get("NEXUS_S5_LLM_PROVIDER", "")

    @staticmethod
    def enabled() -> bool:
        return os.environ.get("NEXUS_S5_ENABLE_LLM", "").lower() in ("1", "true", "oui")

    @staticmethod
    def pseudonymise(ctx: dict) -> dict:
        """Ce qui partirait, si cela partait un jour : sans nom, sans identifiant d'élève."""
        safe = dict(ctx)
        safe["first_name"] = "ÉLÈVE_01"
        safe["display_name"] = "ÉLÈVE_01"
        analysis = dict(ctx.get("analysis") or {})
        analysis.pop("student_name", None)
        analysis.pop("student_id", None)
        safe["analysis"] = analysis
        return safe

    def blocks(self, kind: str, ctx: dict) -> List[Block]:
        if not self.enabled():
            raise RuntimeError(
                "le générateur assisté par modèle de langage est désactivé. "
                "Le rapport complet se produit sans lui ; l'activer demande "
                "NEXUS_S5_ENABLE_LLM=1 et une configuration explicite du fournisseur.")
        raise NotImplementedError(
            "aucun fournisseur n'est câblé dans cette version : la génération "
            "déterministe reste la seule voie de production.")


def get_generator(name: str = "deterministic") -> NarrativeGenerator:
    if name == "llm_suggestion":
        return LLMNarrativeGenerator()
    return DeterministicNarrativeGenerator()
