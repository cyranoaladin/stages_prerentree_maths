# 1ere_spe_Evaluation_Finale_PROF_Corrige
## Évaluation finale - Corrigé et exploitation

## Annexe G — Évaluation finale proposée

Durée : 25 minutes.
Certitude 1 à 4 obligatoire.

1. Développer :
   $$(2x-5)^2.$$

2. Factoriser :
   $$9x^2-16.$$

3. Résoudre :
   $-4x+8\geq0$.

4. Résoudre :
   $$(x-3)(2x+1)<0.$$

5. Soit $f(x)=x^2+2x-3$. Calculer (f(-3)).

6. Si $(2;5)\in\mathcal C_f$, traduire cette information de deux manières.

7. Comparer (x) et $x^2$ pour (0<x<1).

8. Calculer le taux de variation de $g(x)=x^2$ entre (2) et (2+h).

9. Pour (A(-2;1)) et (B(4;-5)), calculer $\overrightarrow{AB}$.

10. Calculer le coefficient directeur de ((AB)).

11. Un prix augmente de 20 %, puis diminue de 25 %. Calculer l’évolution globale.

12. Sur un dé, (A={1,2,3,4}) et (B={3,4,5}). Calculer $P(A\cup B)$.

13. Donner $P(\overline A)$.

14. Soit $u_0=4$ et $u_{n+1}=u_n+5$. Calculer $u_3$ et donner $u_n$.

15. Soit $v_0=100$ et $v_{n+1}=1{,}02v_n$. Donner $v_n$.

16. Donner la valeur de `L` :

```python
L = []
u = 2

for _ in range(4):
    L.append(u)
    u = 3 * u
```

### Corrigé

1.

$$4x^2-20x+25.$$

2.

$$(3x-4)(3x+4).$$

3.

$$x\leq2.$$

4.

$$x\in\left]-\frac12;3\right[.$$

5.

$$f(-3)=9-6-3=0.$$

6.

$$f(2)=5.$$

(5) est l’image de (2) et (2) est un antécédent de (5).

7.

$$x^2<x.$$

8.

$$\frac{(2+h)^2-4}{h}=4+h.$$

9.

$$\overrightarrow{AB}=(6;-6).$$

10.

$$m=\frac{-5-1}{4-(-2)}=-1.$$

11.

$$1{,}20\times0{,}75=0{,}90.$$

Baisse globale de 10 %.

12.

$$A\cup B={1,2,3,4,5},$$

donc :

$$P(A\cup B)=\frac56.$$

13.

$$P(\overline A)=1-\frac46=\frac13.$$

14.

$$u_3=19,\qquad u_n=4+5n.$$

15.

$$v_n=100\times1{,}02^n.$$

16.

```python
[2, 6, 18, 54]
```

---


## Barème d’exploitation conseillé

- 1 point par procédure ou résultat correct.
- 0,5 point lorsque la démarche est correcte mais comporte une erreur de calcul secondaire.
- 0 point lorsque la relation utilisée n’est pas pertinente.
- La certitude n’ajoute ni ne retire de point ; elle détermine le geste pédagogique.

## Lecture réussite × confiance

| Résultat | Certitude | Décision |
|---|---:|---|
| juste | 3-4 | entretenir ou transférer |
| juste | 1-2 | consolider et faire expliquer |
| faux | 1-2 | installer la notion |
| faux | 3-4 | confronter puis reconstruire |
| vide | - | diagnostiquer oralement |
