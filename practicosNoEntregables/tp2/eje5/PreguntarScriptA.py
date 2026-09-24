# 5) El dataset website tiene información sobre el tiempo de permanencia de sus usuarios 
# en cada una de las páginas del sitio. El formato de los datos del dataset es:  
#  <id_user, id_page, time>  
# Implemente una aplicación MapReduce, utilizando combiners en los casos que 
# considere necesario, que calcule 
# a. La página más visitada (la página en la que más tiempo permaneció) para cada 
# usuario 

# Pensa usa la cabeza...
# 
#
#
from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "outputA/"

# inputDir2 = outputDir  
# outputDir2 = root_path + "output2/"

def fmap(key, value, context):
    context.write(key, (value[1], value[2])) # escribo la pagina como clave y el id del usuario y el tiempo como valor

def fcom (key, values, context):
    #suma
    total_time = 0
    id_page = ""
    for v in values:
        page, time = v
        total_time += int(time)
        id_page = page
    context.write(key, (id_page, total_time))

def fred(key, values, context):
    max_time = 0
    max_page = ""
    for v in values:
        page, time = v
        if int(time) > max_time:
            max_time = int(time)
            max_page = page
    context.write("usuario: " + key, ("id pagina: " + max_page, "tiempo: " + str(max_time)))

job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fcom) 
success = job.waitForCompletion()


#PREGUNTA
# EL COMBINER LO TOMAMOS COMO UN PUEDE EJECUTARSE COMO NO, ESO LO DECIDE EL EMULADOR
#AHORA AL LLEGAR AL COMBINER YO NO ME PUEDO ASEGURAR QUE ESTOY LABURANDO SOBRE UN GRUPO DE DATOS INDIVIDUALES AGRUPADOS POR UN CRITERIO... SIGO EN LA SALIDA DEL MAP.. NO ES UN REDUCER QUE LOS TENGO AGRUPADOS X KEY
# Por lo tanto este ejercicio tendria que realizarse por 2 Jobs, uno que haga el map y el combine y otro que haga el reduce final.