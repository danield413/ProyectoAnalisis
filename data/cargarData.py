#* metodo que me lee un archivo csv

import pandas as pd

def cargarData(ruta):
    data = pd.read_csv(ruta)
    return data