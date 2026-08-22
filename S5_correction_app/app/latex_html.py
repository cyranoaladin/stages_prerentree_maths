# -*- coding: utf-8 -*-
"""Conversion des structures LaTeX documentaires des énoncés en HTML sûr.

KaTeX rend les *expressions* mathématiques ; il ne transforme pas les
*environnements documentaires* LaTeX. Sans cette couche, un énoncé structuré
s'affiche littéralement dans le navigateur :

    \\begin{enumerate} \\item Développer $5(x-3)$. \\item ...

Ce module comble cet écart, pour les constructions **réellement présentes dans le
corpus** et pour elles seules. L'inventaire est tenu dans
``docs/LATEX_WEB_RENDERER_INVENTORY.md`` ; on n'implémente rien qui n'y figure pas.

Trois garanties, dans cet ordre :

1. **Rien de brut à l'écran.** Une structure non prise en charge n'apparaît jamais
   sous forme de ``\\begin{...}`` : elle est remplacée par un renvoi explicite au
   PDF distribué, affiché en vis-à-vis. Corriger juste importe plus que reproduire
   parfaitement une mise en page.
2. **Rien d'exécutable.** Chaque fragment est échappé avant d'entrer dans le
   résultat ; les seules balises produites sont écrites par ce module, depuis une
   liste fermée.
3. **Rien qui vienne d'un enseignant.** La fonction ne s'applique qu'au contenu du
   référentiel interne. Une observation saisie reste échappée par le gabarit.

L'ordre de traitement porte une contrainte : les structures sont extraites du texte
**brut**, avant échappement. Un tableau se découpe sur ses « & », qui deviendraient
« &amp; » si l'on échappait d'abord ; et le contenu d'un listing est verbatim, donc
il ne doit subir aucune des conversions qui suivent.

Le résultat est renvoyé en Markup et n'est destiné qu'au *contenu* d'un élément,
jamais à une valeur d'attribut.
"""

import html
import re

from markupsafe import Markup

__all__ = ["render_statement", "render_plain", "unsupported_structures",
           "STRUCTURES_PRISES_EN_CHARGE",
           "STRUCTURES_AVEC_REPLI", "MACROS_PRISES_EN_CHARGE", "FALLBACK_TEXTE"]

# Environnements convertis en HTML.
STRUCTURES_PRISES_EN_CHARGE = ("enumerate", "lstlisting", "tabularx")

# Environnements dont une forme inattendue bascule sur un renvoi au PDF.
STRUCTURES_AVEC_REPLI = ("tabularx",)

# Macros en ligne converties.
MACROS_PRISES_EN_CHARGE = ("textbf", "emph", "code", "par", "noindent", "item")

FALLBACK_TEXTE = "Voir le tableau ou le code dans le PDF distribué, à gauche."

# ------------------------------------------------------------------ expressions
# Segments mathématiques : laissés strictement intacts, KaTeX les rendra.
_MATH = re.compile(r"(\$\$.+?\$\$|\\\[.+?\\\]|\$.+?\$|\\\(.+?\\\))", re.DOTALL)

_LSTLISTING = re.compile(
    r"\\begin\{lstlisting\}(\[[^\]]*\])?\r?\n?(.*?)\\end\{lstlisting\}", re.DOTALL)

_ENUMERATE = re.compile(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}", re.DOTALL)

# Toute autre structure : repérée pour être remplacée par un renvoi.
_ENV_RESTANT = re.compile(r"\\begin\{(\w+\*?)\}.*?\\end\{\1\}", re.DOTALL)
_ENV_ORPHELIN = re.compile(r"\\(?:begin|end)\{\w+\*?\}")

_LANGUAGE = re.compile(r"language\s*=\s*\{?([A-Za-z0-9+#-]*)\}?")
_ESPACES = re.compile(r"\s*\n\s*")
_SENTINELLE = re.compile(r"\x00B(\d+)\x00")

_TABULARX_DEBUT = "\\begin{tabularx}"
_TABULARX_FIN = "\\end{tabularx}"


# ------------------------------------------------------- accolades équilibrées
def _groupe(texte, position):
    """Lit un groupe ``{...}`` à accolades équilibrées à partir de ``position``.

    Retourne (contenu, position_après) ou (None, position) si aucun groupe ne
    commence là. Indispensable : la spécification de colonnes d'un tableau du
    corpus vaut ``{|>{\\bfseries}p{16mm}|X|X|X|X|}``, et une expression régulière
    en ``[^}]*`` s'arrêterait à la première accolade fermante interne.
    """
    while position < len(texte) and texte[position] in " \t\r\n":
        position += 1
    if position >= len(texte) or texte[position] != "{":
        return None, position
    profondeur, curseur = 1, position + 1
    while curseur < len(texte) and profondeur:
        if texte[curseur] == "{":
            profondeur += 1
        elif texte[curseur] == "}":
            profondeur -= 1
        curseur += 1
    if profondeur:
        return None, position
    return texte[position + 1:curseur - 1], curseur


