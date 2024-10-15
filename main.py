from utils import generar_combinaciones_binarias_little_endian
from utils import transponer_matriz

# ENTRADAS DE DATOS

#* Matriz de probabilidades
TPM = [
    [0.7, 0.3, 1  , 0  ], 
    [0.4, 0.6, 0.2, 1  ],
    [0.3, 0  , 1  , 0.4],
    [0.5, 0.5, 0.3, 0.7],
]

subconjuntoSistemaCandidato = [
    'at', 'bt', 'ct', 'at+1', 'bt+1', 'ct+1'
]

estadoActualElementos = {
    'at': 1,
    'bt': 0,
    'ct': 0,
    'dt': 0
}


#* El subconjunto de elementos a analizar 
#* SISTEMA CANDIDATO
subconjuntoElementos = ['at', 'bt', 'ct']

#* Calcular distribución
# def calcularDistribucion(TPM):
#     #* obtener los elementos del sistema
#     elementos = [ ]
#     for i in estadoActualElementos:
#         elementos.append(i)

#     #* Crear matriz en t siguiendo la notacion little endian
#     matrizT = [ ]

#     for i in range(0, len(elementos)):
        


# calcularDistribucion(TPM)



# Ejemplo para n = 4
n = 4
matrizPresente = generar_combinaciones_binarias_little_endian(n)

# Imprimir todas las combinaciones en little endian
for combinacion in matrizPresente:
    print(combinacion)

MatrizFuturo = transponer_matriz(matrizPresente)
for i in MatrizFuturo:
    print(i)

#* Condiciones de background

# obtener los elementos del sistema que no hacen parte del sistema candidato y su posicion
elementosBackground = [ ]
posicion = []
for i in estadoActualElementos:
    if i not in subconjuntoElementos:
        elementosBackground.append({ i: estadoActualElementos[i] })

print(elementosBackground)

#* aplicar condiciones de background
if len(elementosBackground) > 0:
    for elemento in elementosBackground:
        #* obtener el index del elemento en la matriz presente y futuro
        index = 0
        for i in estadoActualElementos:
            if i == list(elemento.keys())[0]:
                index = list(estadoActualElementos.keys()).index(i)
                break
        
        #* aplicar la condicion de background
        #* verificar el valor del elemento en el estado actual
        if list(elemento.values())[0] == 0:
            pass

        else:
            pass