"""Configuración del archivo de logs (único uso de archivos del sistema)."""
import logging
import os

# Carpeta y archivo donde se guardan los eventos y errores
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger de la aplicación (se configura una sola vez)."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        os.makedirs(RUTA_LOGS, exist_ok=True)  # crea la carpeta si no existe
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger
