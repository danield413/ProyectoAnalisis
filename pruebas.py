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

# Ejemplo de uso
if __name__ == "__main__":
    # Distribución P(X)
    P_X = np.array([0,1], dtype=np.float64)
    
    # Distribución P(X')
    P_X_prima = np.array([1, 0], dtype=np.float64)
    
    # Distribución objetivo P(V)
    P_V = np.array([0, 0, 0, 0], dtype=np.float64)

    # Paso 1: Calcular el producto tensorial de P(X) y P(X')
    P_X_X_prima = producto_tensorial(P_X, P_X_prima)
    print("Producto tensorial P(X) ⊗ P(X'):")
    print(P_X_X_prima)
    
    # Paso 2: Aplanar la matriz resultante
    P_X_X_prima_flat = aplanar_matriz(P_X_X_prima)
    print("\nProducto tensorial aplanado:")
    print(P_X_X_prima_flat)
    
    # Paso 3: Calcular la EMD entre el producto tensorial y P(V)
    resultado_emd = emd_manual(P_X_X_prima_flat, P_V)
    
    # Imprimir el resultado
    print(f"\nEMD entre P(X) ⊗ P(X') y P(V): {resultado_emd}")
