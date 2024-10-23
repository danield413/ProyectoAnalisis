import numpy as np

# Función para calcular el producto tensorial entre dos distribuciones
def producto_tensorial(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    # Calculamos el producto tensorial usando np.outer
    tensor_product = np.outer(p1, p2)
    return tensor_product

# Función para aplanar una matriz en un vector
def aplanar_matriz(matriz: np.ndarray) -> np.ndarray:
    return matriz.flatten()

# Función para calcular EMD manualmente (como antes)
def emd_manual(u: np.ndarray, v: np.ndarray) -> float:
    if len(u) != len(v):
        raise ValueError("Los arrays deben tener el mismo tamaño.")
    
    total_emd = 0
    diferencia_acumulada = 0

    for i in range(len(u)):
        diferencia = u[i] - v[i]
        diferencia_acumulada += diferencia
        total_emd += abs(diferencia_acumulada)

    return total_emd

# Producto tensorial entre 3 vectores
# v1 = np.array([1, 0])
# v2 = np.array([1, 0])
# v3 = np.array([1, 0])

# # Calculamos el producto tensorial entre los 3 vectores
# tensor_12 = producto_tensorial(v1, v2)
# tensor_123 = producto_tensorial(tensor_12.flatten(), v3)

# print(tensor_123.flatten())

# emdresult = emd_manual(tensor_123.flatten(), np.array([0, 1, 0, 0, 0, 0, 0, 0]))
# print(emdresult)

# Producto tensorial entre 3 vectores
v1 = np.array([1, 0,0,0,0,0,0,0])
v2 = np.array([0])

# Calculamos el producto tensorial entre los 3 vectores
tensor_123 = producto_tensorial(v1, v2)

print(tensor_123.flatten())

# emdresult = emd_manual(tensor_123.flatten(), np.array([0, 1, 0, 0, 0, 0, 0, 0]))
# print(emdresult)
