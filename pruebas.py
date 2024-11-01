from tkinter import messagebox, ttk
import tkinter as tk

def generarCombinacionesEstadosIniciales(n):
    #* generar un arreglo con todas las combinaciones para n elementos en binario
    combinaciones = []
    for i in range(2**n):
        combinaciones.append(bin(i)[2:].zfill(n))
    return combinaciones

print(generarCombinacionesEstadosIniciales(5))

combinaciones = generarCombinacionesEstadosIniciales(5)

def show_selection():
    # Obtener la opción seleccionada.
    selection = combo.get()
    messagebox.showinfo(
        message=f"La opción seleccionada es: {selection}",
        title="Selección"
    )
main_window = tk.Tk()
main_window.config(width=300, height=200)
main_window.title("Combobox")
combo = ttk.Combobox(
    state="readonly",
    values=combinaciones
)
combo.place(x=50, y=50)
button = ttk.Button(text="Mostrar selección", command=show_selection)
button.place(x=50, y=100)
main_window.mainloop()