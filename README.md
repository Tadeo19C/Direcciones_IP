# Red y Subredes en Python
Este proyecto proporciona una herramienta para gestionar redes IPv4, permitiendo la obtención de información detallada sobre una red, como la dirección de red, la dirección de broadcast, el número de direcciones IP disponibles, y la posibilidad de dividir la red en subredes.

## Características
Clases Principales:

Red: Permite calcular información básica sobre una red IPv4, incluyendo la dirección de red, dirección de broadcast, número de IPs disponibles, y más.
RedSubred: Extiende la funcionalidad de la clase Red para soportar la creación y gestión de subredes.
ArchivoRed: Proporciona métodos para crear y leer archivos de texto con la información de la red.

## Funciones Clave:

Obtención de la dirección de red y de broadcast.
Cálculo del número de IPs disponibles y la creación de subredes.
Generación automática de archivos que contienen toda la información sobre la red y sus subredes.
Requisitos
Python 3.x
Módulos estándar: ipaddress, os

## Uso
Ejecución del Programa
El programa se ejecuta en la terminal e incluye un menú interactivo que permite al usuario:

## Crear información sobre una red, especificando la dirección IP base y la máscara de subred.
Mostrar la información de la red previamente creada.
Salir del programa.

## Ejemplo de Ejecución
bash
Copiar código
$ python nombre_del_script.py


## Opciones del menú:

Crear Información de Red
Mostrar Información de Red
Salir

## Estructura del Proyecto
Red: Clase que permite calcular información básica sobre una red IPv4.
RedSubred: Subclase de Red, utilizada para crear subredes y obtener información detallada sobre ellas.
ArchivoRed: Clase con métodos estáticos para crear y leer archivos con la información de la red.
Archivos Generados
Al crear información de la red, se generará un archivo de texto (informacion_red.txt) en la carpeta archivos_red/ con detalles sobre la red y sus subredes.

## Contribuciones
Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.
