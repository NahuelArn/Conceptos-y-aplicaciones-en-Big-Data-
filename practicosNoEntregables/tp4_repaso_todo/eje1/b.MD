# b. ¿Cuántos reducers se ejecutan en este problema? Sabiendo que se cuenta con el doble de nodos para la tarea de reduce
En este caso, la clave es la primera letra de cada palabra. Eso significa que habrá como máximo 26 claves diferentes (a–z). Por lo tanto, se ejecutará un reducer por cada letra presente en los datos. Si el dataset solo tiene palabras con 10 letras distintas, entonces habrá 10 reducers efectivos; si están las 26 letras, serán 26.

# ¿Cómo podría usar los comparadores para aprovechar todos los nodos?

Si contamos con el doble de nodos de reduce (más de los 26 posibles), algunos quedarían ociosos porque no hay más de 26 claves naturales. Para aprovecharlos, se puede:

Particionar las claves en sub-claves, por ejemplo transformar la letra A en (A,0) y (A,1) según un criterio (hash, posición, etc.).
Usar un comparador de Shuffle que considere equivalentes todas las sub-claves con la misma letra (A0 y A1 se agrupan luego como “A”), pero que en la fase de distribución permita repartir la carga entre distintos reducers. De esta forma, se paraleliza más el trabajo y luego se consolidan los resultados parciales.