def generar_combinaciones_binarias_little_endian(n):
    combinaciones = []
    # Generamos números del 0 al 2^n - 1, que son todas las combinaciones binarias
    for i in range(2 ** n):
        # Convierte el número 'i' a su representación binaria y lo rellena con ceros para que tenga 'n' bits
        combinacion = format(i, f'0{n}b')
        # Convertir el string binario a una lista de enteros y luego invertir el orden (little endian)
        combinaciones.append([int(bit) for bit in combinacion[::-1]])
    
    return combinaciones


def transponer_matriz(matriz):
    # Usar comprensión de listas para transponer la matriz
    return [[fila[i] for fila in matriz] for i in range(len(matriz[0]))]