import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
from data.cargarData import obtenerInformacionCSV

import copy
import numpy as np
import tkinter as tk

from utilidades.evaluarParticionesFinales import evaluarParticionesFinales
from utilidades.background import aplicarCondicionesBackground
from utilidades.marginalizacionInicial import aplicarMarginalizacion
from utilidades.organizarCandidatas import buscarValorUPrima, organizarParticionesCandidatasFinales
from utilidades.utils import generarMatrizPresenteInicial, obtenerParticion
from utilidades.utils import generarMatrizFuturoInicial
from utilidades.utils import elementosNoSistemaCandidato
from utilidades.partirRepresentacion import partirRepresentacion
from utilidades.utils import producto_tensorial
from utilidades.comparaciones import compararParticion

# Clase para la interfaz de usuario
class InterfazCargarDatos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargar y Mostrar Datos CSV")
        self.root.geometry("700x600")
        self.root.config(bg="#f2f2f2")
        
        self.estado_actual_elementos = []  # Lista para almacenar los estados ingresados
        self.nombres_validos = []  # Lista para almacenar los nombres válidos del subconjunto elementos

        # Atributos para almacenar datos cargados como np.array
        self.subconjuntoSistemaCandidato = np.array([])
        self.subconjuntoElementos = np.array([])
        self.TPM = np.array([])

        # Atributo para almacenar el estado actual de los elementos
        self.estado_actual = None
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # Etiqueta y botón para cargar archivo
        tk.Label(self.root, text="Seleccione un archivo CSV:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=10)
        btn_cargar = tk.Button(self.root, text="Cargar Archivo", command=self.cargar_archivo, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        btn_cargar.pack(pady=5)

        # Crear Notebook para organizar resultados en pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear pestañas y cuadros de texto para cada resultado
        self.text_subconjuntoSistemaCandidato = self.crear_pestana("Subconjunto Sistema Candidato")
        self.text_subconjuntoElementos = self.crear_pestana("Subconjunto Elementos")
        self.text_TPM = self.crear_pestana("TPM")

        # Crear pestaña para entrada manual de estadoActualElementos
        self.crear_pestana_estado_actual()

        # Botón para resolver en la ventana principal
        btn_resolver = tk.Button(self.root, text="Resolver", command=self.resolver, font=("Arial", 10), bg="#2196F3", fg="white")
        btn_resolver.pack(pady=10)


    def crear_pestana(self, titulo):
        # Crear un frame para cada pestaña
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=titulo)
        
        # Crear cuadro de texto dentro de la pestaña
        text_widget = tk.Text(frame, wrap="none", height=15, width=60, state='disabled')
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        return text_widget

    def crear_pestana_estado_actual(self):
        frame_estado_actual = ttk.Frame(self.notebook)
        self.notebook.add(frame_estado_actual, text="Estado Actual Elementos")

        # Crear entrada para nombre y valor de cada estado
        tk.Label(frame_estado_actual, text="Nombre del estado:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre_estado = tk.Entry(frame_estado_actual, width=15)
        self.entry_nombre_estado.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_estado_actual, text="Valor del estado (0 o 1):", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.entry_valor_estado = tk.Entry(frame_estado_actual, width=10)
        self.entry_valor_estado.grid(row=0, column=3, padx=5, pady=5)

        # Botón para agregar el estado
        btn_agregar = tk.Button(frame_estado_actual, text="Agregar Estado", command=self.agregar_estado, font=("Arial", 10), bg="#4CAF50", fg="white")
        btn_agregar.grid(row=0, column=4, padx=5, pady=5)

        # Crear cuadro de texto para mostrar el estado actual
        self.text_estado_actual = tk.Text(frame_estado_actual, wrap="none", height=10, width=60, state='disabled')
        self.text_estado_actual.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

    def agregar_estado(self):
        # Obtener el nombre y valor ingresado
        nombre = self.entry_nombre_estado.get().strip()
        valor = self.entry_valor_estado.get().strip()

        # Verificar si el nombre está en la lista de nombres válidos
        if nombre not in self.nombres_validos:
            messagebox.showerror("Error", f"El nombre '{nombre}' no es válido. Use uno de los siguientes: {', '.join(self.nombres_validos)}")
            return

        # Validar que el valor sea un 0 o 1
        if not valor.isdigit() or int(valor) not in [0, 1]:
            messagebox.showerror("Error", "Ingrese un valor de 0 o 1.")
            return

        # Verificar si el estado ya existe en estado_actual_elementos
        if any(nombre in estado for estado in self.estado_actual_elementos):
            messagebox.showerror("Error", f"El estado '{nombre}' ya ha sido agregado.")
            return

        # Agregar el estado a la lista
        self.estado_actual_elementos.append({nombre: int(valor)})
        self.mostrar_estado_actual()

        # Actualizar el estado actual
        self.estado_actual = self.estado_actual_elementos.copy()  # Guardar el estado actual

        # Limpiar entradas
        self.entry_nombre_estado.delete(0, tk.END)
        self.entry_valor_estado.delete(0, tk.END)

    def mostrar_estado_actual(self):
        # Mostrar la lista de estados en el cuadro de texto
        self.text_estado_actual.config(state='normal')
        self.text_estado_actual.delete(1.0, tk.END)
        for estado in self.estado_actual_elementos:
            self.text_estado_actual.insert(tk.END, f"{estado}\n")
        self.text_estado_actual.config(state='disabled')

    def resolver(self):
        # Verificar si se ha cargado un archivo
        if not self.nombres_validos:
            messagebox.showerror("Error", "Por favor, cargue primero un archivo CSV.")
            return

        # Verificar que todos los elementos del subconjunto estén en estado_actual_elementos
        elementos_faltantes = [estado for estado in self.nombres_validos if all(estado not in e for e in self.estado_actual_elementos)]
        
        if elementos_faltantes:
            messagebox.showerror("Error", f"Faltan los siguientes elementos: {', '.join(elementos_faltantes)}")
            return
        
                #? ----------------- ENTRADAS DE DATOS ---------------------------------
        #from data.matrices import TPM
        TPM = self.TPM
        #from data.matrices import subconjuntoSistemaCandidato
        subconjuntoSistemaCandidato = self.subconjuntoSistemaCandidato
        #from data.matrices import estadoActualElementos
        estadoActualElementos = self.estado_actual
        #from data.matrices import subconjuntoElementos
        subconjuntoElementos = self.subconjuntoElementos
        from utilidades.vectorProbabilidad import encontrarVectorProbabilidades


        #? ----------------- MATRIZ PRESENTE Y MATRIZ FUTURO ---------------------------------

        matrizPresente = generarMatrizPresenteInicial( len(estadoActualElementos) )
        matrizFuturo = generarMatrizFuturoInicial(matrizPresente)

        #? ----------------- APLICAR CONDICIONES DE BACKGROUND ---------------------------------

        #? Elementos que no hacen parte del sistema cantidato
        elementosBackground = elementosNoSistemaCandidato(estadoActualElementos, subconjuntoElementos)

        #? Realizar una copia de las matrices para no modificar las originales
        nuevaTPM = np.copy(TPM)
        nuevaMatrizPresente = np.copy(matrizPresente)
        nuevaMatrizFuturo = np.copy(matrizFuturo)


        #? Ejecución de las condiciones de background
        nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarCondicionesBackground(matrizPresente, nuevaTPM, elementosBackground, nuevaMatrizFuturo, estadoActualElementos)


        #? ----------------- APLICAR MARGINALIZACIÓN INICIAL ---------------------------------

        nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, nuevosIndicesElementos = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, elementosBackground, estadoActualElementos, nuevaMatrizPresente)


        #?  ------------------------ DIVIDIR EN LA REPRESENTACION -----------------------------------
        #? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

        #* tomar el subconjunto de elementos (los de t y t+1) con su indice
        elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
        elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]

        indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

        #? Ejecución de la representación
        partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT1, nuevosIndicesElementos)


        particionesCandidatas = []
        listaDeUPrimas = []

        print("------ ALGORITMO -----------")
        def algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos):

            V = subconjuntoSistemaCandidato #* {at, bt, ct, at+1, bt+1, ct+1}
            # print("V", V)

            #*crear un arreglo W de len(V) elementos
            W = []
            for i in range(len(V)+1):
                W.append([])

            W[0] = []
            W[1] = [ V[0] ]
            # print(W)

            restas = []

            #* Iteración Principal: Para i = 2 hasta n (donde n es el número de nodos en V) se calcula :
            for i in range( 2, len(V) + 1 ):
                # print()
                # print(" - - - - - - - Iteración - - - - - - - - - ", i)

                #* se recorren los elementos V - W[i-1]
                elementosRecorrer = [elem for elem in V if elem not in W[i-1]]

                for elemento in elementosRecorrer:
                    if 'u' not in elemento:
                        
                        #* W[i-1] U {u}
                        wi_1Uelemento = W[i-1] + [elemento]
                        #* {u}
                        u = elemento

                        #? Calcular  EMD(W[i-1] U {u})
                        # print("EMD(W[i-1] U {u})", wi_1Uelemento)
                        particionNormal = obtenerParticion(wi_1Uelemento)
                        # print("     - particionNormal", particionNormal)
                        particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
                        # print("     - particionEquilibrio", particionEquilibrio)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                        vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                        vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)   


                        #* Calcular la diferencia entre los vectores
                        resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                        valorEMDParticionNormal = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)
                        
                        #? Calcular EMD({u})
                        particionNormal = obtenerParticion([u])
                        particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
                        
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

                        vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

                        vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        #* Calcular la diferencia entre los vectores
                        resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                        valorEMDU = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)

                        valorEMDFinal = valorEMDParticionNormal - valorEMDU
                        # print("          - valorEMDFinal", valorEMDFinal)

                        # print("elemento", elemento, "valorEMDFinal", valorEMDFinal)
                        restas.append((elemento, valorEMDFinal))

                    #! paso importante: verificar la existencia de u
                    #! si hay una u debo ir a la lista de u' y tomar el valor correspondiente
                    if 'u' in elemento:

                        valor = buscarValorUPrima(listaDeUPrimas, elemento)

                        #* W[i-1] U {u}
                        wi_1Uelemento = W[i-1] + valor
                        #* {u}
                        u = elemento

                        # print("wi_1Uelemento", wi_1Uelemento)
                        # print("u formula", u)

                        #? Calcular  EMD(W[i-1] U {u})
                        # print("EMD(W[i-1] U {u})", wi_1Uelemento)
                        particionNormal = obtenerParticion(wi_1Uelemento)
                        # print("     - particionNormal", particionNormal)
                        particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
                        # print("     - particionEquilibrio", particionEquilibrio)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                        vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)

                        vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)   


                        #* Calcular la diferencia entre los vectores
                        resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                        valorEMDParticionNormal = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)
                        
                        #? Calcular EMD({u})
                        particionNormal = obtenerParticion([u])
                        particionEquilibrio = ([elem for elem in V if elem not in particionNormal[0] and 't+1' in elem],[elem for elem in V if elem not in particionNormal[1] and 't' in elem and 't+1' not in elem] )
                        
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

                        vectorNormal = encontrarVectorProbabilidades(particionNormal, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaMatrizFuturo = copy.deepcopy(nuevaMatrizFuturo)

                        vectorEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos,indicesElementosT, copiaNuevaMatrizPresente, copiaNuevaMatrizFuturo, copiaNuevaTPM, elementosT)

                        #* Calcular la diferencia entre los vectores
                        resultado = producto_tensorial(vectorNormal, vectorEquilibrio)
                        copiaNuevaMatrizPresente = copy.deepcopy(nuevaMatrizPresente)
                        copiaNuevaTPM = copy.deepcopy(nuevaTPM)
                        valorEMDU = compararParticion(resultado,copiaNuevaMatrizPresente, copiaNuevaTPM, subconjuntoElementos, estadoActualElementos)

                        valorEMDFinal = valorEMDParticionNormal - valorEMDU
                        # print("          - valorEMDFinal", valorEMDFinal)

                        # print("elemento", elemento, "valorEMDFinal", valorEMDFinal)
                        restas.append((elemento, valorEMDFinal))
                        
                    
                    

                #* Seleccionar el vi que minimiza EMD(W[i-1] U {vi})
                menorTupla = ()
                if len(restas) > 0:
                    menorTupla = min(restas, key=lambda x: x[1])
                    valoresI = copy.deepcopy(W[i-1])
                    valoresI.append(menorTupla[0])

                # print(menorTupla)
                W[i] = valoresI
                restas = []

                #*Sacar el par candidato
                if i == len(V):
                    SecuenciaResultante = []
                    for x in W:
                        if x == []:
                            continue
                        #*agregar el elemento de la ultima posicion de x
                        SecuenciaResultante.append(x[-1])


                    parCandidato = (SecuenciaResultante[-2], SecuenciaResultante[-1])

                    ultimoElemento = SecuenciaResultante[-1]
                    p1 = None
                    p2 = None
                    #* si el ultimo elemento tiene t+1
                    if 't+1' in ultimoElemento:
                        p1 = ([ultimoElemento], [])
                        p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )
                    else:
                        p1 = ([],[ultimoElemento])
                        p2 = ([elem for elem in V if elem not in p1[0] and 't+1' in elem],[elem for elem in V if elem not in p1[1] and 't' in elem and 't+1' not in elem] )

                    particionCandidata = {
                        'p1': p1,
                        'p2': p2
                    }

                    particionesCandidatas.append(particionCandidata)


                    # print()
                    # print("Par candidato", parCandidato)
                    ultimoElemento = SecuenciaResultante[-1]
                    elementosParticionNormal = [ultimoElemento]
                    # print("Elementos Particion Normal", elementosParticionNormal)
                    
                    uActual = [SecuenciaResultante[-2], SecuenciaResultante[-1]]
                    # print("uActual", uActual)
                    nombreU = ""
                    if(len(listaDeUPrimas) == 0):
                        nombreU = "u1"
                    else:
                        nombreU = "u" + str(len(listaDeUPrimas) + 1)
                    listaDeUPrimas.append({nombreU: uActual})
                    # print("Lista de U'", listaDeUPrimas)

                    #* nuevoV = los elementos de V que no son el par candidato + nombre del uActual
                    nuevoV = []
                    nuevoV = [elem for elem in V if elem not in parCandidato]
                    nuevoV = nuevoV + [nombreU]
                    # print("Nuevo V", nuevoV)

                    #* se procede con la recursión mandando el nuevoV
                    algoritmo(nuevaTPM, subconjuntoElementos, nuevoV, estadoActualElementos)
            
                # print()
                # print()

            # print()
            # print()
            # print("---------------------------------------------------")
            # print('Lista de U Primas')
            # for x in listaDeUPrimas:
            #     print(x)
            # print("Candidatas")
            # for x in particionesCandidatas:
            #     print(x)
            particionesFinales = organizarParticionesCandidatasFinales(copy.deepcopy(particionesCandidatas), listaDeUPrimas, subconjuntoElementos)

            resultado = evaluarParticionesFinales(particionesFinales, partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
            # for x in particionesFinales:
            #     print("Particiones Final", x)
            return resultado
   



        resultado_algoritmo = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
        for i in resultado_algoritmo['particionesEMD']:
            print(i)
            
        print("Particion con menor EMD", resultado_algoritmo['particionMenorEMD'])

        # self.actualizar_resultado(resultado_algoritmo['particionMenorEMD'])
        
        # Abrir una nueva ventana para mostrar el resultado
        self.mostrar_resultado_ventana(resultado_algoritmo['particionesEMD'], resultado_algoritmo['particionMenorEMD'])

    def mostrar_resultado_ventana(self, particionesEMD, particionMenorEMD):
        
        particionesEMDFormateadas = []
        for x in particionesEMD:
            particion = x[0]
            string = "{ "
            for i in particion[0][0]:
                string += i + " "
            string += " | "
            for i in particion[0][1]:
                string += i + " "
            string += " } "
            string += "- { "
            for i in particion[1][0]:
                string += i + ", "
            string += " | "
            for i in particion[1][1]:
                string += i + " "
            string += "} "
            particionesEMDFormateadas.append((string, x[1]))
            
        particionMenorEMDFormateada = ""

        valorEMD = particionMenorEMD[1]
        print(particionMenorEMD[0][0])
        print(particionMenorEMD[0][1])

        stringResultado = "{ "
        for i in particionMenorEMD[0][0][0]:
            stringResultado += i + " "
        stringResultado += " | "
        for i in particionMenorEMD[0][0][1]:
            stringResultado += i + " "
        stringResultado += " } "
        stringResultado += "- { "
        for i in particionMenorEMD[0][1][0]:
            stringResultado += i + " "
        stringResultado += " | "
        for i in particionMenorEMD[0][1][1]:
            stringResultado += i + " "
        stringResultado += "} "
        
        stringResultado += " con Valor EMD: " + str(valorEMD)
        
        # Crear una nueva ventana Toplevel
        resultado_ventana = tk.Toplevel(self.root)
        resultado_ventana.title("Resultado del Cálculo")
        resultado_ventana.geometry("700x550")
         # Crear una tabla (Treeview) con dos columnas
        tabla = ttk.Treeview(resultado_ventana, columns=("col1", "col2"), show="headings", height=len(particionesEMDFormateadas))
        tabla.heading("col1", text="Partición")
        tabla.heading("col2", text="Valor EMD")

        #Ajustamos el ancho de la primera columna
        tabla.column("col1", width=350)

        # Insertar los datos en la tabla
        for elemento in particionesEMDFormateadas:
            tabla.insert("", "end", values=(elemento[0], elemento[1]))

        tabla.pack(pady=10)

        tk.Label(resultado_ventana, text=f"La partición elegida, con la menor diferencia es", font=("Arial", 12)).pack(pady=20)
        tk.Label(resultado_ventana, text=stringResultado, font=("Verdana", 12)).pack(pady=20)
        # Label para mostrar el resultado en la nueva ventana
        # tk.Label(resultado_ventana, text=self.result_label.cget("text"), font=("Arial", 12)).pack(pady=20)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta:
            try:
                # Cargar los datos y almacenarlos en los atributos
                self.subconjuntoSistemaCandidato, self.subconjuntoElementos, self.TPM = obtenerInformacionCSV(ruta)
                
                print(self.subconjuntoSistemaCandidato, self.subconjuntoElementos, self.TPM)

                # Guardar los nombres válidos desde subconjuntoElementos
                #TODO: NO SON LOS NOMBRES VALIDOS
                #* obtener numero de filas de la matriz TPM original
                numeroFilas = len(self.TPM)
                cantidadElementosIniciales = math.log2(numeroFilas)
                #*crear un arreglo de elementos validos
                elementosValidos = np.arange(1, cantidadElementosIniciales + 1)
                # print("elementosValidos", elementosValidos)
                
                abecedarioT = ['at', 'bt', 'ct', 'dt', 'et', 'ft', 'gt', 'ht', 'it', 'jt', 'kt', 'lt', 'mt', 'nt', 'ot', 'pt', 'qt', 'rt', 'st', 'tt', 'ut', 'vt', 'wt', 'xt', 'yt', 'zt']
                
                nombres_validos = []
                for i in range(len(elementosValidos)):
                    nombres_validos.append(abecedarioT[i])
                    
                # print("nombres_validos", nombres_validos)
                
                self.nombres_validos = nombres_validos

                # Mostrar resultados en cada cuadro de texto
                self.mostrar_resultado(self.text_subconjuntoSistemaCandidato, self.subconjuntoSistemaCandidato)
                self.mostrar_resultado(self.text_subconjuntoElementos, self.subconjuntoElementos)
                self.mostrar_resultado(self.text_TPM, self.TPM)

            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo: {str(e)}")

    def mostrar_resultado(self, text_widget, data):
        # Mostrar los resultados en el cuadro de texto
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, str(data))
        text_widget.config(state='disabled')

    def actualizar_resultado(self, valor):
        # Actualizar el Label con el valor calculado
        self.result_label.config(text=f"Resultado: {valor}")