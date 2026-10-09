# Modulo API
# Aqui va todo lo que tiene que ver con leer el excel y sacar los datos
# (la parte de la interfaz esta en la carpeta ui)

import datetime
import os
import unicodedata
import pandas as pd

# busco el excel a partir de la carpeta del proyecto, asi funciona
# aunque el programa se ejecute desde otra carpeta
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_EXCEL = os.path.join(CARPETA_PROYECTO, "datos", "resultado_laboratorio_suelo.xlsx")

# nombres de las columnas del excel que voy a usar
COL_PH = "pH agua:suelo 2,5:1,0"
COL_FOSFORO = "Fósforo (P) Bray II mg/kg"
COL_POTASIO = "Potasio (K) intercambiable cmol(+)/kg"

# El excel tiene un problema: a muchos numeros se les perdio la coma decimal
# (por ejemplo 0,2227 quedo como 222708744) y algunos se volvieron fechas.
# Para arreglarlo divido entre 10 hasta que el numero quede por debajo
# de un maximo razonable para cada variable.
MAXIMOS = {
    COL_PH: 14,        # el pH va de 0 a 14
    COL_FOSFORO: 40,   # mg/kg
    COL_POTASIO: 1,    # cmol(+)/kg
}


def cargar_datos():
    """Lee el excel y devuelve un DataFrame"""
    print("Cargando el archivo de excel, espere un momento...")
    datos = pd.read_excel(RUTA_EXCEL)
    datos = preparar_datos(datos)
    return datos


def limpiar_valor(valor, maximo):
    """Convierte un valor del excel en un numero decimal (float).
    Si no se puede convertir devuelve None"""

    # si esta vacio no hay nada que hacer
    if pd.isna(valor):
        return None

    # algunos valores se volvieron fechas, ej: 6,5 -> 6 de mayo
    # entonces el dia es la parte entera y el mes la parte decimal
    if isinstance(valor, datetime.datetime):
        texto = str(valor.day) + "." + str(valor.month)
        numero = float(texto)

    # si es texto le quito el signo < y cambio la coma por punto
    # ej: "<3,87" -> 3.87 (se toma el limite de deteccion)
    elif isinstance(valor, str):
        texto = valor.replace("<", "").replace(",,", ",").replace(",", ".").strip()
        try:
            numero = float(texto)
        except ValueError:
            return None  # cosas como "ND" (no determinado)
    else:
        numero = float(valor)

    # arreglo los numeros que perdieron la coma
    while numero >= maximo:
        numero = numero / 10

    return numero


def normalizar(texto):
    """Pasa el texto a mayusculas, le quita las tildes y los espacios
    de sobra, para que 'platano' y 'Plátano' se consideren iguales"""
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize("NFD", texto)
    sin_tildes = ""
    for letra in texto:
        if unicodedata.category(letra) != "Mn":  # Mn = tildes sueltas
            sin_tildes = sin_tildes + letra
    sin_tildes = " ".join(sin_tildes.split())  # quita espacios dobles
    return sin_tildes


def esta_en_lista(texto, lista):
    """Revisa si el texto esta en la lista (sin importar tildes ni mayusculas)"""
    for elemento in lista:
        if normalizar(elemento) == normalizar(texto):
            return True
    return False


def preparar_datos(datos):
    """Agrega columnas auxiliares con los nombres normalizados
    para que las busquedas sean mas faciles"""
    datos["dep_aux"] = datos["Departamento"].apply(normalizar)
    datos["mun_aux"] = datos["Municipio"].apply(normalizar)
    datos["cul_aux"] = datos["Cultivo"].apply(normalizar)
    return datos


def buscar_registros(datos, departamento, municipio, cultivo, cantidad):
    """Filtra los datos por departamento, municipio y cultivo
    y devuelve los primeros 'cantidad' registros"""

    filtro = (
        (datos["dep_aux"] == normalizar(departamento))
        & (datos["mun_aux"] == normalizar(municipio))
        & (datos["cul_aux"] == normalizar(cultivo))
    )
    resultado = datos[filtro].head(cantidad)
    return resultado


def calcular_medianas(registros):
    """Arma la tabla con la mediana de pH, fosforo y potasio
    agrupando por departamento, municipio, cultivo y topografia"""

    tabla = registros[["Departamento", "Municipio", "Cultivo", "Topografia"]].copy()

    # limpio cada columna con la funcion de arriba
    tabla["pH"] = registros[COL_PH].apply(lambda v: limpiar_valor(v, MAXIMOS[COL_PH]))
    tabla["Fosforo (P)"] = registros[COL_FOSFORO].apply(lambda v: limpiar_valor(v, MAXIMOS[COL_FOSFORO]))
    tabla["Potasio (K)"] = registros[COL_POTASIO].apply(lambda v: limpiar_valor(v, MAXIMOS[COL_POTASIO]))

    # agrupo y saco la mediana
    medianas = tabla.groupby(["Departamento", "Municipio", "Cultivo", "Topografia"]).median()
    medianas = medianas.round(2).reset_index()

    # tambien cuento cuantos registros hay en cada grupo
    conteo = tabla.groupby(["Departamento", "Municipio", "Cultivo", "Topografia"]).size()
    medianas["Registros"] = conteo.values

    return medianas


def lista_municipios(datos, departamento):
    """Devuelve los municipios que hay en un departamento"""
    filtro = datos["dep_aux"] == normalizar(departamento)
    return sorted(datos[filtro]["Municipio"].dropna().unique())


def lista_cultivos(datos, departamento, municipio):
    """Devuelve los cultivos que hay en un municipio"""
    filtro = (datos["dep_aux"] == normalizar(departamento)) & (
        datos["mun_aux"] == normalizar(municipio)
    )
    return sorted(datos[filtro]["Cultivo"].dropna().unique())
