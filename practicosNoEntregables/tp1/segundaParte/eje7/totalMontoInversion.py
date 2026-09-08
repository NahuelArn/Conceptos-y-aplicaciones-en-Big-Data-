from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"
def fmap(key, value, context):
  campos = value.strip().split()
  monto = float(campos[4])
  context.write(1, monto)
def fred(key, values, context):
  total = sum(values)
  context.write("Total monto invertido", total)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()