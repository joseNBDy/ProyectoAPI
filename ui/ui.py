# Modulo UI
# Aqui van las funciones para pedir datos al usuario y mostrar resultados


def mostrar_titulo():
    print("=" * 60)
    print("   CONSULTA DE PROPIEDADES EDAFICAS - SUELOS DE COLOMBIA")
    print("=" * 60)


def pedir_departamento():
    departamento = input("Ingrese el departamento: ")
    return departamento.strip()


def pedir_municipio(municipios):
    print("\nMunicipios disponibles:")
    for m in municipios:
        print("  -", m)
    municipio = input("Ingrese el municipio: ")
    return municipio.strip()


def pedir_cultivo(cultivos):
    print("\nCultivos disponibles:")
    for c in cultivos:
        print("  -", c)
    cultivo = input("Ingrese el cultivo: ")
    return cultivo.strip()


def pedir_cantidad():
    # repito hasta que el usuario escriba un numero valido
    while True:
        texto = input("Ingrese el numero de registros a consultar: ")
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Error: debe ingresar un numero entero mayor que 0")


def mostrar_tabla(tabla):
    print("\nRESULTADOS (mediana de las variables edaficas)")
    print("-" * 100)
    print(tabla.to_string(index=False))
    print("-" * 100)


def mostrar_mensaje(mensaje):
    print("\n" + mensaje)


def preguntar_otra_consulta():
    respuesta = input("\n¿Desea hacer otra consulta? (s/n): ")
    return respuesta.strip().lower() == "s"
