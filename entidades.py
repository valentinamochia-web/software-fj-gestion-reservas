"""Clase abstracta EntidadBase y clase Cliente."""
import re
from abc import ABC, abstractmethod
from itertools import count

from excepciones import ClienteInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    _contador = count(1)  # generador de identificadores consecutivos

    def __init__(self, prefijo: str):
        # Identificador único, por ejemplo CLI-001, SRV-002
        self._id = f"{prefijo}-{next(EntidadBase._contador):03d}"

    @property
    def id(self) -> str:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma (polimorfismo)."""

    def __str__(self) -> str:
        return self.describir()


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__("CLI")
        # Se asignan mediante las propiedades para que se ejecuten las validaciones
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self._nombre = valor.strip().title()

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos.")
        self._documento = valor

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo con formato inválido: {valor!r}.")
        self._correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos.")
        self._telefono = valor

    def describir(self) -> str:
        return f"[{self.id}] {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
