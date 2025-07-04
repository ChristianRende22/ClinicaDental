# Importaciones necesarias para no tener porblema con los path o importaciones de clase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from typing import List

from Modelos.PacienteModelo import Paciente
from Modelos.DoctorModelo import Doctor
from Modelos.CitaModelo import Cita

from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtCore import QDateTime


class ControladorCita:    
    def __init__(self, vista):
        self.vista = vista
        self.citas: List[Cita] = []  # Lista para almacenar las citas creadas
        self.editando_cita = None
        
        # MOVER LOS DATOS AQUÍ
        self.doctores = [
            Doctor("Melisa", "Rivas", "12345678-9", "Cirujano Dentista", 12345678, "correo@gmail.com"), 
            Doctor("Carlos", "López", "98765432-1", "Ortodontista", 87654321, "coreo1@gmail.com")
        ]
        
        self.pacientes = [
            Paciente("Juan", "Pérez", "06-12-05", "12345678-9", 12345567, "correo@gmail.com"), 
            Paciente("Ana", "Gomex", "07-31-07", "12345678-0", 12345678, "correo1@gmail.com")
        ]
        
        self.tratamientos = [
            {'descripcion': 'Limpieza', 'costo': 20.0}
        ]
        
        # Inicializar la vista con los datos
        self.inicializar_vista()

    def inicializar_vista(self):
        """Inicializa la vista con los datos del controlador"""
        self.vista.actualizar_combos(self.doctores, self.pacientes, self.tratamientos)

    def crear_cita(self):
        """Crea una nueva cita verificando disponibilidad de la Cita"""
        self.vista.resultado_text.clear()
        id_cita = self.vista.id_edit.text().strip()
        paciente_idx = self.vista.paciente_combo.currentIndex()
        doctor_idx = self.vista.doctor_combo.currentIndex()
        tratamiento_idx = self.vista.tratamiento_combo.currentIndex()
        hora_inicio = self.vista.fecha_inicio_edit.dateTime().toPyDateTime()
        hora_fin = self.vista.fecha_fin_edit.dateTime().toPyDateTime()
        costo = self.vista.costo_edit.text().strip()
        estado = self.vista.estado_combo.currentText()

        # Verificar disponibilidad del doctor
        doctor = self.doctores[doctor_idx]

        # Esta funcion se implmenetara cuando este lista la clase y controlador de horario
        # for cita in self.citas:
        #     """ Verifica si el doctor está disponible en el horario de la cita """
        #     if cita.doctor == doctor and not (hora_fin <= cita.hora_inicio or hora_inicio >= cita.hora_fin):
        #         QMessageBox.warning(self.vista, "❌ Error", "El doctor no está disponible en ese horario.")
        #         return

        # Validar costo (por si acaso)
        try:
            costo_float = float(costo)
            if costo_float <= 0:
                QMessageBox.warning(self.vista, "❌ Error", "El costo debe ser mayor que 0.")
                return
        except ValueError:
            QMessageBox.warning(self.vista, "❌ Error", "El costo debe ser un número válido.")
            return


        # Valida que no se repita el id de cita
        for cita in self.citas:
            if cita.id_cita == id_cita:
                QMessageBox.warning(self.vista, "❌ Error", "Ya existe una cita con ese ID.")
                return

        # Usar datos del controlador, no de la vista
        paciente = self.pacientes[paciente_idx]
        doctor = self.doctores[doctor_idx]
        tratamiento = self.tratamientos[tratamiento_idx]
        nueva_cita = Cita(id_cita, paciente, doctor, hora_inicio, hora_fin, float(costo))
        nueva_cita.tratamiento = tratamiento
        nueva_cita.estado = estado

        self.citas.append(nueva_cita)
        self.vista.resultado_text.append(f"Cita creada:\n{nueva_cita}")
        QMessageBox.information(self.vista, "✅ Éxito", "Cita creada exitosamente.")
        self.limpiar_campos()

    def listar_citas(self):
        """Lista todas las citas creadas"""
        self.vista.resultado_text.clear()
        if not self.citas:
            self.vista.resultado_text.append("No hay citas registradas...")
            return
        
        self.vista.resultado_text.append("📃Citas registradas:")
        for cita in self.citas:
            self.vista.resultado_text.append(str(cita))

    def cancelar_cita(self):
        """Cancela una cita por ID"""
        self.vista.resultado_text.clear()
        self.listar_citas()
        id_cita, ok = QInputDialog.getText(self.vista, "Cancelar Cita", "Ingrese el ID de la cita a cancelar:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                cita.estado = "Cancelada"
                self.vista.resultado_text.append(f"Cita cancelada:\n{cita}")
                QMessageBox.information(self.vista, "✅ Éxito", "Cita cancelada exitosamente.")
                return
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")

    def modificar_cita(self):
        """
        Si no estamos editando, pide el ID de la cita, la busca y permite editar sus datos (excepto el ID).
        Si ya estamos editando, guarda los cambios realizados.
        """
        self.vista.resultado_text.clear()

        if not self.citas:
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        # Si ya estamos editando, guardar los cambios
        if self.editando_cita is not None:
            try:
                # Obtener nuevos datos del formulario
                paciente_idx = self.vista.paciente_combo.currentIndex()
                doctor_idx = self.vista.doctor_combo.currentIndex()
                tratamiento_idx = self.vista.tratamiento_combo.currentIndex()
                hora_inicio = self.vista.fecha_inicio_edit.dateTime().toPyDateTime()
                hora_fin = self.vista.fecha_fin_edit.dateTime().toPyDateTime()
                costo = self.vista.costo_edit.text().strip()
                estado = self.vista.estado_combo.currentText()
                
                # Validaciones
                if paciente_idx == -1 or doctor_idx == -1 or tratamiento_idx == -1 or not costo:
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios.")
                    return
                
                try:
                    costo_float = float(costo)
                except ValueError:
                    QMessageBox.warning(self.vista, "❌ Error", "El costo debe ser un número válido.")
                    return
                
                if hora_inicio >= hora_fin:
                    QMessageBox.warning(self.vista, "❌ Error", "La hora de fin debe ser posterior a la hora de inicio.")
                    return
                
                # Actualizar la cita existente
                cita = self.editando_cita
                cita.paciente = self.pacientes[paciente_idx]
                cita.doctor = self.doctores[doctor_idx]
                cita.tratamiento = self.tratamientos[tratamiento_idx]
                cita.hora_inicio = hora_inicio
                cita.hora_fin = hora_fin
                cita.costo_cita = costo_float
                cita.estado = estado
                
                QMessageBox.information(self.vista, "✅ Éxito", "Cita modificada correctamente.")
                self.vista.resultado_text.append(
                    f"Cita modificada:\n"
                    f"ID: {cita.id_cita}\n"
                    f"Paciente: {cita.paciente.nombre} {cita.paciente.apellido}\n"
                    f"Doctor: {cita.doctor.nombre} {cita.doctor.apellido}\n"
                    f"Fecha inicio: {cita.hora_inicio.strftime('%d/%m/%Y %H:%M')}\n"
                    f"Fecha fin: {cita.hora_fin.strftime('%d/%m/%Y %H:%M')}\n"
                    f"Costo: ${cita.costo_cita:.2f}\n"
                    f"Estado: {cita.estado}\n"
                )
                
                # Rehabilitar el campo ID y salir del modo edición
                self.vista.id_edit.setReadOnly(False)
                self.editando_cita = None
                self.limpiar_campos()
                return
                
            except Exception as e:
                QMessageBox.critical(self.vista, "❌ Error", f"Error al modificar la cita: {str(e)}")
                return

        # Si NO estamos editando, mostrar lista de citas y pedir ID
        self.listar_citas()  # Mostrar citas disponibles
        
        id_cita, ok = QInputDialog.getText(self.vista, "Modificar Cita", "Ingrese el ID de la cita a modificar:")
        if not ok or not id_cita.strip():
            return
        
        # Buscar la cita
        cita_encontrada = None
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                cita_encontrada = cita
                break
        
        if not cita_encontrada:
            QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")
            return
        
        # Cargar datos actuales en la vista
        self.vista.id_edit.setText(cita_encontrada.id_cita)
        self.vista.id_edit.setReadOnly(True)  # No permitir editar el ID
        
        # Establecer valores en los combos
        for i, paciente in enumerate(self.pacientes):
            if paciente.dui == cita_encontrada.paciente.dui:
                self.vista.paciente_combo.setCurrentIndex(i)
                break
        
        for i, doctor in enumerate(self.doctores):
            if doctor.dui == cita_encontrada.doctor.dui:
                self.vista.doctor_combo.setCurrentIndex(i)
                break
        
        if hasattr(cita_encontrada, 'tratamiento'):
            for i, tratamiento in enumerate(self.tratamientos):
                if tratamiento == cita_encontrada.tratamiento:
                    self.vista.tratamiento_combo.setCurrentIndex(i)
                    break
        
        # Establecer fechas y otros campos
        self.vista.fecha_inicio_edit.setDateTime(QDateTime(cita_encontrada.hora_inicio))
        self.vista.fecha_fin_edit.setDateTime(QDateTime(cita_encontrada.hora_fin))
        self.vista.costo_edit.setText(str(cita_encontrada.costo_cita))
        self.vista.estado_combo.setCurrentText(cita_encontrada.estado)
        
        # Guardar referencia para editar después
        self.editando_cita = cita_encontrada
        
        QMessageBox.information(self.vista, "Editar Cita", 
            f"Cita {cita_encontrada.id_cita} cargada para edición.\n\n"
            "Modifique los campos que desee y presione nuevamente 'Modificar Cita' para guardar los cambios.")

    def confirmar_asistencia(self):
        """Confirma si se asistió a la cita"""
        self.vista.resultado_text.clear()
        self.listar_citas()

        id_cita, ok = QInputDialog.getText(self.vista, "Confirmar Asistencia", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                cita.estado = "Confirmada"
                self.vista.resultado_text.append(f"Asistencia confirmada:\n{cita}")
                QMessageBox.information(self.vista, "✅ Éxito", "Asistencia confirmada.")
                return
            
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")

    def calcular_monto(self):
        """Calcula el monto a pagar según el tipo de consulta y tratamiento"""
        self.vista.resultado_text.clear()
        self.listar_citas()  

        id_cita, ok = QInputDialog.getText(self.vista, "Calcular Monto", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        
        for cita in self.citas:
            if cita.id_cita == id_cita.strip():
                costo_cita = cita.costo_cita
                costo_tratamiento = getattr(cita, 'tratamiento', {}).get('costo', 0)
                total = costo_cita + costo_tratamiento
                self.vista.resultado_text.append(
                    f"Monto a pagar para la cita {cita.id_cita}:\n"
                    f"Consulta: ${costo_cita:.2f}\n"
                    f"Tratamiento: ${costo_tratamiento:.2f}\n"
                    f"Total: ${total:.2f}\n"
                )
                QMessageBox.information(self.vista, "Monto a Pagar", f"Total a pagar: ${total:.2f}")
                return
        
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")

    def limpiar_campos(self):
        self.vista.id_edit.clear()
        self.vista.id_edit.setReadOnly(False)  # Rehabilitar el campo ID
        self.vista.fecha_inicio_edit.setDateTime(QDateTime.currentDateTime())
        self.vista.fecha_fin_edit.setDateTime(QDateTime.currentDateTime())
        self.vista.costo_edit.clear()
        self.vista.estado_combo.setCurrentIndex(0)
        self.vista.paciente_combo.setCurrentIndex(0)
        self.vista.doctor_combo.setCurrentIndex(0)
        self.vista.tratamiento_combo.setCurrentIndex(0)
        self.editando_cita = None  # Resetear el modo edición

