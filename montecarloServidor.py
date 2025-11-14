"""
Módulo MontecarloServidor
-------------------------
Define al servidor como productor en la arquitectura productor–consumidor.
Su responsabilidad es generar valores aleatorios para C1, C2 y X y, cuando
el cliente lo solicite, producir muestras en una cola compartida.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple
from queue import Queue


class MontecarloServidor:
    """
    Productor de valores aleatorios usados en la simulación Montecarlo.

    Esta clase conoce las distribuciones de probabilidad de las variables
    C1, C2 y X, y puede generar muestras individuales o producir múltiples
    muestras en una cola compartida para que un consumidor las procese.
    """

    def __init__(self) -> None:
        """
        Inicializa las distribuciones de probabilidad necesarias para
        generar los valores C1, C2 y X.
        """
        # Distribución discreta para C1
        self.c1_valores = np.array([10000, 13000, 16000, 19000, 22000])
        self.c1_prob = np.array([0.10, 0.30, 0.30, 0.20, 0.10])

        # Distribución uniforme para C2
        self.c2_min = 25000.0
        self.c2_max = 35000.0

        # Distribución normal truncada para X
        self.x_media = 14500.0
        self.x_desv = 4000.0
        self.x_min = 9000.0
        self.x_max = 28500.0

    def generar_c1(self) -> float:
        """
        Genera el costo de mano de obra C1 usando una distribución discreta.

        Returns:
            float: Valor generado para C1.
        """
        return float(np.random.choice(self.c1_valores, p=self.c1_prob))

    def generar_c2(self) -> float:
        """
        Genera el costo de componentes C2 usando una distribución uniforme.

        Returns:
            float: Valor generado para C2.
        """
        return float(np.random.uniform(self.c2_min, self.c2_max))

    def generar_x(self) -> float:
        """
        Genera la demanda del primer año X usando una distribución normal
        truncada dentro del rango definido.

        Returns:
            float: Valor generado para X.
        """
        x = np.random.normal(self.x_media, self.x_desv)
        return float(np.clip(x, self.x_min, self.x_max))

    def generar_muestra(self) -> Tuple[float, float, float]:
        """
        Genera una tupla de valores (C1, C2, X) para una iteración de simulación.

        Returns:
            tuple[float, float, float]: Valores aleatorios generados para
                (C1, C2, X).
        """
        return (
            self.generar_c1(),
            self.generar_c2(),
            self.generar_x(),
        )

    def hilo_productor(self, cola: "Queue[tuple[float, float, float] | None]", iteraciones: int) -> None:
        """
        Función de hilo productor: genera muestras y las coloca en la cola.

        Esta función está pensada para ejecutarse en un hilo separado.
        Produce exactamente ``iteraciones`` muestras y, al terminar, coloca
        un valor centinela ``None`` para indicar al consumidor que no habrá
        más datos.

        Args:
            cola (Queue[tuple[float, float, float] | None]): Cola compartida
                utilizada para enviar muestras al consumidor.
            iteraciones (int): Número de muestras a producir.

        Returns:
            None: No retorna valores, solo coloca elementos en la cola.
        """
        for _ in range(iteraciones):
            muestra = self.generar_muestra()
            cola.put(muestra)

        # Centinela que indica fin de producción
        cola.put(None)
