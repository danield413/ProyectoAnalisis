import copy
import numpy as np
import tkinter as tk

from utilidades.evaluarParticionesFinales import evaluarParticionesFinales
from utilidades.background import aplicarCondicionesBackground
from utilidades.marginalizacionInicial import aplicarMarginalizacion
from utilidades.organizarCandidatas import organizarParticionesCandidatasFinales
from utilidades.utils import generarMatrizPresenteInicial
from utilidades.utils import generarMatrizFuturoInicial
from utilidades.utils import elementosNoSistemaCandidato
from utilidades.partirRepresentacion import partirRepresentacion
from utilidades.utils import producto_tensorial
from utilidades.comparaciones import compararParticion
from UI.interfaz import InterfazCargarDatos



#? ----------------- CARGAR LA INTERFAZ ---------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCargarDatos(root)
    root.mainloop()


# #? ----------------- ENTRADAS DE DATOS ---------------------------------
# #from data.matrices import TPM
# TPM = app.TPM
# #from data.matrices import subconjuntoSistemaCandidato
# subconjuntoSistemaCandidato = app.subconjuntoSistemaCandidato
# #from data.matrices import estadoActualElementos
# estadoActualElementos = app.estado_actual
# #from data.matrices import subconjuntoElementos
# subconjuntoElementos = app.subconjuntoElementos
# from utilidades.vectorProbabilidad import encontrarVectorProbabilidades


# #? ----------------- MATRIZ PRESENTE Y MATRIZ FUTURO ---------------------------------

# matrizPresente = generarMatrizPresenteInicial( len(estadoActualElementos) )
# matrizFuturo = generarMatrizFuturoInicial(matrizPresente)

# #? ----------------- APLICAR CONDICIONES DE BACKGROUND ---------------------------------

# #? Elementos que no hacen parte del sistema cantidato
# elementosBackground = elementosNoSistemaCandidato(estadoActualElementos, subconjuntoElementos)

# #? Realizar una copia de las matrices para no modificar las originales
# nuevaTPM = np.copy(TPM)
# nuevaMatrizPresente = np.copy(matrizPresente)
# nuevaMatrizFuturo = np.copy(matrizFuturo)


# #? Ejecución de las condiciones de background
# nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, nuevaTPM, elementosBackground, nuevaMatrizFuturo, estadoActualElementos)


# #? ----------------- APLICAR MARGINALIZACIÓN INICIAL ---------------------------------

# nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, elementosBackground, estadoActualElementos, nuevaMatrizPresente)


# #?  ------------------------ DIVIDIR EN LA REPRESENTACION -----------------------------------
# #? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

# #* tomar el subconjunto de elementos (los de t y t+1) con su indice
# elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
# elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]

# indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

# #? Ejecución de la representación
# print("------ REPRESENTACIÓN -----------")
# partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1, indicesElementosT)


# particionesCandidatas = []
# listaDeU = []

# print("------ ALGORITMO -----------")
# def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):

#     V = subconjuntoSistemaCandidato #* {at, bt, ct, at+1, bt+1, ct+1}
#     # print("V", V)

#     #*crear un arreglo W de len(V) elementos
#     W = []
#     for i in range(len(V)+1):
#         W.append([])

#     W[0] = []
#     W[1] = [ V[0] ]
#     # print(W)

#     restas = []

#     #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
#     for i in range(2, len(V)+1):
#         # print()
#         # print(">>>>>>>>>> LONGITUD V ACTUAL", (len(V)+1), "CONJUNTO: ", V)
#         if (len(V)+1) == 2:
#             break

#         #* ahora recorremos para cada elemento en V que no esté en W[i-1] (el anterior)
#         for elem in V:
#             if  elem not in W[i-1]:
#                 elementoActual = elem

#                 #* aquí planteamos el conjunto que le vamos a pasar a la función de comparación
#                 union = []
#                 for elem in W[i-1]:
#                     union.append(elem)
#                 if 'u' not in elementoActual:
#                     union.append(elementoActual)

#                 #* si elemento es una u
#                 if 'u' in elementoActual:
#                     #* buscar los elementos que conforman la u
#                     for u in listaDeU:
#                         #* cojo el nombre de la llave
#                         nombre = list(u.keys())[0]
#                         if nombre == elementoActual:
#                             #* cojo el valor de la llave
#                             elementosU = u[nombre]
#                             #* recorro los elementos de la u
#                             for elem in elementosU:
#                                 # print("ELEMENTO U", elem)
#                                 union.append(elem)

#                 # print("UNION", union)

#                 #* separamos de la union los elementos que estan en t+1 y en t
#                 particion = ( [ elem for elem in union if 't+1' in elem ], [ elem for elem in union if 't' in elem and 't+1' not in elem ] )
#                 # print("PARTICION", particion)

#                 #! ------------------ g(Wi-1 ∪ {vi}) ----------------------------

#                 #? crear copias de las matrices para no modificar las originales
#                 copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
#                 copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
#                 copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

#                 #* obtenemos el vector de probabilidades de la partición

#                 vectorProbabilidades = encontrarVectorProbabilidades(particion, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
#                 # print("vectorProbabilidades", vectorProbabilidades)

#                 #* Obtenemos el vector de probabilidades del conjunto que equilibra la particion
#                 #* Obtener el equilibrio de la partición (lo que le falta a la partición para ser igual a la original)
#                 particionEquilibrio = ([elem for elem in V if elem not in particion[0] and 't+1' in elem],[elem for elem in V if elem not in particion[1] and 't' in elem and 't+1' not in elem] )
#                 # print("particionEquilibrio", particionEquilibrio)

#                 #? crear copias de las matrices para no modificar las originales
#                 copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
#                 copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
#                 copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

