from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(key, value, context):
    if value == ("muy satisfecho"):
      context.write("muy satisfecho", 1)
    elif value == "algo satisfecho":
      context.write("algo satisfecho", 1)
    elif value == "poco satisfecho":
      context.write("poco satisfecho", 1)
    elif value == "disconforme":
      context.write("disconforme", 1)
    elif value == "muy disconforme":
      context.write("muy disconforme", 1) 
    else :
      context.write("otros", 1)

def fred(key, values, context):
  cont = 0
  for v in values:
    cont = cont + 1
  context.write(key, cont)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()