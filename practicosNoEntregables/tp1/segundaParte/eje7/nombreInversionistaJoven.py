from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"
#dni,nombres,fecha de nacimiento (día, mes y año 
#como  campos  separados)  e  importe  invertido  por  diferentes  personas 

  #cuando se me pide el X mas joven o El mas alto etc etc.. se tiene que hacer
  #sobre un unico reducer, ya que los datos tiene que ser comparados entre si

def fmap(key, value, context):
    campos = value.strip().split()
    # dni,nombre, dia, mes, anio, importe = campos
    nombre = campos[0]
    dia = (campos[1])
    mes = (campos[2])
    anio = (campos[3])
    fecha = int(anio.zfill(4) + mes.zfill(2) + dia.zfill(2))
    context.write(1, (nombre, fecha))


def fred(key, values, context):
    max_fecha = -1
    nombre_joven = ""
    for nombre, fecha in values:
        if fecha > max_fecha:
            max_fecha = fecha
            nombre_joven = nombre
    context.write("Inversionista más joven", nombre_joven)


job = Job(inputDir, outputDir, fmap, fred)
success = job.waitForCompletion()
