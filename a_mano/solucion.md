# Parte 5: un bloque de transformer, paso a paso

Desarrollo de `ejercicio.md` para "El banco aguanta" y "El banco presta". Todos los valores están a tres decimales y se contrastan con `python a_mano/verificar.py`, que usa el `atencion.py` de la parte 4. Cada operación va con su **razón** (qué hace) y su **utilidad** (para qué sirve en el modelo).

> La consigna pide las hojas escritas a mano y escaneadas en `a_mano/`. Este archivo es el desarrollo y la justificación de cada paso, pero **no reemplaza las hojas**: las cuentas hay que copiarlas a papel antes de la entrega.

Notación: d = 4, √d = 2. Las filas de cada matriz son los tokens en orden: "El", "banco" y la tercera palabra.

---

## Parte A: bloque completo como decoder (con máscara causal)

### Frase 1: "El banco aguanta"

**1. Entrada, X = E + P.** Se suma al embedding de cada palabra el de su posición.
- Razón: el embedding de palabra dice *qué* palabra es, y el de posición dice *dónde* está.
- Utilidad: la atención por sí sola no distingue el orden (si se permutan los tokens, la salida se permuta igual). Sin P, "banco aguanta El" sería lo mismo que "El banco aguanta".

| token | E | + P | = X |
|---|---|---|---|
| El | 0 0 0 1 | 0 0 0 0 | 0 0 0 1 |
| banco | 1 1 0 0 | 0 0 0 1 | 1 1 0 1 |
| aguanta | 1 0 1 0 | 0 0 0 2 | 1 0 1 2 |

**2. Proyecciones, Q = X·Wq, K = X·Wk, V = X·Wv.**
- Razón: cada token se transforma de tres formas. Q es lo que *busca*, K es lo que *ofrece* para ser encontrado y V es lo que *aporta* si lo eligen.
- Utilidad: separar los tres papeles deja que el modelo aprenda a buscar una cosa y aportar otra. Con Wq = Wv = I, Q = V = X. Con Wk, la columna 1 de K = d1 + d3 de X, la columna 2 = d2 + d3 y las demás quedan en 0.

| | Q = X | K = X·Wk | V = X |
|---|---|---|---|
| El | 0 0 0 1 | 0 0 0 0 | 0 0 0 1 |
| banco | 1 1 0 1 | 1 1 0 0 | 1 1 0 1 |
| aguanta | 1 0 1 2 | 2 1 0 0 | 1 0 1 2 |

(K de aguanta: d1 = 1 + 1 = 2, d2 = 0 + 1 = 1.) La dimensión 4 de K es 0 en todos los tokens: Wk la anula. Por eso la posición no influye en las afinidades, solo en lo que se mezcla (V) y en las sumas posteriores.

**3. Afinidades, S = Q·Kᵀ.**
- Razón: el producto punto entre la consulta de un token y la clave de otro mide cuánto se parecen.
- Utilidad: da una puntuación de "cuánto me sirve mirar a ese token".

```
S =  0  0  0
     0  2  3
     0  1  2
```
Ejemplo: S[banco, aguanta] = Q_banco · K_aguanta = 1·2 + 1·1 + 0·0 + 1·0 = 3.

**4. Escala, S/√d.**
- Razón: se divide por √4 = 2.
- Utilidad: con dimensiones grandes los productos punto crecen y el softmax se satura (un token se lleva casi todo y los gradientes casi desaparecen). La escala mantiene los valores en un rango donde el softmax sigue siendo suave.

```
S/2 =  0    0    0
       0    1    1.5
       0    0.5  1
```

**5. Máscara causal.** Se pone −∞ sobre la diagonal (los tokens posteriores).
- Razón: un token no puede mirar a los que vienen después.
- Utilidad: en la generación el modelo predice la palabra siguiente sin conocerla. Si durante el entrenamiento pudiera mirarla, haría trampa y no aprendería a predecir.

