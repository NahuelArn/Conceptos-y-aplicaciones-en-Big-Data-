# El dataset website tiene información sobre el tiempo de permanencia de sus usuarios 
# en cada una de las páginas del sitio. El formato de los datos del dataset es:  
#  <id_user, id_page, time>  
# Implemente una aplicación MapReduce, utilizando combiners en los casos que 
# considere necesario, que calcule 

# b. El usuario que más páginas distintas visitó 

from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "outputBtemp/"

inputDir2 = outputDir  
outputDir2 = root_path + "outputBfinal/"


# JOB 1

def fmap(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write(id_user, id_page)

#SET() estructura de datos que no permite elementos repetidos, por lo que es ideal para contar paginas distintas... AMAZING
#aca en la entrada del combiner, agrupa valores por key, internamente.. (pero sigue siendo en un sola salida del mapper)
def fcomb(key, values, context):
    paginas_visitadas = set()
    for v in values:
        paginas_visitadas.add(v)
    #aca ya se tiene un set de paginas distintas, y se puede pasar al reducer
    #esta parte esta medio al pedo... solo gano creo que eficiencia? key X reducers, tengo mas reducers, menos tiempo de espera, pero no cambia el resultado final
    for p in paginas_visitadas:
        context.write(key, p)

def fred(key, values, context):
    paginas_visitadas = set()
    for v in values:
        paginas_visitadas.add(v)
    context.write(key, len(paginas_visitadas))
    

job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()

# JOB 2

def fmap(key, value, context):
    id_user = key
    paginas_visitadas = value
    context.write("total", (id_user, paginas_visitadas))
#saco un maximo, ligado una kety y la muestro
def fred(key, values, context):
    max_paginas = -1
    max_user = None
    for v in values:
        id_user, paginas_visitadas = v
        if int(paginas_visitadas) > max_paginas:
            max_paginas = int(paginas_visitadas)
            max_user = id_user
    context.write(key, (max_user, max_paginas))

job = Job(inputDir2, outputDir2, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()