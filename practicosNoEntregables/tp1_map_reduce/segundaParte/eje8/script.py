from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(key, value, context):
    respuesta = value.strip().upper()
    bucket = random.randint(0, 32)
    context.write(f"{respuesta}_{bucket}", 1)
    #esto era el key+un identificador externo.. era como una clave compuesta de dbd

def fred(key, values, context):
    total = 0
    for v in values:
        total += v
    context.write(key, total)

job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()