```
 0   -∞   -∞
 0    1   -∞
 0   0.5   1
```

**6. Matriz de atención, A = softmax por fila.**
- Razón: convierte cada fila en pesos positivos que suman 1 (e^(−∞) = 0, así que lo enmascarado queda en 0).
- Utilidad: son los porcentajes con los que cada token mezcla a los demás.

- Fila "El": solo se mira a sí mismo → [1, 0, 0].
- Fila "banco": e⁰ = 1 y e¹ = 2,718, suma 3,718 → [0,269, 0,731, 0].
- Fila "aguanta": e⁰ = 1, e^0,5 = 1,649, e¹ = 2,718, suma 5,367 → [0,186, 0,307, 0,506].

```
A =  1      0      0
     0.269  0.731  0
     0.186  0.307  0.506
```

**7. Mezcla, A·V, y proyección de salida, (A·V)·Wo.**
- Razón: cada token toma un promedio de los V de los tokens que mira, ponderado por A. Wo = I devuelve el resultado al espacio del modelo.
- Utilidad: así cada vector incorpora información del contexto. Es el paso que hace contextual a "banco".

```
A·V = El:      1·(0 0 0 1)                                       = 0     0     0     1
      banco:   0,269·(0 0 0 1) + 0,731·(1 1 0 1)                = 0.731 0.731 0     1
      aguanta: 0,186·(0 0 0 1) + 0,307·(1 1 0 1) + 0,506·(1 0 1 2) = 0.814 0.307 0.506 1.506
```

**8. Residual, Z = X + (A·V)·Wo.**
- Razón: se suma la entrada original a lo que aportó la atención.
- Utilidad: la identidad del token no se pierde, y los gradientes pasan directo por la suma, lo que permite apilar muchas capas.

```
Z =  0      0      0      2
     1.731  1.731  0      2
     1.814  0.307  1.506  3.506
```

**9. Layer norm, LN(Z), fila por fila.**
- Razón: a cada fila se le resta su media y se divide por su desvío (ε despreciable).
- Utilidad: evita que la escala de los vectores crezca capa tras capa y mantiene el entrenamiento estable. Es independiente del tamaño del lote porque normaliza cada token por separado.

- "El": media 0,5, varianza 0,75, desvío 0,866 → [−0,577, −0,577, −0,577, 1,732].
- "banco": media 1,366, varianza 0,634, desvío 0,796 → [0,459, 0,459, −1,715, 0,797].
- "aguanta": media 1,783, varianza 1,306, desvío 1,143 → [0,026, −1,292, −0,242, 1,507].

```
LN(Z) =  -0.577 -0.577 -0.577  1.732
          0.459  0.459 -1.715  0.797
          0.026 -1.292 -0.242  1.507
```

**10. Feed-forward, FFN = ReLU(LN(Z)·W1)·W2.**
- Razón: LN(Z)·W1 calcula, en las dos primeras dimensiones, la diferencia d1 − d2 (columna 1) y d2 − d1 (columna 2). ReLU deja pasar solo lo positivo. W2 = I.
- Utilidad: la atención mezcla entre tokens y el FFN procesa cada token por separado, con una no linealidad. Sin ReLU, dos capas lineales se colapsarían en una.

- "El": d1 − d2 = 0 → ReLU(0, 0) = [0, 0].
- "banco": 0,459 − 0,459 = 0 → [0, 0].
- "aguanta": d1 − d2 = 0,026 − (−1,292) = 1,318 → ReLU(1,318, −1,318) = [1,318, 0].

```
FFN =  0      0 0 0
       0      0 0 0
       1.318  0 0 0
```

**11. Residual, H = Z + FFN.** Misma razón y utilidad que el paso 8.

```
H =  0      0      0      2
     1.731  1.731  0      2
     3.132  0.307  1.506  3.506
```

**12. Layer norm final, LN(H).** Igual que el paso 9, antes de la predicción.

