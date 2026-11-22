"""Gestor principal: administra listas internas y mantiene el sistema estable."""
from entidades import Cliente
from excepciones import ErrorSoftwareFJ, ReservaInvalidaError
from logger import obtener_logger
from reserva import Reserva

log = obtener_logger()


class SistemaFJ:
    """Controla clientes, servicios y reservas sin base de datos."""

    def __init__(self):
        self.clientes: list = []
        self.servicios: list = []
        self.reservas: list = []

    def _ejecutar(self, descripcion: str, funcion, *args, **kwargs):
        """Ejecuta una operación; si falla, registra el error y devuelve None.

        Así el programa NUNCA se detiene por un error controlado.
        """
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as error:
            causa = f" | causa: {error.__cause__!r}" if error.__cause__ else ""
            log.error("%s FALLÓ: %s (%s)%s", descripcion, error, type(error).__name__, causa)
            print(f"   [ERROR] {descripcion}: {error}")
            return None
        except Exception as error:  # error imprevisto: se registra y se continúa
            log.critical("%s ERROR INESPERADO: %r", descripcion, error)
            print(f"   [ERROR INESPERADO] {descripcion}: {error!r}")
            return None
        else:
            log.info("%s OK", descripcion)
            print(f"   [OK] {descripcion}")
            return resultado
        finally:
            log.info("Fin de operación: %s", descripcion)

    def registrar_cliente(self, **datos):
        cliente = self._ejecutar("Registrar cliente", Cliente, **datos)
        if cliente:
            self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase, **datos):
        servicio = self._ejecutar(f"Crear servicio {clase.__name__}", clase, **datos)
        if servicio:
            self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, horas, impuesto=0.19, descuento=0.0, procesar=True):
        """Crea y confirma una reserva; si procesar=True también la procesa."""
        def flujo():
            reserva = Reserva(cliente, servicio, horas)
            self.reservas.append(reserva)  # se guarda para dejar trazabilidad
            reserva.confirmar()
            if procesar:
                reserva.procesar(impuesto, descuento)
            return reserva
        return self._ejecutar("Crear y procesar reserva", flujo)

    def cancelar_reserva(self, reserva):
        if reserva is None:
            return self._ejecutar("Cancelar reserva",
                                  lambda: (_ for _ in ()).throw(
                                      ReservaInvalidaError("No existe la reserva a cancelar.")))
        return self._ejecutar(f"Cancelar reserva {reserva.id}", reserva.cancelar)

    def resumen(self):
        print("\n=== RESUMEN ===")
        print(f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | Reservas: {len(self.reservas)}")
        for r in self.reservas:
            print("  ", r.describir())
