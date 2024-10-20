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
    'at','bt', 'ct','at+1', 'bt+1', 'ct+1'
])

#? El estado actual de todos los elementos del sistema
estadoActualElementos = np.array([
    {'at': 0},
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
def aplicarCondicionesBackground(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosBackground):
    
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
nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, matrizFuturo, nuevaTPM, elementosBackground)            

print("Matriz presente")
print(nuevaMatrizPresente)
print("Matriz futuro")
print(nuevaMatrizFuturo)
print("TPM")
print(nuevaTPM)


