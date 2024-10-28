
def buscarValorUPrima(listaDeU, uprima):
    for u in listaDeU:
        nombre = list(u.keys())[0]
        if nombre == uprima:
            return u[nombre]

def organizarParticionesCandidatasFinales(particionesCandidatasFinales, listaDeU, subconjuntoElementos):

    nuevas = []

    #* remocion de las u
    for i in particionesCandidatasFinales:
        # print("Particion candidata", i)
        p1 = i['p1']
        p2 = i['p2']

        #* valores a reemplazar
        for x in p1[0]:
            if 'u' in x:
                valor = buscarValorUPrima(listaDeU, x)
                # print(x, valor)
                p1[0].extend(valor)
                p1[0].remove(x)

        for x in p1[1]:
            if 'u' in x:
                valor = buscarValorUPrima(listaDeU, x)
                # print(x, valor)
                p1[1].extend(valor)
                p1[1].remove(x)

        for x in p2[0]:
            if 'u' in x:
                valor = buscarValorUPrima(listaDeU, x)
                # print(x, valor)
                p2[0].extend(valor)
                p2[0].remove(x)

        for x in p2[1]:
            if 'u' in x:
                valor = buscarValorUPrima(listaDeU, x)
                # print(x, valor)
                p2[1].extend(valor)
                p2[1].remove(x)

        nuevas.append({
            'p1': p1,
            'p2': p2
        })

    #* ahora, poner los elementos de t+1 en la primera posición de la partición y los de t en la segunda
    for i in nuevas:
        p1 = i['p1']
        p2 = i['p2']

        p1[0].sort()
        p1[1].sort()
        p2[0].sort()
        p2[1].sort()


    # for i in nuevas:
    #     print(i)

    # print("-------------------------------")

    #* organizar t+1 en izquierda y t en derecha
    for i in nuevas:
        particion1 = i['p1']
        particion2 = i['p2']

        # Para particion1
        elementos_a_mover = []

        # Identificar elementos que contienen 't' en particion1[0]
        for elem in particion1[0]:
            if 't' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion1[1] y eliminarlos de particion1[0]
        for elem in elementos_a_mover:
            particion1[0].remove(elem)
            particion1[1].append(elem)

        # Resetear elementos_a_mover
        elementos_a_mover = []

        # Identificar elementos que contienen 't+1' en particion1[1]
        for elem in particion1[1]:
            if 't+1' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion1[0] y eliminarlos de particion1[1]
        for elem in elementos_a_mover:
            particion1[1].remove(elem)
            particion1[0].append(elem)

        # Repetir el mismo proceso para particion2

        elementos_a_mover = []

        # Identificar elementos que contienen 't' en particion2[0]
        for elem in particion2[0]:
            if 't' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion2[1] y eliminarlos de particion2[0]
        for elem in elementos_a_mover:
            particion2[0].remove(elem)
            particion2[1].append(elem)

        # Resetear elementos_a_mover
        elementos_a_mover = []

        # Identificar elementos que contienen 't+1' en particion2[1]
        for elem in particion2[1]:
            if 't+1' in elem:
                elementos_a_mover.append(elem)

        # Mover los elementos de 'elementos_a_mover' a particion2[0] y eliminarlos de particion2[1]
        for elem in elementos_a_mover:
            particion2[1].remove(elem)
            particion2[0].append(elem)

    # for i in nuevas:
    #     print(i)

    # print("-------------------------------")

    #* Ahora, equilibrar correctamente la partición 2

    tuplasFinales = []

    for i in nuevas:
        particion1 = i['p1']
        particion2 = i['p2']

        #* Obtener el equilibrio de la partición 2

        elementosT1 = [elem for elem in subconjuntoElementos if 't+1' in elem]
        #* ver que elemenos de t+1 están en la particion 1 izquierda
        elementosT1_particion1 = [elem for elem in particion1[0] if 't+1' in elem and 't' not in elem]
        #* Calculo la diferencia entre los elementos de t+1 y los elementos de t+1 en la particion 1
        diferenciaT1 = [elem for elem in elementosT1 if elem not in elementosT1_particion1]
        # print("Diferencia t+1", diferenciaT1)

        if diferenciaT1 != []:
            # print("es diferente de vacio")
            # print("Particion 2[1]", particion2[1])
            # Convertir la tupla en lista para hacer modificaciones
            particion2 = list(particion2)
            particion2[0] = diferenciaT1  # Realizar el cambio
            particion2 = tuple(particion2)  # Convertir de nuevo en tupla si es necesario

        elementosT = [elem for elem in subconjuntoElementos if 't' in elem]

        #* ver que elemenos de t están en la particion 1 derecha
        elementosT_particion1 = [elem for elem in particion1[1] if 't' in elem]
        #* Calculo la diferencia entre los elementos de t y los elementos de t en la particion 1
        diferenciaT = [elem for elem in elementosT if elem not in elementosT_particion1]
        # print("Diferencia t", diferenciaT)

        if diferenciaT != []:
            # Convertir la tupla en lista para hacer modificaciones
            particion2 = list(particion2)
            particion2[1] = diferenciaT  # Realizar el cambio
            particion2 = tuple(particion2)  # Convertir de nuevo en tupla si es necesario

        # print("particion", (particion1, particion2))

        tuplasFinales.append([particion1, particion2])

    # for i in tuplasFinales:
    #     p1 = i[0]
    #     p2 = i[1]
    #     print("Particion 1", p1, "Particion 2", p2)

    return tuplasFinales