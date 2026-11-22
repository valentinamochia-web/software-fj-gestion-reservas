"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
)
from logger import obtener_logger
from servicios import Servicio

log = obtener_logger()


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA, FALLIDA = (
        "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA", "FALLIDA",
    )

    def __init__(self, cliente=None, servicio=None, horas=None):
        super().__init__("RES")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE
        self._costo_total = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self) -> None:
        """Pasa de PENDIENTE a CONFIRMADA validando el servicio."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        try:
            self._servicio.validar_parametros(self._horas)
        except ErrorSoftwareFJ as error:
            self._estado = self.FALLIDA
            # Encadenamiento de excepciones: se conserva la causa original
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva {self.id}.") from error
        else:  # solo si no hubo error
            self._estado = self.CONFIRMADA
            log.info("Reserva %s confirmada.", self.id)

    def cancelar(self) -> None:
        """Cancela una reserva que no esté procesada ni cancelada."""
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        self._estado = self.CANCELADA
        log.info("Reserva %s cancelada.", self.id)

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Calcula el costo final de una reserva confirmada."""
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas CONFIRMADAS (estado actual: {self._estado})."
            )
        try:
            total = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except (TypeError, ValueError, ArithmeticError) as error:
            # Errores de Python se convierten en errores propios (encadenamiento)
            raise CalculoInconsistenteError("Fallo inesperado en el cálculo.") from error
        except ErrorSoftwareFJ:
            self._estado = self.FALLIDA
            raise
        else:
            self._costo_total = total
            self._estado = self.PROCESADA
            return total
        finally:
            # Se ejecuta siempre: éxito o fallo
            log.info("Intento de procesamiento de %s -> estado %s", self.id, self._estado)

    def describir(self) -> str:
        costo = f"${self._costo_total:,.2f}" if self._costo_total is not None else "N/A"
        return (f"[{self.id}] {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | Total: {costo}")
