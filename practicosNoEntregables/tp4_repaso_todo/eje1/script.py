from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def map(key, values, context):
    words = values.split()
    for w in words:
        context.write(w[0], 1)

def reduce(key, values, context):
    c = 0
    for v in values:
        c += 1
    # normalizamos a minúscula para el output
    context.write(key.lower(), c)
#comparador de si A = a | b = B | c = C etc...
# --- Comparadores case-insensitive ---
def shuffle_case_insensitive(k1, k2):
    if k1.lower() == k2.lower():
        return 0
    elif k1.lower() < k2.lower():
        return -1
    else:
        return 1
#orden quein aparece primero A, b c, d etc... o sino podria tener una salida tipo b, c ,z, a
def sort_case_insensitive(k1, k2):
    if k1.lower() == k2.lower():
        return 0
    elif k1.lower() < k2.lower():
        return -1
    else:
        return 1

# Configuración del job
job = Job(inputDir, outputDir, map, reduce)
job.setShuffleCmp(shuffle_case_insensitive)
job.setSortCmp(sort_case_insensitive)

success = job.waitForCompletion()
