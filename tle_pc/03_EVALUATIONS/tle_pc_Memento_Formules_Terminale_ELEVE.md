# Terminale Spécialité Physique-Chimie — Mémento de formules
## À garder dans le portfolio, et à emporter en septembre

Ce mémento ne contient que les acquis de **Première** dont la Terminale a un besoin
immédiat. Il ne remplace pas le cours : il rassemble ce qui doit être disponible sans
réfléchir.

---

## 1. Transformations chimiques

### Le tableau d'avancement

| État | $\ce{aA}$ | $\ce{+ bB}$ | $\longrightarrow$ | $\ce{cC}$ |
|---|---|---|---|---|
| Initial | $n_0(\mathrm{A})$ | $n_0(\mathrm{B})$ | | $0$ |
| Avancement $x$ | $n_0(\mathrm{A}) - a\,x$ | $n_0(\mathrm{B}) - b\,x$ | | $c\,x$ |

### Le réactif limitant

$$x_{\max} = \min\left(\frac{n_0(\mathrm{A})}{a},\ \frac{n_0(\mathrm{B})}{b}\right)$$

Le réactif dont le quotient est le plus petit est le **limitant**. **On ne compare jamais
les quantités brutes.**

**Contrôle.** Remplacer $x$ par $x_{\max}$ dans chaque quantité restante : une seule doit
valoir zéro, les autres doivent être positives.

### Oxydo-réduction

Un couple associe **toujours** un oxydant et un réducteur.

- Le **réducteur cède** des électrons.
- L'**oxydant capte** des électrons.
- L'oxydant est écrit à gauche du slash : $\ce{Cu^2+/Cu}$, $\ce{Ag+/Ag}$, $\ce{Zn^2+/Zn}$.

$$\ce{Cu^2+ + 2e^- <=> Cu}$$

### Acide-base et pH

- Selon **Brønsted** : un acide **cède** un proton $\ce{H+}$, une base le **capte**.
- La définition par les ions $\ce{HO^-}$ est celle d'**Arrhenius**, et concerne les bases.
- pH **faible** $\Rightarrow$ solution **acide**.
- Une unité de pH en moins $\Rightarrow$ concentration en $\ce{H3O+}$ **dix fois** plus
  grande.

---

## 2. Mécanique

### Vecteur vitesse

En chaque point, le vecteur vitesse est **tangent à la trajectoire** et orienté dans le
sens du mouvement.

- La trajectoire impose la **direction**.
- La **norme** peut varier, même sur une trajectoire courbe.
- Norme constante $\neq$ vecteur constant. Sur un cercle parcouru à norme constante, la
  direction change : le mouvement est **accéléré**.

### Bilan des forces — toujours dans cet ordre

1. Le **système** : quel objet.
2. Le **référentiel** : par rapport à quoi.
3. La **liste** des forces extérieures, avec pour chacune l'objet qui l'exerce.
4. Seulement ensuite : une relation.

**Contrôle.** Pour chaque force : « exercée par quel objet ? » Si la phrase reste
inachevée, la force n'existe pas.

### Chute libre

Un corps est en chute libre lorsqu'il est soumis à **son seul poids**. Le frottement de
l'air n'y figure pas : ce n'est pas un oubli, c'est la définition. Si l'énoncé demande
d'en tenir compte, le mouvement **n'est plus** une chute libre.

---

## 3. Énergie

### Travail d'une force constante

$$W_{AB}(\vv{F}) = \vv{F} \cdot \vv{AB} = F \times AB \times \cos\alpha$$

| $\alpha$ | $\cos\alpha$ | Travail |
|---|---:|---|
| $0°$ | $1$ | maximal, **moteur** |
| $90°$ | $0$ | **nul** |
| $180°$ | $-1$ | minimal, **résistant** |

**Une force peut s'exercer en permanence sans jamais travailler.** C'est le cas du poids
lors d'un déplacement horizontal.

### Les trois énergies

| Grandeur | Expression | Dépend de |
|---|---|---|
| Énergie cinétique | $E_c = \dfrac{1}{2}mv^{2}$ | la **vitesse** |
| Énergie potentielle de pesanteur | $E_{pp} = mgz$ | l'**altitude** |
| Énergie mécanique | $E_m = E_c + E_{pp}$ | les deux |

Toutes trois en **joules**.

**Conservation.** $E_m$ reste constante lorsque le poids est la seule force qui
travaille — donc en l'absence de frottement, mais aussi de toute traction ou
poussée. Une force motrice fait croître $E_m$ ; le frottement la fait décroître.

