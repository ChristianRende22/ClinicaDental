import sys
import os
import mysql.connector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from datetime import datetime
from typing import List, Optional, Dict, Any
from mysql.connector import Error

# Importar los modelos existentes que ya funcionan
try:
    from .PacienteModelo import Paciente
    from .TratamientoModelo import Tratamiento
except ImportError:
    from PacienteModelo import Paciente
    from TratamientoModelo import Tratamiento

class Factura:
    def __init__(self, id_factura: str, 
                 paciente: Paciente, 
                 servicios: List[str], 
                 montos: List[float],
                 fecha_emision: datetime = None,
                 estado_pago: str = "Pendiente"):
        self.id_factura = id_factura
        self.paciente = paciente
        self.servicios = servicios
        self.montos = montos
        self.monto_total = sum(montos)
        self.fecha_emision = fecha_emision or datetime.now()
        self.estado_pago = estado_pago

    def __str__(self):
        servicios_str = "\n".join(f"   - {servicio}: ${monto:.2f}" 
                                 for servicio, monto in zip(self.servicios, self.montos))
        return (f"🧾 Factura ID: {self.id_factura}\n"
                f"📅 Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}\n"
                f"👤 Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
                f"📋 DUI: {self.paciente.dui}\n"
                f"🩺 Servicios:\n{servicios_str}\n"
                f"💰 Estado: {self.estado_pago}\n"
                f"💵 Total: ${self.monto_total:.2f}\n"
                f"{'='*30}")

class FacturacionModel:
    """Modelo que maneja la lógica de negocio y conexión con la BD"""
    
    @staticmethod
    def obtener_pacientes() -> List[Paciente]:
        """Obtiene todos los pacientes usando el método que ya funciona en CitaModelo"""
        try:
            print("📡 Intentando obtener pacientes desde PacienteModelo...")
            pacientes = Paciente.obtener_todos_los_pacientes()
            print(f"✅ Pacientes obtenidos exitosamente: {len(pacientes)}")
            
            # Verificar que los pacientes tengan los atributos necesarios
            if pacientes:
                primer_paciente = pacientes[0]
                print(f"🔍 Verificando estructura del primer paciente: {primer_paciente.nombre} {primer_paciente.apellido}")
            
            return pacientes
            
        except mysql.connector.Error as db_error:
            print(f"❌ Error de conexión MySQL: {db_error}")
            print(f"   Error Code: {db_error.errno}")
            print(f"   SQL State: {db_error.sqlstate}")
            print(f"   Message: {db_error.msg}")
            raise db_error
            
        except AttributeError as attr_error:
            print(f"❌ Error de atributo en modelo Paciente: {attr_error}")
            import traceback
            traceback.print_exc()
            raise attr_error
            
        except ImportError as import_error:
            print(f"❌ Error de importación: {import_error}")
            raise import_error
            
        except Exception as e:
            print(f"❌ Error general al obtener pacientes: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            raise e
    
    @staticmethod
    def obtener_tratamientos() -> List[Tratamiento]:
        """Obtiene todos los tratamientos usando el método que ya funciona en CitaModelo"""
        try:
            print("📡 Intentando obtener tratamientos desde TratamientoModelo...")
            tratamientos = Tratamiento.obtener_todos_tratamientos()
            print(f"✅ Tratamientos obtenidos exitosamente: {len(tratamientos)}")
            
            # Verificar que los tratamientos tengan los atributos necesarios
            if tratamientos:
                primer_tratamiento = tratamientos[0]
                print(f"🔍 Verificando estructura del primer tratamiento: {primer_tratamiento.descripcion}")
            
            return tratamientos
            
        except mysql.connector.Error as db_error:
            print(f"❌ Error de conexión MySQL al obtener tratamientos: {db_error}")
            raise db_error
            
        except Exception as e:
            print(f"❌ Error general al obtener tratamientos: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            raise e

    @staticmethod
    def insertar_factura_bd(factura: Factura) -> bool:
        """
        Inserta una nueva factura en la base de datos.
        :param factura: Instancia de la clase Factura a insertar.
        :return: True si la inserción fue exitosa, False en caso contrario.
        """
        conexion = None
        cursor = None

        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )

            cursor = conexion.cursor()

            # Consulta SQL corregida sin la columna 'Servicios' que no existe
            query = """
            INSERT INTO Factura (ID_Factura, ID_Paciente, Monto_Total, Fecha_Emision, Estado_Pago)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                factura.id_factura,
                factura.paciente.id_paciente,
                factura.monto_total,
                factura.fecha_emision,
                factura.estado_pago
            ))

            conexion.commit()
            print(f"✅ Factura {factura.id_factura} insertada correctamente en la base de datos")
            return True

        except Error as e:
            print(f"❌ Error al insertar la factura: {e}")
            if conexion:
                conexion.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def factura_existe(id_factura: str) -> bool:
        """
        Verifica si ya existe una factura con el ID dado.
        :param id_factura: ID de la factura a verificar.
        :return: True si existe, False en caso contrario.
        """
        conexion = None
        cursor = None

        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )

            cursor = conexion.cursor()

            # CORREGIDO: Usar el nombre correcto de la columna
            query = "SELECT COUNT(*) FROM Factura WHERE ID_Factura = %s"
            cursor.execute(query, (id_factura,))
            
            resultado = cursor.fetchone()
            existe = resultado[0] > 0
            
            print(f"🔍 Verificando factura {id_factura}: {'Existe' if existe else 'No existe'}")
            return existe

        except Error as e:
            print(f"❌ Error al verificar factura: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    @staticmethod
    def obtener_todas_facturas_bd() -> List[Factura]:
        """
        Obtiene todas las facturas de la base de datos.
        :return: Lista de objetos Factura.
        """
        conexion = None
        cursor = None
        facturas = []

        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )

            cursor = conexion.cursor()

            # Consulta corregida sin columnas que no existen
            query = """
            SELECT f.ID_Factura, f.ID_Paciente, f.Monto_Total, f.Fecha_Emision, f.Estado_Pago,
                   p.Nombre, p.Apellido, p.DUI
            FROM Factura f
            INNER JOIN Paciente p ON f.ID_Paciente = p.ID_Paciente
            ORDER BY f.Fecha_Emision DESC
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            for row in resultados:
                # Crear objeto Paciente
                paciente = Paciente(
                    nombre=row[5],
                    apellido=row[6], 
                    dui=row[7],
                    telefono="",  # Agregar campos faltantes según tu modelo
                    id_paciente=row[1]
                )

                # Crear objeto Factura sin servicios específicos
                factura = Factura(
                    id_factura=row[0],
                    paciente=paciente,
                    servicios=["Consulta Dental"],  # Servicio genérico
                    montos=[row[2]],  # Usar el monto total
                    fecha_emision=row[3],
                    estado_pago=row[4]
                )

                facturas.append(factura)

            print(f"✅ {len(facturas)} facturas obtenidas de la base de datos")
            return facturas

        except Error as e:
            print(f"❌ Error al obtener facturas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()