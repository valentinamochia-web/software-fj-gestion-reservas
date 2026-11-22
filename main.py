"""Simulación de 14 operaciones de Software FJ (válidas e inválidas)."""
from gestor import SistemaFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main():
    fj = SistemaFJ()

    print("\n--- CLIENTES ---")
    print("1) Cliente válido")
    ana = fj.registrar_cliente(nombre="ana maría pérez", documento="1049123456",
                               correo="ana@correo.com", telefono="3101234567")
    print("2) Cliente con correo inválido")
    fj.registrar_cliente(nombre="Luis Gómez", documento="1049000111",
                         correo="luis-correo", telefono="3109876543")
    print("3) Cliente válido")
    carlos = fj.registrar_cliente(nombre="Carlos Ruiz", documento="79123456",
                                  correo="carlos@fj.co", telefono="3205551234")
    print("4) Cliente con parámetros faltantes")
    fj.registrar_cliente(nombre="Sin Datos")

    print("\n--- SERVICIOS ---")
    print("5) Sala válida")
    sala = fj.registrar_servicio(ReservaSala, nombre="Sala Boyacá", tarifa_hora=50000, capacidad=25)
    print("6) Equipo válido")
    equipo = fj.registrar_servicio(AlquilerEquipo, nombre="Videobeam", tarifa_hora=15000, deposito=400000)
    print("7) Asesoría válida")
    asesoria = fj.registrar_servicio(AsesoriaEspecializada, nombre="Arquitectura de software",
                                     tarifa_hora=80000, nivel="experto")
    print("8) Servicio con tarifa negativa")
    fj.registrar_servicio(AlquilerEquipo, nombre="Portátil", tarifa_hora=-5, deposito=100)

    print("\n--- RESERVAS ---")
    print("9) Reserva exitosa de sala con IVA")
    fj.crear_reserva(ana, sala, 3)
    print("10) Reserva exitosa de asesoría con IVA y 10 % de descuento")
    fj.crear_reserva(carlos, asesoria, 2, impuesto=0.19, descuento=0.10)
    print("11) Reserva fallida: duración excede el límite de la asesoría")
    fj.crear_reserva(carlos, asesoria, 10)
    print("12) Reserva fallida: servicio no disponible")
    equipo.cambiar_disponibilidad(False)
    fj.crear_reserva(ana, equipo, 4)
    print("13) Reserva fallida: cliente inexistente")
    fj.crear_reserva(None, sala, 2)
    print("14) Cancelar una reserva y luego intentar cancelarla otra vez")
    r = fj.crear_reserva(ana, sala, 1, procesar=False)
    fj.cancelar_reserva(r)
    fj.cancelar_reserva(r)
    print("15) Descuento inconsistente (150 %)")
    fj.crear_reserva(ana, sala, 2, descuento=1.5)

    fj.resumen()
    print("\nEl sistema terminó sin interrupciones. Revise logs/software_fj.log")


if __name__ == "__main__":
    main()
