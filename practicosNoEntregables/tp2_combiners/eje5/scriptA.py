# 5) El dataset website tiene información sobre el tiempo de permanencia de sus usuarios 
# en cada una de las páginas del sitio. El formato de los datos del dataset es:  
#  <id_user, id_page, time>  
# Implemente una aplicación MapReduce, utilizando combiners en los casos que 
# considere necesario, que calcule 
# a. La página más visitada (la página en la que más tiempo permaneció) para cada 
# usuario 

# 
#
#
from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "outputAtemp/"

inputDir2 = outputDir  
outputDir2 = root_path + "outputAfinal/"

# JOB 1: Calcular el tiempo total de permanencia de cada usuario en cada página

def fmap(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write((id_user, id_page), time)


def fred(key, values, context):
    total_time = 0
    for v in values:
        total_time += int(v)
    context.write(key, total_time)
    

job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()


# JOB 2: Calcular la página más visitada por cada usuario

def fmap2(key, value, context):
    id_user = key
    id_page, time = value.split()
    context.write(id_user, (id_page, time))

def fred2(key, values, context):
    max  = -1
    max_page = None
    for v in values:
        id_page, time = v
        if int(time) > max:
            max = int(time)
            max_page = id_page
    context.write(key, (max_page, max))


job = Job(inputDir2, outputDir2, fmap2, fred2)
job.setCombiner(fred2) 
success = job.waitForCompletion()
