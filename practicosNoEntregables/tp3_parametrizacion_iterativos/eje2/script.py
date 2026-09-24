# 2) Resuelva el problema del método de Jacobi con el dataset jacobi2. 
# Este dataset tiene los datos almacenados de la siguiente forma: 
#  <incognita_i, coef_i, valor> 
# Donde  para  cada  incógnita,  los términos  de  la  ecuación  correspondiente  aparecen  en 
# distintas  tuplas,  inclusive  el  término  independiente.  El  valor  de  coef_i  es,  o  bien  el 
# nombre de la incógnita afectada por el coeficiente valor, o bien el string “TI”, haciendo 
# referencia a que valor es el término independiente de dicha ecuación. Ejemplo: 
#  incognita_i coef_i  valor 
#   X TI  1 
#   X Y  3 
#   X Z  0.5 
#   Y TI  -4 
#   Y X  1/10 
#   Y Z  1/10 
#   Z TI  1 
#   Z X  1/2 
#   Z Y  1/2 
# Nota: Continúe enviando los valores de las incógnitas por parámetros a los mappers y 
# reducers, según corresponda. 


#   <incognita_i, coef_i, valor> 


from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(incog, value, context):
    # incog = primera columna (varX)
    parts = value.strip().split('\t')
    coef, val = parts
    val = float(val)
    x_prev = context["x_prev"]

    if coef == "TI":
        # término independiente b_i
        context.write(incog, ("TI", val))
    else:
        # contribución coef * x_prev[coef]
        contrib = val * x_prev.get(coef, 0.0)
        context.write(incog, ("SUM", contrib))

def fred(incog, values, context):
    b = 0.0
    suma = 0.0
    for tag, v in values:
        if tag == "TI":
            b = v
        else:
            suma += v
    nuevo = b - suma
    context.write(incog, nuevo)

# ejemplo: valores iniciales todos en 0
x0 = {"X": 0.0, "Y": 0.0, "Z": 0.0}

params = {"x_prev": x0}
job = Job(inputDir, outputDir, fmap, fred)
job.setParams(params)
job.waitForCompletion()