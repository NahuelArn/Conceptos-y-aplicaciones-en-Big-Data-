
# Explicacion eje1, de como funciona el Mapper y el Reducer con Jacobi
Tomemos esta línea:

```text
var1    1    0    0.3    0.16    0.17    -0.13    ...
```

`MRE` separa solo por el primer tabulador:

```python
var  = "var1"
value = "1\t0\t0.3\t0.16\t0.17\t-0.13\t..."
```

Entonces, dentro del Mapper:

```python
cols = value.strip().split("\t")
```

queda:

```python
cols = [
    "1",      # término independiente
    "0",      # coeficiente de var1
    "0.3",    # coeficiente de var2
    "0.16",   # coeficiente de var3
    "0.17",   # coeficiente de var4
    "-0.13",  # coeficiente de var5
    ...
]
```

Por eso, en tu código actual hay un desplazamiento incorrecto:

```python
b = float(cols[1])
coefs = [float(c) for c in cols[2:]]
```

Debería ser:

```python
b = float(cols[0])
coefs = [float(c) for c in cols[1:]]
```

Porque `cols[0]` es el término independiente.

El Mapper corregido sería:

```python
def fmap(var, value, context):
    cols = value.strip().split("\t")

    b = float(cols[0])
    coefs = [float(c) for c in cols[1:]]
    x_prev = context["x_prev"]

    total = b

    for j, aij in enumerate(coefs):
        total -= aij * x_prev[j]

    context.write(var, total)
```

### Primera línea: `var1`

Entrada:

```text
var1    1    0    0.3    0.16 ...
```

Se interpreta como:

```python
var = "var1"
b = 1.0
coefs = [0.0, 0.3, 0.16, ...]
x_prev = [0.0, 0.0, ..., 0.0]
```

Comienza:

```python
total = 1.0
```

Luego recorre los coeficientes:

```python
j = 0
aij = 0.0
total -= 0.0 * x_prev[0]
total = 1.0
```

Después:

```python
j = 1
aij = 0.3
total -= 0.3 * x_prev[1]
total = 1.0
```

Como todos los valores iniciales son cero, todos los productos dan cero:

```text
var1 nueva = 1.0
```

El Mapper emite:

```text
var1    1.0
```

### Segunda línea: `var2`

Entrada:

```text
var2    -4    0.05    0    -0.08 ...
```

Se interpreta como:

```python
var = "var2"
b = -4.0
coefs = [0.05, 0.0, -0.08, ...]
x_prev = [0.0, 0.0, ..., 0.0]
```

Comienza:

```python
total = -4.0
```

Todos los productos vuelven a ser cero:

```text
var2 nueva = -4.0
```

El Mapper emite:

```text
var2    -4.0
```

### Resultado de la primera iteración

Con:

```python
x0 = [0.0] * 15
```

se obtiene aproximadamente:

```text
var1 -> 1.0
var2 -> -4.0
```

Y así sucesivamente para las 15 ecuaciones.

El Reducer recibe cada variable y su valor:

```python
def fred(var, values, context):
    for value in values:
        context.write(var, value)
```

Por ejemplo:

```python
fred("var1", [1.0], context)
```

y escribe:

```text
var1    1.0
```

Importante: con tu código original, `var1` habría quedado mal calculada porque tomabas:

```python
b = cols[1]
```

es decir, usabas el primer coeficiente `0` como término independiente.