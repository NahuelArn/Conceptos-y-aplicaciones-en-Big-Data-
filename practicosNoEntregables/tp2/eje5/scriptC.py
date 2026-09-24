# c. La página más visitada (en cuanto a cantidad de visitas, sin importar el tiempo 
# de permanencia) por todos los usuarios. 

from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "outputCtemp/"

inputDir2 = outputDir  
outputDir2 = root_path + "outputCfinal/"


# JOB 1

def fmap(key, value, context):
    pagina = value.split()[0]
    context.write(pagina, 1)

def fred(key, values, context):
    c = 0
    for v in values:
        c = c + int(v)
    context.write(key, c)

job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()

# JOB 2

def fmap(key, value, context):
    context.write("total", (key, value))

def fred(key, values, context):
    max  = -1
    max_page = None
    for v in values:
        id_page, visitas = v
        if int(visitas) > max:
            max = int(visitas)
            max_page = id_page
    context.write(key, (max_page, max))


job = Job(inputDir2, outputDir2, fmap, fred)
job.setCombiner(fred)
success = job.waitForCompletion()