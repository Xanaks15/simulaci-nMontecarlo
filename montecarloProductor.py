"""
Módulo ``MontecarloServidor``
----------------------------

Este módulo define la clase ``MontecarloServidor``, que actúa como
el **productor** en una arquitectura productor–consumidor. Su
responsabilidad es generar valores aleatorios para las variables
aleatorias involucradas en el cálculo de la utilidad de la impresora.

Variables generadas:

- ``C1`` – Coste de mano de obra por unidad, con una distribución
  discreta definida por probabilidades específicas.
- ``C2`` – Coste de componentes por unidad, con una distribución
  uniforme en un rango determinado.
- ``X`` – Demanda del primer año, con una distribución normal
  acotada (truncada) dentro de un rango especificado.

Las funciones de este módulo están documentadas con docstrings
detallados para explicar sus parámetros, su funcionamiento y el
valor de retorno.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple


class MontecarloServidor:
    """Clase que representa al productor de la simulación Montecarlo.

    Esta clase genera combinaciones aleatorias de variables de entrada
    necesarias para calcular la utilidad de la impresora portátil.

    Distribuciones usadas:

    - ``C1`` (coste de mano de obra): Distribución discreta con valores
      de {10 000, 13 000, 16 000, 19 000, 22 000} y probabilidades
      {0.1, 0.3, 0.3, 0.2, 0.1}.
    - ``C2`` (coste de componentes): Distribución uniforme continua
      entre 25 000 y 35 000 unidades monetarias.
    - ``X`` (demanda del primer año): Distribución normal con media
      14 500 y desviación estándar 4 000, truncada en el rango
      [9 000, 28 500].
    """

    def __init__(self) -> None:
        """Inicializa el productor con las distribuciones predefinidas."""
        # Valores y probabilidades para la distribución discreta de C1
        self._c1_valores: np.ndarray = np.array([10000, 13000, 16000, 19000, 22000], dtype=float)
        self._c1_probabilidades: np.ndarray = np.array([0.10, 0.30, 0.30, 0.20, 0.10], dtype=float)
        # Parámetros de C2 (uniforme) y X (normal truncada)
        self._c2_min: float = 25000.0
        self._c2_max: float = 35000.0
        self._x_media: float = 14500.0
        self._x_desv: float = 4000.0
        self._x_min: float = 9000.0
        self._x_max: float = 28500.0

    def generar_c1(self) -> float:
        """Genera un valor aleatorio para ``C1`` según la distribución discreta.

        Returns:
            float: Un valor de coste de mano de obra por unidad.
        """
        c1 = float(np.random.choice(self._c1_valores, p=self._c1_probabilidades))
        return c1

    def generar_c2(self) -> float:
        """Genera un valor aleatorio para ``C2`` (coste de componentes).

        ``C2`` sigue una distribución uniforme continua entre ``_c2_min``
        y ``_c2_max``. Se utiliza ``numpy.random.uniform`` para generar
        el valor.

        Returns:
            float: Un valor de coste de componentes por unidad.
        """
        c2 = float(np.random.uniform(self._c2_min, self._c2_max))
        return c2

    def generar_x(self) -> float:
        """Genera un valor aleatorio para ``X`` (demanda del primer año).

        ``X`` sigue una distribución normal con media ``_x_media`` y
        desviación estándar ``_x_desv``, pero los valores se limitan
        mediante truncado al intervalo [``_x_min``, ``_x_max``]. Si el
        muestreo inicial cae fuera del intervalo, se ajusta mediante
        ``numpy.clip`` para forzarlo a permanecer dentro del rango.

        Returns:
            float: Un valor de demanda para el primer año.
        """
        # Generar valor normal y truncarlo al rango válido
        x = np.random.normal(self._x_media, self._x_desv)
        x_trunc = float(np.clip(x, self._x_min, self._x_max))
        return x_trunc

    def generar_muestra(self) -> Tuple[float, float, float]:
        """Genera una tupla de valores (C1, C2, X) para una simulación.

        Esta función llama internamente a ``generar_c1()``,
        ``generar_c2()`` y ``generar_x()`` para producir una combinación
        de las variables aleatorias necesarias para el cálculo de la
        utilidad. No requiere parámetros de entrada y produce una
        salida completa en una única tupla.

        Returns:
            tuple[float, float, float]: Una tupla con los valores
                (C1, C2, X) generados.
        """
        c1 = self.generar_c1()
        c2 = self.generar_c2()
        x = self.generar_x()
        return (c1, c2, x)
