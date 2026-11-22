"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSoftwareFJ, de modo que el sistema puede capturar
cualquier error propio con un único ``except ErrorSoftwareFJ``.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la aplicación."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un servicio son incorrectos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio no disponible."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva se crea con datos incorrectos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se ejecuta una operación no válida para el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inconsistente."""
