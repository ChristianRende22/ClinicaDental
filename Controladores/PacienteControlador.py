# Agregar el directorio padre al path
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================

from Modelos.PacienteModelo import *
from Modelos.PacienteModelo import Paciente

from Modelos.CitaModelo import Cita
from Modelos.TratamientoModelo import Tratamiento
from datetime import datetime
from typing import List
import re

# ==========================================
# CLASE: PacienteControlador
# PROPÓSITO: Controlador para manejar la lógica 
# ==========================================

class PacienteControlador:
    """Controlador para manejar la lógica de negocio de los pacientes"""
    
    def __init__(self):
        self.pacientes_registrados: List[Paciente] = []
        self.paciente_actual: Paciente = None
        self.vista = None  # Referencia a la vista
        # No inicializar el contador aquí - se hará cuando se carguen los datos
        print("🔧 PacienteControlador inicializado")
    
    def set_vista(self, vista):
        """Establece la referencia a la vista"""
        self.vista = vista
    
    def inicializar_vista(self):
        """Inicializa y muestra la vista"""
        # Inicializar el sistema de IDs secuenciales la primera vez
        if not hasattr(self, '_sistema_inicializado'):
            self.inicializar_sistema_ids_secuenciales()
            self._sistema_inicializado = True
        
        if not self.vista:
            # Importación tardía para evitar dependencias circulares
            from Vistas.PacienteVista import PacienteWindow
            self.vista = PacienteWindow(self)  # Pasar el controlador a la vista
        
        self.vista.show()
        return self.vista
    
    def cerrar_vista(self):
        """Cierra la vista"""
        if self.vista:
            self.vista.close()
            self.vista = None

    # ==========================================
    # MÉTODOS DE COMUNICACIÓN CON LA VISTA
    # PROPÓSITO: Manejar la comunicación bidireccional con la vista
    # ==========================================
    
    def actualizar_vista(self):
        """Actualiza la vista con los datos actuales"""
        if self.vista:
            self.vista.actualizar_interfaz()
    
    def mostrar_mensaje_en_vista(self, titulo: str, mensaje: str, tipo: str = "info"):
        """Muestra un mensaje en la vista"""
        if self.vista:
            self.vista.mostrar_mensaje(titulo, mensaje, tipo)
    
    def actualizar_lista_pacientes_en_vista(self):
        """Actualiza la lista de pacientes en la vista"""
        if self.vista:
            self.vista.actualizar_lista_pacientes()
    
    def limpiar_campos_vista(self):
        """Limpia los campos de la vista"""
        if self.vista:
            self.vista.limpiar_campos()

    # ==========================================
    # MÉTODOS DE VALIDACIÓN Y REGLAS DE NEGOCIO
    # PROPÓSITO: Validar datos y aplicar reglas de negocio
    # ==========================================
    
    def validar_email(self, email: str) -> bool:
        """Valida el formato del email usando el modelo"""
        return Paciente.validar_formato_email(email)
    
    def mostrar(self):
        self.inicializar_vista()

    def validar_dui(self, dui: str) -> bool:
        """Valida el formato del DUI usando el modelo"""
        return Paciente.validar_formato_dui(dui)
    
    def validar_telefono(self, telefono) -> bool:
        """Valida que el teléfono tenga el formato correcto (acepta str o int)"""
        # Si es None o 0, es válido (teléfono opcional)
        if not telefono:
            return True
        
        # Convertir a string si es necesario
        telefono_str = str(telefono) if isinstance(telefono, int) else telefono
        
        # Si es string, validar que no esté vacío
        if isinstance(telefono, str) and not telefono.strip():
            return True  # Teléfono opcional
        
        # Remover espacios y caracteres especiales
        telefono_limpio = ''.join(filter(str.isdigit, telefono_str))
        
        # Debe tener al menos 8 dígitos
        return len(telefono_limpio) >= 8
    
    def validar_edad_minima(self, fecha_nacimiento: datetime) -> tuple[bool, str]:
        """Valida que la edad sea válida (regla de negocio)"""
        hoy = datetime.now()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if edad <= 0:
            return False, "La edad debe ser mayor a 0"
        if edad > 120:
            return False, "La edad no puede ser mayor a 120 años"
        
        return True, "Edad válida"
    
    def validar_datos_completos(self, nombre: str, apellido: str) -> tuple[bool, str]:
        """Valida que los datos obligatorios estén completos (DUI ya no es obligatorio)"""
        # Validación simple sin usar strip()
        if not nombre or not apellido:
            return False, "Nombre y Apellido son campos obligatorios"
        
        # Verificar que no sean solo espacios
        if len(nombre.replace(" ", "")) == 0 or len(apellido.replace(" ", "")) == 0:
            return False, "Nombre y Apellido no pueden estar vacíos"
            
        return True, "Datos completos"
    
    # ==========================================
    # MÉTODOS DE BÚSQUEDA Y VERIFICACIÓN (LÓGICA DE NEGOCIO)
    # PROPÓSITO: Buscar y verificar existencia de pacientes
    # ==========================================
    

    def buscar_pacientes_por_nombre_apellido(self, nombre: str = "", apellido: str = "") -> List[Paciente]:
        """Busca pacientes por nombre y/o apellido (coincidencia parcial)"""
        pacientes_encontrados = []
        
        nombre_lower = nombre.lower() if nombre else ""
        apellido_lower = apellido.lower() if apellido else ""
        
        for paciente in self.pacientes_registrados:
            nombre_paciente = paciente.nombre.lower()
            apellido_paciente = paciente.apellido.lower()
            
            # Verificar si coincide con la búsqueda
            coincide_nombre = not nombre_lower or nombre_lower in nombre_paciente
            coincide_apellido = not apellido_lower or apellido_lower in apellido_paciente
            
            if coincide_nombre and coincide_apellido:
                pacientes_encontrados.append(paciente)
        
        return pacientes_encontrados

    def existe_paciente_con_dui(self, dui: str) -> bool:
        """
        Verifica si ya existe un paciente registrado con el DUI especificado
        
        Args:
            dui (str): DUI a verificar
            
        Returns:
            bool: True si existe un paciente con ese DUI, False en caso contrario
        """
        if not dui or not dui.strip():
            return False
        
        dui_limpio = dui.strip().replace(" ", "").replace("-", "")
        
        for paciente in self.pacientes_registrados:
            if paciente.dui:
                dui_paciente_limpio = paciente.dui.strip().replace(" ", "").replace("-", "")
                if dui_limpio == dui_paciente_limpio:
                    return True
        
        return False

    def resetear_contador_ids_secuencial(self):
        """
        Resetea el contador de IDs para que sea secuencial basándose en los pacientes en memoria
        """
        if not self.pacientes_registrados:
            # Si no hay pacientes, el próximo ID debería ser 1
            Paciente._contador_id = 1
            Paciente._pacientes_existentes = []
            print("🔄 Contador de IDs reseteado a 1 (sin pacientes)")
        else:
            # Renumerar todos los pacientes secuencialmente
            for i, paciente in enumerate(self.pacientes_registrados, 1):
                paciente.id_paciente = i
            
            # Establecer el contador para el siguiente paciente
            Paciente._contador_id = len(self.pacientes_registrados) + 1
            
            # Actualizar la lista de IDs existentes
            Paciente._pacientes_existentes = [p.id_paciente for p in self.pacientes_registrados]
            
            print(f"🔄 IDs renumerados secuencialmente. Próximo ID: {Paciente._contador_id}")
            print(f"📊 IDs asignados: {sorted(Paciente._pacientes_existentes)}")

    # ==========================================
    # MÉTODOS DE GESTIÓN DE PACIENTES (LÓGICA DE NEGOCIO)
    # PROPÓSITO: Crear, modificar y gestionar pacientes
    # ==========================================
    
    def crear_paciente(self, nombre: str, apellido: str, fecha_nacimiento: datetime, 
                      telefono: int, correo: str, dui: str = "", saldo_pendiente: float = 0.0) -> tuple[bool, str]:
        """
        Crea un nuevo paciente aplicando todas las validaciones y reglas de negocio
        Retorna: (éxito: bool, mensaje: str)
        """
        try:
            # Validaciones usando el controlador (reglas de negocio)
            valido, mensaje = self.validar_datos_completos(nombre, apellido)
            if not valido:
                return False, mensaje
            
            # Validar DUI solo si se proporciona
            if dui and len(dui.replace(" ", "")) > 0:
                if not self.validar_dui(dui):
                    return False, "El DUI debe tener el formato: 12345678-9"
                
                if self.existe_paciente_con_dui(dui):
                    return False, f"Ya existe un paciente registrado con el DUI: {dui}"
            
            if correo and not self.validar_email(correo):
                return False, "El email no tiene un formato válido"
            
            if not self.validar_telefono(telefono):
                return False, "El teléfono debe tener al menos 8 dígitos"
            
            valido_edad, mensaje_edad = self.validar_edad_minima(fecha_nacimiento)
            if not valido_edad:
                return False, mensaje_edad
            
            # Crear el nuevo paciente usando el modelo (el ID se asigna automáticamente)
            nuevo_paciente = Paciente(
                nombre, apellido, fecha_nacimiento, telefono, correo, dui, saldo_pendiente
            )
            
            # Insertar en la base de datos
            if not Paciente.insertar_en_bd(nuevo_paciente):
                return False, "Error al insertar paciente en la base de datos"

            # Agregar a la lista local
            self.pacientes_registrados.append(nuevo_paciente)
            self.paciente_actual = nuevo_paciente

            # Renumerar secuencialmente
            self.resetear_contador_ids_secuencial()

            # Registrar la creación del paciente en el historial médico
            notas_creacion = f"""
PACIENTE REGISTRADO EN EL SISTEMA:
• Nombre Completo: {nombre} {apellido}
• Fecha de Nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}
• Edad: {nuevo_paciente.calcular_edad()} años
• DUI: {dui if dui else 'No proporcionado'}
• Teléfono: {self.formatear_telefono(telefono)}
• Correo: {correo if correo else 'No proporcionado'}
• Saldo Inicial: ${saldo_pendiente:,.2f}
• Fecha de Registro: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

Paciente registrado exitosamente en la Clínica Dental.
Bienvenido/a al sistema de gestión médica.
            """
            
            # Insertar registro inicial en historial médico
            nuevo_paciente.agregar_nota_historial_medico(
                notas_creacion.strip(), 
                "Activo"
            )

            return True, f"Paciente #{nuevo_paciente.id_paciente}: {nombre} {apellido} creado exitosamente y registrado en historial médico"

        except ValueError as e:
                return False, f"Error al crear paciente: {str(e)}"
        except Exception as e:
                return False, f"Error inesperado: {str(e)}"
            
    def seleccionar_paciente(self, paciente: Paciente) -> bool:
        """Selecciona un paciente como el actual"""
        if paciente in self.pacientes_registrados:
            self.paciente_actual = paciente
            return True
        return False
    
    def modificar_paciente_actual(self, **kwargs) -> tuple[bool, str]:
        """Modifica los datos del paciente actual"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        try:
            for campo, valor in kwargs.items():
                if hasattr(self.paciente_actual, campo):
                    # Validaciones específicas según el campo
                    if campo == 'dui' and valor and len(str(valor).replace(" ", "")) > 0:
                        if not self.validar_dui(valor):
                            return False, "El DUI debe tener el formato: 12345678-9"
                    elif campo == 'correo' and valor and not self.validar_email(valor):
                        return False, "El email no tiene un formato válido"
                    elif campo == 'telefono' and not self.validar_telefono(valor):
                        return False, "El teléfono debe tener al menos 8 dígitos"
                    
                    setattr(self.paciente_actual, campo, valor)
            
            return True, "Paciente modificado exitosamente"
        except Exception as e:
            return False, f"Error al modificar paciente: {str(e)}"
    
    def eliminar_paciente(self, id_paciente: int) -> tuple[bool, str]:
        """Elimina un paciente del sistema usando su ID"""
        paciente = self.buscar_paciente_por_id(id_paciente)
        if not paciente:
            return False, "Paciente no encontrado"
        
        # Regla de negocio: No eliminar pacientes con citas futuras o saldo pendiente
        if paciente.obtener_proximas_citas():
            return False, "No se puede eliminar un paciente con citas futuras"
        
        if paciente.tiene_saldo_pendiente():
            return False, "No se puede eliminar un paciente con saldo pendiente"
        
        self.pacientes_registrados.remove(paciente)
        if self.paciente_actual == paciente:
            self.paciente_actual = None
        
        return True, f"Paciente #{paciente.id_paciente}: {paciente.nombre} {paciente.apellido} eliminado exitosamente"
    
    # ==========================================
    # MÉTODOS DE GESTIÓN DE TRATAMIENTOS Y CITAS (LÓGICA DE NEGOCIO)
    # PROPÓSITO: Agregar tratamientos y citas a pacientes con validaciones
    # ==========================================
    
    def agregar_tratamiento_a_paciente(self, tratamiento: Tratamiento) -> tuple[bool, str]:
        """Agrega un tratamiento al paciente actual con validaciones y lo registra en el historial médico"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not tratamiento:
            return False, "El tratamiento no puede estar vacío"
        
        try:
            # Agregar tratamiento a la memoria del paciente
            self.paciente_actual.agregar_tratamiento(tratamiento)
            
            # Registrar el tratamiento en el historial médico de la base de datos
            notas_tratamiento = f"""
NUEVO TRATAMIENTO REGISTRADO:
• Tipo de Tratamiento: {getattr(tratamiento, 'tipo', 'No especificado')}
• Descripción: {getattr(tratamiento, 'descripcion', 'Sin descripción')}
• Costo: ${getattr(tratamiento, 'costo', 0):,.2f}
• Estado: {getattr(tratamiento, 'estado', 'Pendiente')}
• Doctor: {getattr(tratamiento, 'doctor', 'No especificado')}
• Fecha de Registro: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

Tratamiento agregado exitosamente al paciente {self.paciente_actual.nombre} {self.paciente_actual.apellido}.
            """
            
            # Insertar en el historial médico de la base de datos
            exito_historial = self.paciente_actual.agregar_nota_historial_medico(
                notas_tratamiento.strip(), 
                "Activo"
            )
            
            if exito_historial:
                return True, f"Tratamiento agregado exitosamente a {self.paciente_actual.nombre} y registrado en historial médico"
            else:
                return True, f"Tratamiento agregado a {self.paciente_actual.nombre} pero no se pudo registrar en historial médico"
                
        except Exception as e:
            return False, f"Error al agregar tratamiento: {str(e)}"
    
    def agregar_cita_a_paciente(self, cita: Cita) -> tuple[bool, str]:
        """Agrega una cita al paciente actual con validaciones y la registra en el historial médico"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not cita:
            return False, "La cita no puede estar vacía"
        
        # Validar que no haya conflicto de horarios
        if self._tiene_conflicto_horario(cita):
            return False, "El paciente ya tiene una cita en ese horario"
        
        try:
            # Agregar cita a la memoria del paciente
            self.paciente_actual.agregar_cita(cita)
            
            # Registrar la cita en el historial médico de la base de datos
            fecha_cita = getattr(cita, 'fecha', 'No especificada')
            hora_cita = getattr(cita, 'hora_inicio', 'No especificada')
            
            notas_cita = f"""
NUEVA CITA PROGRAMADA:
• Fecha de la Cita: {fecha_cita}
• Hora de Inicio: {hora_cita}
• Tipo de Consulta: {getattr(cita, 'tipo_consulta', 'Consulta general')}
• Doctor: {getattr(cita, 'doctor', 'No especificado')}
• Estado: {getattr(cita, 'estado', 'Programada')}
• Duración Estimada: {getattr(cita, 'duracion', 'No especificada')}
• Costo de la Cita: ${getattr(cita, 'costo_cita', 0):,.2f}
• Observaciones: {getattr(cita, 'observaciones', 'Sin observaciones')}
• Fecha de Registro: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

Cita programada exitosamente para el paciente {self.paciente_actual.nombre} {self.paciente_actual.apellido}.
            """
            
            # Insertar en el historial médico de la base de datos
            exito_historial = self.paciente_actual.agregar_nota_historial_medico(
                notas_cita.strip(), 
                "Activo"
            )
            
            if exito_historial:
                return True, f"Cita agregada exitosamente a {self.paciente_actual.nombre} y registrada in historial médico"
            else:
                return True, f"Cita agregada a {self.paciente_actual.nombre} pero no se pudo registrar en historial médico"
                
        except Exception as e:
            return False, f"Error al agregar cita: {str(e)}"

    # ==========================================
    # MÉTODOS DE CONSULTA Y REPORTES (LÓGICA DE NEGOCIO)
    # PROPÓSITO: Obtener información procesada para la vista
    # ==========================================
    
    def get_paciente_actual(self) -> Paciente:
        """Retorna el paciente actual"""
        return self.paciente_actual
    
    def get_todos_los_pacientes(self) -> List[Paciente]:
        """Retorna la lista de todos los pacientes registrados"""
        return self.pacientes_registrados.copy()  # Copia para evitar modificaciones externas
    
    def get_resumen_pacientes(self) -> dict:
        """Obtiene un resumen estadístico de todos los pacientes"""
        total_pacientes = len(self.pacientes_registrados)
        pacientes_con_saldo = len(self.buscar_pacientes_con_saldo_pendiente())
        pacientes_menores = len(self.buscar_pacientes_menores_edad())
        
        saldo_total_pendiente = sum(p.saldo_pendiente for p in self.pacientes_registrados)
        ingresos_totales = sum(p.get_balance_total() for p in self.pacientes_registrados)
        
        return {
            'total_pacientes': total_pacientes,
            'pacientes_con_saldo_pendiente': pacientes_con_saldo,
            'pacientes_menores_edad': pacientes_menores,
            'saldo_total_pendiente': saldo_total_pendiente,
            'ingresos_totales': ingresos_totales,
            'promedio_saldo_por_paciente': saldo_total_pendiente / total_pacientes if total_pacientes > 0 else 0
        }
    
    def get_pacientes_ordenados_por_nombre(self) -> List[Paciente]:
        """Obtiene la lista de pacientes ordenada por nombre"""
        return sorted(self.pacientes_registrados, key=lambda p: f"{p.apellido} {p.nombre}")
    
    def get_pacientes_ordenados_por_saldo(self, descendente: bool = True) -> List[Paciente]:
        """Obtiene la lista de pacientes ordenada por saldo pendiente"""
        return sorted(self.pacientes_registrados, 
                     key=lambda p: p.saldo_pendiente, reverse=descendente)
    
    # ==========================================
    # MÉTODOS DE FORMATEO Y UTILIDADES PARA LA VISTA
    # PROPÓSITO: Formatear datos para presentación en la vista
    # ==========================================
    
    def formatear_telefono(self, telefono: int) -> str:
        """Formatea el número de teléfono para mejor presentación"""
        if telefono == 0:
            return "No especificado"
        
        telefono_str = str(telefono)
        if len(telefono_str) == 8:
            return f"{telefono_str[:4]}-{telefono_str[4:]}"
        elif len(telefono_str) >= 8:
            return f"+503 {telefono_str[-8:-4]}-{telefono_str[-4:]}"
        return telefono_str
    
    def get_estado_icon(self, estado: str) -> str:
        """Devuelve un icono basado en el estado"""
        estado_lower = estado.lower()
        if 'completado' in estado_lower or 'finalizado' in estado_lower:
            return "✅"
        elif 'pendiente' in estado_lower or 'programado' in estado_lower:
            return "⏳"
        elif 'cancelado' in estado_lower:
            return "❌"
        elif 'en proceso' in estado_lower or 'activo' in estado_lower:
            return "🔄"
        else:
            return "📋"
    
    def formatear_moneda(self, cantidad: float) -> str:
        """Formatea una cantidad como moneda"""
        return f"${cantidad:,.2f}"
    
    def generar_info_basica_paciente(self, paciente: Paciente) -> str:
        """Genera información básica formateada del paciente para mostrar en la vista"""
        edad = paciente.calcular_edad()
        tipo_paciente = "Menor de edad" if paciente.es_menor_de_edad() else "Mayor de edad"
        estado_saldo = "Con saldo pendiente" if paciente.tiene_saldo_pendiente() else "Al día"
        dui_info = f"📋 DUI: {paciente.dui}" if paciente.tiene_dui() else "📋 DUI: No registrado"
        
        return f"""
