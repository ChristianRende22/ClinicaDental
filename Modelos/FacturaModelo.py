import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar configuración centralizada
from Config.database_config import obtener_conexion, conectar_bd, cerrar_conexion_segura
import mysql.connector  # Mantener para manejo de errores específicos
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
    def generar_id_factura_automatico() -> str:
        """
        Genera automáticamente un ID de factura siguiendo el patrón: F001, F002, F003, etc.
        Similar al sistema de horarios.
        """
        try:
            conexion = conectar_bd()
            if not conexion:
                print("❌ No se pudo establecer conexión a la base de datos.")
                return "F001"  # ID por defecto si hay error de conexión
            
            cursor = conexion.cursor()
            
            # Obtener todas las facturas existentes
            cursor.execute("SELECT ID_Factura FROM Factura")
            resultados = cursor.fetchall()
            
            if not resultados:
                cursor.close()
                conexion.close()
                return "F001"  # Primera factura
            
            # Extraer los números de los IDs existentes y ordenarlos
            numeros_existentes = set()
            for row in resultados:
                id_factura = str(row[0]).strip()
                # Verificar que el ID tenga el formato correcto (F seguido de 3 dígitos)
                if id_factura.startswith('F') and len(id_factura) == 4:
                    try:
                        numero = int(id_factura[1:])  # Extraer número después de 'F'
                        numeros_existentes.add(numero)
                    except ValueError:
                        continue
            
            if not numeros_existentes:
                cursor.close()
                conexion.close()
                return "F001"  # Si no hay IDs válidos, empezar con F001
            
            # Buscar el primer número disponible en la secuencia
            siguiente_numero = 1
            while siguiente_numero in numeros_existentes:
                siguiente_numero += 1
            
            cursor.close()
            conexion.close()
            
            # Formatear con ceros a la izquierda (siempre 3 dígitos)
            nuevo_id = f"F{siguiente_numero:03d}"
            print(f"🆔 ID de factura generado: {nuevo_id}")
            return nuevo_id
            
        except Exception as e:
            print(f"❌ Error generando ID automático: {e}")
            return "F001"  # ID por defecto en caso de error
    
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
            # Validar datos antes de insertar
            print(f"🔍 Validando datos de factura:")
            print(f"   - ID Factura: {factura.id_factura}")
            print(f"   - ID Paciente: {factura.paciente.id_paciente}")
            print(f"   - Nombre Paciente: {factura.paciente.nombre} {factura.paciente.apellido}")
            print(f"   - Monto Total: {factura.monto_total}")
            print(f"   - Fecha Emisión: {factura.fecha_emision}")
            print(f"   - Estado Pago: {factura.estado_pago}")
            
            # Verificar que los datos no sean None
            if not factura.id_factura:
                print("❌ Error: ID Factura está vacío")
                return False
                
            if not factura.paciente.id_paciente:
                print("❌ Error: ID Paciente está vacío")
                return False
            
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False

            cursor = conexion.cursor()
            print("✅ Conexión a la base de datos establecida")

            # Consulta SQL usando ID_Factura directamente
            query = """
            INSERT INTO Factura (ID_Factura, ID_Paciente, Fecha_Emision, Descripcion_Servicio, Monto_Servicio, Monto_Total, Estado_Pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Preparar la descripción de servicios
            descripcion_servicios = ", ".join(factura.servicios)
            monto_servicio = sum(factura.montos)
            
            valores = (
                factura.id_factura,
                factura.paciente.id_paciente,
                factura.fecha_emision,
                descripcion_servicios,
                monto_servicio,
                factura.monto_total,
                factura.estado_pago
            )
            
            print(f"📝 Ejecutando consulta SQL con valores: {valores}")
            cursor.execute(query, valores)

            conexion.commit()
            print(f"✅ Factura {factura.id_factura} insertada correctamente en la base de datos")
            return True

        except Error as e:
            print(f"❌ Error de MySQL al insertar la factura: {e}")
            print(f"   - Código de error: {e.errno}")
            print(f"   - Mensaje SQL: {e.msg}")
            if conexion:
                conexion.rollback()
            return False
            
        except Exception as e:
            print(f"❌ Error general al insertar la factura: {e}")
            import traceback
            traceback.print_exc()
            if conexion:
                conexion.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()
                print("🔒 Conexión a la base de datos cerrada")

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
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False

            cursor = conexion.cursor()

            # Usar el nombre correcto de la columna ID_Factura
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
    def paciente_tiene_factura_hoy(id_paciente: int) -> bool:
        """
        Verifica si un paciente ya tiene una factura creada el día de hoy.
        :param id_paciente: ID del paciente a verificar
        :return: True si ya tiene factura hoy, False si no
        """
        conexion = None
        cursor = None
        
        try:
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False
            cursor = conexion.cursor()
            
            # Buscar facturas del paciente creadas hoy
            hoy = datetime.now().strftime('%Y-%m-%d')
            query = """
                SELECT COUNT(*) 
                FROM Factura 
                WHERE ID_Paciente = %s 
                AND DATE(Fecha_Emision) = %s
            """
            cursor.execute(query, (id_paciente, hoy))
            
            resultado = cursor.fetchone()
            tiene_factura_hoy = resultado[0] > 0
            
            print(f"🔍 [VERIFICACIÓN] Paciente ID {id_paciente} - Facturas hoy: {resultado[0]}")
            return tiene_factura_hoy

        except Error as e:
            print(f"❌ Error al verificar facturas del día: {e}")
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
            conexion= conectar_bd()
            if not conexion:
                print("No se pudo establecer conexión con la base de datos.")
                return False

            cursor = conexion.cursor()

            # Consulta usando las columnas correctas de la tabla Factura
            query = """
            SELECT f.ID_Factura, f.ID_Paciente, f.Monto_Total, f.Fecha_Emision, f.Estado_Pago,
                   f.Descripcion_Servicio, p.Nombre, p.Apellido, p.DUI
            FROM Factura f
            INNER JOIN Paciente p ON f.ID_Paciente = p.ID_Paciente
            ORDER BY f.Fecha_Emision DESC
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            for row in resultados:
                # Crear objeto Paciente con todos los campos requeridos
                paciente = Paciente(
                    nombre=row[6],
                    apellido=row[7], 
                    fecha_nacimiento=datetime(1990, 1, 1),  # Fecha por defecto
                    telefono=0,  # Teléfono por defecto
                    correo="",  # Correo por defecto
                    dui=row[8],
                    id_paciente=row[1]
                )

                # Crear objeto Factura con la descripción de servicios
                descripcion_servicio = row[5] if row[5] else "Consulta Dental"
                factura = Factura(
                    id_factura=row[0],
                    paciente=paciente,
                    servicios=[descripcion_servicio],  # Usar descripción de la BD
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