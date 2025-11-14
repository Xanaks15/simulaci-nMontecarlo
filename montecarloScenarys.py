"""
Módulo ``Scenery``
------------------

Este módulo actúa como punto de entrada de la aplicación para la
simulación Montecarlo de la impresora portátil. Su función es
coordinar la creación de las instancias necesarias (factory, productor
y consumidor), ejecutar la simulación y mostrar los resultados
finales al usuario.

La función ``main`` se invoca cuando se ejecuta el módulo desde la
línea de comandos. Dentro de ``main``, se realiza lo siguiente:

1. Crear una factoría ``FlyweightFactory`` para obtener los costes
   fijos como flyweight.
2. Instanciar ``MontecarloServidor`` que actuará como productor.
3. Solicitar un ``CostFlyweight`` con los valores de coste fijos
   (PV, CA, CB).
4. Instanciar ``MontecarloCliente`` con el servidor y los costes
   obtenidos.
5. Ejecutar la simulación con el número de iteraciones deseado.
6. Imprimir por pantalla la utilidad mínima, máxima y media.

Las funciones están documentadas para facilitar su comprensión y
reutilización.
"""

from __future__ import annotations

from flyweight import FlyweightFactory
from montecarloProductor import MontecarloServidor
from montecarloCliente import MontecarloCliente


def ejecutar_simulacion(iteraciones: int = 10000) -> None:
    """Configura y ejecuta la simulación Montecarlo.

    Este procedimiento se encarga de crear los objetos necesarios
    utilizando la arquitectura productor–consumidor y el patrón
    Flyweight. A continuación, ejecuta la simulación un número
    configurable de iteraciones y muestra los resultados obtenidos.

    Args:
        iteraciones (int, opcional): Número de simulaciones a ejecutar.
            Si no se especifica, se utilizan 10 000 iteraciones.

    Returns:
        None. Los resultados se imprimen en la salida estándar.
    """
    # Crear factoría para obtener los costes fijos compartidos
    factory = FlyweightFactory()
    # Definir los valores fijos: precio de venta, costes administrativos y de publicidad
    PRECIO_VENTA = 70000.0
    COSTO_ADMIN = 160000000.0
    COSTO_PUBLICIDAD = 80000000.0
    costos = factory.get_flyweight(PRECIO_VENTA, COSTO_ADMIN, COSTO_PUBLICIDAD)
    # Crear productor (servidor) y consumidor (cliente)
    servidor = MontecarloServidor()
    cliente = MontecarloCliente(servidor, costos)
    # Ejecutar simulación y obtener estadísticas
    util_min, util_max, util_media = cliente.ejecutar_simulacion(iteraciones)
    # Mostrar resultados
    print("Resultados de la simulación Montecarlo:")
    print(f"Iteraciones: {iteraciones}")
    print(f"Utilidad mínima: {util_min:,.2f}")
    print(f"Utilidad máxima: {util_max:,.2f}")
    print(f"Utilidad promedio: {util_media:,.2f}")


def main() -> None:
    """Función principal para ejecutar la simulación al llamar el script.

    Esta función sirve como punto de inicio cuando se ejecuta
    ``python Scenery.py``. Delega la responsabilidad a
    ``ejecutar_simulacion`` con un número predeterminado de
    iteraciones.

    Returns:
        None.
    """
    # Por defecto se ejecutan 10 000 simulaciones
    ejecutar_simulacion(10000)


if __name__ == "__main__":
    main()
