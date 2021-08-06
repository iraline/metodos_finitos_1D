import numpy as np
import matplotlib.pyplot as mat

#Constante
e0 = 8.85*(10**(-12)) #permissividade no vácuo

#Questao_3 - Aproximação para o potencial entre as placas
L = 0.02 # lado do capacitor em metros
d1 = 0.001 #largura do dieletrico 1 em metros
d2 = 0.001 #largura do dieletrico 2 em metros
e1 = 2 #permissividade do dieletrico 1
e2 = 4 #permissividade do dieletrico 2
V0 = 1 #Tensão
nSeg = 11 #quantidade de segmentos
Vn = 0 #Tensão
l = (d1+d2)/nSeg

# matrizes sem estar no formato reduzido
matSistema = np.zeros(shape=(nSeg , nSeg))
matV = np.zeros(shape=(nSeg-2, 1))
matSaida = np.zeros(shape=(nSeg, 1))

# matriz reduzida
matSistemaR = np.zeros(shape=(nSeg - 2, nSeg - 2))

"""
Retorna a permissividade do segmento que está sendo passado como parâmetro

:param nSeg: int (numero de Segmentos)
:param seg: int (segmento atual)
:param d1: float (largura dieletrico 1)
:param d2: float (largura dieletrico 2)

:return permissividade
"""
def verificaPermissividade(nSeg, seg, d1, d2):
    if (seg*((d1+d2)/nSeg)) < d1:
        return e1
    else:
        return e2

#Preenchendo a matriz das tensões
matV[0][0] = -(e0/l) * (verificaPermissividade(nSeg,0,d1,d2)*V0)
matV[nSeg-3][0] = -(e0/ l) * (verificaPermissividade(nSeg,nSeg-1,d1,d2)*Vn)

#A matriz será preenchida sempre tendo como referencia sua diagonal principal, por isso será preenchida apenas quando i==j
for i in range(nSeg):
    for j in range(nSeg):
        if i == j:
            if i == 0:
                matSistema[i][j] = -(e0/l) * verificaPermissividade(nSeg,i,d1,d2)
            if i != 0:
                matSistema[i][j] = -((e0/l) * verificaPermissividade(nSeg,i,d1,d2)) - ((e0/l) * verificaPermissividade(nSeg,i+1,d1,d2))
            if i >= 1:
                matSistema[i-1][j] = (e0/l) * verificaPermissividade(nSeg,i,d1,d2)
            if i <= nSeg-2:
                matSistema[i+1][j] = (e0/l) * verificaPermissividade(nSeg,i+1,d1,d2)
            if i == nSeg-1:
                matSistema[i][j] = -(e0/l) * verificaPermissividade(nSeg,i,d1,d2)

# Redução da matriz retirando a primeira e ultima linha e coluna 
for i in range(nSeg - 2):
    for j in range(nSeg - 2):
        matSistemaR[i][j] = matSistema[i + 1][j + 1]

# Solucionando a equacao matricial linear
solucao = np.linalg.solve(matSistemaR, matV)

matSaida[0][0] = V0
matSaida[nSeg - 1][0] = Vn

for i in range(nSeg - 2):
    matSaida[i + 1][0] = solucao[i][0]

potnV = []
for i in range(nSeg):
    potnV.insert(i, f'V{i}')

mat.title("Resultado")
mat.plot(potnV, matSaida)
mat.show()