from utils import generarMatrizPresenteInicial
from utils import generarMatrizFuturoInicial
from utils import elementosNoSistemaCandidato
import numpy as np


#? ----------------- ENTRADAS DE DATOS ---------------------------------
#? Matriz de transición de probabilidad
TPM = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
])

#? El subconjunto del sistema candidato a analizar 
#? (aquí deben darse los elementos tanto en t como en t+1, ya que no necesariamente se tendrán en t+1 los mismos elementos que en t)
subconjuntoSistemaCandidato = np.array([
    'at','bt','at+1', 'bt+1'
])

#? El estado actual de todos los elementos del sistema
estadoActualElementos = np.array([
    {'at': 0},
    {'bt': 0},
    {'ct': 1},
    {'dt': 0}
])

#? SISTEMA CANDIDATO
#? El subconjunto de elementos a analizar (sistema candidato) aquí solo se requiere n los elementos en t
subconjuntoElementos = np.array(['at', 'bt'])

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
#? Parámetros
#? matrizPresente: matriz presente en t
#? matrizFuturo: matriz futuro en t+1
#? TPM: matriz de transición de probabilidad
#? elementosBackground: elementos del background {elemento: valor inicial}
def aplicarCondicionesBackground(nuevaMatrizPresente, nuevaTPM, elementosBackground):
    
    if len(elementosBackground) > 0:

        #* Extraemos primero los indices con su respectivo elemento del estado actual
        #* Crear un diccionario que mapea los nombres a su índice
        indicesCondicionesBackGround = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos)}
        #print(indicesCondicionesBackGround)

        for elemento in elementosBackground:

            llave = list(elemento.keys())[0]  

            indice = indicesCondicionesBackGround[llave]

            valorActualElemento = elemento[llave]
            
            #* Ya sabemos la posicion del elemento
            #* Ahora buscamos en la matriz presente y futura la fila y columna correspondiente
            #* Si el valor actual del elemento es 0 dejamos las filas que tengan 0
            #* Si el valor actual del elemento es 1 dejamos las filas que tengan 1
            for i in range(len(nuevaMatrizPresente)):
                if nuevaMatrizPresente[i][indice] == (1 if valorActualElemento == 0 else 0):
                    nuevaMatrizPresente[i].fill(99)
                    
            filas_a_eliminar = []
            for i in range(len(nuevaMatrizPresente)):
                if 99 in nuevaMatrizPresente[i]:
                    filas_a_eliminar.append(i)

            #* Ahora eliminamos las filas de la matriz presente usando los índices acumulados
            nuevaMatrizPresente = np.delete(nuevaMatrizPresente, filas_a_eliminar, axis=0)

            #* Ahora eliminamos las columnas de la matriz presente que estén en la posición indice
            nuevaMatrizPresente = np.delete(nuevaMatrizPresente, indice, axis=1)

            #* Ahora eliminamos las columnas de la matriz futura que estén en la posición indice
            nuevaTPM = np.delete(nuevaTPM, filas_a_eliminar, axis=0)

    
    return nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM
            

#? Ejecución de las condiciones de background
nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, nuevaTPM, elementosBackground)            

# print("------ BACKGROUND -----------")
# print("Matriz presente")
# print(nuevaMatrizPresente)
# print("Matriz futuro")
# print(nuevaMatrizFuturo)
# print("TPM")
# print(nuevaTPM)

