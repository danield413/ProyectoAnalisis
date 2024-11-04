import numpy as np

def particionComplemento(particion1, subconjuntoSistemaCandidato):
    print(particion1)
    
    #* calcular elementos que hacen falta en t+1 basandose en el subconjunto del sistema candidato
    faltantesT1 = []
    faltantesT = []
    
    for i in subconjuntoSistemaCandidato:
        if 't+1' in i:
            if i not in particion1[0]:
                faltantesT1.append(i)
        
        if 't' in i and 't+1' not in i:
            if i not in particion1[1]:
                faltantesT.append(i)
        
    return (faltantesT1, faltantesT)
            
    
particion1 = (['at+1'], ['c+1'])
subconjuntoSistemaCandidato = np.array([
    'at', 'bt', 'ct', 'at+1', 'bt+1',  'ct+1',
])

complemento = particionComplemento(particion1, subconjuntoSistemaCandidato)
print(complemento)