**Contrôle.** Objet immobile $\Rightarrow E_c = 0$. Objet au niveau de référence
$\Rightarrow E_{pp} = 0$.

---

## 4. Ondes

$$\lambda = v \times T = \frac{v}{f} \qquad\text{et}\qquad T = \frac{1}{f}$$

| Grandeur | Imposée par | Change de milieu ? |
|---|---|---|
| Fréquence $f$ | la **source** | **non** |
| Célérité $v$ | le **milieu** | **oui** |
| Longueur d'onde $\lambda$ | les deux | **oui** |

**Contrôle par les unités.** $\si{\metre} = ( \si{\metre\per\second} )/( \si{\per\second} )$.
Le produit $v \times f$ ne donne pas une longueur.

**Contrôle qualitatif.** Fréquence grande $\Rightarrow$ longueur d'onde **petite**.

---

## 5. Optique

### Les trois rayons particuliers d'une lentille mince convergente

1. Un rayon **parallèle à l'axe** émerge en passant par le foyer image $F'$.
2. Un rayon **passant par $F$** émerge parallèle à l'axe.
3. Un rayon **passant par le centre optique $O$** n'est **pas dévié**.

Deux rayons suffisent pour construire une image : leur intersection après la lentille
**est** l'image.

**Objet à l'infini** $\Rightarrow$ image dans le **plan focal image**. Le centre optique
est un point de la lentille : rien ne s'y forme.

---

## 6. Électricité

$$P = U \times I \qquad\text{et}\qquad E = P \times \Delta t$$

Ces deux relations valent pour **tout** dipôle. Les deux suivantes ne valent que pour un
**conducteur ohmique** — ni pour une pile, ni pour un moteur :

$$U = R \times I \qquad\text{et}\qquad P = R\,I^{2}$$

| Grandeur | Symbole | Unité |
|---|---|---|
| Tension | $U$ | volt ($\si{\volt}$) |
| Intensité | $I$ | ampère ($\si{\ampere}$) |
| Résistance | $R$ | ohm ($\si{\ohm}$) |
| Puissance | $P$ | watt ($\si{\watt}$) |
| Énergie | $E$ | joule ($\si{\joule}$) |

**Effet Joule.** L'énergie électrique est dissipée sous forme **thermique**. Ce n'est
**pas** une perte de courant : l'intensité qui sort d'une résistance est la même que celle
qui y entre.

**Puissance et énergie.** La puissance est une énergie **par seconde**. Convertir les
durées en secondes avant de multiplier.

---

## 7. Chimie organique

| Groupe | Exemple | Famille |
|---|---|---|
| $\ce{-OH}$ | $\ce{CH3-CH2-OH}$ | alcool |
| $\ce{-CHO}$ | $\ce{CH3-CHO}$ | aldéhyde |
| $\ce{-CO-}$ | $\ce{CH3-CO-CH3}$ | cétone |
| $\ce{-COOH}$ | $\ce{CH3-COOH}$ | acide carboxylique |
| $\ce{-COO-}$ | $\ce{CH3-COO-CH3}$ | ester |

$\ce{-CHO}$ est en **bout** de chaîne ; $\ce{-CO-}$ est au **milieu**. C'est ce qui distingue
un aldéhyde d'une cétone.

---

## 8. Les trois gestes, et quelques ordres de grandeur

1. **La relation d'abord.** Aucune valeur numérique avant la relation littérale.
2. **L'unité toujours.** Un résultat sans unité n'est pas un résultat.
3. **L'ordre de grandeur en dernier.** Avant de conclure, comparer à un repère.

| Grandeur | Ordre de grandeur |
|---|---|
| Vitesse d'un piéton | $\SI{1.5}{\metre\per\second}$ |
| Célérité du son dans l'air | $\SI{340}{\metre\per\second}$ |
| Célérité du son dans l'eau | $\SI{1500}{\metre\per\second}$ |
| Célérité de la lumière dans le vide | $\SI{3.0e8}{\metre\per\second}$ |
| Intensité de pesanteur | $g = \SI{9.8}{\newton\per\kilogram}$ |
| Longueur d'onde d'un son audible | de $\SI{1.7}{\centi\metre}$ ($\SI{20}{\kilo\hertz}$) à $\SI{17}{\metre}$ ($\SI{20}{\hertz}$) |
| Énergie potentielle gagnée en montant un étage | quelques $\si{\kilo\joule}$ |
| Énergie cinétique d'une voiture sur autoroute | quelques centaines de $\si{\kilo\joule}$ |

**Chiffres significatifs.** Le résultat ne peut pas être plus précis que la donnée la
moins précise qui a servi à le calculer.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
