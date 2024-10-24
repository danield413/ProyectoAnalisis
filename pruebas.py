import numpy as np
from scipy.stats import wasserstein_distance

def producto_tensorial_n(vectores: list[np.ndarray]) -> np.ndarray:
    resultado = vectores[0]
    for vector in vectores[1:]:
        resultado = np.outer(resultado, vector).flatten()
    
    return resultado

# Crear una lista de np.array
lista_vectores = [np.array([0.25, 0.75]), np.array([0.5, 0.5]),  np.array([0.5, 0.5])]

# Calcular productos tensores para cada lista
producto = producto_tensorial_n(lista_vectores)

print(producto)

def calcularEMD(a: np.ndarray, b: np.ndarray):
    emd_value = wasserstein_distance(a, b)
    return emd_value

#calcular emd
emd = calcularEMD(producto, np.array([0,0,0,0,0,1,0,0]))
print(emd)