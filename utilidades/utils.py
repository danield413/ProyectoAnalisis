import numpy as np
from scipy.stats import wasserstein_distance

def generarMatrizPresenteInicial(n):
    # Generamos un array de números de 0 a 2^n - 1
    combinaciones = np.arange(2 ** n)
    
    # Convertimos cada número a su representación binaria, rellenamos con ceros, invertimos (little-endian)
    binario_array = np.unpackbits(combinaciones[:, None].astype(np.uint8), axis=1)[:, -n:]
    
    return np.fliplr(binario_array)

import numpy as np

def generarMatrizFuturoInicial(matriz):
    # Convertir la lista de listas a una matriz NumPy y luego transponerla
    return np.array(matriz).T


def elementosNoSistemaCandidato(estadoActualElementos, subconjuntoElementos):
    return [elemento for elemento in reversed(estadoActualElementos) if next(iter(elemento)) not in subconjuntoElementos]

#* Función que calcula el producto tensorial entre n vectores
def producto_tensorial_n(vectores: list[np.ndarray]) -> np.ndarray:
    resultado = vectores[0]
    for vector in vectores[1:]:
        resultado = np.kron(resultado, vector).flatten()
    
    return resultado

def producto_tensorial(a: np.ndarray ,b: np.ndarray):
    return np.kron(a,b).flatten()

#* Función para calcular la distancia EMD
def calcularEMD(a: np.ndarray, b: np.ndarray):
    emd_value = wasserstein_distance(a, b)
    return emd_value

def obtenerParticion(elementos):
    elementosT = [elem for elem in elementos if 't' in elem and 't+1' not in elem]
    elementosT1 = [elem for elem in elementos if 't+1' in elem]
    return (elementosT1, elementosT)

def obtenerParticionEquilibrio(elementos, subconjuntoSistemaCandidato):
    #*elemento de t+1 que no estan en subconjuntoSistemaCandidato
    elementosT1 = []
    for elemento in subconjuntoSistemaCandidato:
        if 't+1' in elemento and 't' not in elemento:
            print("elemento", elemento)

    # print("elementosT1", elementosT1)
        
def generarCombinacionesEstadosIniciales(n):
    #* generar un arreglo con todas las combinaciones para n elementos en binario
    combinaciones = []
    for i in range(2**n):
        combinaciones.append(bin(i)[2:].zfill(n))
    return combinaciones