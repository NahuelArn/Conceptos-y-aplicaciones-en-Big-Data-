# 1) El dataset Jacobi tiene los coeficientes de un sistema de 15 ecuaciones de 15 
# incógnitas.  Las  ecuaciones  en  el  archivo  ya  están  "despejadas"  como  lo  requiere  el 
# método de Jacobi. Cada línea del archivo posee: 
#  <var_N, term_ind, coef_var1, coef_var2, ... , coef_ var15> 
# Por simplicidad, para cada variable N su correspondiente coeficiente es cero. 
# Implemente  en  MapReduce  el  cálculo  del  método  de  Jacobi  para  la  solución  del 
# sistema de ecuaciones dado. 


#  <var_N, term_ind, coef_var1, coef_var2, ... , coef_ var15> 

from MRE import Job
root_path = "./"
inputDir = root_path + "input/"
outputDir = root_path + "output/"

def fmap(var, value, context):
    cols = value.strip().split('\t')
    b = float(cols[1])            # término independiente
    coefs = [float(c) for c in cols[2:]]  # coeficientes
    x_prev = context["x_prev"]    # vector de la iteración anterior

    # índice de la variable actual (var1 → 0, var2 → 1, …)
    #idx = int(var.replace("var", "")) - 1

    # Jacobi: xᵢ^(k+1) = bᵢ - Σⱼ aᵢⱼ * xⱼ^(k)
    total = b
    for j, aij in enumerate(coefs):
        total -= aij * x_prev[j]

    context.write(var, total)

def fred(var, values, context):
    for v in values:
        context.write(var, v)

# ejemplo: vector inicial todo en 0
x0 = [0.0] * 15

params = {"x_prev": x0}
job = Job(inputDir, outputDir, fmap, fred)
job.setParams(params)
job.waitForCompletion()