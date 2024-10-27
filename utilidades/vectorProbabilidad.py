import copy
from utilidades.utils import producto_tensorial_n
import numpy as np

def encontrarVectorProbabilidades(particion, matricesPresentes, matricesFuturas, matricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT):
    
    vectorProbabilidades = []
    lista_nueva, lista_anterior = particion
    subDivisiones = [([elem], lista_anterior) for elem in lista_nueva]

    #*verificar si alguna de las particiones está vacia
    # print("particion separada", particion[0], particion[1])

    #? CASO 1: cuando el futuro es vacio
    #* Para estos casos es mas conveniente usar la matriz presente, la matriz futura y la tpm original sin partir

    if particion[1] == [] and particion[0] == []:
        return 0

    if particion[0] == []:
        
        elementosPresente = particion[1] #* elementos en t

        #*Recorro todos los elementos en t
        for elementot in elementosPresente:

            copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
            copiaNuevaTPM = copy.deepcopy(nuevaTPM)
            copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)


            #*Buscar el indice del elemento en la matriz presente
            indiceElementot = indicesElementosT[elementot]
            # print("Elemento t", elementot, "Indice", indicesElementosT)

            #* la idea es marginalizar todas las columnas del presente que no sean el indice
            #*obtener las columnas que no son el indice
            columnasNoIndice = [i for i in range(len(copiaNuevaMatrizPresente[0])) if i != indiceElementot]
            columnasNoIndice.sort(reverse=True) #* 2,1

            for columna in columnasNoIndice:
                #*Eliminar las columnas que no son el indice
                #* Transponemos la matriz para eliminar las columnas con esos indices
                copiaNuevaMatrizPresente = copiaNuevaMatrizPresente.T
                #*Eliminar las columnas con esos indices
                copiaNuevaMatrizPresente = np.delete(copiaNuevaMatrizPresente, columna, axis=0)
                #*Transponer la matriz para dejarla como estaba
                copiaNuevaMatrizPresente = copiaNuevaMatrizPresente.T

            copiaNuevaMatrizPresente = copiaNuevaMatrizPresente.T
            # print(copiaNuevaMatrizPresente)

            #* identificar los grupos que se repiten en columnas
            arreglo = [[] for i in range(len(copiaNuevaMatrizPresente[0]))]
            # print(arreglo)

            arreglo = [[] for i in range(len(copiaNuevaMatrizPresente[0]))]
            for fila in copiaNuevaMatrizPresente:
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
            # print("Repetidos", repetidos_con_indices)

            for subarreglo, indices in repetidos_con_indices.items():
                menorIndice = min(indices)
                #* recorre [0,1,16]
                for i in indices:
                    if i != menorIndice:
                        for k in range(len(copiaNuevaTPM[i])):
                            copiaNuevaTPM[menorIndice][k] += copiaNuevaTPM[i][k]
                            copiaNuevaTPM[i][k] = 99

                    #* i != 0
                    if i != menorIndice:
                        for k in copiaNuevaMatrizPresente:
                            k[i] = 77

                #*Obtener el numero de columnas de la tpm
                numero_columnas = len(copiaNuevaTPM[0])

                #*Recorrer el numero de columnas
                for k in range(numero_columnas):
                    division = copiaNuevaTPM[menorIndice][k] / len(indices)
                    copiaNuevaTPM[menorIndice][k] = division
                
                        
            #* Transponer la matriz para eliminar las columnas con 77 y dejarla como estaba
            copiaNuevaMatrizPresente = copiaNuevaMatrizPresente.T

            #* Eliminar las columnas con 77
            filas_a_eliminar = []
            for i in range(len(copiaNuevaMatrizPresente)):
                if 77 in copiaNuevaMatrizPresente[i]:
                    filas_a_eliminar.append(i)

            copiaNuevaMatrizPresente = np.delete(copiaNuevaMatrizPresente, filas_a_eliminar, axis=0)

            #*Eliminar las columnas con 99
            filas_a_eliminar = []
            for i in range(len(copiaNuevaTPM)):
                if 99 in copiaNuevaTPM[i]:
                    filas_a_eliminar.append(i)

            copiaNuevaTPM = np.delete(copiaNuevaTPM, filas_a_eliminar, axis=0)
        
            # print(copiaNuevaMatrizPresente)
            # print(copiaNuevaMatrizFuturo)
            # print(copiaNuevaTPM)

            # print("indiceselementost", indicesElementosT)
            valores = []
            for i in estadoActualElementos:
                if list(i.keys())[0] in elementosT:
                    valor = list(i.values())[0]
                    valores.append(valor)

            #*cortar valores a la cantidad de columnas de la matriz presente
            valores = valores[:len(copiaNuevaMatrizPresente.T)]
            valor = valores[0]
            
            sumaValoresTpm = sum(copiaNuevaTPM[valor])
            
            if sumaValoresTpm == 1:
                return 0


    #? CASO 2: cuando el futuro es vacio
    if particion[1] == []:
        #* uso la matriz presente, la matriz futura y la tpm original partidas
        valores = []
        elementosFuturo = particion[0]

        for elemento in elementosFuturo:
            #* selecciono la matriz futura y tpm correspondiente

            copiaMatricesPresentes = copy.deepcopy(matricesPresentes)
            copiaMatricesFuturas = copy.deepcopy(matricesFuturas)
            copiaMatricesTPM = copy.deepcopy(matricesTPM)

            matrizPresente  = copiaMatricesPresentes
            matrizFuturo = copiaMatricesFuturas[elemento]
            matrizTpm = copiaMatricesTPM[elemento]

            # print("Matriz presente", matrizPresente)
            # print("Matriz futuro", matrizFuturo)
            # print("Matriz tpm", matrizTpm)

            #* sumar el valor de cada columna de la tpm
            matrizTpm = matrizTpm.T
            for i in range(len(matrizTpm)):
                suma = sum(matrizTpm[i])
                valores.append(suma)

            # print(len(matrizTpm[0]))
            for i in range(len(valores)):
                valores[i] = valores[i] / len(matrizTpm[0])

            # print("Valores", valores)

        return sum(valores)

    #? CASO 3: cuando el futuro y el presente no son vacios
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