def _remplacer_macro(texte, nom, ouvrante, fermante):
    """Remplace ``\\nom{...}`` en respectant les accolades imbriquées.

    Cas réel du corpus : ``\\code{mesures = [{"id": "C01"}]}``.
    """
    marque = "\\" + nom + "{"
    sortie, position = [], 0
    while True:
        debut = texte.find(marque, position)
        if debut < 0:
            sortie.append(texte[position:])
            return "".join(sortie)
        sortie.append(texte[position:debut])
        contenu, suite = _groupe(texte, debut + len(marque) - 1)
        if contenu is None:                  # accolade non refermée : on n'invente rien
            sortie.append(texte[debut:])
            return "".join(sortie)
        sortie.append(ouvrante + contenu + fermante)
        position = suite


# -------------------------------------------------------------- texte en ligne
def _inline(fragment):
    """Conversions en ligne sur un fragment **déjà échappé**.

    ``\\textbf``, ``\\emph`` et ``\\code`` ne sont convertis qu'en dehors des
    délimiteurs mathématiques : à l'intérieur, ces commandes appartiennent à KaTeX
    et doivent lui parvenir intactes.
    """
    morceaux = []
    for part in _MATH.split(fragment):
        if not part:
            continue
        if _MATH.fullmatch(part):
            morceaux.append(part)
            continue
        part = _remplacer_macro(part, "textbf", "<strong>", "</strong>")
        part = _remplacer_macro(part, "emph", "<em>", "</em>")
        part = _remplacer_macro(part, "code", "<code>", "</code>")
        part = part.replace("\\noindent", "").replace("\\par", " ")
        morceaux.append(part)
    # En LaTeX, un simple passage à la ligne vaut une espace ; on reproduit cette
    # sémantique plutôt que d'inventer des sauts de ligne HTML.
    return _ESPACES.sub(" ", "".join(morceaux)).strip()


def _echapper(brut):
    # quote=False : le résultat n'est inséré que comme contenu d'élément. « < »,
    # « > » et « & » sont neutralisés, ce qui suffit à ce contexte, et les
    # apostrophes françaises restent lisibles.
    return html.escape(brut, quote=False)


def _texte(brut):
    return _inline(_echapper(brut))


# ------------------------------------------------------------------- enumerate
def _liste(corps):
    elements = [_inline(p) for p in corps.split("\\item")[1:]]
    elements = [e for e in elements if e]
    if not elements:
        return ""
    return '<ol class="enonce-liste">%s</ol>' % "".join(
        "<li>%s</li>" % e for e in elements)


# ------------------------------------------------------------------ lstlisting
def _bloc_code(options, contenu):
    """Un listing devient un bloc de code inerte.

    Le contenu est repris tel quel — indentation et retours à la ligne compris,
    puisqu'ils portent le sens en Python — puis échappé. Aucune coloration
    syntaxique : elle exigerait une dépendance externe, et l'application doit
    fonctionner sans réseau.

    ``[language={}]`` désigne un contenu qui n'est pas du code (un extrait de
    fichier CSV, dans le corpus) : aucune classe de langage n'est alors apposée.
    """
    classe = "code-bloc"
    if options is None:
        classe += " code-python"
    else:
        trouve = _LANGUAGE.search(options)
        if trouve and trouve.group(1):
            classe += " code-%s" % trouve.group(1).lower()
    contenu = contenu.strip("\r\n")
    contenu = re.sub(r"[ \t]+$", "", contenu, flags=re.MULTILINE)
    return '<pre class="%s"><code>%s</code></pre>' % (classe, _echapper(contenu))


# -------------------------------------------------------------------- tabularx
def _repli():
    return ('<p class="latex-repli"><span class="badge">%s</span></p>'
            % _echapper(FALLBACK_TEXTE))


def _tableau(specification, corps):
    """Convertit un tableau simple. Toute forme incertaine bascule sur le repli.

    Le corpus n'en contient qu'une forme : une ligne d'en-tête, puis des lignes
    dont la première cellule est en gras. On refuse tout ce qui s'en écarte plutôt
    que de produire une grille approximative — le PDF distribué reste la source de
    vérité, et il est affiché en vis-à-vis.
    """
    lignes = []
    for brute in corps.replace("\\hline", "\n").split("\\\\"):
        if not brute.strip():
            continue
        lignes.append([c.strip() for c in brute.split("&")])
    if len(lignes) < 2:
        return _repli()

    largeur = len(lignes[0])
    if largeur < 2 or any(len(l) != largeur for l in lignes):
        return _repli()
    # Une commande LaTeX résiduelle dans une cellule : on ne devine pas son rendu.
    for ligne in lignes:
        for cellule in ligne:
            reste = _remplacer_macro(cellule, "code", "", "")
            reste = _remplacer_macro(reste, "textbf", "", "")
            reste = _remplacer_macro(reste, "emph", "", "")
            if "\\" in reste.replace("\\\\", ""):
                return _repli()

    premiere_en_gras = ">{\\bfseries}" in specification
    entete = "".join("<th>%s</th>" % (_texte(c) or "&nbsp;") for c in lignes[0])
    corps_html = []
    for ligne in lignes[1:]:
        cellules = []
        for index, cellule in enumerate(ligne):
            rendu = _texte(cellule) or "&nbsp;"
            if index == 0 and premiere_en_gras:
                cellules.append('<th scope="row">%s</th>' % rendu)
            else:
                cellules.append("<td>%s</td>" % rendu)
        corps_html.append("<tr>%s</tr>" % "".join(cellules))
    return ('<table class="enonce-tableau"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table>' % (entete, "".join(corps_html)))


