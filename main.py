from gastos import Agenda


if __name__ == "__main__":
    agenda = Agenda()
    print(
        """
Bienvenido a la agenda de gastos

1. Añadir gasto
2. Añadir gasto en cuotas
3. Añadir gasto mensual
4. Añadir ingreso
5. Añadir sueldo

6. Ver gastos
7. Ver ingresos
8. Ver sueldo
9. Ver gastos mensuales
10. Ver gastos en cuotas

11. Ver gastos en cuotas pendientes
12. Ver gastos en cuotas pagados

13. Cerrar mes (mes vencido)
14. Eliminar mes
15. Resetear agenda

0. Salir
"""
    )
    opcion = int(input("Ingrese una opcion: "))
    while opcion != 0 or opcion > 15:
        match opcion:
            case 1:
                agenda.añadir_gasto()
            case 2:
                agenda.añadir_gasto_cuotas()
            case 3:
                agenda.añadir_gasto_mensual()
            case 4:
                agenda.añadir_ingreso()
            case 5:
                agenda.update_sueldo()
            case 6:
                pass
            case 7:
                pass
            case 8:
                pass
            case 9:
                pass
            case 10:
                pass
            case 11:
                pass
            case 12:
                pass
            case 13:
                agenda.cerrar_mes()
            case 14:
                agenda.borrar_mes()
            case 15:
                agenda.resetear_agenda()
            case 0:
                agenda.cerrar_agenda()
            case _:
                print("Opcion invalida")
        opcion = int(input("Ingrese una opcion: "))