🆔 ID: #{paciente.id_paciente}
👤 {paciente.nombre} {paciente.apellido}
{dui_info}
🎂 Edad: {edad} años ({tipo_paciente})
📞 Teléfono: {self.formatear_telefono(paciente.telefono)}
📧 Email: {paciente.correo if paciente.correo else 'No especificado'}
💰 Saldo: {self.formatear_moneda(paciente.saldo_pendiente)} ({estado_saldo})
📅 Registrado: {paciente.fecha_registro}
🩺 Tratamientos: {len(paciente.historial_medico)}
📅 Citas: {len(paciente.citas)}
"""
    
    def generar_resumen_financiero(self, paciente: Paciente) -> str:
        """Genera un resumen financiero del paciente"""
        total_tratamientos = paciente.calcular_total_tratamientos()
        total_citas = paciente.calcular_total_citas()
        balance_total = paciente.get_balance_total()
        
        return f"""
💰 RESUMEN FINANCIERO:
   • Costo total tratamientos: {self.formatear_moneda(total_tratamientos)}
   • Costo total citas: {self.formatear_moneda(total_citas)}
   • Saldo pendiente: {self.formatear_moneda(paciente.saldo_pendiente)}
   • Balance total: {self.formatear_moneda(balance_total)}
"""
    
    # ==========================================
    # MÉTODOS DE CÁLCULO Y UTILES (ELIMINADOS - MOVIDOS AL MODELO)
    # PROPÓSITO: Estos métodos ahora están en el modelo Paciente
    # ==========================================
    
    def calcular_edad(self, fecha_nacimiento: datetime) -> int:
        """OBSOLETO: Usar paciente.calcular_edad() directamente del modelo"""
        # Mantenemos por compatibilidad pero delegamos al modelo
        temp_paciente = Paciente("temp", "temp", fecha_nacimiento, "00000000-0", 12345678, "")
        return temp_paciente.calcular_edad()
    
    def cargar_todos_los_pacientes_desde_bd(self) -> tuple[bool, str]:
        """
        Carga todos los pacientes desde la base de datos y los almacena en memoria
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Obtener todos los pacientes desde la base de datos
            pacientes_bd = Paciente.obtener_todos_los_pacientes()
            
            if not pacientes_bd:
                return False, "No se encontraron pacientes en la base de datos"
            
            # Actualizar la lista de pacientes registrados
            self.pacientes_registrados = pacientes_bd
            
            # IMPORTANTE: Renumerar secuencialmente para mantener orden
            self.resetear_contador_ids_secuencial()
            
            # Actualizar la vista si está disponible
            if self.vista:
                self.vista.actualizar_lista_pacientes()
            
            mensaje = f"✅ Se cargaron {len(pacientes_bd)} pacientes desde la base de datos con IDs secuenciales"
            print(mensaje)
            return True, mensaje
            
        except Exception as e:
            mensaje_error = f"❌ Error al cargar pacientes desde la BD: {str(e)}"
            print(mensaje_error)
            return False, mensaje_error
    
    def obtener_todos_los_pacientes_para_vista(self) -> List[Paciente]:
        """
        Obtiene todos los pacientes para mostrar en la vista
        Si no hay pacientes en memoria, intenta cargarlos desde la BD
        
        Returns:
            List[Paciente]: Lista de todos los pacientes disponibles
        """
        # Si no hay pacientes en memoria, intentar cargar desde BD
        if not self.pacientes_registrados:
            exito, mensaje = self.cargar_todos_los_pacientes_desde_bd()
            if not exito:
                print(f"⚠️ No se pudieron cargar pacientes desde BD: {mensaje}")
        
        return self.pacientes_registrados.copy()

    def obtener_historial_medico_paciente_actual(self) -> List[dict]:
        """
        Obtiene el historial médico del paciente actual desde la base de datos
        
        Returns:
            List[dict]: Lista del historial médico o lista vacía si no hay paciente seleccionado
        """
        if not self.paciente_actual:
            return []
        
        return self.paciente_actual.obtener_historial_medico_completo()
    
    def agregar_nota_historial_medico_actual(self, notas: str, estado: str = "Activo") -> tuple[bool, str]:
        """
        Agrega una nueva nota al historial médico del paciente actual
        
        Args:
            notas (str): Notas médicas a agregar
            estado (str): Estado del registro
            
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not notas or not notas.strip():
            return False, "Las notas médicas no pueden estar vacías"
        
        try:
            exito = self.paciente_actual.agregar_nota_historial_medico(notas.strip(), estado)
            if exito:
                return True, f"Nota médica agregada exitosamente al historial de {self.paciente_actual.nombre} {self.paciente_actual.apellido}"
            else:
                return False, "Error al agregar la nota médica a la base de datos"
        except Exception as e:
            return False, f"Error al agregar nota médica: {str(e)}"

    def registrar_evento_en_historial(self, evento: str, descripcion: str, estado: str = "Activo") -> tuple[bool, str]:
        """
        Registra un evento general en el historial médico del paciente actual
        
        Args:
            evento (str): Tipo de evento (ej: "CONSULTA", "EXAMEN", "PROCEDIMIENTO")
            descripcion (str): Descripción detallada del evento
            estado (str): Estado del registro
            
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not evento or not descripcion:
            return False, "El evento y la descripción son obligatorios"
        
        try:
            notas_evento = f"""
{evento.upper()}:
{descripcion}

• Paciente: {self.paciente_actual.nombre} {self.paciente_actual.apellido}
• Fecha del Evento: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}
• Estado: {estado}
            """
            
            exito = self.paciente_actual.agregar_nota_historial_medico(
                notas_evento.strip(), 
                estado
            )
            
            if exito:
                return True, f"Evento '{evento}' registrado exitosamente en el historial médico"
            else:
                return False, "Error al registrar el evento en la base de datos"
                
        except Exception as e:
            return False, f"Error al registrar evento: {str(e)}"


    def crear_historial_medico_inicial(self) -> tuple[bool, str]:
        """
        Crea un historial médico inicial para el paciente actual si no tiene uno
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        # Primero probar la conexión a la BD
        conexion_ok, mensaje_conexion = self.probar_conexion_bd()
        if not conexion_ok:
            return False, f"Error de conexión a la base de datos: {mensaje_conexion}"
        
        # Verificar si ya tiene historial médico
        try:
            if self.paciente_actual.tiene_historial_medico():
                return False, f"El paciente {self.paciente_actual.nombre} {self.paciente_actual.apellido} ya tiene historial médico registrado"
        except Exception as e:
            return False, f"Error al verificar historial existente: {str(e)}"
        
        try:
            # Crear historial médico inicial
            notas_inicial = f"""
