# 4) Utilice  el  dataset  Libros  para  implementar  una  aplicación  MapReduce  que  devuelva 
# como salida todos los párrafos que tienen una longitud mayor al promedio. 


#CADA LINEA DEL DATASET ES UN PARRAFO

from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

inputDir2 = outputDir  #lo uso de entrada
outputDir2 = root_path + "output2/"
#funcion map       IDENTIDAD 
#Si yo se que por cada linea se va ejcutar un maper
# y que cada linea representa un parrafo, entonces puedo usar la funcion map para contar la cantidad de palabras de cada parrafo y devolverla al reducer, para que el reducer pueda calcular el promedio de palabras por parrafo.
def fmap(key, value, context):
    size = len(value)
    context.write(1, (size))
        
#funcion reduce       
def fred(key, values, context):
    #osea aca vos recibis... una lista que cada valor representa la cantidad de palabras de cada parrafo...
    sum = 0 #sumas la cantidad de (ya calculada) palabras de cada parrafo
    prom = 0
    cant = 0 #contatas la cantidad de parrafos
    for v in values:
        sum = sum + int(v)
        cant += 1
    prom = sum / cant # cantidad total de palabras de todos los parrafos / cantidad de parrafos = promedio de palabras por parrafo
    context.write("prom:", prom)

#funcion combiner
#No usamos al combiner, si sabemos que vamos a tener un solo reducer, no tiene sentido usarlo, ya que el combiner se usa para reducir la cantidad de datos que se envian al reducer, pero si tenemos un solo reducer, no hay necesidad de reducir los datos antes de enviarlos al reducer. O tal vez si... Hotel? Trivago

job = Job(inputDir, outputDir, fmap, fred)
# job.setCombiner(fcom) 
success = job.waitForCompletion()


# JOB 2: COSAS


import math

promedio = 0
from pathlib import Path

archivo_stats = Path(inputDir2) / "output.txt"

with open(archivo_stats, "r", encoding="utf-8") as f:
    for linea in f:
        clave, valor = linea.strip().split("\t")
        if clave == "prom:":
            promedio = float(valor)

# JOB 2

def fmap(key, value, context):
    if len(value) > promedio:
        context.write("parrafo", value)

def fred(key, values, context):
    for parrafo in values:
        context.write(len(parrafo), parrafo)

job2 = Job(inputDir, outputDir2, fmap, fred)
success = job2.waitForCompletion()

# La secuencia es:

# Job 1 calcula el promedio.
# Job 1 lo guarda en output/output.txt.
# El programa abre ese archivo.
# Lee el promedio y lo guarda en promedio.
# Job 2 compara cada párrafo contra ese promedio.