import copy
import numpy as np
import time

from utilidades.evaluarParticionesFinales import evaluarParticionesFinales
from utilidades.background import aplicarCondicionesBackground
from utilidades.marginalizacionInicial import aplicarMarginalizacion
from utilidades.organizarCandidatas import buscarValorUPrima, organizarParticionesCandidatasFinales
from utilidades.utils import encontrarParticionEquilibrioComplemento, generarMatrizPresenteInicial, obtenerParticion
from utilidades.utils import generarMatrizFuturoInicial
from utilidades.utils import elementosNoSistemaCandidato
from utilidades.utils import producto_tensorial
from utilidades.partirRepresentacion import partirRepresentacion
from utilidades.comparaciones import compararParticion
from utilidades.vectorProbabilidad import encontrarVectorProbabilidades

#? ----------------- ENTRADAS DE DATOS ---------------------------------

from data.matrices import TPM
from data.matrices import subconjuntoSistemaCandidato
from data.matrices import subconjuntoElementos
from data.matrices import estadoActualElementos
# subconjuntoSistemaCandidato, subconjuntoElementos, TPM = obtenerInformacionCSV('csv/TPM1.csv')

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

nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, nuevosIndicesElementos = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, elementosBackground, estadoActualElementos, nuevaMatrizPresente)


#?  ------------------------ DIVIDIR EN LA REPRESENTACION -----------------------------------
#? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

#* tomar el subconjunto de elementos (los de t y t+1) con su indice
elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]


indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

# print("elementosT1", elementosT1)
# print("indicesElementosT viejos y nuevos", indicesElementosT,  nuevosIndicesElementos)

#? Ejecución de la representación
# print("------ REPRESENTACIÓN -----------")
partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT1, nuevosIndicesElementos)

particionesCandidatas = []
listaDeUPrimas = []


