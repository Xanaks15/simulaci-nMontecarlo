"""
Módulo ``MontecarloCliente``
---------------------------

Este módulo define la clase ``MontecarloCliente``, que actúa como
el **consumidor** en la arquitectura productor–consumidor. Su tarea
principal es recibir las muestras generadas por un ``MontecarloServidor``
e utilizar un ``CostFlyweight`` para calcular la utilidad de la
impresora portátil. Luego acumula las utilidades de múltiples
simulaciones y calcula estadísticas como la mínima, máxima y media.

Para su correcto funcionamiento, el cliente depende de dos objetos:

* ``servidor``: instancia de ``MontecarloServidor`` que produce los
  valores aleatorios de las variables.
* ``costos``: instancia de ``CostFlyweight`` que encapsula los
  costes fijos (precio de venta, costes administrativos y
  costes de publicidad).

Las funciones de este módulo están documentadas para describir
claramente los parámetros, procesos y valores de retorno involucrados.
"""

from __future__ import annotations

from typing import Tuple, List

from flyweight import CostFlyweight
from montecarloProductor import MontecarloServidor


class MontecarloCliente:
    """Clase que representa al consumidor en la simulación Montecarlo.

    Esta clase coordina las iteraciones de la simulación. Para cada
    iteración, solicita una muestra de entradas al ``servidor``,
    calcula la utilidad con ayuda de los costes fijos proporcionados
    por el flyweight ``costos`` y acumula los resultados para
    derivar estadísticas al final.
    """

    def __init__(self, servidor: MontecarloServidor, costos: CostFlyweight) -> None:
        """Inicializa el cliente con el productor y los costes fijos.

        Args:
            servidor (MontecarloServidor): Instancia que genera los valores
                aleatorios de las variables (C1, C2, X).
            costos (CostFlyweight): Flyweight con los valores fijos de
                precio de venta (PV), costes administrativos (CA) y
                costes de publicidad (CB).
        """
        self.servidor = servidor
        self.costos = costos

    def calcular_utilidad(self, c1: float, c2: float, x: float) -> float:
        """Calcula la utilidad para un conjunto dado de variables.

        La fórmula de la utilidad es:

        .. code-block:: text

            Utilidad = (PV - C1 - C2) * X - (CA + CB)

        donde los costes fijos (PV, CA, CB) provienen de ``self.costos``.

        Args:
            c1 (float): Coste de mano de obra por unidad.
            c2 (float): Coste de componentes por unidad.
            x (float): Demanda del primer año.

        Returns:
            float: Valor de la utilidad calculada.
        """
        margen_unitario = self.costos.precio_venta - c1 - c2
        utilidad = margen_unitario * x - (self.costos.costo_admin + self.costos.costo_publicidad)
        return float(utilidad)

    def ejecutar_simulacion(self, iteraciones: int = 10000) -> Tuple[float, float, float]:
        """Ejecuta la simulación Montecarlo y calcula estadísticas.

        Este método realiza las siguientes operaciones:

        1. Repite ``iteraciones`` veces:
            - Obtiene un conjunto (C1, C2, X) desde el ``servidor``.
            - Calcula la utilidad con ``calcular_utilidad``.
            - Almacena la utilidad en una lista interna.
        2. Determina la utilidad mínima, máxima y media a partir de
           la lista acumulada.

        Args:
            iteraciones (int, opcional): Número de simulaciones a realizar.
                Por defecto, 10 000.

        Returns:
            tuple[float, float, float]: Una tupla que contiene (mínimo,
                máximo, promedio) de las utilidades obtenidas.
        """
        utilidades: List[float] = []
        for _ in range(iteraciones):
            c1, c2, x = self.servidor.generar_muestra()
            utilidad = self.calcular_utilidad(c1, c2, x)
            utilidades.append(utilidad)
        # Calcular estadísticas
        utilidad_minima = float(min(utilidades)) if utilidades else 0.0
        utilidad_maxima = float(max(utilidades)) if utilidades else 0.0
        utilidad_media = float(sum(utilidades) / len(utilidades)) if utilidades else 0.0
        return (utilidad_minima, utilidad_maxima, utilidad_media)
        #dsdfdsf
