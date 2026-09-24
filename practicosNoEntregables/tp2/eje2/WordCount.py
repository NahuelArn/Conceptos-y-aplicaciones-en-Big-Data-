
# Implemente una función combiner para el problema del WordCount.
from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"
#funcion map       
def fmap(key, value, context):
    words = value.split()
    for w in words:
        context.write(w, 1)
#funcion reduce       
def fred(key, values, context):
    c=0
    for v in values:
        c=c+ int(v)
    context.write(key, c)

#funcion combiner
def fcom(key, values, context):
    c=0
    for v in values:
        c=c+ int(v)
    context.write(key, c)

job = Job(inputDir, outputDir, fmap, fred)
job.setCombiner(fcom) #Aca le digo, donde puede encontrar el combiner si lo quiere utilizar
#en este caso el combiner=reduce... por lo tanto podria poner directamente job.setCombiner(fred)
success = job.waitForCompletion()
