from MRE import Job 
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(key, value, context):
    if key == 0:
        context.write("titulo", value)

def fred(key, values, context):
    for v in values:
        context.write(key, v)
job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()