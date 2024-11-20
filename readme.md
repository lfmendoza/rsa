# Sistema de Encriptación RSA en Python

## Descripción

Este proyecto implementa el sistema de encriptación RSA en Python, permitiendo la generación de llaves, encriptación y desencriptación de mensajes. Está diseñado para manejar mensajes grandes y complejos de manera eficiente y segura.

## Características

- **Generación de Llaves**: Genera pares de llaves pública y privada de tamaño configurable (por defecto, 2048 bits).
- **Encriptación y Desencriptación**: Soporta mensajes de texto completos, dividiéndolos en bloques adecuados para el proceso de encriptación.
- **Pruebas Unitarias y E2E**: Incluye pruebas que validan el correcto funcionamiento del sistema con mensajes largos y complejos.
- **Optimizaciones**: Utiliza algoritmos eficientes para operaciones matemáticas intensivas, como la generación de números primos y la exponenciación modular.

## Requisitos

- Python 3.6 o superior.

## Instalación

No se requieren dependencias adicionales. Puedes clonar este repositorio o descargar los archivos `rsa.py` y `test_rsa.py`.

## Uso

Ejecuta el script desde la línea de comandos:

```bash
python rsa.py
```
