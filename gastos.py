import sqlite3
import datetime


class Agenda:
    def __init__(self):
        self.conexion = sqlite3.connect("gastos.db")
        self.cursor = self.conexion.cursor()
        # Crear tablas
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, cantidad REAL, mes TEXT, año INTEGER)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS ingresos (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, cantidad REAL, mes TEXT, año INTEGER)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS fijos (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, cantidad REAL)"
        )
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sueldo (cantidad REAL)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS cuotas (id INTEGER PRIMARY KEY AUTOINCREMENT, descripcion TEXT, cantidad REAL, estado TEXT, cuotas_restantes INTEGER, fecha_inicio DATE)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS meses (id INTEGER PRIMARY KEY AUTOINCREMENT, mes TEXT, año INTEGER, remanente REAL)"
        )

        self.meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

    def ver_gastos(self):
        """
        Muestra los gastos en la tabla gastos
        """
        self.cursor.execute("SELECT * FROM gastos")
        gastos = self.cursor.fetchall()
        for gasto in gastos:
            print(f"{gasto[0]} - {gasto[1]}: ${gasto[2]}")

    def update_sueldo(self):
        """
        Actualiza el sueldo en la tabla sueldo
        """
        sueldo = float(input("Ingrese el sueldo: "))
        self.cursor.execute("DELETE FROM sueldo")
        self.cursor.execute(
            "INSERT INTO sueldo (cantidad) VALUES (?)",
            (sueldo,),
        )
        self._añadir_sueldo()

        self.conexion.commit()

    def añadir_gasto(self):
        """
        Añade un gasto a la tabla gastos
        """
        descripcion = input("Ingrese la descripcion del gasto: ")
        cantidad = float(input("Ingrese la cantidad del gasto: "))
        self.cursor.execute(
            "INSERT INTO gastos (descripcion, cantidad, mes, año) VALUES (?, ?, ?, ?)",
            (
                descripcion,
                cantidad,
                self.meses[datetime.datetime.now().month],
                datetime.datetime.now().year,
            ),
        )
        self.conexion.commit()

    def añadir_gasto_cuotas(self):
        """
        Añade un gasto a la tabla cuotas
        """
        descripcion = input("Ingrese la descripcion del gasto: ")
        cantidad = float(input("Ingrese la cantidad del gasto: "))
        cuotas = int(input("Ingrese la cantidad de cuotas: "))
        self.cursor.execute(
            "INSERT INTO cuotas (descripcion, cantidad, estado, cuotas restantes) VALUES (?, ?, ?, ?, ?)",
            (
                descripcion,
                cantidad,
                "Pendiente",
                cuotas,
                datetime.datetime.now().date(),
            ),
        )
        self.conexion.commit()

    def añadir_gasto_mensual(self):
        """
        Añade un gasto a la tabla fijos
        """
        descripcion = input("Ingrese la descripcion del gasto: ")
        cantidad = float(input("Ingrese la cantidad del gasto: "))
        self.cursor.execute(
            "INSERT INTO fijos (descripcion, cantidad) VALUES (?, ?)",
            (descripcion, cantidad),
        )
        self._añadir_mensuales()

        self.conexion.commit()

    def añadir_ingreso(self):
        """
        Añade un ingreso a la tabla ingresos
        """
        descripcion = input("Ingrese la descripcion del ingreso: ")
        cantidad = float(input("Ingrese la cantidad del ingreso: "))
        self.cursor.execute(
            "INSERT INTO ingresos (descripcion, cantidad, mes, año) VALUES (?, ?, ?, ?)",
            (
                descripcion,
                cantidad,
                self.meses[datetime.datetime.now().month],
                datetime.datetime.now().year,
            ),
        )
        self.conexion.commit()

    def _añadir_sueldo(self):
        """
        Añade el sueldo a la tabla ingresos
        """
        self.cursor.execute("SELECT * FROM sueldo")
        sueldo = self.cursor.fetchall()[0][0]
        self.cursor.execute(
            "INSERT INTO ingresos (descripcion, cantidad, mes, año) VALUES (?, ?, ?, ?)",
            (
                "Sueldo",
                sueldo,
                self.meses[datetime.datetime.now().month],
                datetime.datetime.now().year,
            ),
        )
        self.conexion.commit()

    def _añadir_mensuales(self):
        """
        Añade los gastos mensuales a la tabla gastos
        """
        self.cursor.execute("SELECT * FROM fijos")
        fijos = self.cursor.fetchall()
        for fijo in fijos:
            self.cursor.execute(
                "INSERT INTO gastos (descripcion, cantidad, mes, año) VALUES (?, ?, ? ,?)",
                (
                    fijo[1],
                    fijo[2],
                    self.meses[datetime.datetime.now().month],
                    datetime.datetime.now().year,
                ),
            )

        self.cursor.execute("SELECT * FROM cuotas")
        cuotas = self.cursor.fetchall()
        for cuota in cuotas:
            if cuota[3] == "Pendiente":
                self.cursor.execute(
                    "INSERT INTO gastos (descripcion, cantidad) VALUES (?, ?)",
                    (cuota[1], cuota[2]),
                )

        self.conexion.commit()

    def update_cuotas(self):
        self.cursor.execute("SELECT * FROM cuotas")
        cuotas = self.cursor.fetchall()
        for cuota in cuotas:
            if cuota[3] == "Pendiente":
                self.cursor.execute(
                    "UPDATE cuotas SET cuotas_restantes = ? WHERE id = ?",
                    (cuota[4] - 1, cuota[0]),
                )
                if cuota[4] - 1 == 0:
                    self.cursor.execute(
                        "UPDATE cuotas SET estado = ? WHERE id = ?",
                        ("Pagado", cuota[0]),
                    )
        self.conexion.commit()

    def cerrar_mes(self):
        """
        Cierra el mes actual y crea uno nuevo
        """
        mes = self.meses[datetime.datetime.now().month]
        año = datetime.datetime.now().year
        # Obtener remanente del mes anterior
        self.cursor.execute("SELECT * FROM meses")
        meses = self.cursor.fetchall()
        if len(meses) > 0:
            total = meses[-1][3]
        else:
            total = 0
        # Obtener gastos e ingresos
        self.cursor.execute(
            "SELECT * FROM gastos WHERE mes = ? AND año = ?", (mes, año)
        )
        gastos = self.cursor.fetchall()
        self.cursor.execute(
            "SELECT * FROM ingresos WHERE mes = ? AND año = ?", (mes, año)
        )
        ingresos = self.cursor.fetchall()
        # Calcular total
        total_gastos = sum([gasto[2] for gasto in gastos])
        total_ingresos = sum([ingreso[2] for ingreso in ingresos])
        # Calcular remanente
        total += total_ingresos - total_gastos
        # Añadir remanente a la tabla meses
        self.cursor.execute(
            "INSERT INTO meses (mes, año, remanente) VALUES (?, ?, ?)",
            (
                mes,
                año,
                total,
            ),
        )

        # Actualizar cuotas
        self.update_cuotas()
        # Añadir sueldo y gastos mensuales
        self._añadir_sueldo(1)
        self._añadir_mensuales(1)

        self.conexion.commit()

    def borrar_mes(self):
        """
        Borra un mes de la tabla meses
        """
        mes = int(input("Ingrese el mes a borrar (numero): "))
        mes = self.meses[mes]
        año = int(input("Ingrese el año a borrar: "))
        self.cursor.execute("DELETE FROM meses WHERE mes = ? AND año = ?", (mes, año))
        self.conexion.commit()

    def resetear_agenda(self):
        """
        Borra todos los datos de la agenda
        """
        self.cursor.execute("DELETE FROM meses")
        self.cursor.execute("DELETE FROM gastos")
        self.cursor.execute("DELETE FROM ingresos")
        self.cursor.execute("DELETE FROM fijos")
        self.cursor.execute("DELETE FROM sueldo")
        self.cursor.execute("DELETE FROM cuotas")
        self.cursor.execute("DELETE FROM sqlite_sequence")

        self.conexion.commit()

    def cerrar_agenda(self):
        """
        Cierra la conexion con la base de datos
        """
        self.conexion.close()


# agenda = Agenda()
# agenda.resetear_agenda()
# agenda.añadir_gasto("Comida", 100)
# agenda.añadir_ingreso("Sueldo", 1000)
# agenda.cerrar_mes()
