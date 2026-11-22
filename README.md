# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso Programación 213023 – UNAD · Fase 4

Ejecución: `python main.py` (Python 3.8+, sin librerías externas).
Los errores y eventos quedan en `logs/software_fj.log`.

| Archivo | Contenido |
|---|---|
| excepciones.py | Excepciones personalizadas |
| logger.py | Configuración del log |
| entidades.py | `EntidadBase` (abstracta) y `Cliente` |
| servicios.py | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| reserva.py | `Reserva` (confirmar, cancelar, procesar) |
| gestor.py | `SistemaFJ` (listas internas y control de errores) |
| main.py | Simulación de 15 operaciones |
