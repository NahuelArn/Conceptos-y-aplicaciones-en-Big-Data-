# 3) Implemente  un  job  MapReduce  para  calcular  el  máximo,  mínimo,  promedio  y  desvío 
# stándard de las ocurrencias de todas las palabras del dataset Libros. 
from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output_estadistica/"

inputDir2 = inputDir #lo uso de entrada
outputDir2 = root_path + "output_desvio_estandar/"
#funcion map       IDENTIDAD 
#Fijate aca... cuando vos queres armar tu tupla (key, value) y vos queres que el key sea la palabra y el value sea la cantidad de ocurrencias de esa palabra, vos tenes que hacer que el map te devuelva (palabra, cantidad de ocurrencias).
#key por convencion siempre va ser la primera palabra de la tupla, y value lo que sigue de esa fila.
def fmap(key, value, context):
    context.write(1, (key, value))
        
#funcion reduce       
def fred(key, values, context):
    maxStr= ""
    minStr= ""
    max = -1
    min = 999
    sum = 0
    prom = 0
    cantXpalabra = 0
    cant = 0
    # leng = len(values) big data no puedo hacer esto...
    for v in values:
        if int(v[1]) > max:
            max = int (v[1])
            maxStr =  (v[0])
        if int (v[1]) < min:
            min = int (v[1])
            minStr =  (v[0])
        sum = sum + int(v[1])
        cantXpalabra += int(v[1])
        cant += 1
    prom = sum / cant

    context.write("total_palabras:", cant)
    context.write("total_ocurrencias_x_palabra:", cantXpalabra)
    context.write("max: ", (maxStr, " con ", max))
    context.write("min: ", (minStr, " con ", min))
    context.write("prom:", prom)

#funcion combiner
#en este caso el combiner estaria al pedo... usamos el combiner
# cuando sabemos que podemos reducir la cantidad de datos a enviar al reducer, en este caso no se puede hacer eso, ya que necesitamos todos los datos para calcular el maximo, minimo y promedio.
# def fcom(key, values, context):
#     c=0
#     for v in values:
#         c=c+ int(v)
#     context.write(key, c)

job = Job(inputDir, outputDir, fmap, fred)
# job.setCombiner(fcom) 
success = job.waitForCompletion()


#Ahora necesito otra funcion map para calcular el desvio estandar, ya que el desvio estandar se calcula a partir del promedio, y el promedio se calcula a partir de la suma y la cantidad de elementos, entonces necesito una funcion map que me devuelva la suma y la cantidad de elementos para poder calcular el promedio en el reducer.

# JOB 2: Desvío estándar

import math

promedio_global = 0
cantidad_palabras = 0
from pathlib import Path

archivo_stats = Path(outputDir) / "output.txt"

# print("Ruta del archivo:", archivo_stats)
# print("Contenido del archivo:")

with open(archivo_stats, "r", encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split("\t")
        if len(partes) == 2:
            clave, valor = partes
            if clave == "prom:":
                promedio_global = float(valor)
                # print("Promedio global:", promedio_global)
            elif clave == "total_palabras:":
                cantidad_palabras = int(valor)
                # print("Cantidad de palabras:", cantidad_palabras)
        
def fmap2(key, value, context):
    frecuencia = int(value)
    dif_cuadrado = (frecuencia - promedio_global) ** 2
    context.write("desvio", dif_cuadrado)

def fcomb2(key, values, context):
    suma_parcial = 0
    for v in values:
        suma_parcial = suma_parcial + float(v)
    context.write(key, suma_parcial)

def fred2(key, values, context):
    suma_total = 0
    for v in values:
        suma_total = suma_total + float(v)
        
    # varianza = suma_total / (cantidad_palabras - 1)
    varianza = suma_total / cantidad_palabras
    desvio_estandar = math.sqrt(varianza)
    
    context.write("desvio_estandar", desvio_estandar)


job2 = Job(inputDir2, outputDir2, fmap2, fred2)
job2.setCombiner(fcomb2)
success = job2.waitForCompletion()

