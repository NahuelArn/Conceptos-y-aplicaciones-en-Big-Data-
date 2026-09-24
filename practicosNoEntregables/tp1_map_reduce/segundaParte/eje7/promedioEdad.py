from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap (key, value, context):
  campos = value.strip().split()
  edad = 2026 - int(campos[3])
  context.write(1, edad)

def fred(key, values, context):
  total = 0
  cant = 0
  for edad in values:
    total += edad 
    cant+=1
  
  promedio = total / cant
  context.write("Promedio de edad", promedio)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion() 