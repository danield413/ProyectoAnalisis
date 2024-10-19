import numpy as np

# Creamos una matriz de ejemplo
nuevaMatrizPresente = np.array([[1, 2, 3, 4],
                                 [5, 6, 7, 8],
                                 [9, 10, 11, 12]])

# Imprimimos la matriz original
print("Matriz original:")
print(nuevaMatrizPresente)

# Definimos el índice de la columna que queremos eliminar
indice = 2  # Por ejemplo, eliminaremos la tercera columna (índice 2)

# Ahora eliminamos las columnas que estén en la posición 'indice'
nuevaMatrizPresente = np.delete(nuevaMatrizPresente, indice, axis=1)

# Imprimimos la matriz después de la eliminación
print("Matriz después de eliminar la columna en la posición", indice, ":")
print(nuevaMatrizPresente)
