
# Ejercicio 2
## ¿Qué operaciones de resumen realizadas por los reducers se ven beneficiados por la definición de funciones de comparación personalizadas?
GROUP BY + agregación (ej. sumas, conteos, promedios).

Un comparador de shuffle puede agrupar claves equivalentes bajo un mismo criterio (ej. mayúsculas = minúsculas, agrupar por la primer letra, agrupar por ID de cliente sin importar el prefijo).
DISTINCT.

Un comparador puede unificar tuplas que son “distintas en el valor crudo” pero equivalentes según un criterio (ej. “Juan Pérez” y “JUAN PÉREZ”).
JOINs.

Comparadores son fundamentales: en shuffle garantizan que todos los registros con el mismo identificador vayan al mismo reducer; en sort permiten que lleguen ordenados de cierta manera (ej. primero el cliente y después sus cuentas).
Ordenamientos previos a agregados complejos.

Por ejemplo, calcular mínimos/máximos o consolidar en orden temporal.
En general: todo resumen que requiera agrupar o consolidar datos equivalentes bajo reglas distintas de la igualdad exacta de claves.

# ¿Qué consideraciones habría que tener en cuenta relacionado con la tarea de los mappers?
Definición de la clave intermedia: El mapper debe emitir las claves de forma consistente con el criterio que luego aplicarán los comparadores. Ejemplo: si el comparador de shuffle agrupa por la primer letra, el mapper debe emitir como clave la palabra o un prefijo de ella.

Etiquetado para joins: En joins 1:1 o 1:n es clave que el mapper agregue etiquetas (“C” para cliente, “CA” para caja) porque el comparador por sí solo no distingue el origen.

Minimizar datos: Emitir solo lo necesario (filtrado y proyección) para no sobrecargar shuffle/sort.

Consistencia en el formato: Si se usan claves compuestas (tuplas), el mapper debe respetar esa estructura (ej. (“C”, id_cliente) vs (“CA”, id_cliente)).