```
LN(H) =  -0.577 -0.577 -0.577  1.732
          0.459  0.459 -1.715  0.797
          0.793 -1.405 -0.472  1.084
```

**13. Predicción.** Se usa la última fila: logits = [0,793, −1,405, −0,472, 1,084]·Wout.
- Razón: la última posición es la que predice la palabra siguiente. Wout proyecta los 4 valores a una puntuación por palabra del vocabulario, y el softmax las vuelve probabilidades.
- Utilidad: es la salida del modelo: una distribución sobre las seis palabras.

Logits = [El 0, banco 0, aguanta −0,472, presta −0,472, peso 1,585, dinero −2,810] (peso = 2·0,793; dinero = 2·(−1,405); aguanta = presta = −0,472).

Exponenciales: 1, 1, 0,624, 0,624, 4,879, 0,060; suma 8,187.

| El | banco | aguanta | presta | **peso** | dinero |
|---|---|---|---|---|---|
| 0,122 | 0,122 | 0,076 | 0,076 | **0,596** | 0,007 |

**"El banco aguanta" → "peso" (probabilidad 0,596).**

### Frase 2: "El banco presta"

El único cambio es la tercera palabra: X = [0 1 1 2] (presta = 0 1 1 0, más P = 0 0 0 2). Las dos primeras filas no cambian, porque la máscara impide que miren a la tercera palabra.

| | Q = V = X | K |
|---|---|---|
| El | 0 0 0 1 | 0 0 0 0 |
| banco | 1 1 0 1 | 1 1 0 0 |
| presta | 0 1 1 2 | 1 2 0 0 |

S = [[0,0,0],[0,2,3],[0,1,2]] (idéntica a la frase 1: S[banco, presta] = 1·1 + 1·2 = 3), así que **A es la misma** que en la frase 1.

```
A·V:  0 0 0 1 / 0.731 0.731 0 1 / 0.307 0.814 0.506 1.506
Z  =  0 0 0 2 / 1.731 1.731 0 2 / 0.307 1.814 1.506 3.506
LN(Z) = -0.577 -0.577 -0.577 1.732 / 0.459 0.459 -1.715 0.797 / -1.292 0.026 -0.242 1.507
FFN: la última fila tiene d1 − d2 = −1,292 − 0,026 = −1,318 → ReLU(−1,318, 1,318) = [0, 1,318]
H  =  0 0 0 2 / 1.731 1.731 0 2 / 0.307 3.132 1.506 3.506
LN(H) última fila = -1.405  0.793 -0.472  1.084
```

Logits = [0, 0, −0,472, −0,472, **−2,810, 1,585**] → **"El banco presta" → "dinero" (probabilidad 0,596)**; peso 0,007.

---

## Parte B: la misma atención sin máscara (encoder)

Pasos 5 a 9 sin máscara. Los pasos 1 a 4 son los mismos de la parte A.

**Paso 5 (sin máscara):** no se pone −∞. Razón y utilidad: cada token puede mirar a todos, anteriores y posteriores; es lo que se necesita para *comprender* un texto ya completo.

**Paso 6, A (frase 1 y 2, es la misma):**
- "El": scores [0, 0, 0] → [0,333, 0,333, 0,333].
- "banco": [0, 1, 1,5] → exponenciales 1, 2,718, 4,482, suma 8,200 → [0,122, 0,331, 0,547].
- tercera palabra: [0,186, 0,307, 0,506] (igual que en la parte A, porque ya miraba a todos).

**Frase 1, "El banco aguanta":**
```
A·V = 0.667 0.333 0.333 1.333 / 0.878 0.331 0.547 1.547 / 0.814 0.307 0.506 1.506
Z   = 0.667 0.333 0.333 2.333 / 1.878 1.331 0.547 2.547 / 1.814 0.307 1.506 3.506
LN(Z) = -0.302 -0.704 -0.704 1.709 / 0.412 -0.333 -1.403 1.323 / 0.026 -1.292 -0.242 1.507
```
**Fila de "banco" en LN(Z): [0,412, −0,333, −1,403, 1,323].**

