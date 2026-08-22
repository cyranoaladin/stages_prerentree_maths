"""Vérifie les résultats annoncés dans les corrigés de la piste excellence et des ateliers."""
from fractions import Fraction as F
import math

ok, ko = 0, 0
def check(label, calcule, annonce, tol=0.0):
    global ok, ko
    bon = (abs(calcule - annonce) <= tol) if tol else (calcule == annonce)
    print(("  OK   " if bon else "  ÉCHEC") + f" {label}: calculé {calcule}, annoncé {annonce}")
    ok += bon; ko += (not bon)

print("MATHS S1 — suite u_{n+1} = u_n/(1+u_n), u_0 = 1")
u = F(1)
for n in range(1, 4):
    u = u / (1 + u)
check("u_1", u_1 := F(1,2), F(1,2)); u = F(1)
vals = []
for _ in range(3):
    u = u/(1+u); vals.append(u)
check("u_2", vals[1], F(1,3)); check("u_3", vals[2], F(1,4))
check("u_n = 1/(n+1) en n=3", F(1,4), vals[2])

print("MATHS S2 — f(x) = (x-1)e^x + 2")
f  = lambda x: (x-1)*math.exp(x) + 2
fp = lambda x: x*math.exp(x)
check("f(0)", f(0), 1.0, 1e-12)
check("f'(0)", fp(0), 0.0, 1e-12)
check("minimum de f atteint en 0", min(f(x/100) for x in range(-500, 501)), f(0), 1e-9)

print("MATHS S3 — P(x) = 2x^3 - 3x^2 - 3x + 2")
P = lambda x: 2*x**3 - 3*x**2 - 3*x + 2
check("P(2)", P(2), 0)
check("factorisation (x-2)(2x^2+x-1) en x=5", (5-2)*(2*25+5-1), P(5))
check("racines de 2x^2+x-1 : -1", 2*(-1)**2 + (-1) - 1, 0)
check("racines de 2x^2+x-1 : 1/2", F(2)*F(1,2)**2 + F(1,2) - 1, F(0))
print("MATHS S3 ex10 — mx^2-4x+1, m=4 racine double")
check("discriminant en m=4", 16 - 4*4, 0)
check("m=0 donne x=1/4", -4*F(1,4)+1, F(0))

print("MATHS S4 — f(x) = 2x/(x^2+1)")
f  = lambda x: 2*x/(x**2+1)
fp = lambda x: 2*(1-x**2)/(x**2+1)**2
check("f(-1)", f(-1), -1.0, 1e-12); check("f(1)", f(1), 1.0, 1e-12)
check("f'(0)", fp(0), 2.0, 1e-12)
check("max de f sur R", max(f(x/1000) for x in range(-20000, 20001)), 1.0, 1e-6)

print("MATHS S5 — A(1;2) B(5;0) C(4;5)")
AB, AC, BC = (4,-2), (3,3), (-1,5)
check("AB.AC", AB[0]*AC[0]+AB[1]*AC[1], 6)
check("cos(BAC) = 1/sqrt(10)", 6/(math.hypot(*AB)*math.hypot(*AC)), 1/math.sqrt(10), 1e-12)
check("H(3;2,4) sur x-5y+9=0", 3 - 5*2.4 + 9, 0.0, 1e-12)
proba = lambda n: (n**2+9)/(n+3)**2
check("proba(3)", proba(3), 0.5, 1e-12)
check("minimum de proba sur n=1..50", min(proba(n) for n in range(1,51)), 0.5, 1e-12)

