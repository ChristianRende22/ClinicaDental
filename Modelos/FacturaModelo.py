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
    def generar_id_factura_automatico() -> str:
        """
        Genera automáticamente un ID de factura siguiendo el patrón: FAC-{numero}-{fecha}{hora}
        Ejemplo: FAC-1-20250718143324
        """
        try:
            # Usar la misma lógica de conexión que el resto del archivo
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                password=''
            )
            cursor = conexion.cursor()
            
            # Buscar TODAS las facturas con formato FAC-numero- y encontrar el número máximo
            cursor.execute("""
                SELECT ID_Factura_Custom 
                FROM Factura 
                WHERE ID_Factura_Custom REGEXP '^FAC-[0-9]+-[0-9]+$'
                ORDER BY ID_Factura DESC
            """)
            
            resultados = cursor.fetchall()
            print(f"🔍 [DEBUG] Todas las facturas encontradas: {resultados}")
            
            siguiente_numero = 1  # Valor por defecto
            
            if resultados:
                # Analizar todos los resultados para encontrar el número máximo
                numeros_encontrados = []
                for resultado in resultados:
                    if resultado[0]:
                        partes = resultado[0].split('-')
                        if len(partes) >= 2:
                            try:
                                numero = int(partes[1])
                                numeros_encontrados.append(numero)
                                print(f"🔍 [DEBUG] Número extraído de {resultado[0]}: {numero}")
                            except ValueError:
                                continue
                
                if numeros_encontrados:
                    ultimo_numero = max(numeros_encontrados)
                    siguiente_numero = ultimo_numero + 1
                    print(f"🔍 [DEBUG] Números encontrados: {numeros_encontrados}")
                    print(f"🔍 [DEBUG] Último número: {ultimo_numero}, Siguiente: {siguiente_numero}")
                else:
                    print(f"🔍 [DEBUG] No se pudieron extraer números válidos")
            else:
                print(f"🔍 [DEBUG] No se encontraron facturas previas")
            
            # Generar timestamp actual (YYYYMMDDHHMMSS)
            ahora = datetime.now()
            timestamp = ahora.strftime("%Y%m%d%H%M%S")
            
            # 🚀 ALGORITMO INTELIGENTE: Buscar el primer número disponible
            print(f"🔍 [SMART-SEARCH] Buscando primer ID disponible desde {siguiente_numero}...")
            numero_actual = siguiente_numero
            id_encontrado = False
            intentos = 0
            max_intentos = 1000  # Límite de seguridad para evitar bucle infinito
            
            while not id_encontrado and intentos < max_intentos:
                # Generar ID candidato
                id_candidato = f"FAC-{numero_actual}-{timestamp}"
                
                # Verificar si este ID ya existe en la base de datos
                cursor.execute("SELECT COUNT(*) FROM Factura WHERE ID_Factura_Custom = %s", (id_candidato,))
                existe = cursor.fetchone()[0] > 0
                
                if not existe:
                    # ✅ Encontramos un ID libre!
                    nuevo_id = id_candidato
                    id_encontrado = True
                    print(f"✅ [SMART-SEARCH] ID libre encontrado: {nuevo_id} (intento #{intentos + 1})")
                else:
                    # ❌ Este ID ya existe, probar el siguiente número
                    print(f"⚠️ [SMART-SEARCH] ID {id_candidato} ya existe, probando siguiente...")
                    numero_actual += 1
                    intentos += 1
            
            if not id_encontrado:
                # Si llegamos aquí, usamos un fallback con timestamp más específico
                timestamp_especifico = ahora.strftime("%Y%m%d%H%M%S%f")[:17]  # Incluir microsegundos
                nuevo_id = f"FAC-{numero_actual}-{timestamp_especifico}"
                print(f"🆘 [FALLBACK] Usando ID con microsegundos: {nuevo_id}")
            
            cursor.close()
            conexion.close()
            
            print(f"🆔 [AUTO-ID] ID final generado: {nuevo_id}")
            return nuevo_id
            
        except Exception as e:
            print(f"❌ Error generando ID automático: {e}")
            # Fallback: usar timestamp simple
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            fallback_id = f"FAC-1-{timestamp}"
            print(f"🆔 [FALLBACK] Usando ID de respaldo: {fallback_id}")
            return fallback_id
    
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
            
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )

            cursor = conexion.cursor()
            print("✅ Conexión a la base de datos establecida")

            # Consulta SQL corregida usando ID_Factura_Custom en lugar de ID_Factura
            query = """
            INSERT INTO Factura (ID_Factura_Custom, ID_Paciente, Monto_Total, Fecha_Emision, Estado_Pago)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            valores = (
                factura.id_factura,
                factura.paciente.id_paciente,
                factura.monto_total,
                factura.fecha_emision,
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
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                port=3307,
                password='1234'
            )

            cursor = conexion.cursor()

            # CORREGIDO: Usar el nombre correcto de la columna ID_Factura_Custom
            query = "SELECT COUNT(*) FROM Factura WHERE ID_Factura_Custom = %s"
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
            # Conectar a la base de datos
            conexion = mysql.connector.connect(
                host='localhost',
                database='ClinicaDental',
                user='root',
                password=''
            )
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