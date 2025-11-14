"""
Módulo MontecarloCliente
------------------------
Define al cliente en la arquitectura productor–consumidor. El cliente es el
punto de entrada del programa: crea al servidor, coordina la simulación,
consume las muestras y calcula las métricas finales de utilidad.
"""

from __future__ import annotations

from typing import List, Dict, Tuple
from queue import Queue
import threading

from flyweight import FlyweightFactory, CostFlyweight
from montecarloServidor import MontecarloServidor


class MontecarloCliente:
    """
    Cliente/consumidor que calcula la utilidad a partir de las muestras
    generadas por el servidor.
    """

    def __init__(self, servidor: MontecarloServidor, costos: CostFlyweight) -> None:
        """
        Inicializa el cliente con una referencia al servidor y a los costos fijos.

        Args:
            servidor (MontecarloServidor): Instancia del servidor que genera
                las muestras (C1, C2, X).
            costos (CostFlyweight): Flyweight que contiene los costos fijos
                (precio de venta, costos administrativos y de publicidad).
        """
        self.servidor = servidor
        self.costos = costos
        self.utilidades: List[float] = []

    def calcular_utilidad(self, c1: float, c2: float, x: float) -> float:
        """
        Calcula la utilidad usando la fórmula del modelo:

            Utilidad = (PV - C1 - C2) * X - (CA + CB)

        Args:
            c1 (float): Costo de mano de obra por unidad.
            c2 (float): Costo de componentes por unidad.
            x  (float): Demanda del primer año.

        Returns:
            float: Utilidad económica generada para el conjunto (C1, C2, X).
        """
        margen = self.costos.precio_venta - c1 - c2
        utilidad = margen * x - (self.costos.costo_admin + self.costos.costo_publicidad)
        return float(utilidad)

    def consumir(self, cola: "Queue[tuple[float, float, float] | None]") -> None:
        """
        Consume muestras de la cola compartida y calcula la utilidad de cada una.

        Este método está pensado para ejecutarse en un hilo separado o en el
        hilo principal. Lee elementos de la cola hasta encontrar el valor
        centinela ``None``, que indica que el servidor ya no producirá más
        datos.

        Args:
            cola (Queue[tuple[float, float, float] | None]): Cola desde la cual
                se obtienen las tuplas (C1, C2, X). Cuando se recibe ``None``,
                el método deja de consumir.

        Returns:
            None: Las utilidades calculadas se almacenan en ``self.utilidades``.
        """
        while True:
            muestra = cola.get()
            if muestra is None:
                # Señal de fin de datos
                cola.task_done()
                break

            c1, c2, x = muestra
            utilidad = self.calcular_utilidad(c1, c2, x)
            self.utilidades.append(utilidad)
            cola.task_done()

    def ejecutar_simulacion_concurrente(self, iteraciones: int = 10000) -> Dict[str, float]:
        """
        Ejecuta la simulación Montecarlo completa desde el lado del cliente,
        usando un esquema concurrente productor–consumidor.

        El flujo es:
            1. Crear una cola compartida.
            2. Crear un hilo productor que llama al servidor para generar
               ``iteraciones`` muestras.
            3. Consumir la cola desde el cliente hasta recibir el centinela.
            4. Calcular métricas (mínima, máxima y promedio) a partir de las
               utilidades acumuladas.

        Args:
            iteraciones (int, opcional): Número total de simulaciones a ejecutar.
                Por defecto, 10000.

        Returns:
            dict: Diccionario con las métricas de utilidad:
                - "min": Utilidad mínima.
                - "max": Utilidad máxima.
                - "mean": Utilidad promedio.
        """
        cola: "Queue[tuple[float, float, float] | None]" = Queue()

        # Hilo productor ejecutando código del servidor
        hilo_prod = threading.Thread(
            target=self.servidor.hilo_productor,
            args=(cola, iteraciones),
            name="HiloProductor",
        )

        # Iniciar productor
        hilo_prod.start()

        # Consumir en el hilo actual (cliente)
        self.consumir(cola)

        # Esperar a que el productor termine
        hilo_prod.join()
        # Asegurarnos de que la cola esté vacía
        cola.join()

        if not self.utilidades:
            return {"min": 0.0, "max": 0.0, "mean": 0.0}

        return {
            "min": min(self.utilidades),
            "max": max(self.utilidades),
            "mean": sum(self.utilidades) / len(self.utilidades),
        }


def main() -> None:
    """
    Punto de entrada del programa.

    Crea el flyweight de costos fijos, instancia el servidor y el cliente,
    ejecuta la simulación concurrente y muestra las métricas finales.

    Returns:
        None. Los resultados se imprimen en pantalla.
    """
    factory = FlyweightFactory()
    costos = factory.get_flyweight(
        pv=70000.0,
        ca=160_000_000.0,
        cb=80_000_000.0,
    )

    servidor = MontecarloServidor()
    cliente = MontecarloCliente(servidor, costos)

    resultados = cliente.ejecutar_simulacion_concurrente(iteraciones=10000)

    print("\nResultados de la simulación Montecarlo (cliente → servidor):")
    print("------------------------------------------------------------")
    print(f"Utilidad mínima:   {resultados['min']:,.2f}")
    print(f"Utilidad máxima:   {resultados['max']:,.2f}")
    print(f"Utilidad promedio: {resultados['mean']:,.2f}")


if __name__ == "__main__":
    main()