print("EXPERTES — arithmétique")
check("PGCD(252,198)", math.gcd(252,198), 18)
check("252/18", 252//18, 14); check("198/18", 198//18, 11)
check("diviseurs de 60", sum(1 for d in range(1,61) if 60 % d == 0), 12)
check("diviseurs de 360 par la formule", (3+1)*(2+1)*(1+1),
      sum(1 for d in range(1,361) if 360 % d == 0))
check("système 2x+3y=8, 5x-y=3 -> x=1", 1, 1)
check("vérif système", 2*1+3*2, 8); check("vérif système 2", 5*1-2, 3)
check("déterminant", 2*(-1)-3*5, -17)

print("NSI S1 — complément à deux sur 8 bits")
check("-45 en complément à deux", (~45 + 1) & 0xFF, 0xD3)
check("45 + (-45) sur 8 bits", (45 + 0xD3) & 0xFF, 0)
check("max 8 bits signé", 127, 2**7 - 1); check("min 8 bits signé", -128, -2**7)
check("max 4 bits non signé", 15, 2**4-1); check("max 5 bits", 31, 2**5-1)
check("2*15+1", 2*15+1, 31)
check("max 4 bits signé", 7, 2**3-1); check("2*7+1", 2*7+1, 15)

print("NSI S1 atelier — adressage IP")
ip, masque = (192,168,1,37), (255,255,255,0)
check("adresse réseau", tuple(a & b for a, b in zip(ip, masque)), (192,168,1,0))
check("192.168.1.200 même réseau",
      tuple(a & b for a, b in zip((192,168,1,200), masque)), (192,168,1,0))
check("192.168.2.37 réseau différent",
      tuple(a & b for a, b in zip((192,168,2,37), masque)) != (192,168,1,0), True)
check("adresses utilisables", 2**8 - 2, 254)

print("NSI S2 atelier — arbre binaire de recherche 8,3,10,1,6,14,4")
arbre = None
def insere(a, v):
    if a is None: return {"v": v, "g": None, "d": None}
    if v < a["v"]: a["g"] = insere(a["g"], v)
    else: a["d"] = insere(a["d"], v)
    return a
for v in (8,3,10,1,6,14,4): arbre = insere(arbre, v)
def infixe(a): return [] if a is None else infixe(a["g"]) + [a["v"]] + infixe(a["d"])
check("parcours infixe trié", infixe(arbre), sorted([8,3,10,1,6,14,4]))
def hauteur(a): return 0 if a is None else 1 + max(hauteur(a["g"]), hauteur(a["d"]))
check("hauteur de l'arbre équilibré", hauteur(arbre), 4)
degenere = None
for v in (1,3,4,6,8,10,14): degenere = insere(degenere, v)
check("hauteur de l'arbre dégénéré", hauteur(degenere), 7)

print("NSI S4 — dichotomie et bascule des coûts")
check("comparaisons dichotomie sur 10^6", math.ceil(math.log2(10**6)), 20)

# La bascule est le premier rang où le tri par insertion coûte davantage que le tri fusion.
bascule = next(n for n in range(2, 2000) if 3*n**2 + 2*n > 100*n*math.log2(n))
print(f"  INFO   bascule 3n²+2n vs 100n·log2(n) : n = {bascule}")
check("bascule annoncée « vers 270 »", abs(bascule - 270) <= 5, True)

print("PC S1 — fer + acide chlorhydrique")
n_fe, n_h = 2.0/56, 0.50*0.100
check("n(Fe)", round(n_fe, 4), 0.0357, 1e-4)
check("n(H+)", n_h, 0.050, 1e-12)
check("limitant = H+", n_h/2 < n_fe/1, True)
xmax = n_h/2
check("V(H2)", round(xmax*24, 2), 0.60, 1e-9)
check("m(Fe) restant", round((n_fe - xmax)*56, 2), 0.60, 0.01)

print("PC S2 — plan incliné")
check("P_x", round(0.50*9.8*math.sin(math.radians(30)), 2), 2.45, 1e-9)
check("R", round(0.50*9.8*math.cos(math.radians(30)), 1), 4.2, 1e-9)
check("accélération a = F/m", round(2.45/0.50, 1), 4.9, 1e-9)
check("a indépendante de la masse", round(2.0*9.8*0.5/2.0, 1), 4.9, 1e-9)

print("PC S3 — luge")
epp, ec = 40*9.8*12, 0.5*40*12**2
check("Epp", epp, 4704.0, 1e-9); check("Ec", ec, 2880.0, 1e-9)
check("dissipée", epp-ec, 1824.0, 1e-9)
check("v sans frottement", round(math.sqrt(2*9.8*12)), 15)
check("rendement", round(100*ec/epp), 61)
check("ΔT neige", round(1824/(5.0*2100), 2), 0.17, 1e-9)
check("ΔU = W + Q", 500 + (-200), 300)

print("PC S4 — onde 680 Hz")
check("λ air", 340/680, 0.50, 1e-12)
check("T", round(1/680, 6), 0.001471, 1e-6)
check("λ eau", round(1500/680, 1), 2.2, 1e-9)
check("0,25 m = λ/2", 0.25/(340/680), 0.5, 1e-12)
check("niveau sonore 1e-6 W/m²", 10*math.log10(1e-6/1e-12), 60.0, 1e-12)
check("doubler l'intensité = +3 dB", round(10*math.log10(2)), 3)
check("+20 dB = ×100", 10*math.log10(100), 20.0, 1e-12)
check("120 dB = 10^12", 10*math.log10(1e12), 120.0, 1e-12)

print("PC S5 — conducteur ohmique")
U, P = 47*0.25, 47*0.25**2
check("U", U, 11.75, 1e-12); check("P", round(P, 2), 2.94, 1e-9)
check("E sur 180 s", round(P*180), 529)
check("incertitude relative sur P", round(2*(0.01/0.25)*100), 8)
check("incertitude absolue", round(0.08*P, 1), 0.2, 1e-9)
check("charge pile 0,10 A pendant 1 h", 0.10*3600, 360.0, 1e-12)
check("(2+i)(2-i)", complex(2,1)*complex(2,-1), complex(5,0))

# Le mémento est le seul document que l'élève emporte en septembre : ce qui y est faux le
# suit toute l'année. Les quatre contrôles ci-dessous gardent les corrections apportées
# après relecture ligne à ligne — un défaut d'exactitude ne se rattrape pas à la relecture
# suivante s'il n'est pas tenu par un test.
print("PC MÉMENTO — exactitude et domaines de validité")
import pathlib
memento = pathlib.Path("tle_pc/03_EVALUATIONS/tle_pc_Memento_Formules_Terminale_ELEVE.md").read_text(encoding="utf-8")

# Le son audible descend à 20 Hz, où la longueur d'onde vaut 17 m et non « quelques mètres ».
check("λ du son audible à 20 kHz, en cm", round(340/20000*100, 1), 1.7, 1e-9)
check("λ du son audible à 20 Hz, en m", 340/20, 17.0, 1e-9)
check("le mémento annonce la borne haute 17 m", r"\SI{17}{\metre}" in memento, True)
check("le mémento n'annonce plus « quelques mètres »",
      "à quelques $\\si{\\metre}$" not in memento, True)

# P = R I² ne vaut que pour un conducteur ohmique : ni pour une pile, ni pour un moteur.
check("le mémento restreint la loi d'Ohm au conducteur ohmique",
      "conducteur ohmique**" in memento and "ni pour une pile" in memento, True)
check("le mémento n'enchaîne plus P = U I = R I²",
      r"P = U \times I = R\,I^{2}" not in memento, True)

# L'énergie mécanique ne se conserve pas « sans frottement » : il faut que seul le poids travaille.
check("le mémento nomme la condition de conservation de E_m",
      "seule force qui" in memento, True)
check("le mémento ne réduit plus la condition à l'absence de frottement",
      "Sans frottement, $E_m$ reste constante." not in memento, True)

# Les ordres de grandeur annoncés, recalculés.
check("piéton 1,5 m/s en km/h", round(1.5*3.6, 1), 5.4, 1e-9)
check("E_pp d'un étage (60 kg, 3 m) en kJ", round(60*9.8*3/1000, 1), 1.8, 1e-9)
check("E_c d'une voiture (1200 kg, 130 km/h) en kJ",
      round(0.5*1200*(130/3.6)**2/1000), 782)
check("l'ordre de grandeur annoncé est bien « quelques centaines de kJ »",
      100 <= 0.5*1200*(130/3.6)**2/1000 < 1000, True)

# Le mémento ne doit porter que des acquis de Première : les notions de Terminale
# qui lui ressemblent le plus sont nommément exclues.
for notion in ("décibel", "niveau d'intensité sonore", "quotient de réaction",
               "vecteur accélération", "condensateur", "diffraction"):
    check(f"le mémento ne contient pas « {notion} » (Terminale)",
          notion.lower() not in memento.lower(), True)

print(f"\n{ok} vérifications passées, {ko} en échec.")
raise SystemExit(1 if ko else 0)
