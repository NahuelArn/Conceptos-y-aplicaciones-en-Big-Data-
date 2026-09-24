from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"
#armo las keys y values para el map
def fmap(key, value, context):
  words = value.split()
  for char in value.lower():
    if char in "aeiou":
      context.write("vocales", 1)
    elif char in "bcdfghjklmnpqrstvwxyz":
      context.write("consonantes", 1) 
    elif char in "0123456789":
      context.write("numeros", 1)
    else:
      context.write("otros", 1)
#laburo sobre los grupos de values para el reduce
def fred(key, values, context):
  c=0
  for v in values:
    c=c+1
  context.write(key, c)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()