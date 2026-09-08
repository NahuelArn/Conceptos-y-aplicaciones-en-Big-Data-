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
    c=c+1
  context.write(key, c)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()
