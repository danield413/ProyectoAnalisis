import numpy as np
from scipy.stats import wasserstein_distance

def producto_tensorial(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    tensor_product = np.outer(p1, p2)
    return tensor_product

v1 = np.array([0.5, 0.5])
v2 = np.array([1, 0])
v3 = np.array([0.5, 0.5])

# Calculamos el producto tensorial entre los 3 vectores
t1 = producto_tensorial(v1, v2)
t2 = producto_tensorial(t1.flatten(), v3)

# print(tensor_123.flatten())

def calculateEmd(a,b):
    emd_value = wasserstein_distance(a, b)
    return emd_value

t = producto_tensorial(t2, 1)
print(t.flatten())

print(calculateEmd(t.flatten(), np.array([0,0.25,0,0.5,0,0,0.25,0])))