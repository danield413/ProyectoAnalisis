from utils import generarMatrizPresenteInicial
from utils import generarMatrizFuturoInicial
from utils import elementosNoSistemaCandidato
from utils import producto_tensorial_n
from utils import producto_tensorial
from utils import calcularEMD
import numpy as np
import copy


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
], dtype=float)

#? El subconjunto del sistema candidato a analizar 
#? (aquí deben darse los elementos tanto en t como en t+1, ya que no necesariamente se tendrán en t+1 los mismos elementos que en t)
subconjuntoSistemaCandidato = np.array([
    'at','bt', 'ct','at+1','bt+1', 'ct+1'
])

#? El estado actual de todos los elementos del sistema
estadoActualElementos = np.array([
    {'at': 1},
    {'bt': 0},
    {'ct': 0},
    {'dt': 0}
])

#? SISTEMA CANDIDATO
#? El subconjunto de elementos a analizar (sistema candidato) aquí solo se requiere n los elementos en t
subconjuntoElementos = np.array(['at', 'bt', 'ct'])

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

# print("Matriz presente")
# print(nuevaMatrizPresente)
# print("Matriz futuro")
# print(nuevaMatrizFuturo)
# print("TPM")
# print(nuevaTPM)
# print("-----------------")

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
            # print("Matriz futuro")
            # print(copiaMatrizFuturo)

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

