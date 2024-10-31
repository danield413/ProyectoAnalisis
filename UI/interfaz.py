import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
from data.cargarData import obtenerInformacionCSV

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

        # Label para mostrar el valor calculado
        self.result_label = tk.Label(self.root, text="Resultado: ", font=("Arial", 12), bg="#f2f2f2")
        self.result_label.pack(pady=10)

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

        nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM = aplicarMarginalizacion(nuevaMatrizFuturo, nuevaTPM, elementosBackground, estadoActualElementos, nuevaMatrizPresente)


        #?  ------------------------ DIVIDIR EN LA REPRESENTACION -----------------------------------
        #? P(ABC t | ABC t+1) = P(ABC t | A t+1) X P(ABC t | B t+1) X P(ABC t | C t+1)

        #* tomar el subconjunto de elementos (los de t y t+1) con su indice
        elementosT = [elem for elem in subconjuntoSistemaCandidato if 't' in elem and 't+1' not in elem]
        elementosT1 = [elem for elem in subconjuntoSistemaCandidato if 't+1' in elem]

        indicesElementosT = {list(elem.keys())[0]: idx for idx, elem in enumerate(estadoActualElementos) if list(elem.keys())[0] in elementosT}

        #? Ejecución de la representación
        print("------ REPRESENTACIÓN -----------")
        partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM = partirRepresentacion(nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT, elementosT1, indicesElementosT)


        particionesCandidatas = []
        listaDeU = []

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
            for i in range(2, len(V)+1):
                # print()
                # print(">>>>>>>>>> LONGITUD V ACTUAL", (len(V)+1), "CONJUNTO: ", V)
                if (len(V)+1) == 2:
                    break

                #* ahora recorremos para cada elemento en V que no esté en W[i-1] (el anterior)
                for elem in V:
                    if  elem not in W[i-1]:
                        elementoActual = elem

                        #* aquí planteamos el conjunto que le vamos a pasar a la función de comparación
                        union = []
                        for elem in W[i-1]:
                            union.append(elem)
                        if 'u' not in elementoActual:
                            union.append(elementoActual)

                        #* si elemento es una u
                        if 'u' in elementoActual:
                            #* buscar los elementos que conforman la u
                            for u in listaDeU:
                                #* cojo el nombre de la llave
                                nombre = list(u.keys())[0]
                                if nombre == elementoActual:
                                    #* cojo el valor de la llave
                                    elementosU = u[nombre]
                                    #* recorro los elementos de la u
                                    for elem in elementosU:
                                        # print("ELEMENTO U", elem)
                                        union.append(elem)

                        # print("UNION", union)

                        #* separamos de la union los elementos que estan en t+1 y en t
                        particion = ( [ elem for elem in union if 't+1' in elem ], [ elem for elem in union if 't' in elem and 't+1' not in elem ] )
                        # print("PARTICION", particion)

                        #! ------------------ g(Wi-1 ∪ {vi}) ----------------------------

                        #? crear copias de las matrices para no modificar las originales
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                        #* obtenemos el vector de probabilidades de la partición

                        vectorProbabilidades = encontrarVectorProbabilidades(particion, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
                        # print("vectorProbabilidades", vectorProbabilidades)

                        #* Obtenemos el vector de probabilidades del conjunto que equilibra la particion
                        #* Obtener el equilibrio de la partición (lo que le falta a la partición para ser igual a la original)
                        particionEquilibrio = ([elem for elem in V if elem not in particion[0] and 't+1' in elem],[elem for elem in V if elem not in particion[1] and 't' in elem and 't+1' not in elem] )
                        # print("particionEquilibrio", particionEquilibrio)

                        #? crear copias de las matrices para no modificar las originales
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                        #*Obtenemos el vector de probabilidades de la partición de equilibrio
                        vectorProbabilidadesEquilibrio = encontrarVectorProbabilidades(particionEquilibrio, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
                        # print("vectorProbabilidadesEquilibrio", vectorProbabilidadesEquilibrio)

                        #* Calcular la diferencia entre los dos vectores de probabilidades
                        vectorResultado = producto_tensorial(vectorProbabilidades, vectorProbabilidadesEquilibrio)
                        valorwi_gu = compararParticion(vectorResultado, nuevaMatrizPresente, nuevaTPM, subconjuntoElementos, estadoActualElementos)
                        # print("VALOR EMD valorwi_gu", valorwi_gu)

                        #! ----------------------------- g({vi}) --------------------------------------

                        print("ELEMENTO ACTUAL", elementoActual)
                        #*Obtenemos la particion solamente del elemento actual sin nada mas
                        particionElementoActual2 = ([elem for elem in V if elem == elementoActual and 't+1' in elem],[elem for elem in V if elem == elementoActual and 't' in elem and 't+1' not in elem] )

                        #*Obtenemos la particion de equilibrio del elemento actual
                        particionEquilibrioElementoActual2 = ([elem for elem in V if elem != elementoActual and 't+1' in elem],[elem for elem in V if elem != elementoActual and 't' in elem and 't+1' not in elem] )


                        #? crear copias de las matrices para no modificar las originales
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                        vectorProbabilidades2 = encontrarVectorProbabilidades(particionElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
                        # print("vectorProbabilidades2", vectorProbabilidades2)

                        #? crear copias de las matrices para no modificar las originales
                        copiaMatricesPresentes = copy.deepcopy(partirMatricesPresentes)
                        copiaMatricesFuturas = copy.deepcopy(partirMatricesFuturas)
                        copiaMatricesTPM = copy.deepcopy(partirMatricesTPM)

                        vectorProbabilidadesEquilibrioElementoActual2 = encontrarVectorProbabilidades(particionEquilibrioElementoActual2, copiaMatricesPresentes, copiaMatricesFuturas, copiaMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
                        # print("vectorProbabilidadesEquilibrioElementoActual2", vectorProbabilidadesEquilibrioElementoActual2)

                        #* Calcular la diferencia entre los dos vectores de probabilidades
                        vectorResultadoElementoActual = producto_tensorial(vectorProbabilidades2, vectorProbabilidadesEquilibrioElementoActual2)

                        valorg_u = compararParticion(vectorResultadoElementoActual, nuevaMatrizPresente, nuevaTPM, subconjuntoElementos, estadoActualElementos)
                        valorRestaFinal = valorwi_gu - valorg_u

                        restas.append((elementoActual, valorRestaFinal))

                menorTupla = ()
                if len(restas) > 0:
                    menorTupla = min(restas, key=lambda x: x[1])
                    valoresI = copy.deepcopy(W[i-1])
                    valoresI.append(menorTupla[0])

                W[i] = valoresI
                restas = []

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

                #* se crea una nueva variable llamada u' que es la union de los dos elementos del par candidato
                nuevoV = np.array([ elem for elem in V if elem not in parCandidato ])

                uprima = [ parCandidato[0], parCandidato[1] ]

                #*verifico si en uprima hay una u embebida
                if 'u' in uprima[0]:
                    for u in listaDeU:
                        nombre = list(u.keys())[0]
                        if nombre == uprima[0]:
                            for x in u[nombre]:
                                uprima.append(x)
                if 'u' in uprima[1]:
                    #*voy a la lista de u a buscar el nombre de la u
                    for u in listaDeU:
                        nombre = list(u.keys())[0]
                        if nombre == uprima[1]:
                            for x in u[nombre]:
                                uprima.append(x)
                    #* elimino la u de la lista de u

                for elementoU in listaDeU:
                    valor = list(elementoU.values())[0]
                    for x in range(len(valor) - 1, -1, -1):  # Itera en orden inverso
                        if 'u' in valor[x]:
                            valor.pop(x)  # Elimina el elemento sin afectar los índices restantes

                total = 0
                for x in listaDeU:
                    nombre = list(x.keys())[0]
                    if 'u' in nombre:
                        total += 1

                nombreU = 'u_prima' + str(total+1)
                nuevoV = np.append(nuevoV, nombreU)
                listaDeU.append({nombreU: uprima})


                #* LA 1ERA VEZ QUE OBTIENE LA SECUENCIA RESULTANTE SE CIERRA EL CICLO Y SE LLAMA A LA RECURSIÓN
                if i == 2:
                    if((len(V)+1) > 2):
                        print("SE LLAMÓ LA RECURSIÓN")
                        algoritmo(nuevaTPM, subconjuntoElementos, nuevoV, estadoActualElementos)
                        break

            particionesFinales = organizarParticionesCandidatasFinales(copy.deepcopy(particionesCandidatas), listaDeU, subconjuntoElementos)
            particionElegida = evaluarParticionesFinales(particionesFinales, partirMatricesPresentes, partirMatricesFuturas, partirMatricesTPM, estadoActualElementos, subconjuntoElementos, indicesElementosT, nuevaMatrizPresente, nuevaMatrizFuturo, nuevaTPM, elementosT)
            return particionElegida, particionesFinales


        x, y = algoritmo(nuevaTPM, subconjuntoElementos, subconjuntoSistemaCandidato, estadoActualElementos)
        print("resultado algoritmo", x)
        print('------------------')
        for i in y :
            print (i)
        print('------------------')

        resultado_algoritmo = x  # Este sería el valor obtenido de un algoritmo
        self.actualizar_resultado(resultado_algoritmo)
        
        # Abrir una nueva ventana para mostrar el resultado
        self.mostrar_resultado_ventana(y)

    def mostrar_resultado_ventana(self, lista_datos):
        # Crear una nueva ventana Toplevel
        resultado_ventana = tk.Toplevel(self.root)
        resultado_ventana.title("Resultado del Cálculo")
        resultado_ventana.geometry("700x550")
         # Crear una tabla (Treeview) con dos columnas
        tabla = ttk.Treeview(resultado_ventana, columns=("col1", "col2"), show="headings", height=len(lista_datos))
        tabla.heading("col1", text="Partición")
        tabla.heading("col2", text="Valor EMD")

        #Ajustamos el ancho de la primera columna
        tabla.column("col1", width=350)

        # Insertar los datos en la tabla
        for elemento in lista_datos:
            tabla.insert("", "end", values=(elemento, ""))

        tabla.pack(pady=10)

        tk.Label(resultado_ventana, text="La partición elegida, con la menor diferencia es:", font=("Arial", 12)).pack(pady=20)
        # Label para mostrar el resultado en la nueva ventana
        tk.Label(resultado_ventana, text=self.result_label.cget("text"), font=("Arial", 12)).pack(pady=20)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta:
            try:
                # Cargar los datos y almacenarlos en los atributos
                self.subconjuntoSistemaCandidato, self.subconjuntoElementos, self.TPM = obtenerInformacionCSV(ruta)

                # Guardar los nombres válidos desde subconjuntoElementos
                self.nombres_validos = self.subconjuntoElementos.tolist()

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