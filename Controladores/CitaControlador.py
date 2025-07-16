# Importaciones necesarias para no tener porblema con los path o importaciones de clase
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date
from typing import List

from Modelos.PacienteModelo import Paciente
from Modelos.DoctorModelo import Doctor
from Modelos.CitaModelo import Cita
from Vistas.FacturaVista import FacturacionView
from Controladores.FacturaControlador import FacturacionController
from Modelos.TratamientoModelo import Tratamiento

from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtCore import QDateTime, QDate


class ControladorCita:    
    def __init__(self):
        self.vista = None  # Vista asociada al controlador
        self.citas_agendadas: List[Cita] = []  # Lista para almacenar las citas creadas
        self.cita: Cita = None  # Cita actual que se está editando o creando
        self.doctores: List[Doctor] = []  # Lista de doctores disponibles
        self.pacientes: List[Paciente] = []  # Lista de pacientes disponibles
        self.tratamientos: List[Tratamiento] = []  # Lista de tratamientos disponibles
        self.editando_cita = None
        
        # Cargar datos desde la base de datos
        self.cargar_datos_desde_bd()

    def cargar_datos_desde_bd(self):
        """Carga todos los datos necesarios desde la base de datos"""
        try:
            # Cargar pacientes
            self.pacientes = Paciente.obtener_todos_pacientes()
            print(f"Pacientes cargados: {len(self.pacientes)}")
            
            # Cargar doctores
            self.doctores = Doctor.obtener_todos_doctores()
            print(f"Doctores cargados: {len(self.doctores)}")
            
            # Cargar tratamientos
            self.tratamientos = Tratamiento.obtener_todos_tratamientos()
            print(f"Tratamientos cargados: {len(self.tratamientos)}")
            
        except Exception as e:
            print(f"Error al cargar datos desde BD: {e}")
            # En caso de error, usar listas vacías
            self.pacientes = []
            self.doctores = []
            self.tratamientos = []

    def set_vista(self, vista):
        """Establece la vista asociada al controlador"""
        self.vista = vista

    def inicializar_vista(self):
        """Inicializa la vista con los datos del controlador"""
        if not self.vista:
            from Vistas.CitaVista import CitaWindow
            self.vista = CitaWindow(self)

        # Actualizar combos con datos de la BD
        self.actualizar_vista()
        self.vista.show()
        return self.vista

    def cerrar_vista(self):
        """Cierra la vista actual"""
        if self.vista:
            self.vista.close()
            self.vista = None

    def actualizar_vista(self):
        """Actualiza la vista con los datos actuales del controlador"""
        if self.vista:
            self.vista.actualizar_combos(self.doctores, self.pacientes, self.tratamientos)
            self.vista.resultado_text.clear()

    def crear_cita(self):
        """Crea una nueva cita con los datos ingresados en la vista"""
        self.vista.resultado_text.clear()
        
        try:
            # Obtener datos del formulario
            paciente_idx = self.vista.paciente_combo.currentIndex()
            doctor_idx = self.vista.doctor_combo.currentIndex()
            tratamiento_idx = self.vista.tratamiento_combo.currentIndex()
            fecha = self.vista.fecha_edit.date().toPyDate()
            hora_inicio_dt = self.vista.inicio_edit.dateTime().toPyDateTime()
            hora_fin_dt = self.vista.fin_edit.dateTime().toPyDateTime()
            hora_inicio = hora_inicio_dt.time()
            hora_fin = hora_fin_dt.time()
            costo = self.vista.costo_edit.text().strip()
            estado = self.vista.estado_combo.currentText()
            
            # Validaciones básicas (recordar que índice 0 es "-- Seleccionar --")
            if paciente_idx <= 0:
                QMessageBox.warning(self.vista, "❌ Error", "Debe seleccionar un paciente.")
                return
            
            if doctor_idx <= 0:
                QMessageBox.warning(self.vista, "❌ Error", "Debe seleccionar un doctor.")
                return
            
            if not costo:
                QMessageBox.warning(self.vista, "❌ Error", "Debe ingresar el costo de la cita.")
                return
            
            # Validar fecha
            fecha_actual = date.today()
            if fecha < fecha_actual:
                QMessageBox.warning(self.vista, "❌ Error", 
                                "No se pueden crear citas en fechas pasadas.\n"
                                "Por favor seleccione una fecha actual o futura.")
                return
            
            # Si es hoy, verificar que la hora no haya pasado
            if fecha == fecha_actual:
                hora_actual = datetime.now().time()
                if hora_inicio <= hora_actual:
                    QMessageBox.warning(self.vista, "❌ Error", 
                                    f"No se pueden crear citas en horarios pasados.\n"
                                    f"Hora actual: {hora_actual.strftime('%H:%M')}\n"
                                    f"Por favor seleccione una hora futura.")
                    return
            
            # Validar costo
            try:
                costo_float = float(costo)
                if costo_float < 0:
                    QMessageBox.warning(self.vista, "❌ Error", "El costo no puede ser negativo.")
                    return
            except ValueError:
                QMessageBox.warning(self.vista, "❌ Error", "El costo debe ser un número válido.")
                return
            
            # Validar horarios
            if hora_inicio >= hora_fin:
                QMessageBox.warning(self.vista, "❌ Error", "La hora de fin debe ser posterior a la hora de inicio.")
                return
            
            # Obtener objetos seleccionados (restar 1 porque índice 0 es texto placeholder)
            paciente_seleccionado = self.pacientes[paciente_idx - 1]
            doctor_seleccionado = self.doctores[doctor_idx - 1]
            
            # Tratamiento es opcional
            tratamiento_seleccionado = None
            if tratamiento_idx > 0:
                tratamiento_seleccionado = self.tratamientos[tratamiento_idx - 1]
            
            # Crear la instancia de Cita
            nueva_cita = Cita(
                paciente=paciente_seleccionado,
                doctor=doctor_seleccionado,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                costo_cita=costo_float
            )
            
            # Asignar tratamiento si se seleccionó
            if tratamiento_seleccionado:
                nueva_cita.tratamiento = tratamiento_seleccionado
            
            # Insertar en la base de datos
            if Cita.insert_Cita_bd(nueva_cita):
                # Si la inserción fue exitosa, agregar a la lista local
                self.citas_agendadas.append(nueva_cita)  # CORREGIDO: usar citas_agendadas
                
                QMessageBox.information(self.vista, "✅ Éxito", 
                                    f"Cita creada correctamente.\nID: {nueva_cita.id_cita}")
                
                # Mostrar los detalles de la cita creada
                self.vista.resultado_text.append(
                    f"Cita creada exitosamente:\n"
                    f"ID: {nueva_cita.id_cita}\n"
                    f"Paciente: {nueva_cita.paciente.nombre} {nueva_cita.paciente.apellido}\n"
                    f"Doctor: {nueva_cita.doctor.nombre} {nueva_cita.doctor.apellido}\n"
                    f"Fecha: {nueva_cita.fecha.strftime('%d/%m/%Y')}\n"
                    f"Hora inicio: {nueva_cita.hora_inicio.strftime('%H:%M')}\n"
                    f"Hora fin: {nueva_cita.hora_fin.strftime('%H:%M')}\n"
                    f"Costo: ${nueva_cita.costo_cita:.2f}\n"
                    f"Estado: {nueva_cita.estado}\n"
                )
                
                # Limpiar el formulario
                self.limpiar_campos()
                
            else:
                QMessageBox.critical(self.vista, "❌ Error", 
                                "Error al guardar la cita en la base de datos.")
                
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", 
                            f"Error inesperado al crear la cita: {str(e)}")

    def listar_citas(self):
        """Lista todas las citas creadas"""
        self.vista.resultado_text.clear()
        if not self.citas_agendadas:  # CORREGIDO
            self.vista.resultado_text.append("No hay citas registradas...")
            return
        
        for cita in self.citas_agendadas:  # CORREGIDO
            self.vista.resultado_text.append(f"{cita}\n" + "-"*50 + "\n")

    def cancelar_cita(self):
        """Cancela una cita por ID"""
        self.vista.resultado_text.clear()
        self.listar_citas()
        id_cita, ok = QInputDialog.getText(self.vista, "Cancelar Cita", "Ingrese el ID de la cita a cancelar:")
        if not ok or not id_cita.strip():
            return
        for cita in self.citas_agendadas:  # CORREGIDO
            if str(cita.id_cita) == id_cita.strip():  # CORREGIDO: convertir a string
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

        if not self.citas_agendadas:  # CORREGIDO
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        # Si ya estamos editando, guardar los cambios
        if self.editando_cita is not None:
            try:
                # Obtener nuevos datos del formulario
                paciente_idx = self.vista.paciente_combo.currentIndex()
                doctor_idx = self.vista.doctor_combo.currentIndex()
                tratamiento_idx = self.vista.tratamiento_combo.currentIndex()
                fecha = self.vista.fecha_edit.date().toPyDate()
                hora_inicio_dt = self.vista.inicio_edit.dateTime().toPyDateTime()
                hora_fin_dt = self.vista.fin_edit.dateTime().toPyDateTime()
                hora_inicio = hora_inicio_dt.time()
                hora_fin = hora_fin_dt.time()
                costo = self.vista.costo_edit.text().strip()
                estado = self.vista.estado_combo.currentText()
                
                # Validaciones
                if paciente_idx == -1 or doctor_idx == -1 or tratamiento_idx == -1 or not costo:
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios.")
                    return
                
                # Verificar que la fecha no sea pasada
                fecha_actual = date.today()
                if fecha < fecha_actual:
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      "No se pueden modificar citas a fechas pasadas.\n"
                                      "Por favor seleccione una fecha actual o futura.")
                    return

                # Si es hoy, verificar que la hora no haya pasado
                if fecha == fecha_actual:
                    hora_actual = datetime.now().time()
                    if hora_inicio <= hora_actual:
                        QMessageBox.warning(self.vista, "❌ Error", 
                                          f"No se pueden modificar citas a horarios pasados.\n"
                                          f"Hora actual: {hora_actual.strftime('%H:%M')}\n"
                                          f"Por favor seleccione una hora futura.")
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
                cita.fecha = fecha
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
                    f"Fecha: {cita.fecha.strftime('%d/%m/%Y')}\n"
                    f"Hora inicio: {cita.hora_inicio.strftime('%H:%M')}\n"
                    f"Hora fin: {cita.hora_fin.strftime('%H:%M')}\n"
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
        for cita in self.citas_agendadas:  # CORREGIDO
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
            if doctor.num_junta_medica == cita_encontrada.doctor.num_junta_medica:
                self.vista.doctor_combo.setCurrentIndex(i)
                break
        
        if hasattr(cita_encontrada, 'tratamiento'):
            for i, tratamiento in enumerate(self.tratamientos):
                if tratamiento == cita_encontrada.tratamiento:
                    self.vista.tratamiento_combo.setCurrentIndex(i)
                    break
        
        # Establecer fechas y otros campos
        if hasattr(cita_encontrada, 'fecha'):
            if hasattr(cita_encontrada.fecha, 'year'):
                qdate = QDate(cita_encontrada.fecha.year, cita_encontrada.fecha.month, cita_encontrada.fecha.day)
                self.vista.fecha_edit.setDate(qdate)
            else:
                self.vista.fecha_edit.setDate(QDate.currentDate())

        from datetime import datetime, time
        if isinstance(cita_encontrada.hora_inicio, time):
            dt_inicio = datetime.combine(datetime.today().date(), cita_encontrada.hora_inicio)
            self.vista.inicio_edit.setDateTime(QDateTime(dt_inicio))
    
        if isinstance(cita_encontrada.hora_fin, time):
            dt_fin = datetime.combine(datetime.today().date(), cita_encontrada.hora_fin)
            self.vista.fin_edit.setDateTime(QDateTime(dt_fin))

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
        
        for cita in self.citas_agendadas:  # CORREGIDO
            if cita.id_cita == id_cita.strip():
                cita.estado = "Confirmada"
                self.vista.resultado_text.append(f"Asistencia confirmada:\n{cita}")
                QMessageBox.information(self.vista, "✅ Éxito", "Asistencia confirmada.")
                return
            
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")

    def calcular_monto(self):
        """Calcula el monto a pagar según el tipo de consulta y tratamiento y abre la vista de factura"""
        self.vista.resultado_text.clear()
        self.listar_citas()  

        id_cita, ok = QInputDialog.getText(self.vista, "Calcular Monto", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        
        for cita in self.citas_agendadas:  # CORREGIDO
            if cita.id_cita == id_cita.strip():
                costo_cita = cita.costo_cita
                costo_tratamiento = getattr(cita, 'tratamiento', None)
                if costo_tratamiento:
                    costo_tratamiento = costo_tratamiento.costo
                else:
                    costo_tratamiento = 0
                total = costo_cita + costo_tratamiento

                respuesta = QMessageBox.question(
                    self.vista, 
                    "💰 Monto Calculado", 
                    f"Total a pagar: ${total:.2f}\n\n¿Desea generar una factura?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if respuesta == QMessageBox.StandardButton.Yes:
                    try:
                        if hasattr(self, 'factura_window') and self.factura_window is not None:
                            self.factura_window.close()
                            self.factura_window = None

                        self.factura_window = FacturacionView()
                        self.factura_controller = FacturacionController(self.factura_window)
                        self.factura_window.cargar_pacientes(self.pacientes)

                        for i in range(self.factura_window.paciente_combo.count()):
                            paciente_combo = self.factura_window.paciente_combo.itemData(i)
                            if paciente_combo and hasattr(paciente_combo, "dui") and paciente_combo.dui == cita.paciente.dui:
                                self.factura_window.paciente_combo.setCurrentIndex(i)
                                break

                        fecha_actual = datetime.now().strftime('%d/%m/%Y')
                        self.factura_window.fecha_edit.setText(fecha_actual)
                        descripcion_servicio = f"Consulta médica"
                        if hasattr(cita, 'tratamiento') and cita.tratamiento:
                            descripcion_servicio += f", {cita.tratamiento.descripcion}"
                        self.factura_window.servicio_edit.setText(descripcion_servicio)
                        self.factura_window.monto_edit.setText(f"{costo_cita}, {costo_tratamiento}")
                        id_factura = f"FAC-{cita.id_cita}-{datetime.now().strftime('%Y%m%d')}"
                        self.factura_window.id_factura_edit.setText(id_factura)

                        self.factura_window.show()

                    except Exception as e:
                        QMessageBox.critical(self.vista, "❌ Error", f"Error al abrir la ventana de facturación: {str(e)}")
                return  # <-- SOLO aquí, después de procesar la cita encontrada

        # Si no se encontró la cita, muestra el mensaje de error
        QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita.")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        if self.vista:
            # Limpiar combos a la primera opción
            self.vista.paciente_combo.setCurrentIndex(-1)
            self.vista.doctor_combo.setCurrentIndex(-1)
            self.vista.tratamiento_combo.setCurrentIndex(-1)
            
            # Resetear fecha y hora a valores actuales
            self.vista.fecha_edit.setDate(QDate.currentDate())
            self.vista.inicio_edit.setDateTime(QDateTime.currentDateTime())
            self.vista.fin_edit.setDateTime(QDateTime.currentDateTime())
            
            # Limpiar campos de texto
            self.vista.costo_edit.clear()
            
            # Resetear estado a Pendiente
            self.vista.estado_combo.setCurrentIndex(0)
            
            # Resetear modo edición
            self.editando_cita = None

# ==========================================
# EJECUCIÓN AUTOMÁTICA DEL CONTROLADOR
# PROPÓSITO: Inicializar la aplicación directamente desde el controlador
# ==========================================

if __name__ == "__main__":  
    from PyQt6.QtWidgets import QApplication
    from Vistas.CitaVista import CitaWindow

    app = QApplication([])
    window = CitaWindow()
    window.show()
    app.exec()