#? ----------------- APLICAR MARGINALIZACIÓN INICIAL ---------------------------------
def aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, subconjuntoSistemaCandidato, elementosBackground):

    if len(elementosBackground) > 0:

        indicesCondicionesBackGround = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos)}

        for elemento in elementosBackground:
            
            llave = list(elemento.keys())[0]  

            indice = indicesCondicionesBackGround[llave]

            print(elemento, indice)

            #* Eliminar la fila #indice de la matriz futuro
            nuevaMatrizFuturo = np.delete(nuevaMatrizFuturo, indice, axis=0)
            
            #* identificar los grupos que se repiten en columnas
            arreglo = [[] for i in range(len(nuevaMatrizFuturo[0]))]
            for fila in nuevaMatrizFuturo:
                for idx, valor in enumerate(fila):
                    arreglo[idx].append(valor)

            #* recorrer los grupos
            subarreglos_repetidos = {}

            # Iterar sobre el arreglo y buscar repetidos
            for i, subarreglo in enumerate(arreglo):
                subarreglo_tuple = tuple(subarreglo)  # Convertir el subarreglo a tupla (para ser hashable)
                if subarreglo_tuple in subarreglos_repetidos:
                    subarreglos_repetidos[subarreglo_tuple].append(i)
                else:
                    subarreglos_repetidos[subarreglo_tuple] = [i]

            # Filtrar solo los subarreglos que están repetidos (es decir, que tienen más de un índice)
            repetidos_con_indices = {k: v for k, v in subarreglos_repetidos.items() if len(v) > 1}

            # Mostrar los subarreglos repetidos y sus respectivos índices

            for subarreglo, indices in repetidos_con_indices.items():
                menorIndice = min(indices)
                #* recorre [0,1,16]
                for i in indices:
                    #* i != 0
                    if i != menorIndice:
                        
                        #* si es menor recorro las fila de TPM
                        #* recorrer la tpm y sumar a la fila menorIndice la fila i
                        for k in nuevaTPM:
                            k[menorIndice] += k[i]
                            #* el valor de la columna de la fila k
                            k[i] = 99

                        for k in nuevaMatrizFuturo:
                            k[i] = 77

            #* Transponer la matriz para eliminar las columnas con 99
            nuevaTPM = nuevaTPM.T
            nuevaMatrizFuturo = nuevaMatrizFuturo.T

            #* Eliminar las columnas con 99
            filas_a_eliminar = []
            for i in range(len(nuevaTPM)):
                if 99 in nuevaTPM[i]:
                    filas_a_eliminar.append(i)

            nuevaTPM = np.delete(nuevaTPM, filas_a_eliminar, axis=0)

            #* Eliminar las columnas con 77
            filas_a_eliminar = []
            for i in range(len(nuevaMatrizFuturo)):
                if 77 in nuevaMatrizFuturo[i]:
                    filas_a_eliminar.append(i)

            nuevaMatrizFuturo = np.delete(nuevaMatrizFuturo, filas_a_eliminar, axis=0)

            #* Transponer la matriz para dejarla como estaba
            nuevaTPM = nuevaTPM.T
            nuevaMatrizFuturo = nuevaMatrizFuturo.T

            # for i in nuevaMatrizFuturo:
            #     print(i)

            # for i in nuevaTPM:
            #     print(i)


            # for i in nuevaMatrizFuturo:
            #     print(i)



    return nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM


#? Ejecución de la marginalización
nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, subconjuntoSistemaCandidato, elementosBackground)

# print("------ MARGINALIZACIÓN -----------")

print("Matriz presente")
print(nuevaMatrizPresente)
print("Matriz futuro")
print(nuevaMatrizFuturo)
print("TPM")
print(nuevaTPM)
print("-----------------")

#? ------------------ INICIAR PROCESO DE COMPARACION ----------------------------

#? DIVIDIR EN LA REPRESENTACION
#? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

#* tomar el subconjunto de elementos (los de t y t+1) con su indice
elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]

indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

def partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1):

    #* Matrices resultantes del proceso de representacion
    matricesPresentes = nuevaMatrizPresente
    matricesFuturas = dict()
    matricesTPM = dict()

    elementosT1Revisados = np.array([])
  

    for elementoT1 in elementosT1:

        copiaMatrizFuturo = np.copy(nuevaMatrizFuturo)
        copiaTPM = np.copy(nuevaTPM)

        #* si el elemento futuro no se ha revisado
        if (elementoT1 not in elementosT1Revisados):
            elementosT1Revisados = np.append(elementosT1Revisados, elementoT1)
            
            #* buscar el indice del elemento (si es por ejm at+1, buscar at) en el estado actual
            indice = indicesElementosT[elementoT1[:-2]]
            #* borrar las filas de la matriz futuro excepto la fila indice
            copiaMatrizFuturo = np.delete(copiaMatrizFuturo, [i for i in range(len(copiaMatrizFuturo)) if i != indice], axis=0)
            print("Matriz futuro")
            print(copiaMatrizFuturo)

            #? proceso
            #* identificar los grupos que se repiten en columnas
            arreglo = [[] for i in range(len(copiaMatrizFuturo[0]))]
            for fila in copiaMatrizFuturo:
                for idx, valor in enumerate(fila):
                    arreglo[idx].append(valor)

            #* recorrer los grupos
            subarreglos_repetidos = {}

            # Iterar sobre el arreglo y buscar repetidos
            for i, subarreglo in enumerate(arreglo):
                subarreglo_tuple = tuple(subarreglo)  # Convertir el subarreglo a tupla (para ser hashable)
                if subarreglo_tuple in subarreglos_repetidos:
                    subarreglos_repetidos[subarreglo_tuple].append(i)
                else:
                    subarreglos_repetidos[subarreglo_tuple] = [i]

            # Filtrar solo los subarreglos que están repetidos (es decir, que tienen más de un índice)
            repetidos_con_indices = {k: v for k, v in subarreglos_repetidos.items() if len(v) > 1}

            # print("Repetidos")
            # print(repetidos_con_indices)

            for subarreglo, indices in repetidos_con_indices.items():
                menorIndice = min(indices)
                #* recorre [0,1,16]
                for i in indices:
                    #* i != 0
                    if i != menorIndice:
                        
                        #* si es menor recorro las fila de TPM
                        #* recorrer la tpm y sumar a la fila menorIndice la fila i
                        for k in copiaTPM:
                            k[menorIndice] += k[i]
                            #* el valor de la columna de la fila k
                            k[i] = 99

                        for k in copiaMatrizFuturo:
                            k[i] = 77

            #* Transponer la matriz para eliminar las columnas con 99
            copiaTPM = copiaTPM.T
            copiaMatrizFuturo = copiaMatrizFuturo.T

            #* Eliminar las columnas con 99
            filas_a_eliminar = []
            for i in range(len(copiaTPM)):
                if 99 in copiaTPM[i]:
                    filas_a_eliminar.append(i)

            copiaTPM = np.delete(copiaTPM, filas_a_eliminar, axis=0)

            #* Eliminar las columnas con 77
            filas_a_eliminar = []
            for i in range(len(copiaMatrizFuturo)):
                if 77 in copiaMatrizFuturo[i]:
                    filas_a_eliminar.append(i)

            copiaMatrizFuturo = np.delete(copiaMatrizFuturo, filas_a_eliminar, axis=0)

            #* Transponer la matriz para dejarla como estaba
            copiaTPM = copiaTPM.T
            copiaMatrizFuturo = copiaMatrizFuturo.T

            matricesFuturas[elementoT1] = copiaMatrizFuturo
            matricesTPM[elementoT1] = copiaTPM

    return matricesPresentes, matricesFuturas, matricesTPM