print("------ ALGORITMO -----------")
def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):
    V = subconjuntoSistemaCandidato #* {at, bt, ct, at+1, bt+1, ct+1}

    #*crear un arreglo W de len(V) elementos
    W = []
    for i in range(len(V)+1):
        W.append([])

    W[0] = []
    W[1] = [ V[0] ]

    restas = []

    #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
    for i in range( 2, len(V) + 1 ):

        #* se recorren los elementos V - W[i-1]
        elementosRecorrer = [elem for elem in V if elem not in W[i-1]]

        for elemento in elementosRecorrer:
            if 'u' not in elemento:
                
                #* W[i-1] U {u}
                wi_1Uelemento = W[i-1] + [elemento]
                #* {u}
                u = elemento
                

                # Calcula EMD(W[i-1] U {u})
                particionNormal = obtenerParticion(wi_1Uelemento)
                particionEquilibrio = encontrarParticionEquilibrioComplemento(particionNormal, subconjuntoElementos)

                # Copiar matrices una sola vez
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                # Calcular vector de probabilidades para particionNormal y particionEquilibrio
                vectorNormal = encontrarVectorProbabilidades(
                    particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                vectorEquilibrio = encontrarVectorProbabilidades(
                    particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular la diferencia entre los vectores
                resultado = producto_tensorial(vectorNormal, vectorEquilibrio)

                # Realizar copias de matrices necesarias para la comparación final
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                valorEMDParticionNormal = compararParticion(resultado, copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)

                
                # Calcular EMD({u})
                particionNormal = obtenerParticion([u])
                particionEquilibrio = encontrarParticionEquilibrioComplemento(particionNormal, subconjuntoElementos)

                # Realizar copias de matrices una sola vez
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

                # Calcular vector de probabilidades para particionNormal y particionEquilibrio
                vectorNormal = encontrarVectorProbabilidades(
                    particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                vectorEquilibrio = encontrarVectorProbabilidades(
                    particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular la diferencia entre los vectores
                resultado = producto_tensorial(vectorNormal, vectorEquilibrio)

                # Realizar copias de matrices necesarias para la comparación final
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                valorEMDU = compararParticion(resultado, copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)


                valorEMDFinal = valorEMDParticionNormal - valorEMDU
                # print("          - valorEMDFinal", valorEMDFinal)

                # print("elemento", elemento, "valorEMDFinal", valorEMDFinal)
                restas.append((elemento, valorEMDFinal))

            #! paso importante: verificar la existencia de u
            #! si hay una u debo ir a la lista de u' y tomar el valor correspondiente
            if 'u' in elemento:
                valor = buscarValorUPrima(listaDeUPrimas, elemento)
                # print("ELEMENTO ES U", elemento, valor)

                #* W[i-1] U {u}
                wi_1Uelemento = W[i-1] + valor
                #* {u}
                u = elemento

                # print("wi_1Uelemento", wi_1Uelemento)
                # print("u formula", u)

                # Calcular EMD(W[i-1] U {u})
                particionNormal = obtenerParticion(wi_1Uelemento)
                particionEquilibrio = encontrarParticionEquilibrioComplemento(particionNormal, subconjuntoElementos)

                # Realizar copias de matrices una sola vez al inicio
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                # Calcular vector de probabilidades para particionNormal
                vectorNormal = encontrarVectorProbabilidades(
                    particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular vector de probabilidades para particionEquilibrio usando las mismas copias
                vectorEquilibrio = encontrarVectorProbabilidades(
                    particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular la diferencia entre los vectores
                resultado = producto_tensorial(vectorNormal, vectorEquilibrio)

                # Realizar copias necesarias para la comparación final
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                valorEMDParticionNormal = compararParticion(resultado, copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)

                
                # Calcular EMD({u})
                particionNormal = obtenerParticion(valor)
                particionEquilibrio = encontrarParticionEquilibrioComplemento(particionNormal, subconjuntoElementos)

                # Realizar copias de matrices una sola vez al inicio
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                # Calcular vector de probabilidades para particionNormal
                vectorNormal = encontrarVectorProbabilidades(
                    particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular vector de probabilidades para particionEquilibrio usando las mismas copias
                vectorEquilibrio = encontrarVectorProbabilidades(
                    particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM,
                    estadoActualElementos, subconjuntoElementos, indicesElementosT,
                    copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT
                )

                # Calcular la diferencia entre los vectores
                resultado = producto_tensorial(vectorNormal, vectorEquilibrio)

                # Realizar copias necesarias para la comparación final
                copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                valorEMDU = compararParticion(resultado, copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)


                valorEMDFinal = valorEMDParticionNormal - valorEMDU
                # print("          - valorEMDFinal", valorEMDFinal)

                # print("elemento", elemento, "valorEMDFinal", valorEMDFinal)
                restas.append((elemento, valorEMDFinal))
                
        #* Seleccionar el vi que minimiza EMD(W[i-1] U {vi})
        menorTupla = ()
        if len(restas) > 0:
            menorTupla = min(restas, key=lambda x: x[1])
            valoresI = copy.deepcopy(W[i-1])
            valoresI.append(menorTupla[0])
            
        W[i] = valoresI
        restas = []

        #*Sacar el par candidato
        if i == len(V):
            SecuenciaResultante = []
            for x in W:
                if x == []:
                    continue
                #*agregar el elemento de la ultima posicion de x
                SecuenciaResultante.append(x[-1])


            parCandidato = (SecuenciaResultante[-2], SecuenciaResultante[-1])

            ultimoElemento = SecuenciaResultante[-1]
            p1 = None
            p2 = None
            #* si el ultimo elemento tiene t+1
            if 't+1' in ultimoElemento:
                p1 = ([ultimoElemento], [])
                p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )
            else:
                p1 = ([],[ultimoElemento])
                p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )

            particionCandidata = {
                'p1': p1,
                'p2': p2
            }

            particionesCandidatas.append(particionCandidata)

            ultimoElemento = SecuenciaResultante[-1]
            
            uActual = [SecuenciaResultante[-2], SecuenciaResultante[-1]]
            nombreU = ""
            if(len(listaDeUPrimas) == 0):
                nombreU = "u1"
            else:
                nombreU = "u" + str(len(listaDeUPrimas) + 1)
            listaDeUPrimas.append({nombreU: uActual})

            #* nuevoV = los elementos de V que no son el par candidato + nombre del uActual
            nuevoV = []
            nuevoV = [elem for elem in V if elem not in parCandidato]
            nuevoV = nuevoV + [nombreU]

            #* se procede con la recursión mandando el nuevoV
            algoritmo(nuevaTPM, subconjuntoElementos, nuevoV, estadoActualElementos)
       
    particionesFinales = organizarParticionesCandidatasFinales(copy.deepcopy(particionesCandidatas), listaDeUPrimas, subconjuntoElementos)

    resultado = evaluarParticionesFinales(particionesFinales, partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
    return resultado
   
start_time = time.time()
x = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
end_time = time.time()

# Cálculo del tiempo total
elapsed_time = end_time - start_time
print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")

print()
print("RESULTADOS FINALES")
for i in x["particionesEMD"]:
    print(i[0], " con EMD ", i[1])
    
print("La mejor partición es ", x["particionMenorEMD"])
# print("LISTA DE U PRIMAS")
# for i in listaDeUPrimas:
#     print(i)
