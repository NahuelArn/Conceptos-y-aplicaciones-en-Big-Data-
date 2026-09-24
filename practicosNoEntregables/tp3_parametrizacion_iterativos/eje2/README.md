# Ejercicio 2: Metodo de Jacobi con MapReduce

## Idea general

El objetivo es resolver un sistema de ecuaciones usando el metodo iterativo de Jacobi.

En este ejercicio, los datos no tienen una ecuacion completa por linea. Cada termino de una ecuacion aparece en una tupla diferente:

```text
incognita    coeficiente    valor
```

Por ejemplo:

```text
X    TI    1
X    Y     3
X    Z     0.5
```

Estas lineas representan la ecuacion despejada:

```text
X = 1 - 3Y - 0.5Z
```

`TI` significa termino independiente. Las otras etiquetas (`Y`, `Z`, etc.) indican que el valor es un coeficiente asociado a esa incognita.

## Como funciona Jacobi

Jacobi calcula nuevos valores usando los valores de la iteracion anterior. Primero se elige una aproximacion inicial:

```python
x0 = {"X": 0.0, "Y": 0.0, "Z": 0.0}
```

En cada iteracion se calcula cada incognita con la formula:

```text
nuevo valor = termino independiente - suma de las contribuciones
```

Los valores nuevos se usan como valores anteriores en la siguiente iteracion.

El flujo general es:

```text
Valores iniciales
        |
        v
Mapper: calcula contribuciones
        |
        v
Agrupacion por incognita
        |
        v
Reducer: calcula el nuevo valor
        |
        v
Nuevos valores
```

## Que recibe el Mapper

Para una linea como:

```text
X    Y    3
```

`MRE` llama al Mapper aproximadamente asi:

```python
incog = "X"
value = "Y\t3"
```

El codigo separa el valor usando el tabulador:

```python
parts = value.strip().split("\t")
coef, val = parts
val = float(val)
```

En este caso queda:

```python
coef = "Y"
val = 3.0
```

El Mapper tambien recibe por parametros el vector de la iteracion anterior:

```python
x_prev = context["x_prev"]
```

Por ejemplo:

```python
x_prev = {"X": 0.0, "Y": 2.0, "Z": 4.0}
```

## Funcion Mapper

```python
def fmap(incog, value, context):
    parts = value.strip().split("\t")
    coef, val = parts
    val = float(val)
    x_prev = context["x_prev"]

    if coef == "TI":
        context.write(incog, ("TI", val))
    else:
        contrib = val * x_prev.get(coef, 0.0)
        context.write(incog, ("SUM", contrib))
```

Hay dos casos:

### Termino independiente

Para:

```text
X    TI    1
```

el Mapper emite:

```python
("X", ("TI", 1.0))
```

### Coeficiente de otra variable

Para:

```text
X    Y    3
```

si `Y` vale `2` en la iteracion anterior:

```python
contrib = 3 * 2
```

El Mapper emite:

```python
("X", ("SUM", 6.0))
```

La contribucion representa el termino `3Y` de la ecuacion.

## Agrupacion antes del Reducer

MapReduce agrupa automaticamente todos los valores que tienen la misma clave. Como el Mapper usa la incognita de la ecuacion como clave, el Reducer recibe todos los terminos de esa ecuacion juntos.

Por ejemplo, para `X` puede recibir:

```python
key = "X"
values = [
    ("TI", 1.0),
    ("SUM", 6.0),
    ("SUM", 2.0)
]
```

No se arma esa lista manualmente. La crea MapReduce agrupando las salidas de los Mappers por clave.

## Funcion Reducer

```python
def fred(incog, values, context):
    b = 0.0
    suma = 0.0

    for tag, v in values:
        if tag == "TI":
            b = v
        else:
            suma += v

    nuevo = b - suma
    context.write(incog, nuevo)
```

El Reducer separa el termino independiente de las contribuciones. Luego calcula:

```text
nuevo = termino independiente - suma de contribuciones
```

Por ejemplo:

```text
b = 1
suma = 6 + 2
nuevo X = 1 - 8 = -7
```

La salida seria:

```text
X    -7
```

## Primera iteracion con todos los valores en cero

Si se comienza con:

```python
x_prev = {"X": 0.0, "Y": 0.0, "Z": 0.0}
```

todas las contribuciones de las variables son cero. Para este ejemplo:

```text
X = 1 - 3*0 - 0.5*0 = 1
Y = -4 - 0.1*0 - 0.1*0 = -4
Z = 1 - 0.5*0 - 0.5*0 = 1
```

La primera iteracion produce aproximadamente:

```text
X    1
Y    -4
Z    1
```

## Ejecucion actual

El Job recibe el vector inicial mediante parametros:

```python
params = {"x_prev": x0}
job = Job(inputDir, outputDir, fmap, fred)
job.setParams(params)
job.waitForCompletion()
```

Esto ejecuta una sola iteracion de Jacobi.

Para resolver completamente el sistema, hay que repetir el Job. En cada vuelta se debe:

1. Leer los valores producidos por la iteracion anterior.
2. Construir un nuevo diccionario `x_prev`.
3. Pasarlo nuevamente a los Mappers y Reducers mediante `setParams`.
4. Repetir hasta alcanzar una cantidad de iteraciones o hasta que los valores casi no cambien.

## Importante

El metodo de Jacobi usa los valores de la iteracion anterior para calcular todos los valores nuevos. No debe actualizarse `x_prev` mientras se esta calculando la misma iteracion. Todos los Mappers deben trabajar con el mismo vector anterior.

El codigo actual realiza correctamente el calculo de una iteracion, pero todavia no contiene el ciclo que repite el proceso hasta converger.
