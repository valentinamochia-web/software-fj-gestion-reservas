"""Clase abstracta Servicio y tres servicios especializados."""
from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase):
    """Clase abstracta: define el contrato común de todos los servicios."""

    IVA = 0.19  # impuesto por defecto
    MAX_HORAS = 24

    def __init__(self, nombre=None, tarifa_hora=None):
        super().__init__("SRV")
        if nombre is None or tarifa_hora is None:
            raise ParametroFaltanteError("Nombre y tarifa por hora son obligatorios.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    # ---------- propiedades (encapsulación) ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    # ---------- métodos abstractos (se sobrescriben) ----------
    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos, propio de cada servicio."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción propia de cada servicio."""

    def validar_parametros(self, horas=None) -> None:
        """Validación común; las subclases la extienden con super()."""
        if horas is None:
            raise ParametroFaltanteError("La duración (horas) es obligatoria.")
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise ServicioInvalidoError("La duración debe ser un número.")
        if horas <= 0 or horas > self.MAX_HORAS:
            raise ServicioInvalidoError(f"La duración debe estar entre 0 y {self.MAX_HORAS} horas.")
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    # ---------- "sobrecarga" de métodos ----------
    # Python no tiene sobrecarga nativa: se simula con parámetros opcionales,
    # de modo que el mismo método admite varias variantes de llamada:
    #   calcular_costo(3)                         -> costo base
    #   calcular_costo(3, impuesto=0.19)          -> con impuesto
    #   calcular_costo(3, descuento=0.10)         -> con descuento
    #   calcular_costo(3, 0.19, 0.10)             -> con ambos
    def calcular_costo(self, horas=None, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        self.validar_parametros(horas)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError("Impuesto y descuento deben estar entre 0 y 1.")
        base = self.calcular_costo_base(horas)
        if base <= 0:
            raise CalculoInconsistenteError("El costo base calculado no es válido.")
        return round(base * (1 - descuento) * (1 + impuesto), 2)

    def calcular_costo_con_iva(self, horas=None) -> float:
        """Variante: costo con el IVA por defecto."""
        return self.calcular_costo(horas, impuesto=self.IVA)


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas=None) -> None:
        super().validar_parametros(horas)
        if horas > 12:  # regla propia: una sala no se reserva más de 12 h
            raise ServicioInvalidoError("Una sala no puede reservarse por más de 12 horas.")

    def calcular_costo_base(self, horas: float) -> float:
        # Recargo del 10 % para salas de más de 20 personas
        recargo = 1.10 if self._capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return f"[{self.id}] Sala '{self.nombre}' | Capacidad: {self._capacidad} | ${self.tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(self, nombre=None, tarifa_hora=None, deposito=None):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError("El depósito debe ser un número mayor o igual a 0.")
        self._deposito = float(deposito)

    def calcular_costo_base(self, horas: float) -> float:
        # Se cobra un seguro fijo del 5 % sobre el depósito
        return self._tarifa_hora * horas + self._deposito * 0.05

    def describir(self) -> str:
        return f"[{self.id}] Equipo '{self.nombre}' | Depósito: ${self._deposito:,.0f} | ${self.tarifa_hora:,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con tarifa según el nivel del experto."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre=None, tarifa_hora=None, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}. Use {list(self.NIVELES)}.")
        self._nivel = nivel

    def validar_parametros(self, horas=None) -> None:
        super().validar_parametros(horas)
        if horas > 8:  # regla propia: máximo 8 h de asesoría
            raise ServicioInvalidoError("Una asesoría no puede durar más de 8 horas.")

    def calcular_costo_base(self, horas: float) -> float:
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return f"[{self.id}] Asesoría '{self.nombre}' | Nivel: {self._nivel} | ${self.tarifa_hora:,.0f}/h"
