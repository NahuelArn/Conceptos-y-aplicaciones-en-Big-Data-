from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(key, value, context):
    dni = key
    values = value.strip().split()
    nombre = values[0]
    año = values[3]
    invertido = values[4]
    context.write("completo", (nombre, dni, 2026-int(año), invertido))

def fred(key, values, context):
    suma_edades = 0
    total_personas = 0
    max = -1
    nombre_max = ""
    total_invertido = 0
    for nombre, dni, edad, invertido in values:
        if edad > max:
            max = int(dni)
            nombre_max = nombre
        suma_edades = suma_edades + int(edad)
        total_personas = total_personas + 1
        total_invertido = total_invertido + int(invertido)
    context.write("inversionista mas joven", (nombre_max, max))
    context.write("total_invertido", total_invertido)
    context.write("promedio de edades", suma_edades/total_personas)
    

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion() 