import numpy as np

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
