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
    'at','bt' ,'at+1', 'bt+1'
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

print("------ BACKGROUND -----------")
print("Matriz presente")
print(nuevaMatrizPresente)
print("Matriz futuro")
print(nuevaMatrizFuturo)
print("TPM")
print(nuevaTPM)

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

print("------ MARGINALIZACIÓN -----------")

print("Matriz presente")
print(nuevaMatrizPresente)
print("Matriz futuro")
print(nuevaMatrizFuturo)
print("TPM")
print(nuevaTPM)


#? ------------------ INICIAR PROCESO DE COMPARACION ----------------------------