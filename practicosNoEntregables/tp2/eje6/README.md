## 6. Cómo plantearía una solución MapReduce a los siguientes algoritmos secuenciales:
### rta: No los plantearia 👍
```
a.
	i. entrada
		textos: array [1..N] of string (dataset libros)
	ii. algoritmo
		a={}; b={}; N = len(textos)
		for l in textos:
			words = l.split()
			for w in words:
				a[w] = a[w]+1
		for w in a.keys():
			for l in lines:
				words = l.split()
				if w in words:
					b[w]=b[w]+1
        for k in a.keys():
			print(k + " = " + str(a[w] * (N / b[w])))
```

```
b.
	i. entrada
		datos: array [1..N] of <int1, int2, ..., intM>
			(todos los valores están dentro de un rango de valores conocido, para poder usarlos como índices del tensor)
	ii. algoritmo
    	for t in datos:
        	v = t.split("\t")
            c = v[-1]
            for a in range(len(v)-1):
            	x= v[a]
				m[a][x][c] = m[a][x][c] + 1
            
          max=[[0,0,0], [0,0,0]]
          for x in range(len(m)):
          	  for y in range(len(m[0])):
              	  for z in range(2):
                	  if(m[x][y][z] > max[z][0]):
                    	  max[z][0] = m[x][y][z]
                          max[z][1]=x
                          max[z][2]=y
          for z in range(2):
			  print(z +";" + max[z][1] +";" + max[z][2])
```


a = i , b = ii fuente FabianMartinez la cabra