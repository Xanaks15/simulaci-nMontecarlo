"""
Módulo flyweight
----------------
Implementa el patrón Flyweight para almacenar valores fijos del modelo.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CostFlyweight:
    """
    Representa un conjunto inmutable de costos fijos usados en la simulación.

    Atributos:
        precio_venta (float): Precio de venta por unidad.
        costo_admin (float): Costo administrativo total anual.
        costo_publicidad (float): Costo total de publicidad anual.
    """
    precio_venta: float
    costo_admin: float
    costo_publicidad: float


class FlyweightFactory:
    """
    Crea y administra instancias únicas de CostFlyweight.
    """

    def __init__(self) -> None:
        """Inicializa la fábrica con un diccionario de flyweights."""
        self._flyweights: dict[tuple[float, float, float], CostFlyweight] = {}

    def get_flyweight(self, pv: float, ca: float, cb: float) -> CostFlyweight:
        """
        Obtiene un flyweight con los valores especificados.

        Si ya existe un flyweight con esos valores, lo reutiliza; de lo contrario,
        crea una nueva instancia y la almacena.

        Args:
            pv (float): Precio de venta por unidad.
            ca (float): Costo administrativo anual.
            cb (float): Costo de publicidad anual.

        Returns:
            CostFlyweight: Flyweight con los valores dados.
        """
        clave = (pv, ca, cb)

        if clave not in self._flyweights:
            self._flyweights[clave] = CostFlyweight(pv, ca, cb)

        return self._flyweights[clave]