def encontrarVectorProbabilidades(particion, matricesPresentes, matricesFuturas, matricesTPM):
    # print("SE LLAMO ENCONTRAR VECTOR PROBABILIDADES")
    # print("particion que entra", particion)
    # print("matrices presentes", matricesPresentes)
    # print("matrices futuras", matricesFuturas)
    # print("matrices tpm", matricesTPM)
    #* Inicializar el vector de probabilidades

    
    vectorProbabilidades = []
    lista_nueva, lista_anterior = particion
    subDivisiones = [([elem], lista_anterior) for elem in lista_nueva]

    #*verificar si alguna de las particiones está vacia
    # print("particion separada", particion[0], particion[1])

    #*TODO: PREGUNTAR SI SE RETORNA 1 O 0
    if particion[0] == [] or particion[1] == []:
        return 1 

    for subDivision in subDivisiones:

        # copiaMatricesPresentes = matricesPresentes.copy()
        # copiaMatricesFuturas = matricesFuturas.copy()
        # copiaMatricesTPM = matricesTPM.copy()



        # print("subDivision", subDivision)
        #*Sacar cada elemento del lado izquierdo
        ladoIzquierdo = subDivision[0][0]
        # print(ladoIzquierdo)
        # #* Elegir la matriz presente, futura correspondiente y tpm correspondiente
        
        # print("Copia matrices presentes", matricesPresentes)
        
        # print("Copia matrices futuras", matricesFuturas)

        # print("Copia matrices tpm", matricesTPM)
        # print()

        matrizPresenteVector = matricesPresentes
        # matrizFuturaVector = copiaMatricesFuturas[ladoIzquierdo]
        tpmVector = matricesTPM[ladoIzquierdo]

        #*Si la longitud del lado derecho de la subdivision es menor que la longitud del subconjunto de elementos, hay que marginalizar por filas
        # print('-----------', ladoIzquierdo ,'-----------')
        # if len(subDivision[1]) < len(subconjuntoElementos):

        ordenColumnasPresente = subDivision[1]
        # print("Orden columnas presente")
        # print(ordenColumnasPresente)
    
        #*Marginalizar por filas
        #*Crear un arreglo de indices con la longitud del subconjunto de elementos, desde 0 hasta la longitud del subconjunto de elementos
        indicesIniciales = np.arange(len(subconjuntoElementos))

        #*Crear un arreglo con los indices del lado derecho de la subdivision
        indicesPresente = [indicesIniciales[i] for i in range(len(indicesIniciales)) if subconjuntoElementos[i] in subDivision[1]]
        
        #*Hacer la diferencia entre los indices iniciales y los indices presente
        indicesMarginalizar = np.setdiff1d(indicesIniciales, indicesPresente)

        #*Eliminar esos indices de la matriz presente
        #*Transponemos la matriz para eliminar las filas con esos indices
        matrizPresenteVector = matrizPresenteVector.T
        #*Eliminar las columnas con esos indices
        matrizPresenteVector = np.delete(matrizPresenteVector, indicesMarginalizar, axis=0)

        #*Transponer la matriz para dejarla como estaba
        #matrizPresenteVector = matrizPresenteVector.T

        #* identificar los grupos que se repiten en columnas
        arreglo = [[] for i in range(len(matrizPresenteVector[0]))]
        for fila in matrizPresenteVector:
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


        cantidad_repeticiones = {k: len(v) for k, v in subarreglos_repetidos.items() if len(v) > 1}

        for subarreglo, indices in repetidos_con_indices.items():
            menorIndice = min(indices)
            #* recorre [0,1,16]
            for i in indices:
                if i != menorIndice:
                    for k in range(len(tpmVector[i])):
                        tpmVector[menorIndice][k] += tpmVector[i][k]
                        tpmVector[i][k] = 99

                #* i != 0
                if i != menorIndice:
                    for k in matrizPresenteVector:
                        k[i] = 77

            #*Obtener el numero de columnas de la tpm
            numero_columnas = len(tpmVector[0])

            #*Recorrer el numero de columnas
            for k in range(numero_columnas):
                division = tpmVector[menorIndice][k] / len(indices)
                tpmVector[menorIndice][k] = division
                
                        
        #* Transponer la matriz para eliminar las columnas con 77 y dejarla como estaba
        matrizPresenteVector = matrizPresenteVector.T

        
            #* Eliminar las columnas con 77
        filas_a_eliminar = []
        for i in range(len(matrizPresenteVector)):
            if 77 in matrizPresenteVector[i]:
                filas_a_eliminar.append(i)

        matrizPresenteVector = np.delete(matrizPresenteVector, filas_a_eliminar, axis=0)

        #*Eliminar las columnas con 99
        filas_a_eliminar = []
        for i in range(len(tpmVector)):
            if 99 in tpmVector[i]:
                filas_a_eliminar.append(i)

        tpmVector = np.delete(tpmVector, filas_a_eliminar, axis=0)

        estadosAcutales = []
        for i in estadoActualElementos:
            if list(i.keys())[0] in ordenColumnasPresente:
                estadosAcutales.append(list(i.values())[0])
        
        #*Recorrer la matriz presente
        indiceVector = -1
        for i in range(len(matrizPresenteVector)):
            if matrizPresenteVector[i].tolist() == estadosAcutales:
                indiceVector = i
                break

        
        #*Agregar ese vector a la lista de probabilidades
        vectorProbabilidades.append(tpmVector[indiceVector])

            
    # print("Vector probabilidades", vectorProbabilidades)
    productoTensorialParticion = producto_tensorial_n(vectorProbabilidades)
    return productoTensorialParticion



#* Método que me compara el vector resultante de la partición con el vector original de la TPM con la que estoy trabajando
#* PARAMS
#* resultadoParticion: Vector resultante de la partición
#* nuevaMatrizPresente: Matriz presente
#* nuevaTPM: Matriz de transición de probabilidad
#* con la nuevvaMatrizPresente y la nuevaTPM se obtiene el vector de probabilidades original
def compararParticion(resultadoParticion, nuevaMatrizPresente, nuevaTPM):
    estadosActuales = []
    ordenColumnasPresente = []
    for i in subconjuntoElementos:
        ordenColumnasPresente.append(i)

    # print(ordenColumnasPresente)

    for i in estadoActualElementos:
        if list(i.keys())[0] in ordenColumnasPresente:
            estadosActuales.append(list(i.values())[0])
    
    indiceVector = -1
    for i in range(len(nuevaMatrizPresente)):
        if nuevaMatrizPresente[i].tolist() == estadosActuales:
            indiceVector = i
            break

    vectorCompararTPM = nuevaTPM[indiceVector]

    #* Comparar distribuciones usando la distancia EMD (Earth Mover's Distance)
    valorEMD = calcularEMD(resultadoParticion, vectorCompararTPM)
    return valorEMD