#? Ejecución de la representación
print("------ REPRESENTACIÓN -----------")
matricesPresentes, matricesFuturas, matricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1)

print("Matrices Presentes (para todos los t+1)")
print(matricesPresentes)
print("Matrices Futuras")
for i in matricesFuturas:
    print(i)
    for j in matricesFuturas[i]:
        print(j)
print("Matrices TPM")
for i in matricesTPM:
    print(i)
    for j in matricesTPM[i]:
        print(j)

# def organizar():
#     elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
#     print(elementosT)

#     estadosInicialesElementosT = []

#     for elemento in elementosT:
#         for j in estadoActualElementos:
#             if list(j.keys())[0] == elemento:
#                 estadosInicialesElementosT.append(list(j.values())[0])
    
#     print(estadosInicialesElementosT)

#     # llave = list(elemento.keys())[0]  

#     # indice = indicesCondicionesBackGround[llave]


# organizar()
#? ------------------ INICIAR PROCESO PRINCIPAL ----------------------------
'''
- Proceso:
Comenzar con un conjunto V de todos los elementos en t. Es decir, V tendrá los nodos del
subsistema del conjunto candidato a analizar.
a) Inicializar W0 = ∅ y W1 = {v1}, donde v1 es un elemento arbitrario de V.
b) Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
• Encontrar vi ∈ V \ Wi-1 que minimiza: g(Wi-1 ∪ {vi}) - g({vi})
donde g(X) es la función EMD entre la distribución de probabilidades resultante de
P( X) ⊗ P( X’) y la distribución del sistema sin dividir, asi: EMD(P(X) ⊗ P( X’), P(V) )
• Establecer Wi = Wi-1 ∪ {vi}
c) Construcción de Pares:
• El par (vn-1, vn) forma un "par candidato".
d) Recursión:
• Si |V| > 2, repetir el proceso con V' = V \ {vn-1, vn} ∪ {u}, donde u representa la
unión de vn-1 y vn.
• Continuar hasta que |V| = 2.
e) Evaluación Final:
• Para cada par candidato (a, b) encontrado:
o Evaluar la división que separa {b} del resto de nodos.
• La división con el menor valor de diferencia es la solución al problema.
'''

import numpy as np
from scipy.stats import wasserstein_distance

# Función para calcular EMD con Hamming distance


#* PARAMS
#* nuevaTPM: Matriz de transición de probabilidad: [ [1,0,0, ... ], [0,1,0, ...], [0,0,1, ...], ... ]
#* subconjuntoElementos: Subconjunto de elementos a analizar: ['at', 'bt', 'ct']
#* subconjuntoSistemaCandidato: Subconjunto del sistema candidato a analizar: ['at','bt','ct','at+1', 'bt+1', 'ct+1']
#* estadoActualElementos: Estado actual de todos los elementos del sistema: [{'at': 0}, {'bt': 0}, {'ct': 1}, {'dt': 0}]

# def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):
    
#     V = subconjuntoElementos
#     print(V)

#     #* Inicializar W0 = ∅ y W1 = {v1}, donde v1 es un elemento arbitrario de V (primer elemento).
#     W0 = []
#     W1 = [ V[0] ] 
#     solucion = []

#     #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
#     for i in range(2, len(V)+1):
#         #* Encontrar vi ∈ V \ Wi-1 que minimiza: g(Wi-1 ∪ {vi}) - g({vi})
#         vi = subconjuntoElementos[i-1]
        
        



# Ejecutar el algoritmo
# algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)