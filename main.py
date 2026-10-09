
from api import api
from ui import ui


def main():
    ui.mostrar_titulo()
    datos = api.cargar_datos()

    seguir = True
    while seguir:
        # pido el departamento hasta que exista
        departamento = ui.pedir_departamento()
        municipios = api.lista_municipios(datos, departamento)
        while len(municipios) == 0:
            ui.mostrar_mensaje("No se encontro ese departamento, intente de nuevo.")
            departamento = ui.pedir_departamento()
            municipios = api.lista_municipios(datos, departamento)

        # pido el municipio hasta que exista
        municipio = ui.pedir_municipio(municipios)
        cultivos = api.lista_cultivos(datos, departamento, municipio)
        while len(cultivos) == 0:
            ui.mostrar_mensaje("No se encontro ese municipio, intente de nuevo.")
            municipio = ui.pedir_municipio(municipios)
            cultivos = api.lista_cultivos(datos, departamento, municipio)

        # pido el cultivo hasta que exista
        cultivo = ui.pedir_cultivo(cultivos)
        while not api.esta_en_lista(cultivo, cultivos):
            ui.mostrar_mensaje("No se encontro ese cultivo, intente de nuevo.")
            cultivo = ui.pedir_cultivo(cultivos)

        cantidad = ui.pedir_cantidad()

        registros = api.buscar_registros(datos, departamento, municipio, cultivo, cantidad)

        if len(registros) == 0:
            ui.mostrar_mensaje("No hay registros para ese cultivo.")
        else:
            tabla = api.calcular_medianas(registros)
            ui.mostrar_tabla(tabla)
            if len(registros) < cantidad:
                ui.mostrar_mensaje("Solo habia " + str(len(registros)) + " registros de los "
                                   + str(cantidad) + " que pidio.")
            else:
                ui.mostrar_mensaje("Se consultaron " + str(len(registros)) + " registros.")

        seguir = ui.preguntar_otra_consulta()

    print("Gracias por usar el programa!")


if __name__ == "__main__":
    main()
