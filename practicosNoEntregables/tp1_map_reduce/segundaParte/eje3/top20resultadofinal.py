from MRE import Job
root_path = "./"
inputDir = root_path + "input2/"
outputDir = root_path + "output2/"
def fmap(key, value, context):
  context.write(key, value)

# def fred(key, values, context):
#   #keys nombres
#   #value cantidad de veces que aparece el nombre
#   c=0
#   for v in values:
#     c=c+1
#   context.write(key, c)

# job = Job(inputDir, outputDir, fmap, fred)
# success = job.waitForCompletion()