#* Ejecución de la partición
# print("--------------- PRUEBA ----------------------")
# prodTensorialParticion1 = encontrarVectorProbabilidades((['at+1'], ['at']), matricesPresentes, matricesFuturas, matricesTPM)
# prodTensorialParticion2 = encontrarVectorProbabilidades((['bt+1','ct+1'], ['bt', 'ct']), matricesPresentes, matricesFuturas, matricesTPM)
# print("Producto tensorial 1", prodTensorialParticion1)
# print("Producto tensorial 2", prodTensorialParticion2)
# #* unir ambas particiones
# resultadoParticion = producto_tensorial(prodTensorialParticion1, prodTensorialParticion2)
# print("Resultado particion", resultadoParticion)
# print("-----------------------------------------------------")
# #* Ejecución de la comparación
# compararParticion(resultadoParticion, nuevaMatrizPresente, nuevaTPM)

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

#? Ejecución de la representación
print("------ REPRESENTACIÓN -----------")
partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1)

# print("Matrices Presentes (para todos los t+1)")
# print(matricesPresentes)
# print("Matrices Futuras")
# for i in matricesFuturas:
#     print(i)
#     for j in matricesFuturas[i]:
#         print(j)
# print("Matrices TPM")
# for i in matricesTPM:
#     print(i)
#     for j in matricesTPM[i]:
#         print(j)

