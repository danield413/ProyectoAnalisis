import copy
from utilidades.vectorProbabilidad import encontrarVectorProbabilidades
from utilidades.utils import producto_tensorial
from utilidades.comparaciones import compararParticion

def evaluarParticionesFinales(particionesFinales, partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT):

    particionMenorEMD = None
    
    particionesEMD = []

    for i in particionesFinales:
        particion1 = i[0]
        particion2 = i[1]

        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

        vectorp1 = encontrarVectorProbabilidades(particion1, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

        vectorp2 = encontrarVectorProbabilidades(particion2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)

        vectorResultado = producto_tensorial(vectorp1, vectorp2)

        valorEMD = compararParticion(vectorResultado, nuevaMatrizPresente, nuevaTPM, subconjuntoElementos, estadoActualElementos)
        
        particionesEMD.append((i, valorEMD))
        
        if particionMenorEMD == None:
            particionMenorEMD = (i, valorEMD)
        else:
            if valorEMD < particionMenorEMD[1]:
                particionMenorEMD = (i, valorEMD)

    return {
        "particionesEMD": particionesEMD,
        "particionMenorEMD": particionMenorEMD
    }