def _extraire_tableaux(brut, reserver):
    """Remplace chaque environnement tabularx par une sentinelle."""
    sortie, position = [], 0
    while True:
        debut = brut.find(_TABULARX_DEBUT, position)
        if debut < 0:
            sortie.append(brut[position:])
            return "".join(sortie)
        sortie.append(brut[position:debut])
        curseur = debut + len(_TABULARX_DEBUT)
        largeur, curseur = _groupe(brut, curseur)          # {\linewidth}
        specification, curseur = _groupe(brut, curseur)    # {|>{\bfseries}p{16mm}|X|…}
        fin = brut.find(_TABULARX_FIN, curseur)
        if largeur is None or specification is None or fin < 0:
            sortie.append(reserver(_repli()))
            position = (fin + len(_TABULARX_FIN)) if fin >= 0 else len(brut)
            continue
        sortie.append(reserver(_tableau(specification, brut[curseur:fin])))
        position = fin + len(_TABULARX_FIN)


# --------------------------------------------------------------------- rendu
def render_statement(texte):
    """Rend un énoncé du référentiel en HTML sûr."""
    if not texte:
        return Markup("")
    brut = str(texte)
    blocs = []

    def reserver(html_produit):
        blocs.append(html_produit)
        return "\x00B%d\x00" % (len(blocs) - 1)

    # 1. Les listings d'abord : leur contenu est verbatim et ne doit subir aucune
    #    des conversions qui suivent — un « \code » ou un « $ » y est du texte.
    brut = _LSTLISTING.sub(lambda m: reserver(_bloc_code(m.group(1), m.group(2))), brut)

    # 2. Les tableaux ensuite : ils peuvent se trouver à l'intérieur d'une liste et
    #    doivent donc être réservés avant le traitement de celle-ci. Le découpage
    #    des cellules se fait sur les « & » bruts, d'où l'extraction avant échappement.
    brut = _extraire_tableaux(brut, reserver)

    # 3. Toute autre structure : renvoi au PDF, jamais de LaTeX brut à l'écran.
    brut = _ENV_RESTANT.sub(
        lambda m: m.group(0) if m.group(1) == "enumerate" else reserver(_repli()), brut)

    # 4. Échappement, puis listes et prose.
    echappe = _echapper(brut)
    if _ENUMERATE.search(echappe):
        sortie, curseur = [], 0
        for m in _ENUMERATE.finditer(echappe):
            avant = _inline(echappe[curseur:m.start()])
            if avant:
                sortie.append("<p>%s</p>" % avant)
            sortie.append(_liste(m.group(1)))
            curseur = m.end()
        apres = _inline(echappe[curseur:])
        if apres:
            sortie.append("<p>%s</p>" % apres)
        rendu = "".join(sortie)
    else:
        rendu = _inline(echappe)

    # 5. Un délimiteur orphelin ne doit pas subsister à l'écran.
    rendu = _ENV_ORPHELIN.sub("", rendu)

    # 6. Réinsertion des blocs réservés.
    rendu = _SENTINELLE.sub(lambda m: blocs[int(m.group(1))], rendu)
    return Markup(rendu)


def render_plain(texte) -> str:
    """Version texte d'un fragment de référentiel, pour un attribut HTML.

    Le rendu principal produit des balises ; elles n'ont rien à faire dans un
    attribut comme ``title``. Cette variante retire les commandes LaTeX en
    conservant leur contenu, et ne renvoie **pas** de Markup : le gabarit
    l'échappera comme n'importe quelle chaîne.
    """
    if not texte:
        return ""
    brut = str(texte)
    brut = _LSTLISTING.sub(lambda m: m.group(2).strip(), brut)
    for nom in ("code", "textbf", "emph"):
        brut = _remplacer_macro(brut, nom, "", "")
    brut = _ENV_ORPHELIN.sub("", brut)
    brut = brut.replace("\\item", "·").replace("\\hline", " ")
    brut = brut.replace("\\noindent", "").replace("\\par", " ")
    return _ESPACES.sub(" ", brut).strip()


def unsupported_structures(texte) -> list:
    """Environnements d'un énoncé qui déclencheront un repli. Sert à l'inventaire."""
    if not texte:
        return []
    restant = _LSTLISTING.sub("", str(texte))
    restant = _extraire_tableaux(restant, lambda _: "")
    restant = _ENUMERATE.sub("", restant)
    return sorted(set(re.findall(r"\\begin\{(\w+\*?)\}", restant)))