HISTORIAL MÉDICO INICIAL CREADO:

• Paciente: {self.paciente_actual.nombre} {self.paciente_actual.apellido}
• ID del Paciente: #{self.paciente_actual.id_paciente}
• Edad: {self.paciente_actual.calcular_edad()} años
• DUI: {self.paciente_actual.dui if self.paciente_actual.dui else 'No proporcionado'}
• Fecha de Nacimiento: {self.paciente_actual.fecha_nacimiento.strftime('%d/%m/%Y')}
• Teléfono: {self.formatear_telefono(self.paciente_actual.telefono)}
• Correo: {self.paciente_actual.correo if self.paciente_actual.correo else 'No proporcionado'}

INFORMACIÓN MÉDICA INICIAL:
• Estado de Salud: A evaluar en primera consulta
• Alergias: Por determinar
• Medicamentos Actuales: Por consultar
• Antecedentes Médicos: Por revisar
• Observaciones Iniciales: Historial médico creado para seguimiento

PRÓXIMOS PASOS:
1. Programar primera consulta médica
2. Realizar evaluación inicial completa
3. Registrar antecedentes médicos detallados
4. Establecer plan de tratamiento si es necesario

Historial médico inicial creado el: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}
Sistema: Clínica Dental - Gestión de Pacientes
            """
            
            exito = self.paciente_actual.agregar_nota_historial_medico(
                notas_inicial.strip(), 
                "Activo"
            )
            
            if exito:
                return True, f"Historial médico inicial creado exitosamente para {self.paciente_actual.nombre} {self.paciente_actual.apellido}"
            else:
                return False, "Error al crear el historial médico inicial en la base de datos"
                
        except Exception as e:
            return False, f"Error al crear historial médico inicial: {str(e)}"

    def mostrar(self):
        """Muestra la vista del controlador de pacientes"""
        return self.inicializar_vista()
    
# ==========================================
# QUERYS EJECUNTANDOSE DESDE EL MODELO  
# ==========================================
    def buscar_pacientes_desde_bd(self, nombre, apellido):
        """Busca pacientes directamente en la base de datos"""
        print(f"🧠 Buscando pacientes en BD: nombre='{nombre}', apellido='{apellido}'")
        return Paciente.buscar_pacientes_por_nombre_apellido(nombre, apellido)

    def inicializar_sistema_ids_secuenciales(self):
        """
        Inicializa el sistema asegurando que todos los IDs sean secuenciales
        Debe llamarse al inicio de la aplicación
        """
        print("🔧 Inicializando sistema de IDs secuenciales...")
        
        # Cargar pacientes existentes
        exito, mensaje = self.cargar_todos_los_pacientes_desde_bd()
        
        if exito:
            print(f"✅ {mensaje}")
        else:
            print(f"⚠️ {mensaje}")
            # Si no hay pacientes o hay error, inicializar contador en 1
            Paciente._contador_id = 1
            Paciente._pacientes_existentes = []
            print("🔄 Sistema inicializado sin pacientes existentes")


# ==========================================
# EJECUCIÓN AUTOMÁTICA DEL CONTROLADOR
# PROPÓSITO: Inicializar la aplicación directamente desde el controlador ##tentativo para iniciar la vista
# ==========================================

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from Vistas.PacienteVista import PacienteWindow  # Ajustá si tu estructura de carpetas es diferente

    app = QApplication([])
    ventana = PacienteWindow()
    ventana.show()
    app.exec()



