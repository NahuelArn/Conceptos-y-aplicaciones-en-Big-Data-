
### 3. Cómo plantearía una solución MapReduce al siguiente algoritmo secuencial:

```
i. entrada
	datos: array [1..N] of <int1, int2, ..., intM>
```

```
ii. algoritmo
error = 0.001; dif = 1; K=5; M=5
prom = [ 0, 0, 0, 0, 0 ]; N=len(lines)
for t in lines:
    v = t.split("\t")
    for m in range(M):
        prom[m] = prom[m] + float(v[m])
C = []

for m in range(K):
    e=[]
    for m in range(M):
        e.append( prom[m] / N + random.random())
    C.append(e)

while dif > error:
    S=[]
    for m in range(K):
        S.append([ [0,0,0,0,0], 0 ])
    for t in lines:
        v = t.split("\t")
        min=9999999
        for q in range(K):
            a=0
            for m in range(M):
                a=a + (C[q][m] - float(v[m]))**2
            if(a < min):
                min = a
            Q = q

    for m in range(M):
        S[Q][0][m]= S[Q][0][m] + float(v[m])
    S[Q][1] = S[Q][1] + 1

    for q in range(K):
        if S[q][1] > 0:
            for m in range(M):
                S[q][0][m]= S[q][0][m] / S[q][1]
  
    dif=0
    for q in range(K):
        for m in range(M):
        dif=dif + (S[q][0][m] - C[q][m])**2
        if(S[q][1] > 0):
            C[q][m] = S[q][0][m]
```