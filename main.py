from utils import generarMatrizPresenteInicial
from utils import generarMatrizFuturoInicial
import numpy as np

# ENTRADAS DE DATOS
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


subconjuntoSistemaCandidato = np.array([
    'at', 'bt', 'ct', 'at+1', 'bt+1', 'ct+1'
])

estadoActualElementos = np.array([
    {'at': 1},
    {'bt': 0},
    {'ct': 0},
    {'dt': 0}
])

#* SISTEMA CANDIDATO
subconjuntoElementos = np.array(['at', 'bt', 'ct'])

#* MATRICES INICIALES
n = len(estadoActualElementos)
matrizPresente = generarMatrizPresenteInicial(n)

matrizFuturo = generarMatrizFuturoInicial(matrizPresente)

# #* Condiciones de background

#* Elementos que no hacen parte del sistema cantidato
elementosBackground = [elemento for elemento in estadoActualElementos if next(iter(elemento)) not in subconjuntoElementos]

nuevaTPM = np.copy(TPM)
nuevaMatrizPresente = np.copy(matrizPresente)
nuevaMatrizFuturo = np.copy(matrizFuturo)
#? aplicar condiciones de background
#? Params
#? matrizPresente: matriz presente
#? matrizFuturo: matriz futuro
#? TPM: matriz de transición de probabilidad
#? elementosBackground: elementos del background {elemento: valor inicial}
def aplicarCondicionesBackground(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosBackground):
    if len(elementosBackground) > 0:
        for elemento in elementosBackground:

            llave = list(elemento.keys())[0]

            indice = next((idx for idx, i in enumerate(estadoActualElementos) if llave in i), len(estadoActualElementos))

            valorActualElemento = elemento[llave]
            
            #* Ya sabemos la posicion del elementp
            #* Ahora buscamos en la matriz presente y futura la fila y columna correspondiente
            # Si el valor actual del elemento es 0 dejamos las filas que tengan 1
            # Si el valor actual del elemento es 1 dejamos las filas que tengan 0
            for i in range(len(nuevaMatrizPresente)):
                if nuevaMatrizPresente[i][indice] == 0 if valorActualElemento == 0 else 1:
                    nuevaMatrizPresente[i].fill(99)

            filas_a_eliminar = []
            for i in range(len(nuevaMatrizPresente)):
                if 99 in nuevaMatrizPresente[i]:
                    filas_a_eliminar.append(i)

            # Ahora eliminamos las filas de la matriz presente usando los índices acumulados
            nuevaMatrizPresente = np.delete(nuevaMatrizPresente, filas_a_eliminar, axis=0)

            
            # Ahora eliminamos las columnas de la matriz presente que estén en la posición indice
            nuevaMatrizPresente = np.delete(nuevaMatrizPresente, indice, axis=1)

            nuevaTPM = np.delete(nuevaTPM, filas_a_eliminar, axis=0)

            for i in nuevaMatrizPresente:
                print(i)

    
    return nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM
            

            


#* Aplicar condiciones de background
nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, matrizFuturo, nuevaTPM, elementosBackground)            

print("Matriz presente")
print(nuevaMatrizPresente)
print("Matriz futuro")
print(nuevaMatrizFuturo)
print("TPM")
print(nuevaTPM)


