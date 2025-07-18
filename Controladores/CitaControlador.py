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

from PyQt6.QtWidgets import QMessageBox, QInputDialog, QApplication
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
            self.pacientes = Paciente.obtener_todos_los_pacientes()
            print(f"Pacientes cargados: {len(self.pacientes)}")
            
            # Cargar doctores
            self.doctores = Doctor.obtener_todos_doctores()
            print(f"Doctores cargados: {len(self.doctores)}")
            
            # Cargar tratamientos
            self.tratamientos = Tratamiento.obtener_todos_tratamientos()
            print(f"Tratamientos cargados: {len(self.tratamientos)}")
            
            # NUEVO: Cargar citas desde la base de datos
            self.citas_agendadas = Cita.obtener_citas_bd()
            print(f"Citas cargadas desde BD: {len(self.citas_agendadas)}")
            
            # Inicializar el contador de IDs con las citas existentes
            if self.citas_agendadas:
                Cita.inicializar_contador_desde_citas(self.citas_agendadas)
            
        except Exception as e:
            print(f"Error al cargar datos desde BD: {e}")
            # En caso de error, usar listas vacías
            self.pacientes = []
            self.doctores = []
            self.tratamientos = []
            self.citas_agendadas = []

    def cargar_citas_desde_bd(self):
        """Método específico para recargar solo las citas desde la base de datos"""
        try:
            self.citas_agendadas = Cita.obtener_citas_bd()
            print(f"Citas recargadas desde BD: {len(self.citas_agendadas)}")
            
            # Actualizar el contador de IDs
            if self.citas_agendadas:
                Cita.inicializar_contador_desde_citas(self.citas_agendadas)
                
        except Exception as e:
            print(f"Error al cargar citas desde BD: {e}")
            self.citas_agendadas = []

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
        """Lista todas las citas cargadas desde la base de datos"""
        self.vista.resultado_text.clear()
        
        # NUEVO: Recargar citas desde la BD antes de mostrarlas
        self.cargar_citas_desde_bd()
        
        if len(self.citas_agendadas) == 0: 
            self.vista.resultado_text.append("No hay citas registradas en la base de datos...")
            return
        
        self.vista.resultado_text.append(f"📋 CITAS AGENDADAS ({len(self.citas_agendadas)} total):\n")
        self.vista.resultado_text.append("=" * 60 + "\n")
        
        for i, cita in enumerate(self.citas_agendadas, 1):  
            self.vista.resultado_text.append(f"🏥 CITA #{i}")
            self.vista.resultado_text.append(f"{cita}\n" + "-"*50 + "\n")

    def cancelar_cita(self):
        """Cancela una cita por ID"""
        self.vista.resultado_text.clear()

        # NUEVO: Cargar y mostrar citas desde la BD
        self.cargar_citas_desde_bd()
        
        if len(self.citas_agendadas) == 0:
            self.vista.resultado_text.append("No hay citas registradas en la base de datos...")
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        # Mostrar todas las citas disponibles
        self.listar_citas()
        
        id_cita, ok = QInputDialog.getText(self.vista, "Cancelar Cita", "Ingrese el ID de la cita a cancelar:")
        if not ok or not id_cita.strip():
            return
            
        # Buscar la cita por ID
        cita_encontrada = None
        for cita in self.citas_agendadas:
            if str(cita.id_cita) == id_cita.strip():
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            # NUEVO: Actualizar el estado en la base de datos
            if Cita.actualizar_estado_bd(cita_encontrada.id_cita, "Cancelada"):
                # Solo actualizar en memoria si la BD se actualizó correctamente
                cita_encontrada.estado = "Cancelada"
                
                self.vista.resultado_text.append(f"\n🚫 CITA CANCELADA:\n{cita_encontrada}")
                QMessageBox.information(self.vista, "✅ Éxito", "Cita cancelada exitosamente en la base de datos.")
                
                # Recargar las citas para mostrar el estado actualizado
                self.cargar_citas_desde_bd()
            else:
                QMessageBox.critical(self.vista, "❌ Error", "Error al cancelar la cita en la base de datos.")
        else:
            QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita con ese ID.")


    def modificar_cita(self):
        """
        Si no estamos editando, pide el ID de la cita, la busca y permite editar sus datos (excepto el ID).
        Si ya estamos editando, guarda los cambios realizados.
        """
        self.vista.resultado_text.clear()

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
                if paciente_idx <= 0 or doctor_idx <= 0 or not costo:
                    QMessageBox.warning(self.vista, "❌ Error", "Paciente, Doctor y Costo son obligatorios.")
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
                cita.paciente = self.pacientes[paciente_idx - 1]
                cita.doctor = self.doctores[doctor_idx - 1]
                if tratamiento_idx > 0:
                    cita.tratamiento = self.tratamientos[tratamiento_idx - 1]
                cita.fecha = fecha
                cita.hora_inicio = hora_inicio
                cita.hora_fin = hora_fin
                cita.costo_cita = costo_float
                cita.estado = estado
                
                # TODO: Aquí deberías actualizar la BD también
                # Cita.actualizar_cita_bd(cita)
                
                QMessageBox.information(self.vista, "✅ Éxito", "Cita modificada correctamente.")
                self.vista.resultado_text.append(
                    f"✏️ CITA MODIFICADA:\n"
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

        # NUEVO: Cargar y mostrar citas desde la BD
        self.cargar_citas_desde_bd()
        
        if len(self.citas_agendadas) == 0:
            self.vista.resultado_text.append("No hay citas registradas en la base de datos...")
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        # Si NO estamos editando, mostrar lista de citas y pedir ID
        self.listar_citas()  # Mostrar citas disponibles
        
        id_cita, ok = QInputDialog.getText(self.vista, "Modificar Cita", "Ingrese el ID de la cita a modificar:")
        if not ok or not id_cita.strip():
            return
        
        # Buscar la cita
        cita_encontrada = None
        for cita in self.citas_agendadas:
            if str(cita.id_cita) == id_cita.strip():
                cita_encontrada = cita
                break
        
        if not cita_encontrada:
            QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita con ese ID.")
            return
        
        # Cargar datos actuales en la vista
        self.vista.id_edit.setText(str(cita_encontrada.id_cita))
        self.vista.id_edit.setReadOnly(True)  # No permitir editar el ID
        
        # Establecer valores en los combos
        for i, paciente in enumerate(self.pacientes):
            if paciente.id_paciente == cita_encontrada.paciente.id_paciente:
                self.vista.paciente_combo.setCurrentIndex(i + 1)  # +1 porque el índice 0 es "-- Seleccionar --"
                break
        
        for i, doctor in enumerate(self.doctores):
            if doctor.id_doctor == cita_encontrada.doctor.id_doctor:
                self.vista.doctor_combo.setCurrentIndex(i + 1)  # +1 porque el índice 0 es "-- Seleccionar --"
                break
        
        if hasattr(cita_encontrada, 'tratamiento') and cita_encontrada.tratamiento:
            for i, tratamiento in enumerate(self.tratamientos):
                if tratamiento.id_tratamiento == cita_encontrada.tratamiento.id_tratamiento:
                    self.vista.tratamiento_combo.setCurrentIndex(i + 1)  # +1 porque el índice 0 es "-- Seleccionar --"
                    break
        
        # Establecer fechas y otros campos
        if hasattr(cita_encontrada, 'fecha'):
            if hasattr(cita_encontrada.fecha, 'year'):
                qdate = QDate(cita_encontrada.fecha.year, cita_encontrada.fecha.month, cita_encontrada.fecha.day)
                self.vista.fecha_edit.setDate(qdate)
            else:
                self.vista.fecha_edit.setDate(QDate.currentDate())

        # CORREGIDO: Manejo más simple de las horas
        try:
            if hasattr(cita_encontrada, 'hora_inicio') and cita_encontrada.hora_inicio:
                # Crear QDateTime con la fecha actual y la hora de la cita
                qdt_inicio = QDateTime(QDate.currentDate(), cita_encontrada.hora_inicio)
                self.vista.inicio_edit.setDateTime(qdt_inicio)
            else:
                self.vista.inicio_edit.setDateTime(QDateTime.currentDateTime())
        except Exception as e:
            print(f"Error al establecer hora de inicio: {e}")
            self.vista.inicio_edit.setDateTime(QDateTime.currentDateTime())
    
        try:
            if hasattr(cita_encontrada, 'hora_fin') and cita_encontrada.hora_fin:
                # Crear QDateTime con la fecha actual y la hora de la cita
                qdt_fin = QDateTime(QDate.currentDate(), cita_encontrada.hora_fin)
                self.vista.fin_edit.setDateTime(qdt_fin)
            else:
                self.vista.fin_edit.setDateTime(QDateTime.currentDateTime())
        except Exception as e:
            print(f"Error al establecer hora de fin: {e}")
            self.vista.fin_edit.setDateTime(QDateTime.currentDateTime())

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
        
        # NUEVO: Cargar y mostrar citas desde la BD
        self.cargar_citas_desde_bd()
        
        if len(self.citas_agendadas) == 0:
            self.vista.resultado_text.append("No hay citas registradas en la base de datos...")
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        self.listar_citas()

        id_cita, ok = QInputDialog.getText(self.vista, "Confirmar Asistencia", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        
        # Buscar la cita por ID
        cita_encontrada = None
        for cita in self.citas_agendadas:
            if str(cita.id_cita) == id_cita.strip():
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            # NUEVO: Actualizar el estado en la base de datos
            if Cita.actualizar_estado_bd(cita_encontrada.id_cita, "Confirmada"):
                # Solo actualizar en memoria si la BD se actualizó correctamente
                cita_encontrada.estado = "Confirmada"
                
                self.vista.resultado_text.append(f"\n✅ ASISTENCIA CONFIRMADA:\n{cita_encontrada}")
                QMessageBox.information(self.vista, "✅ Éxito", "Asistencia confirmada exitosamente en la base de datos.")
                
                # Recargar las citas para mostrar el estado actualizado
                self.cargar_citas_desde_bd()
            else:
                QMessageBox.critical(self.vista, "❌ Error", "Error al confirmar la asistencia en la base de datos.")
        else:
            QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita con ese ID.")

    def calcular_monto(self):
        """Calcula el monto a pagar según el tipo de consulta y tratamiento y abre la vista de factura"""
        self.vista.resultado_text.clear()
        
        # NUEVO: Cargar y mostrar citas desde la BD
        self.cargar_citas_desde_bd()
        
        if len(self.citas_agendadas) == 0:
            self.vista.resultado_text.append("No hay citas registradas en la base de datos...")
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay citas registradas")
            return

        self.listar_citas()

        id_cita, ok = QInputDialog.getText(self.vista, "Calcular Monto", "Ingrese el ID de la cita:")
        if not ok or not id_cita.strip():
            return
        
        # Buscar la cita por ID
        cita_encontrada = None
        for cita in self.citas_agendadas:
            if str(cita.id_cita) == id_cita.strip():
                cita_encontrada = cita
                break
        
        if cita_encontrada:
            costo_cita = cita_encontrada.costo_cita
            costo_tratamiento = 0
            
            # Obtener el costo del tratamiento si existe
            if hasattr(cita_encontrada, 'tratamiento') and cita_encontrada.tratamiento:
                costo_tratamiento = cita_encontrada.tratamiento.costo
            
            total = costo_cita + costo_tratamiento

            self.vista.resultado_text.append(f"\n💰 CÁLCULO DE MONTO:\n")
            self.vista.resultado_text.append(f"Cita ID: {cita_encontrada.id_cita}")
            self.vista.resultado_text.append(f"Costo de consulta: ${costo_cita:.2f}")
            self.vista.resultado_text.append(f"Costo de tratamiento: ${costo_tratamiento:.2f}")
            self.vista.resultado_text.append(f"TOTAL A PAGAR: ${total:.2f}")

            respuesta = QMessageBox.question(
                self.vista, 
                "💰 Monto Calculado", 
                f"Total a pagar: ${total:.2f}\n\n¿Desea generar una factura?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                try:
                    print("🧾 Iniciando proceso de facturación...")
                    
                    # Cerrar ventana anterior si existe
                    if hasattr(self, 'factura_window') and self.factura_window is not None:
                        self.factura_window.close()
                        self.factura_window = None

                    # Crear nueva ventana de facturación
                    print("📝 Creando ventana de facturación...")
                    self.factura_window = FacturacionView()
                    
                    # Crear controlador de facturación
                    print("🎮 Creando controlador de facturación...")
                    self.factura_controller = FacturacionController(self.factura_window)
                    
                    # Esperar un momento para que se carguen los datos
                    QApplication.processEvents()
                    
                    # Pre-llenar datos de la cita en la factura
                    print("📋 Pre-llenando datos de la factura...")
                    
                    # Buscar el paciente en el combo
                    paciente_encontrado = False
                    for i in range(self.factura_window.paciente_combo.count()):
                        # Obtener el paciente del combo
                        paciente_combo = self.factura_window.paciente_combo.itemData(i)
                        if paciente_combo and hasattr(paciente_combo, 'id_paciente'):
                            if paciente_combo.id_paciente == cita_encontrada.paciente.id_paciente:
                                self.factura_window.paciente_combo.setCurrentIndex(i)
                                paciente_encontrado = True
                                print(f"✅ Paciente seleccionado: {paciente_combo.nombre}")
                                break
                    
                    if not paciente_encontrado:
                        print("⚠️ No se pudo seleccionar el paciente automáticamente")

                    # Buscar el tratamiento en el combo si existe
                    if hasattr(cita_encontrada, 'tratamiento') and cita_encontrada.tratamiento:
                        tratamiento_encontrado = False
                        for i in range(self.factura_window.tratamiento_combo.count()):
                            tratamiento_combo = self.factura_window.tratamiento_combo.itemData(i)
                            if tratamiento_combo and hasattr(tratamiento_combo, 'id_tratamiento'):
                                if tratamiento_combo.id_tratamiento == cita_encontrada.tratamiento.id_tratamiento:
                                    self.factura_window.tratamiento_combo.setCurrentIndex(i)
                                    tratamiento_encontrado = True
                                    print(f"✅ Tratamiento seleccionado: {tratamiento_combo.descripcion}")
                                    break
                        
                        if not tratamiento_encontrado:
                            print("⚠️ No se pudo seleccionar el tratamiento automáticamente")

                    # Generar ID único de factura
                    fecha_actual = datetime.now().strftime('%Y%m%d%H%M%S')
                    id_factura = f"FAC-{cita_encontrada.id_cita}-{fecha_actual}"
                    
                    # Pre-llenar campos si existen en la vista
                    if hasattr(self.factura_window, 'id_factura_edit'):
                        self.factura_window.id_factura_edit.setText(id_factura)
                        print(f"📝 ID de factura generado: {id_factura}")

                    # Mostrar la ventana de facturación
                    print("👁️ Mostrando ventana de facturación...")
                    self.factura_window.show()
                    self.factura_window.raise_()  # Traer al frente
                    self.factura_window.activateWindow()  # Activar la ventana
                    
                    print("✅ Ventana de facturación abierta correctamente")

                except Exception as e:
                    print(f"❌ Error al abrir la ventana de facturación: {e}")
                    import traceback
                    traceback.print_exc()
                    QMessageBox.critical(self.vista, "❌ Error", 
                                       f"Error al abrir la ventana de facturación:\n{str(e)}")
        else:
            QMessageBox.warning(self.vista, "❌ Error", "No se encontró la cita con ese ID.")
    
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
