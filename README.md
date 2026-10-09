# Proyecto 1 - Programación 4

Autor: Jose Alejandro Quiñones Garcia
Docente: Alejandro Rodas Vásquez
Universidad Tecnológica de Pereira

Programa de consola en Python que lee el Excel de análisis de suelos de Colombia
y muestra la mediana del pH, Fósforo y Potasio según el departamento, municipio
y cultivo que escoja el usuario.

## Archivos

- `main.py`: programa principal
- `api/api.py`: lee el Excel y calcula las medianas
- `ui/ui.py`: pide los datos y muestra la tabla
- `datos/`: archivo de Excel

## Cómo ejecutarlo

```
py -m pip install -r requirements.txt
py main.py
```