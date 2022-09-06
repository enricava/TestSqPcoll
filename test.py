from math import log2
import random
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

def simul(d, l):
    if d < l: return
    particion = random.sample(range(1, d+1), l-1)
    l = l-1
    particion.sort()
    mi = [particion[0]] + [particion[i] - particion[i-1] for i in range(1,l)] + [d - particion[l-1]]
    drr = d/l
    pcoll = sum([mi[i]*(mi[i]-1) for i in range(l)])
    sq = sum([mi[i]*log2(mi[i]) for i in range(l)])/d
    return drr, pcoll, sq

pearsons = []
l = 10000
for i in range(1,8):
    drrs = []
    pcolls = []
    sqs = []
    for k in range(30):
        t_entrada = 10**(5+i)
        #t_salida = l
        t_salida = l*i
        res = simul(t_entrada, t_salida)
        drrs.append(res[0])
        pcolls.append(res[1])
        sqs.append(res[2])
    pearsons.append((t_entrada, t_salida, stats.pearsonr(pcolls, sqs)))

df = pd.DataFrame(columns=['t_entrada', 't_salida', 'pearson_corr', 'p_value'])
df['t_entrada'] = [p[0] for p in pearsons]
df['t_salida'] = [p[1] for p in pearsons]
df['pearson_corr'] = [p[2][0] for p in pearsons]
df['p_value'] = [p[2][1] for p in pearsons]

print(df.to_latex(index=False))

#plt.plot([i for i in range(len(df['t_entrada']))], df['pearson_corr'])
#plt.savefig('increasing.png')