def organizarParticionesCandidatasFinales(particionesCandidatasFinales):

    nuevas = []

    #* remocion de las u
    for i in particionesCandidatasFinales:
        # print("Particion candidata", i)
        p1 = i['p1']
        p2 = i['p2']

        #* valores a reemplazar
        for x in p1[0]:
            if 'u_prima' in x:
                valor = buscarValorUPrima(listaDeU, x)
                print(x, valor)
                p1[0].extend(valor)
                p1[0].remove(x)

        for x in p1[1]:
            if 'u_prima' in x:
                valor = buscarValorUPrima(listaDeU, x)
                print(x, valor)
                p1[1].extend(valor)
                p1[1].remove(x)
        
        for x in p2[0]:
            if 'u_prima' in x:
                valor = buscarValorUPrima(listaDeU, x)
                print(x, valor)
                p2[0].extend(valor)
                p2[0].remove(x)

        for x in p2[1]:
            if 'u_prima' in x:
                valor = buscarValorUPrima(listaDeU, x)
                print(x, valor)
                p2[1].extend(valor)
                p2[1].remove(x)

        nuevas.append({
            'p1': p1,
            'p2': p2
        })
        
    #* ahora, poner los elementos de t+1 en la primera posición de la partición y los de t en la segunda
    for i in nuevas:
        p1 = i['p1']
        p2 = i['p2']

        p1[0].sort()
        p1[1].sort()
        p2[0].sort()
        p2[1].sort()


    # for i in nuevas:
    #     print(i)

    # print("-------------------------------")

    #* organizar t+1 en izquierda y t en derecha
    for i in nuevas:
        particion1 = i['p1']
        particion2 = i['p2']

        # Para particion1
        elementos_a_mover = []

        # Identificar elementos que contienen 't' en particion1[0]
        for elem in particion1[0]:
            if 't' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion1[1] y eliminarlos de particion1[0]
        for elem in elementos_a_mover:
            particion1[0].remove(elem)
            particion1[1].append(elem)

        # Resetear elementos_a_mover
        elementos_a_mover = []

        # Identificar elementos que contienen 't+1' en particion1[1]
        for elem in particion1[1]:
            if 't+1' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion1[0] y eliminarlos de particion1[1]
        for elem in elementos_a_mover:
            particion1[1].remove(elem)
            particion1[0].append(elem)

        # Repetir el mismo proceso para particion2

        elementos_a_mover = []

        # Identificar elementos que contienen 't' en particion2[0]
        for elem in particion2[0]:
            if 't' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion2[1] y eliminarlos de particion2[0]
        for elem in elementos_a_mover:
            particion2[0].remove(elem)
            particion2[1].append(elem)

        # Resetear elementos_a_mover
        elementos_a_mover = []

        # Identificar elementos que contienen 't+1' en particion2[1]
        for elem in particion2[1]:
            if 't+1' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion2[0] y eliminarlos de particion2[1]
        for elem in elementos_a_mover:
            particion2[1].remove(elem)
            particion2[0].append(elem)

    # for i in nuevas:
    #     print(i)

    # print("-------------------------------")

    #* Ahora, equilibrar correctamente la partición 2

    tuplasFinales = []

    for i in nuevas:
        particion1 = i['p1']
        particion2 = i['p2']

        #* Obtener el equilibrio de la partición 2
        
        elementosT1 = [elem for elem in subconjuntoElementos if 't+1' in elem]
        #* ver que elemenos de t+1 están en la particion 1 izquierda
        elementosT1_particion1 = [elem for elem in particion1[0] if 't+1' in elem and 't' not in elem]
        #* Calculo la diferencia entre los elementos de t+1 y los elementos de t+1 en la particion 1
        diferenciaT1 = [elem for elem in elementosT1 if elem not in elementosT1_particion1]
        # print("Diferencia t+1", diferenciaT1)

        if diferenciaT1 != []:
            # print("es diferente de vacio")
            # print("Particion 2[1]", particion2[1])
            # Convertir la tupla en lista para hacer modificaciones
            particion2 = list(particion2)
            particion2[0] = diferenciaT1  # Realizar el cambio
            particion2 = tuple(particion2)  # Convertir de nuevo en tupla si es necesario

        elementosT = [elem for elem in subconjuntoElementos if 't' in elem]

        #* ver que elemenos de t están en la particion 1 derecha
        elementosT_particion1 = [elem for elem in particion1[1] if 't' in elem]
        #* Calculo la diferencia entre los elementos de t y los elementos de t en la particion 1
        diferenciaT = [elem for elem in elementosT if elem not in elementosT_particion1]
        # print("Diferencia t", diferenciaT)

        if diferenciaT != []:
            # Convertir la tupla en lista para hacer modificaciones
            particion2 = list(particion2)
            particion2[1] = diferenciaT  # Realizar el cambio
            particion2 = tuple(particion2)  # Convertir de nuevo en tupla si es necesario

        # print("particion", (particion1, particion2))

        tuplasFinales.append([particion1, particion2])

    # for i in tuplasFinales:
    #     p1 = i[0]
    #     p2 = i[1]
    #     print("Particion 1", p1, "Particion 2", p2)
    
    return tuplasFinales

def buscarValorUPrima(listaDeU, uprima):
    for u in listaDeU:
        nombre = list(u.keys())[0]
        if nombre == uprima:
            return u[nombre]
        
def evaluarParticionesFinales(particionesFinales):
    print("evaluar particiones finales")
    print(particionesFinales)

    particionMenorEMD = None

    for i in particionesFinales:
        print("Particion final", i)
        particion1 = i[0]
        particion2 = i[1]

        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

        vectorp1 = encontrarVectorProbabilidades(particion1, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)
        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

        vectorp2 = encontrarVectorProbabilidades(particion2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)

        vectorResultado = producto_tensorial(vectorp1, vectorp2)

        valorEMD = compararParticion(vectorResultado, nuevaMatrizPresente, nuevaTPM)
        print("Valor EMD", valorEMD)

        if particionMenorEMD == None:
            particionMenorEMD = (i, valorEMD)
        else:
            if valorEMD < particionMenorEMD[1]:
                particionMenorEMD = (i, valorEMD)

    print("Particion con menor EMD", particionMenorEMD)
    return particionMenorEMD