#                 #*Obtenemos el vector de probabilidades de la partición de equilibrio
#                 vectorProbabilidadesEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
#                 # print("vectorProbabilidadesEquilibrio", vectorProbabilidadesEquilibrio)

#                 #* Calcular la diferencia entre los dos vectores de probabilidades
#                 vectorResultado = producto_tensorial(vectorProbabilidades, vectorProbabilidadesEquilibrio)
#                 valorwi_gu = compararParticion(vectorResultado, nuevaMatrizPresente, nuevaTPM, subconjuntoElementos, estadoActualElementos)
#                 # print("VALOR EMD valorwi_gu", valorwi_gu)

#                 #! ----------------------------- g({vi}) --------------------------------------

#                 print("ELEMENTO ACTUAL", elementoActual)
#                 #*Obtenemos la particion solamente del elemento actual sin nada mas
#                 particionElementoActual2 = ([elem for elem in V if elem == elementoActual and 't+1' in elem],[elem for elem in V if elem == elementoActual and 't' in elem and 't+1' not in elem] )

#                 #*Obtenemos la particion de equilibrio del elemento actual
#                 particionEquilibrioElementoActual2 = ([elem for elem in V if elem != elementoActual and 't+1' in elem],[elem for elem in V if elem != elementoActual and 't' in elem and 't+1' not in elem] )


#                 #? crear copias de las matrices para no modificar las originales
#                 copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
#                 copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
#                 copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

#                 vectorProbabilidades2 = encontrarVectorProbabilidades(particionElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
#                 # print("vectorProbabilidades2", vectorProbabilidades2)

#                 #? crear copias de las matrices para no modificar las originales
#                 copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
#                 copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
#                 copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

#                 vectorProbabilidadesEquilibrioElementoActual2 = encontrarVectorProbabilidades(particionEquilibrioElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
#                 # print("vectorProbabilidadesEquilibrioElementoActual2", vectorProbabilidadesEquilibrioElementoActual2)

#                 #* Calcular la diferencia entre los dos vectores de probabilidades
#                 vectorResultadoElementoActual = producto_tensorial(vectorProbabilidades2, vectorProbabilidadesEquilibrioElementoActual2)

#                 valorg_u = compararParticion(vectorResultadoElementoActual, nuevaMatrizPresente, nuevaTPM, subconjuntoElementos, estadoActualElementos)
#                 valorRestaFinal = valorwi_gu - valorg_u

#                 restas.append((elementoActual, valorRestaFinal))

#         menorTupla = ()
#         if len(restas) > 0:
#             menorTupla = min(restas, key=lambda x: x[1])
#             valoresI = copy.deepcopy(W[i-1])
#             valoresI.append(menorTupla[0])

#         W[i] = valoresI
#         restas = []

#         SecuenciaResultante = []
#         for x in W:
#             if x == []:
#                 continue
#             #*agregar el elemento de la ultima posicion de x
#             SecuenciaResultante.append(x[-1])

#         parCandidato = (SecuenciaResultante[-2], SecuenciaResultante[-1])

#         ultimoElemento = SecuenciaResultante[-1]

#         p1 = None
#         p2 = None
#         #* si el ultimo elemento tiene t+1
#         if 't+1' in ultimoElemento:
#             p1 = ([ultimoElemento], [])
#             p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )
#         else:
#             p1 = ([],[ultimoElemento])
#             p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )

#         particionCandidata = {
#             'p1': p1,
#             'p2': p2
#         }

#         particionesCandidatas.append(particionCandidata)

#         #* se crea una nueva variable llamada u' que es la union de los dos elementos del par candidato
#         nuevoV = np.array([ elem for elem in V if elem not in parCandidato ])

#         uprima = [ parCandidato[0], parCandidato[1] ]

#         #*verifico si en uprima hay una u embebida
#         if 'u' in uprima[0]:
#             for u in listaDeU:
#                 nombre = list(u.keys())[0]
#                 if nombre == uprima[0]:
#                    for x in u[nombre]:
#                         uprima.append(x)
#         if 'u' in uprima[1]:
#             #*voy a la lista de u a buscar el nombre de la u
#             for u in listaDeU:
#                 nombre = list(u.keys())[0]
#                 if nombre == uprima[1]:
#                    for x in u[nombre]:
#                         uprima.append(x)
#             #* elimino la u de la lista de u

#         for elementoU in listaDeU:
#             valor = list(elementoU.values())[0]
#             for x in range(len(valor) - 1, -1, -1):  # Itera en orden inverso
#                 if 'u' in valor[x]:
#                     valor.pop(x)  # Elimina el elemento sin afectar los índices restantes

#         total = 0
#         for x in listaDeU:
#             nombre = list(x.keys())[0]
#             if 'u' in nombre:
#                 total += 1

#         nombreU = 'u_prima' + str(total+1)
#         nuevoV = np.append(nuevoV, nombreU)
#         listaDeU.append({nombreU: uprima})


#         #* LA 1ERA VEZ QUE OBTIENE LA SECUENCIA RESULTANTE SE CIERRA EL CICLO Y SE LLAMA A LA RECURSIÓN
#         if i == 2:
#             if((len(V)+1) > 2):
#                 print("SE LLAMÓ LA RECURSIÓN")
#                 algoritmo(nuevaTPM, subconjuntoElementos, nuevoV, estadoActualElementos)
#                 break

#     particionesFinales = organizarParticionesCandidatasFinales(copy.deepcopy(particionesCandidatas), listaDeU, subconjuntoElementos)
#     particionElegida = evaluarParticionesFinales(particionesFinales, partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
#     return particionElegida


# x = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
# print("resultado algoritmo", x)




# copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
# copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
# copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

