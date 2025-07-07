# Importaciones necesarias para no tener porblema con los path o importaciones de clase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QDialog, QMessageBox, QInputDialog, QComboBox, QTimeEdit, QVBoxLayout, QFormLayout, QDialogButtonBox

from PyQt6.QtCore import QTime

from datetime import datetime
from typing import List
import re

from datetime import datetime

from Modelos.DoctorModelo import Doctor
from Vistas.HorarioVista import AgregarHorarioDialog


class ControladorDoctor:
    def __init__(self, vista):
        self.vista = vista
        self.doctores: List[Doctor] = []    
        self.editando_doctor = None  # Variable que ocuparemos para actulizar campos de la informacion del doctor

    # ====================================
    # ========== VALIDACIONES ============
    # ====================================

    def validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_dui(self, dui: str) -> bool:
        """Valida el formato del DUI (########-#)"""
        patron = r'^\d{8}-\d{1}$'
        return re.match(patron, dui) is not None
    
    def validar_telefono(self, telefono: str) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return telefono.isdigit() and len(telefono) >= 8
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.vista.nombre_edit.clear()
        self.vista.apellido_edit.clear()
        self.vista.dui_edit.clear()
        self.vista.telefono_edit.clear()
        self.vista.correo_edit.clear()
        self.vista.especialidad_edit.clear()
        
        # Enfocar el primer campo para facilitar la entrada
        self.vista.nombre_edit.setFocus()
    
    def crear_doctor(self):
        """Crea un nuevo paciente con los datos ingresados"""
        try:
            self.vista.resultado_text.clear()  # Limpia el área de resultados antes de mostrar nuevos datos

            nombre = self.vista.nombre_edit.text().strip().title()
            apellido = self.vista.apellido_edit.text().strip().title()
            especialidad = self.vista.especialidad_edit.text().strip().title()
            dui = self.vista.dui_edit.text().strip()
            telefono_str = self.vista.telefono_edit.text().strip()
            correo = self.vista.correo_edit.text().strip().lower()
            
            # Validaciones básicas
            if not all([nombre, apellido, dui, especialidad]):
                QMessageBox.warning(self.vista, "❌ Error", "Nombre, Apellido, DUI y Especialidad son campos obligatorios")
                return
            
            # Validación DUI
            if not self.validar_dui(dui):
                QMessageBox.warning(self.vista, "❌ Error de Formato", 
                                  "El DUI debe tener el formato: 12345678-9")
                return
            
            # Verificar si ya existe un paciente con el mismo DUI
            for doctor in self.doctores:
                if doctor['dui'] == dui:
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      f"Ya existe un doctor registrado con el DUI: {dui}")
                    return
            
            # Validación teléfono
            if telefono_str and not self.validar_telefono(telefono_str):
                QMessageBox.warning(self.vista, "❌ Error de Formato", 
                                  "El teléfono debe contener al menos 8 dígitos")
                return
            
            telefono = int(telefono_str) if telefono_str else 0
            
            # Validación email
            if correo and not self.validar_email(correo):
                QMessageBox.warning(self.vista, "❌ Error de Formato", 
                                  "El email no tiene un formato válido")
                return
               
            # Crear datos del nuevo paciente
            nuevo_doctor = {
                'nombre': nombre,
                'apellido': apellido,
                'dui': dui,
                'especialidad': especialidad,
                'telefono': telefono,
                'correo': correo,
                'citas': [],
                'fecha_registro': datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            }
            
            # Agregar a la lista de pacientes registrados
            self.doctores.append(nuevo_doctor)
            
            # Establecer como paciente actual
            self.nombre = nombre
            self.apellido = apellido
            self.especialidad = especialidad
            self.dui = dui
            self.telefono = telefono
            self.correo = correo
            self.citas = []
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self.vista, "✅ Éxito", 
                                  f"Doctor {nombre} {apellido} creado exitosamente.\n\n"
                                  f"Total de pacientes registrados: {len(self.doctores)}")
            
            # Mostrar información del paciente creado
            self.vista.resultado_text.append(f"Doctor creado: {nombre} {apellido}\n"
                                       f"DUI: {dui}\n"
                                       f"Especialidad: {especialidad}\n"
                                       f"Teléfono: {telefono}\n"
                                       f"Correo: {correo}\n"
                                       f"Fecha de registro: {nuevo_doctor['fecha_registro']}\n")
            
            # Limpiar campos automáticamente para el siguiente paciente
            self.limpiar_campos()
            
        except ValueError as e:
            QMessageBox.warning(self.vista, "❌ Error", f"Error en el formato de los datos: {str(e)}")
    
    def agregar_horario(self):
        """Abre el diálogo de HorarioVista para agregar un horario"""
        try:
            # Verificar que hay doctores registrados
            if not self.doctores:
                QMessageBox.information(self.vista, "ℹ️ Información", 
                                      "Debe registrar al menos un doctor antes de agregar horarios.")
                return
            
            # Convertir la lista de doctores a objetos Doctor para el diálogo
            doctores_objetos = []
            for doctor_dict in self.doctores:
                doctor_obj = Doctor(
                    nombre=doctor_dict['nombre'],
                    apellido=doctor_dict['apellido'],
                    dui=doctor_dict['dui'],
                    especialidad=doctor_dict['especialidad'],
                    telefono=doctor_dict['telefono'],
                    correo=doctor_dict['correo']
                )
                doctores_objetos.append(doctor_obj)
            
            # Crear y mostrar el diálogo de horario
            dialog = AgregarHorarioDialog(doctores_objetos, self.vista)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                # Validar que todos los campos están completos
                if not all([data['id_horario'], data['dia'], data['hora_inicio'], data['hora_fin'], data['doctor']]):
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios")
                    return
                
                # Mostrar el resultado en el área de texto
                self.vista.resultado_text.append(f"""
🕒 Horario agregado exitosamente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ID Horario: {data['id_horario']}
📅 Día: {data['dia']}
⏰ Hora Inicio: {data['hora_inicio']}
⏳ Hora Fin: {data['hora_fin']}
👨‍⚕️ Doctor: Dr. {data['doctor'].nombre} {data['doctor'].apellido}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
                
                QMessageBox.information(self.vista, "✅ Éxito", 
                                      f"Horario agregado exitosamente para Dr. {data['doctor'].nombre} {data['doctor'].apellido}")
            
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", 
                               f"Error al abrir el diálogo de horarios: {str(e)}")
            print(f"Error detallado: {e}")  # Para debugging

    def mostrar_info_doctor(self):
        """ Muestra un diálogo con la información de todos los doctores registrados """
        self.vista.resultado_text.clear()  # Limpia el área de resultados antes de mostrar nuevos datos

        if not self.doctores:
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
            return
    
        for doctor in self.doctores:
            self.vista.resultado_text.append(f"""- DUI: {doctor['dui']}
Dr. {doctor['nombre']} {doctor['apellido']}
Especialidad: {doctor['especialidad']}
Teléfono: {doctor['telefono']}
Correo: {doctor['correo']}\n""")
            
    def suprimir_doctor(self):
        """
        Permite eliminar un doctor registrado por su DUI.
        Si no se encuentra el doctor, muestra un mensaje de error.
        """
        self.vista.resultado_text.clear()

        if not self.doctores:
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
            return

        dui_a_eliminar, ok = QInputDialog.getText(self.vista, "Eliminar Doctor", "Ingrese el DUI del doctor a eliminar:")
        if not ok or not dui_a_eliminar.strip():
            return

        dui_a_eliminar = dui_a_eliminar.strip()
        for doctor in self.doctores:
            if doctor['dui'] == dui_a_eliminar:
                self.doctores.remove(doctor)
                QMessageBox.information(self.vista, "✅ Éxito", f"Doctor con DUI {dui_a_eliminar} eliminado correctamente.")
                self.vista.resultado_text.append(f"Doctor eliminado: {doctor['nombre']} {doctor['apellido']} (DUI: {dui_a_eliminar})\n")
                return

        QMessageBox.warning(self.vista, "❌ Error", f"No se encontró ningún doctor con el DUI: {dui_a_eliminar}")
            

    def actualizar_info_doctor(self):
        """
        Si no estamos editando, pide el DUI, busca el doctor y permite editar sus datos (excepto el DUI).
        Si ya estamos editando, guarda los cambios realizados.
        """
        self.vista.resultado_text.clear()

        if not self.doctores:
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
            return

        # Si ya estamos editando, guardar los cambios
        if self.editando_doctor is not None:
            doctor = self.editando_doctor
            doctor['nombre'] = self.vista.nombre_edit.text().strip().title()
            doctor['apellido'] = self.vista.apellido_edit.text().strip().title()
            doctor['especialidad'] = self.vista.especialidad_edit.text().strip().title()
            doctor['telefono'] = int(self.vista.telefono_edit.text().strip()) if self.vista.telefono_edit.text().strip().isdigit() else 0
            doctor['correo'] = self.vista.correo_edit.text().strip().lower()

            QMessageBox.information(self.vista, "✅ Éxito", "Información del doctor actualizada correctamente.")
            self.vista.resultado_text.append(
                f"Doctor actualizado:\n"
                f"DUI: {doctor['dui']}\n"
                f"Nombre: {doctor['nombre']}\n"
                f"Apellido: {doctor['apellido']}\n"
                f"Especialidad: {doctor['especialidad']}\n"
                f"Teléfono: {doctor['telefono']}\n"
                f"Correo: {doctor['correo']}\n"
            )
            self.vista.dui_edit.setReadOnly(False)
            self.editando_doctor = None  # Salimos del modo edición
            self.limpiar_campos()
            return

        # Si NO estamos editando, pedir DUI y cargar datos
        dui_a_buscar, ok = QInputDialog.getText(self.vista, "Buscar Doctor", "Ingrese el DUI del doctor a modificar:")
        if not ok or not dui_a_buscar.strip():
            return

        dui_a_buscar = dui_a_buscar.strip()
        for doctor in self.doctores:
            if doctor['dui'] == dui_a_buscar:
                # Llenar los campos con los datos encontrados
                self.vista.dui_edit.setText(doctor['dui'])
                self.vista.nombre_edit.setText(doctor['nombre'])
                self.vista.apellido_edit.setText(doctor['apellido'])
                self.vista.especialidad_edit.setText(doctor['especialidad'])
                self.vista.telefono_edit.setText(str(doctor['telefono']))
                self.vista.correo_edit.setText(doctor['correo'])
                self.vista.dui_edit.setReadOnly(True)  # No permitir editar el DUI

                self.editando_doctor = doctor  # Guardamos referencia para editar después

                QMessageBox.information(self.vista, "Editar Doctor", 
                    "Modifique los campos que desee y presione nuevamente 'Actualizar Info Doctor' para guardar los cambios.")
                return

        QMessageBox.warning(self.vista, "❌ Error", f"No se encontró ningún doctor con el DUI: {dui_a_buscar}")

    # Por el momento, no encontrara ninguna cita para el doctor, una vez se haya hecho la conexion con la base de datos será más fácil
    def ver_citas(self):
        self.vista.resultado_text.clear()
        # Pide el DUI del doctor a consultar
        dui, ok = QInputDialog.getText(self.vista, "Ver Citas", "Ingrese el DUI del doctor:")
        if not ok or not dui.strip():
            return
        for doctor in self.doctores:
            if doctor['dui'] == dui.strip():
                if not doctor.get('citas'):
                    self.vista.resultado_text.append("No hay citas registradas para este doctor.")
                    return
                self.vista.resultado_text.append(f"Citas del Dr. {doctor['nombre']} {doctor['apellido']}:")
                for cita in doctor['citas']:
                    self.vista.resultado_text.append(str(cita))
                return
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró el doctor con ese DUI.")

    # Este metodo sera para que el doctor pueda registrar un diagnostico a un paciente, sin embargo se implementara mas adelante.
    # Especialmente, cuando se haga la conexion con la base de datos
    # def registrar_diagnostico(self):
