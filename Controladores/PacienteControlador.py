# Agregar el directorio padre al path
import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ==========================================
# IMPORTACIONES: Clases del modelo y librerías necesarias
# ==========================================

from Modelos.PacienteModelo import *
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
        # Inicializar el contador de IDs de manera robusta
        Paciente.inicializar_contador_desde_pacientes(self.pacientes_registrados)
    
    def set_vista(self, vista):
        """Establece la referencia a la vista"""
        self.vista = vista
    
    def inicializar_vista(self):
        """Inicializa y muestra la vista"""
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
    
    def buscar_paciente_por_id(self, id_paciente: int) -> Paciente:
        """Busca un paciente por su ID único"""
        for paciente in self.pacientes_registrados:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None
    
    def existe_paciente_con_dui(self, dui: str) -> bool:
        """Verifica si ya existe un paciente con el DUI dado (solo si DUI no está vacío)"""
        if not dui or len(dui.replace(" ", "")) == 0:
            return False  # Si no hay DUI, no hay conflicto
        return any(paciente.dui == dui and paciente.dui for paciente in self.pacientes_registrados)
    

    def buscar_pacientes_por_nombre(self, nombre: str) -> List[Paciente]:
        """Busca pacientes que contengan el nombre dado"""
        nombre_lower = nombre.lower()
        return [p for p in self.pacientes_registrados 
                if nombre_lower in p.nombre.lower() or nombre_lower in p.apellido.lower()]
    
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
    
    def buscar_pacientes_con_saldo_pendiente(self) -> List[Paciente]:
        """Obtiene todos los pacientes con saldo pendiente"""
        return [p for p in self.pacientes_registrados if p.tiene_saldo_pendiente()]
    
    def buscar_pacientes_menores_edad(self) -> List[Paciente]:
        """Obtiene todos los pacientes menores de edad"""
        return [p for p in self.pacientes_registrados if p.es_menor_de_edad()]
    
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
            
            # Agregar a la lista de pacientes registrados
            self.pacientes_registrados.append(nuevo_paciente)
            self.paciente_actual = nuevo_paciente
            
            # Actualizar el contador basado en todos los pacientes existentes (redundancia por seguridad)
            Paciente.inicializar_contador_desde_pacientes(self.pacientes_registrados)
            
            # Actualizar la vista automáticamente
            self.actualizar_vista()
            
            return True, f"Paciente #{nuevo_paciente.id_paciente}: {nombre} {apellido} creado exitosamente"
            
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
        """Agrega un tratamiento al paciente actual con validaciones"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not tratamiento:
            return False, "El tratamiento no puede estar vacío"
        
        try:
            self.paciente_actual.agregar_tratamiento(tratamiento)
            return True, f"Tratamiento agregado exitosamente a {self.paciente_actual.nombre}"
        except Exception as e:
            return False, f"Error al agregar tratamiento: {str(e)}"
    
    def agregar_cita_a_paciente(self, cita: Cita) -> tuple[bool, str]:
        """Agrega una cita al paciente actual con validaciones"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        if not cita:
            return False, "La cita no puede estar vacía"
        
        # Validar que no haya conflicto de horarios
        if self._tiene_conflicto_horario(cita):
            return False, "El paciente ya tiene una cita en ese horario"
        
        try:
            self.paciente_actual.agregar_cita(cita)
            return True, f"Cita agregada exitosamente a {self.paciente_actual.nombre}"
        except Exception as e:
            return False, f"Error al agregar cita: {str(e)}"
    
    def _tiene_conflicto_horario(self, nueva_cita) -> bool:
        """Verifica si la nueva cita tiene conflicto con citas existentes"""
        if not self.paciente_actual:
            return False
        
        for cita_existente in self.paciente_actual.citas:
            # Verificar solapamiento de horarios
            if (nueva_cita.hora_inicio < cita_existente.hora_fin and 
                nueva_cita.hora_fin > cita_existente.hora_inicio):
                return True
        return False
    
    def cancelar_cita(self, id_cita: str) -> tuple[bool, str]:
        """Cancela una cita específica"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        cita = self.paciente_actual.obtener_cita_por_id(id_cita)
        if not cita:
            return False, "Cita no encontrada"
        
        # Regla de negocio: No cancelar citas que ya comenzaron
        if cita.hora_inicio <= datetime.now():
            return False, "No se puede cancelar una cita que ya comenzó"
        
        cita.estado = "Cancelada"
        return True, "Cita cancelada exitosamente"
    
    def finalizar_tratamiento(self, id_tratamiento: str) -> tuple[bool, str]:
        """Finaliza un tratamiento específico"""
        if not self.paciente_actual:
            return False, "No hay paciente seleccionado"
        
        tratamiento = self.paciente_actual.obtener_tratamiento_por_id(id_tratamiento)
        if not tratamiento:
            return False, "Tratamiento no encontrado"
        
        tratamiento.estado = "Completado"
        return True, "Tratamiento finalizado exitosamente"
    
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
    
# ==========================================
# QUERYS EJECUNTANDOSE DESDE EL MODELO  
# ==========================================

# ==========================================
# EJECUCIÓN AUTOMÁTICA DEL CONTROLADOR
# PROPÓSITO: Inicializar la aplicación directamente desde el controlador ##tentativo para iniciar la vista
# ==========================================

def ejecutar_aplicacion_pacientes():
    """Función para ejecutar la aplicación de gestión de pacientes"""
    from PyQt6.QtWidgets import QApplication
    import sys
    
    # Crear la aplicación Qt si no existe
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Crear el controlador
    controlador = PacienteControlador()
    
    # Inicializar la vista desde el controlador
    vista = controlador.inicializar_vista()
    
    # Mensaje de bienvenida
    controlador.mostrar_mensaje_en_vista(
        "Sistema de Gestión de Pacientes", 
        "¡Bienvenido al sistema de gestión de pacientes!\n\nPuede comenzar creando un nuevo paciente o buscando pacientes existentes.", 
        "info"
    )
    
    # Ejecutar la aplicación
    try:
        if app:
            app.exec()
    except SystemExit:
        pass
    
    return controlador, vista

# Si este archivo se ejecuta directamente, iniciar la aplicación
if __name__ == "__main__":
    ejecutar_aplicacion_pacientes()



