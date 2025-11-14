"""
Módulo ``flyweight``
--------------------

Este módulo implementa el patrón de diseño **Flyweight** para
manejar valores constantes en la simulación Montecarlo. El objetivo
del patrón Flyweight es compartir objetos inmutables de forma que
no se generen múltiples instancias idénticas de datos que nunca
cambian, reduciendo así la sobrecarga de memoria.

En este contexto, los costes fijos de la impresora (precio de venta,
costes administrativos y costes de publicidad) son valores que no
varían durante la simulación. Por lo tanto, se encapsulan dentro de
un ``CostFlyweight`` que será gestionado por ``FlyweightFactory``.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CostFlyweight:
    """Estructura inmutable que almacena los costes fijos de la impresora.

    Atributos:
        precio_venta (float): Precio de venta por unidad de impresora.
        costo_admin (float): Costes administrativos totales.
        costo_publicidad (float): Costes de publicidad totales.

    Esta clase es simple y se declara como dataclass con ``frozen=True``
    para que sus atributos sean inmutables. Esto permite que el mismo
    objeto se reutilice sin riesgo de modificar su estado.
    """

    precio_venta: float
    costo_admin: float
    costo_publicidad: float


class FlyweightFactory:
    """Factoría para crear y gestionar instancias ``CostFlyweight``.

    La factoría almacena internamente un diccionario de flyweights
    previamente creados. Cuando se solicita un conjunto de costes
    (precio de venta, administrativos y publicidad), se verifica si ya
    existe un ``CostFlyweight`` con esos valores. En caso afirmativo,
    se devuelve la instancia existente. De lo contrario, se crea una
    nueva, se guarda en la factoría y se devuelve.
    """

    def __init__(self) -> None:
        """Inicializa la factoría con un almacenamiento vacío."""
        self._flyweights: dict[tuple[float, float, float], CostFlyweight] = {}

    def get_flyweight(self, precio_venta: float, costo_admin: float, costo_publicidad: float) -> CostFlyweight:
        """Obtiene un ``CostFlyweight`` con los valores proporcionados.

        Si ya existe un flyweight con estos valores, lo reutiliza;
        de lo contrario, crea uno nuevo y lo almacena internamente.

        Args:
            precio_venta (float): Precio de venta por unidad de impresora.
            costo_admin (float): Costes administrativos totales del año.
            costo_publicidad (float): Costes de publicidad totales del año.

        Returns:
            CostFlyweight: Una instancia que encapsula los costes fijos.
        """
        clave = (precio_venta, costo_admin, costo_publicidad)
        if clave not in self._flyweights:
            self._flyweights[clave] = CostFlyweight(
                precio_venta=precio_venta,
                costo_admin=costo_admin,
                costo_publicidad=costo_publicidad,
            )
        return self._flyweights[clave]
