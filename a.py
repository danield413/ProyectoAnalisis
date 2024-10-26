import copy

def mi_funcion(lista):
    lista_copia = lista.copy()  # Copia superficial
    # Modifica lista_copia sin afectar la lista original
    lista_copia.append(100)
    print("Dentro de la función:", lista_copia)

lista_original = [1, 2, 3]
mi_funcion(lista_original)
print("Fuera de la función:", lista_original)