**Frase 2, "El banco presta":**
```
A·V = 0.333 0.667 0.333 1.333 / 0.331 0.878 0.547 1.547 / 0.307 0.814 0.506 1.506
Z   = 0.333 0.667 0.333 2.333 / 1.331 1.878 0.547 2.547 / 0.307 1.814 1.506 3.506
LN(Z) = -0.704 -0.302 -0.704 1.709 / -0.333 0.412 -1.403 1.323 / -1.292 0.026 -0.242 1.507
```
**Fila de "banco" en LN(Z): [−0,333, 0,412, −1,403, 1,323].**

---

## Preguntas

**1. ¿En cuál de las dos partes el vector de "banco" cambia según la frase?**
En la **parte B**. En la parte A la fila de "banco" en LN(Z) es la misma en las dos frases ([0,459, 0,459, −1,715, 0,797]); en la B es [0,412, −0,333, ...] contra [−0,333, 0,412, ...]: se invierten las dos primeras dimensiones (objeto físico y dinero), que es la diferencia entre "aguanta" y "presta". Con la máscara causal "banco" solo ve a "El" y a sí mismo, que son iguales en las dos frases. Sin máscara también ve la palabra que sigue, y esa le cambia el significado.

**2. En la parte A, ¿cómo "sabe" el modelo si predecir "peso" o "dinero" si "banco" es el mismo?**
Porque la predicción sale de la **última fila**, la de la tercera palabra, que sí es distinta ("aguanta" o "presta"). Esa fila mira a "banco" (con peso 0,307) y a sí misma (0,506), y arrastra su propio vector: "aguanta" tiene d1 alto (objeto) y el FFN lo refuerza (d1 − d2 = 1,318), lo que lleva a "peso". "presta" tiene d2 alto (dinero), y el FFN refuerza d2 → "dinero". El contexto de "banco" llega a la última posición por atención; no hace falta que "banco" cambie.

**3. ¿La predicción de la parte A y la de la B para la última posición son iguales o distintas?**
**Iguales** (peso/dinero con probabilidad 0,596). La máscara causal solo bloquea que un token mire a los que vienen *después*. La última fila no tiene nada posterior, así que mira a los mismos tres tokens con y sin máscara, y como layer norm, residual y FFN actúan fila por fila, el resultado es idéntico. La máscara solo cambia las filas anteriores.

**4. ¿Qué modelo de la clase se parece a la parte A y cuál a la B? ¿Para qué se usa cada uno?**
La parte A se parece a un **decoder** (GPT, Claude, Llama): predice la palabra siguiente, con máscara causal; se usa para *generar* texto. La parte B se parece a un **encoder** (BERT): cada token ve todo el contexto, a ambos lados; se usa para *comprender* y producir embeddings (clasificación, búsqueda semántica, como el e5 que usamos en el RAG).

**5. Si P fuera todo ceros, ¿qué cambiaría? ¿Y si el orden cambia el sentido?**
Los números cambiarían (se verifica con `verificar.py` poniendo P en 0): X ya no lleva el +1 y +2 en d4. Las predicciones siguen siendo "peso" y "dinero", ahora con más confianza (0,859), porque en este ejercicio el sentido lo da el contenido de las palabras y no su posición. Pero sin P el modelo no distingue el orden. En el encoder, permutar las palabras solo permuta las filas de salida (comprobado: "aguanta banco El" da las mismas filas en otro orden), así que "el perro mordió al hombre" y "el hombre mordió al perro" serían indistinguibles. En el decoder la máscara introduce algo de orden (cada token solo ve a los anteriores), pero es una pista débil e indirecta. Por eso los modelos agregan información de posición.