particionesCandidatas = []
listaDeU = []

print("------ ALGORITMO -----------")
def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):

    V = subconjuntoSistemaCandidato #* {at, bt, ct, at+1, bt+1, ct+1}
    print("V", V)

    #*crear un arreglo W de len(V) elementos
    W = []
    for i in range(len(V)+1):
        W.append([])

    W[0] = []
    W[1] = [ V[0] ]
    print(W)

    restas = []

    #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
    for i in range(2, len(V)+1):
        print()
        print(">>>>>>>>>> LONGITUD V ACTUAL", (len(V)+1), "CONJUNTO: ", V)
        if (len(V)+1) == 2:
            break
    
        #* ahora recorremos para cada elemento en V que no esté en W[i-1] (el anterior)
        for elem in V:
            if  elem not in W[i-1]: 
                elementoActual = elem

                #* aquí planteamos el conjunto que le vamos a pasar a la función de comparación
                union = []
                for elem in W[i-1]:
                    union.append(elem)
                if 'u' not in elementoActual:
                    union.append(elementoActual)

                #* si elemento es una u 
                if 'u' in elementoActual:
                    #* buscar los elementos que conforman la u
                    for u in listaDeU:
                        #* cojo el nombre de la llave
                        nombre = list(u.keys())[0]
                        if nombre == elementoActual:
                            #* cojo el valor de la llave
                            elementosU = u[nombre]
                            #* recorro los elementos de la u
                            for elem in elementosU:
                                # print("ELEMENTO U", elem)
                                union.append(elem)

                # print("UNION", union)
                
                #* separamos de la union los elementos que estan en t+1 y en t
                particion = ( [ elem for elem in union if 't+1' in elem ], [ elem for elem in union if 't' in elem and 't+1' not in elem ] )
                print("PARTICION", particion)

                #! ------------------ g(Wi-1 ∪ {vi}) ----------------------------
                
                #? crear copias de las matrices para no modificar las originales
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                #* obtenemos el vector de probabilidades de la partición

                vectorProbabilidades = encontrarVectorProbabilidades(particion, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)
                # print("vectorProbabilidades", vectorProbabilidades)

                #* Obtenemos el vector de probabilidades del conjunto que equilibra la particion
                #* Obtener el equilibrio de la partición (lo que le falta a la partición para ser igual a la original)
                particionEquilibrio = ([elem for elem in V if elem not in particion[0] and 't+1' in elem],[elem for elem in V if elem not in particion[1] and 't' in elem and 't+1' not in elem] )
                print("particionEquilibrio", particionEquilibrio)

                #? crear copias de las matrices para no modificar las originales
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                #*Obtenemos el vector de probabilidades de la partición de equilibrio
                vectorProbabilidadesEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)
                # print("vectorProbabilidadesEquilibrio", vectorProbabilidadesEquilibrio)

                #* Calcular la diferencia entre los dos vectores de probabilidades
                vectorResultado = producto_tensorial(vectorProbabilidades, vectorProbabilidadesEquilibrio)
                valorwi_gu = compararParticion(vectorResultado, nuevaMatrizPresente, nuevaTPM)
                # print("VALOR EMD valorwi_gu", valorwi_gu)

                #! ----------------------------- g({vi}) --------------------------------------

                #*Obtenemos la particion solamente del elemento actual sin nada mas
                particionElementoActual2 = ([elem for elem in V if elem == elementoActual and 't+1' in elem],[elem for elem in V if elem == elementoActual and 't' in elem and 't+1' not in elem] )

                #*Obtenemos la particion de equilibrio del elemento actual
                particionEquilibrioElementoActual2 = ([elem for elem in V if elem != elementoActual and 't+1' in elem],[elem for elem in V if elem != elementoActual and 't' in elem and 't+1' not in elem] )
                

                #? crear copias de las matrices para no modificar las originales
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                vectorProbabilidades2 = encontrarVectorProbabilidades(particionElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)
                # print("vectorProbabilidades2", vectorProbabilidades2)

                #? crear copias de las matrices para no modificar las originales
                copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                vectorProbabilidadesEquilibrioElementoActual2 = encontrarVectorProbabilidades(particionEquilibrioElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM)
                # print("vectorProbabilidadesEquilibrioElementoActual2", vectorProbabilidadesEquilibrioElementoActual2)

                #* Calcular la diferencia entre los dos vectores de probabilidades
                vectorResultadoElementoActual = producto_tensorial(vectorProbabilidades2, vectorProbabilidadesEquilibrioElementoActual2)

                valorg_u = compararParticion(vectorResultadoElementoActual, nuevaMatrizPresente, nuevaTPM)
                valorRestaFinal = valorwi_gu - valorg_u

                restas.append((elementoActual, valorRestaFinal))

        # print("DETERMINANDO EL MENOR")
        # print("Restas", restas)
        #* Encontrar el menor valor de la resta

        menorTupla = ()
        if len(restas) > 0:
            menorTupla = min(restas, key=lambda x: x[1])    
            valoresI = copy.deepcopy(W[i-1])
            valoresI.append(menorTupla[0])

        W[i] = valoresI
        print("W", W)
        restas = [] 

        SecuenciaResultante = []
        for x in W:                                           
            if x == []:
                continue
            #*agregar el elemento de la ultima posicion de x
            SecuenciaResultante.append(x[-1])
        # print("Secuencia resultante", SecuenciaResultante)

        parCandidato = (SecuenciaResultante[-2], SecuenciaResultante[-1])
        # print("Par candidato", parCandidato)

        ultimoElemento = SecuenciaResultante[-1]
        # print("Ultimo elemento", ultimoElemento)

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
        
        #* se crea una nueva variable llamada u' que es la union de los dos elementos del par candidato
        nuevoV = np.array([ elem for elem in V if elem not in parCandidato ])

        uprima = [ parCandidato[0], parCandidato[1] ]

        #*verifico si en uprima hay una u embebida
        if 'u' in uprima[0]:
            # print("HAY U EN U PRIMA[0]")
            #*voy a la lista de u a buscar el nombre de la u
            for u in listaDeU:
                nombre = list(u.keys())[0]
                if nombre == uprima[0]:
                   for x in u[nombre]:
                        uprima.append(x)
        if 'u' in uprima[1]:
            # print("HAY U EN U PRIMA[1]")
            #*voy a la lista de u a buscar el nombre de la u
            for u in listaDeU:
                nombre = list(u.keys())[0]
                if nombre == uprima[1]:
                   for x in u[nombre]:
                        uprima.append(x)
            #* elimino la u de la lista de u
        
        for elementoU in listaDeU:
            valor = list(elementoU.values())[0]
            for x in range(len(valor) - 1, -1, -1):  # Itera en orden inverso
                if 'u' in valor[x]:
                    # print("VALOR", valor[x], "indice", x)
                    valor.pop(x)  # Elimina el elemento sin afectar los índices restantes
                    

        


        total = 0
        for x in listaDeU:
            nombre = list(x.keys())[0]
            if 'u' in nombre:
                total += 1
        # print("total de anteriores u", total)

        nombreU = 'u_prima' + str(total+1)
        nuevoV = np.append(nuevoV, nombreU)
        listaDeU.append({nombreU: uprima})
        # print("Lista de U", listaDeU)

        

        #* LA 1ERA VEZ QUE OBTIENE LA SECUENCIA RESULTANTE SE CIERRA EL CICLO Y SE LLAMA A LA RECURSIÓN
        if i == 2:
            if((len(V)+1) > 2):
                print("SE LLAMÓ LA RECURSIÓN")
                algoritmo(nuevaTPM, subconjuntoElementos, nuevoV, estadoActualElementos)
                break

    particionesFinales = organizarParticionesCandidatasFinales(copy.deepcopy(particionesCandidatas))
    particionElegida = evaluarParticionesFinales(particionesFinales)
    return particionElegida


x = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
print("resultado algoritmo", x)

