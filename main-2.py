import copy
import numpy as np

from utilidades.evaluarParticionesFinales import evaluarParticionesFinales
from utilidades.background import aplicarCondicionesBackground
from utilidades.marginalizacionInicial import aplicarMarginalizacion
from utilidades.organizarCandidatas import organizarParticionesCandidatasFinales
from utilidades.utils import generarMatrizPresenteInicial, obtenerParticion, obtenerParticionEquilibrio
from utilidades.utils import generarMatrizFuturoInicial
from utilidades.utils import elementosNoSistemaCandidato
from utilidades.partirRepresentacion import partirRepresentacion
from utilidades.utils import producto_tensorial
from utilidades.comparaciones import compararParticion


#? ----------------- ENTRADAS DE DATOS ---------------------------------
from data.matrices import TPM
from data.matrices import subconjuntoSistemaCandidato
from data.matrices import estadoActualElementos
from data.matrices import subconjuntoElementos
from utilidades.vectorProbabilidad import encontrarVectorProbabilidades

#? ----------------- MATRIZ PRESENTE Y MATRIZ FUTURO ---------------------------------

matrizPresente = generarMatrizPresenteInicial( len(estadoActualElementos) )
matrizFuturo = generarMatrizFuturoInicial(matrizPresente)

#? ----------------- APLICAR CONDICIONES DE BACKGROUND ---------------------------------

#? Elementos que no hacen parte del sistema cantidato
elementosBackground = elementosNoSistemaCandidato(estadoActualElementos, subconjuntoElementos)

#? Realizar una copia de las matrices para no modificar las originales
nuevaTPM = np.copy(TPM)
nuevaMatrizPresente = np.copy(matrizPresente)
nuevaMatrizFuturo = np.copy(matrizFuturo)


#? Ejecución de las condiciones de background
nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, nuevaTPM, elementosBackground, nuevaMatrizFuturo, estadoActualElementos)


#? ----------------- APLICAR MARGINALIZACIÓN INICIAL ---------------------------------

nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, elementosBackground, estadoActualElementos, nuevaMatrizPresente)


#?  ------------------------ DIVIDIR EN LA REPRESENTACION -----------------------------------
#? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

#* tomar el subconjunto de elementos (los de t y t+1) con su indice
elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]

indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

#? Ejecución de la representación
# print("------ REPRESENTACIÓN -----------")
partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1, indicesElementosT)


particionesCandidatas = []
listaDeU = []

print("------ ALGORITMO -----------")
def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):

    V = subconjuntoSistemaCandidato #* {at, bt, ct, at+1, bt+1, ct+1}
    # print("V", V)

    #*crear un arreglo W de len(V) elementos
    W = []
    for i in range(len(V)+1):
        W.append([])

    W[0] = []
    W[1] = [ V[0] ]
    # print(W)

    restas = []

    #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
    for i in range(2, len(V)+1):
        #* se recorren los elementos V - W[i-1]
        elementosRecorrer = [elem for elem in V if elem not in W[i-1]]
        
        for elemento in elementosRecorrer:
            #* W[i-1] U {u}
            wi_1Uelemento = W[i-1] + [elemento]
            #* {u}
            u = elemento
            
            #? Calcular  EMD(W[i-1] U {u})
            # print("EMD(W[i-1] U {u})", wi_1Uelemento)
            particionNormal = obtenerParticion(wi_1Uelemento)
            # print("     - particionNormal", particionNormal)
            particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
            # print("     - particionEquilibrio", particionEquilibrio)

            copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
            copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
            copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
            copiaNuevaTPM = copy.deepcopy(nuevaTPM)

            vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

            copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
            copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
            copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
            copiaNuevaTPM = copy.deepcopy(nuevaTPM)

            vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)   

            # print("     - vectorNormal", vectorNormal)
            # print("     - vectorEquilibrio", vectorEquilibrio)

            #* Calcular la diferencia entre los vectores
            resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaTPM = copy.deepcopy(nuevaTPM)
            valorEMDParticionNormal = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)
            print("     - valorEMDParticionNormal", valorEMDParticionNormal)
            
            
            #? Calcular EMD({u})
            # print("EMD({u})", u)
            particionNormal = obtenerParticion([u])
            # print("     - particionNormal", particionNormal)
            particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
            # print("     - particionEquilibrio", particionEquilibrio)
            
            copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
            copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
            copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

            vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

            copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
            copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
            copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

            vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

            # print("     - vectorNormal", vectorNormal)
            # print("     - vectorEquilibrio", vectorEquilibrio)

            #* Calcular la diferencia entre los vectores
            resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaTPM = copy.deepcopy(nuevaTPM)
            valorEMDU = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)
            print("     - valorEMDU", valorEMDU)

            valorEMDFinal = valorEMDParticionNormal - valorEMDU
            print("          - valorEMDFinal", valorEMDFinal)
            
        if i >= 2:
            break
        print()
        print()
   


x = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
# print("resultado algoritmo", x)


# copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
# copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
# copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

