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
        self.editando_doctor = None
        # Cargar doctores desde la base de datos al inicializar
        self.cargar_doctores()

    def cargar_doctores(self):
        """Carga los doctores desde la base de datos"""
        try:
            self.doctores = Doctor.obtener_todos_doctores()
            print(f"Doctores cargados: {len(self.doctores)}")
        except Exception as e:
            print(f"Error al cargar doctores: {e}")
            self.doctores = []

    # ====================================
    # ========== VALIDACIONES ============
    # ====================================
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    @staticmethod
    def validar_num_junta_medica( num_junta_medica: str) -> bool:
        """Valida el formato y largo del numero de junta medica (4-7 dígitos)"""
        # Verificar que solo contenga dígitos
        if not num_junta_medica.isdigit():
            return False
        
        # Verificar que tenga entre 4 y 7 dígitos 
        return 4 <= len(num_junta_medica) <= 7
    
    @staticmethod
    def validar_telefono( telefono: str) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return  len(telefono) == 8
    
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.vista.nombre_edit.clear()
        self.vista.apellido_edit.clear()
        self.vista.num_junta_medica_edit.clear()
        self.vista.telefono_edit.clear()
        self.vista.correo_edit.clear()
        self.vista.especialidad_edit.clear()
        
        # Enfocar el primer campo para facilitar la entrada
        self.vista.nombre_edit.setFocus()
    
    def crear_doctor(self, num_junta_medica: int, nombre: str, apellido: str, especialidad: str, telefono: str, correo: str):
        try:
            # Validaciones básicas
            if not nombre or not apellido or not num_junta_medica or not especialidad or not telefono or not correo:
                QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios")
                return None
            
            if not self.validar_num_junta_medica(str(num_junta_medica)):
                QMessageBox.warning(self.vista, "❌ Error", "El número de junta médica debe tener entre 4 y 7 dígitos")
                return None
            
            if not self.validar_telefono(telefono):
                QMessageBox.warning(self.vista, "❌ Error", "El teléfono debe tener exactamente 8 dígitos")
                return None
            
            if not self.validar_email(correo):
                QMessageBox.warning(self.vista, "❌ Error", "El correo electrónico no es válido")
                return None
            
            # Verificar duplicados antes de crear el objeto
            try:
                doctores_existentes = Doctor.obtener_doctores_desde_db()
                for doctor_existente in doctores_existentes:
                    if doctor_existente.num_junta_medica == int(num_junta_medica):
                        QMessageBox.warning(self.vista, "❌ Error", "Ya existe un doctor con ese número de junta médica")
                        return None
            except Exception as e:
                print(f"[WARNING] No se pudo verificar doctores existentes: {e}")
                # Continuar sin verificación si hay problemas con la BD
            
            # Crear el objeto Doctor
            nuevo_doctor = Doctor(
                num_junta_medica=int(num_junta_medica),
                nombre=nombre.title(),
                apellido=apellido.title(),
                especialidad=especialidad.title(),
                telefono=telefono,
                correo=correo.lower()
            )

            # Inserción en la base de datos con manejo detallado de errores
            print(f"[INFO] Intentando insertar doctor: {nuevo_doctor.nombre} {nuevo_doctor.apellido}")
            
            try:
                resultado = Doctor.insert_doc_db(nuevo_doctor)
                print(f"[DEBUG] Resultado de insert_doc_db: {resultado}")
                
                if not resultado:
                    # Intentar obtener más información del error
                    QMessageBox.critical(self.vista, "❌ Error de Base de Datos", 
                                       "No se pudo insertar el doctor en la base de datos.\n\n" +
                                       "Posibles causas:\n" +
                                       "• La base de datos no está disponible\n" +
                                       "• Problemas de permisos\n" +
                                       "• Error en la conexión\n" +
                                       "• Conflicto con datos existentes")
                    return None
                
                # Si llegamos aquí, la inserción fue exitosa
                self.doctores.append(nuevo_doctor)
                QMessageBox.information(self.vista, "✅ Éxito", "Doctor creado exitosamente")
                self.vista.resultado_text.append(f"✅ Doctor creado: Dr. {nuevo_doctor.nombre} {nuevo_doctor.apellido}")
                self.limpiar_campos()
                return nuevo_doctor
                
            except Exception as db_error:
                print(f"[ERROR] Error específico al insertar en BD: {db_error}")
                QMessageBox.critical(self.vista, "❌ Error de Base de Datos", 
                                   f"Error al guardar en la base de datos:\n{str(db_error)}\n\n" +
                                   "Verifique:\n" +
                                   "• Que la base de datos esté funcionando\n" +
                                   "• Los permisos de escritura\n" +
                                   "• La estructura de la tabla")
                return None

        except ValueError as ve:
            print(f"[ERROR] Error de valor: {ve}")
            QMessageBox.warning(self.vista, "❌ Error de Datos", f"Datos inválidos: {str(ve)}")
            return None
            
        except Exception as e:
            print(f"[ERROR] Error general al crear doctor: {e}")
            QMessageBox.critical(self.vista, "❌ Error", f"Error inesperado al crear el doctor: {str(e)}")
            return None


    # def crear_doctor(self):
    #     """Crea un doctor con los datos de los campos de la vista"""
    #     # Obtener datos de los campos de la vista
    #     nombre = self.vista.nombre_edit.text().strip()
    #     apellido = self.vista.apellido_edit.text().strip()
    #     num_junta_medica = self.vista.num_junta_medica_edit.text().strip()
    #     especialidad = self.vista.especialidad_edit.text().strip()
    #     telefono = self.vista.telefono_edit.text().strip()
    #     correo = self.vista.correo_edit.text().strip()
        
        
    #     # Crear el objeto Doctor si todos los campos son válidos
    #     doctor = Doctor(
    #         nombre=nombre.title(),
    #         apellido=apellido.title(),
    #         num_junta_medica=int(num_junta_medica),
    #         especialidad=especialidad.title(),
    #         telefono=telefono,
    #         correo=correo.lower()
    #     )
        
    #     # Agregar doctor en la base de datos
    #     try:
    #         Doctor.insert_doc_db(doctor)
    #         QMessageBox.information(self.vista, "✅ Éxito", "Doctor creado exitosamente")
    #         self.vista.resultado_text.append(f"✅ Doctor creado: Dr. {doctor.nombre} {doctor.apellido}")
    #         self.limpiar_campos()
    #     except Exception as e:
    #         QMessageBox.critical(self.vista, "❌ Error", f"Error al agregar el doctor a la base de datos: {str(e)}")
            
    #     return doctor
    
    def agregar_horario(self):
        """Abre el diálogo de HorarioVista para agregar un horario con ID automático"""
        try:
            # Obtener doctores desde la BD
            doctores_bd = Doctor.obtener_todos_doctores()
            
            if not doctores_bd:
                QMessageBox.information(self.vista, "ℹ️ Información", 
                                      "Debe registrar al menos un doctor antes de agregar horarios.")
                return
            
            # Importar HorarioModel para generar ID automático
            from Modelos.HorarioModelo import HorarioModel
            modelo_horario = HorarioModel()
            
            # Generar el siguiente ID automáticamente (igual que en HorarioController)
            siguiente_id = modelo_horario.generar_siguiente_id()
            print(f"ID de horario generado automáticamente: {siguiente_id}")
            
            # Mostrar IDs existentes para debugging
            ids_existentes = modelo_horario.obtener_ids_existentes()
            print(f"IDs de horarios existentes en BD: {ids_existentes}")
            
            # Crear y mostrar el diálogo con el ID pre-generado
            dialog = AgregarHorarioDialog(doctores_bd, self.vista)
            
            # CLAVE: Establecer el ID generado automáticamente en el diálogo
            dialog.id_edit.setText(siguiente_id)
            dialog.id_edit.setReadOnly(True)  # Hacer que sea solo lectura
            
            # Aplicar estilo visual para indicar que es automático
            dialog.id_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #f0f0f0;
                    border: 2px solid #d0d0d0;
                    border-radius: 4px;
                    padding: 5px;
                    font-weight: bold;
                    color: #333;
                }
            """)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                # Validar que todos los campos están completos
                if not all([data['id_horario'], data['hora_inicio'], data['hora_fin'], data['doctor']]):
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios")
                    return
                
                # Verificar que se está usando el ID generado automáticamente
                if data['id_horario'] != siguiente_id:
                    QMessageBox.warning(self.vista, "⚠️ Advertencia", 
                                      f"Se detectó un cambio en el ID. Usando el ID generado automáticamente: {siguiente_id}")
                    data['id_horario'] = siguiente_id
                
                # Validaciones adicionales (formato de hora, etc.)
                try:
                    from datetime import datetime
                    datetime.strptime(data['hora_inicio'], "%H:%M")
                    datetime.strptime(data['hora_fin'], "%H:%M")
                except ValueError:
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      "Formato de hora inválido. Use HH:MM (ej. 09:00).")
                    return
                
                # Validar que la hora de inicio sea anterior a la hora de fin
                if datetime.strptime(data['hora_inicio'], "%H:%M") >= datetime.strptime(data['hora_fin'], "%H:%M"):
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      "La hora de fin debe ser posterior a la hora de inicio.")
                    return
                
                # Crear el horario y guardarlo en la base de datos
                from Modelos.HorarioModelo import Horario
                
                nuevo_horario = Horario(
                    id_horario=data['id_horario'],
                    hora_inicio=data['hora_inicio'],
                    hora_fin=data['hora_fin'],
                    doctor=data['doctor']
                )
                
                # Validar conflictos de horario
                horarios_existentes = Horario.obtener_horarios_bd()
                for horario_existente in horarios_existentes:
                    if nuevo_horario.horario_ocupado(horario_existente):
                        QMessageBox.warning(self.vista, "❌ Error", 
                                          f"El doctor {data['doctor'].nombre} {data['doctor'].apellido} ya tiene un horario "
                                          f"ocupado en ese rango de horas.\n"
                                          f"Horario conflictivo: {horario_existente.hora_inicio} - {horario_existente.hora_fin}")
                        return
                
                # Intentar guardar en la base de datos
                if Horario.insertar_horario_bd(nuevo_horario):
                    # Mostrar el resultado en el área de texto
                    self.vista.resultado_text.append(f"""
🕒 Horario agregado exitosamente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ID Horario: {data['id_horario']} 
⏰ Hora Inicio: {data['hora_inicio']}
⏳ Hora Fin: {data['hora_fin']}
👨‍⚕️ Doctor: Dr. {data['doctor'].nombre} {data['doctor'].apellido}
🆔 Próximo ID disponible: {modelo_horario.generar_siguiente_id()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
                    
                    QMessageBox.information(self.vista, "✅ Éxito", 
                                          f"Horario agregado exitosamente.\n"
                                          f"ID generado: {data['id_horario']}\n"
                                          f"Doctor: Dr. {data['doctor'].nombre} {data['doctor'].apellido}\n"
                                          f"Horario: {data['hora_inicio']} - {data['hora_fin']}")
                else:
                    QMessageBox.critical(self.vista, "❌ Error", 
                                       "No se pudo guardar el horario en la base de datos.")
    
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", 
                               f"Error al abrir el diálogo de horarios: {str(e)}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrar_info_doctor(self):
        """ Muestra un diálogo con la información de todos los doctores registrados """
        try:
            print("Intentando obtener doctores...")  # Debug
            doctores = Doctor.obtener_doctores_desde_db()
            print(f"Doctores obtenidos: {len(doctores)}")  # Debug
            
            self.vista.resultado_text.clear()
            if not doctores:
                self.vista.resultado_text.append("No hay doctores registrados.")
            else:
                self.vista.resultado_text.append("📋 Listado de Doctores:")
                self.vista.resultado_text.append("=" * 50)
                for doctor in doctores:
                    print(f"Mostrando doctor: {doctor}")  # Debug
                    self.vista.resultado_text.append(f"👨‍⚕️ Dr. {doctor}")
                    self.vista.resultado_text.append(f"   📞 Teléfono: {doctor.telefono}")
                    self.vista.resultado_text.append(f"   📧 Correo: {doctor.correo}")
                    self.vista.resultado_text.append(f"   🆔 N° Junta Médica: {doctor.num_junta_medica}")
                    self.vista.resultado_text.append("-" * 30)
        except Exception as e:
            print(f"Error en mostrar_info_doctor: {e}")  # Debug
            self.vista.resultado_text.clear()
            self.vista.resultado_text.append(f"❌ Error al obtener doctores: {str(e)}")
            
    def suprimir_doctor(self):
        """
        Permite eliminar un doctor registrado por su numero de junta medica.
        Solo se puede eliminar si no tiene citas asignadas.
        """
        self.vista.resultado_text.clear()

        try:
            # Obtener doctores desde la base de datos
            doctores_bd = Doctor.obtener_doctores_desde_db()
            
            if not doctores_bd:
                QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
                return

            # Mostrar lista de doctores disponibles
            self.vista.resultado_text.append("📋 DOCTORES DISPONIBLES PARA ELIMINAR:\n" + "="*60 + "\n")
            for doctor in doctores_bd:
                self.vista.resultado_text.append(
                    f"• Nº Junta Médica: {doctor.num_junta_medica}\n"
                    f"  Nombre: Dr. {doctor.nombre} {doctor.apellido}\n"
                    f"  Especialidad: {doctor.especialidad}\n"
                    f"  {'-'*50}\n"
                )

            num_junta_medica_a_eliminar, ok = QInputDialog.getText(
                self.vista, 
                "Eliminar Doctor", 
                "Ingrese el Número de Junta Médica del doctor a eliminar:"
            )
            
            if not ok or not num_junta_medica_a_eliminar.strip():
                return

            num_junta_medica_a_eliminar = num_junta_medica_a_eliminar.strip()
            
            # Buscar el doctor
            doctor_encontrado = None
            for doctor in doctores_bd:
                # Comparar como strings para evitar problemas de tipos
                if str(doctor.num_junta_medica) == num_junta_medica_a_eliminar:
                    doctor_encontrado = doctor
                    break

            if not doctor_encontrado:
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    f"No se encontró ningún doctor con el Nº Junta Médica: {num_junta_medica_a_eliminar}"
                )
                return

            # Verificar si el doctor tiene citas
            try:
                id_para_bd = int(doctor_encontrado.num_junta_medica)
                citas = Doctor.obtener_citas_por_doctor(id_para_bd)
                
                if citas and len(citas) > 0:
                    QMessageBox.warning(
                        self.vista, 
                        "❌ No se puede eliminar", 
                        f"El Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido} "
                        f"tiene {len(citas)} cita(s) registrada(s).\n\n"
                        f"No se puede eliminar un doctor que tiene citas asignadas.\n"
                        f"Primero debe cancelar o reasignar todas sus citas."
                    )
                    
                    # Mostrar las citas del doctor
                    self.vista.resultado_text.append(
                        f"❌ ELIMINACIÓN CANCELADA\n"
                        f"Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido} tiene {len(citas)} cita(s):\n\n"
                    )
                    
                    for i, cita in enumerate(citas, 1):
                        try:
                            if isinstance(cita['fecha'], str):
                                fecha_str = cita['fecha']
                            else:
                                fecha_str = cita['fecha'].strftime('%d/%m/%Y')
                        except:
                            fecha_str = str(cita['fecha'])
                        
                        self.vista.resultado_text.append(
                            f"  {i}. Fecha: {fecha_str}, "
                            f"Paciente: {cita['paciente_nombre']} {cita['paciente_apellido']}, "
                            f"Estado: {cita['estado']}\n"
                        )
                    
                    return

            except Exception as e:
                print(f"Error verificando citas: {e}")
                QMessageBox.warning(
                    self.vista, 
                    "⚠️ Advertencia", 
                    "No se pudo verificar las citas del doctor. "
                    "Por seguridad, no se eliminará el doctor."
                )
                return

            # Confirmar eliminación
            respuesta = QMessageBox.question(
                self.vista,
                "Confirmar Eliminación",
                f"¿Está seguro que desea eliminar al Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido}?\n\n"
                f"Nº Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                f"Especialidad: {doctor_encontrado.especialidad}\n\n"
                f"Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if respuesta != QMessageBox.StandardButton.Yes:
                return

            # Intentar eliminar de la base de datos
            try:
                if Doctor.eliminar_doctor_bd(id_para_bd):
                    QMessageBox.information(
                        self.vista, 
                        "✅ Éxito", 
                        f"Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido} "
                        f"eliminado correctamente."
                    )
                    
                    self.vista.resultado_text.append(
                        f"✅ DOCTOR ELIMINADO EXITOSAMENTE:\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"👨‍⚕️ Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido}\n"
                        f"🆔 Nº Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                        f"🏥 Especialidad: {doctor_encontrado.especialidad}\n"
                        f"📞 Teléfono: {doctor_encontrado.telefono}\n"
                        f"📧 Correo: {doctor_encontrado.correo}\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    )
                    
                    # Recargar la lista de doctores
                    self.cargar_doctores()
                    
                else:
                    QMessageBox.critical(
                        self.vista, 
                        "❌ Error", 
                        "No se pudo eliminar el doctor de la base de datos."
                    )

            except Exception as e:
                print(f"Error eliminando doctor: {e}")
                QMessageBox.critical(
                    self.vista, 
                    "❌ Error", 
                    f"Error al eliminar el doctor de la base de datos:\n{str(e)}"
                )

        except Exception as e:
            print(f"Error general en suprimir_doctor: {e}")
            QMessageBox.critical(
                self.vista, 
                "❌ Error", 
                f"Error inesperado: {str(e)}"
            )
    
    def actualizar_info_doctor(self):
        """
        Si no estamos editando, pide el N° Junta Medica, busca el doctor y permite editar sus datos (excepto el N° Junta Medica).
        Si ya estamos editando, guarda los cambios realizados.
        """
        self.vista.resultado_text.clear()

        try:
            # Obtener doctores desde la base de datos
            doctores_bd = Doctor.obtener_doctores_desde_db()
            
            if not doctores_bd:
                QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
                return

            # Si ya estamos editando, guardar los cambios
            if self.editando_doctor is not None:
                # Obtener los nuevos datos de los campos
                nombre = self.vista.nombre_edit.text().strip().title()
                apellido = self.vista.apellido_edit.text().strip().title()
                especialidad = self.vista.especialidad_edit.text().strip().title()
                telefono = self.vista.telefono_edit.text().strip()
                correo = self.vista.correo_edit.text().strip().lower()
                
                # Validaciones
                if not all([nombre, apellido, especialidad, telefono, correo]):
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios")
                    return
                
                if not self.validar_telefono(telefono):
                    QMessageBox.warning(self.vista, "❌ Error", "El teléfono debe tener exactamente 8 dígitos")
                    return
                
                if not self.validar_email(correo):
                    QMessageBox.warning(self.vista, "❌ Error", "El correo electrónico no es válido")
                    return
                
                # Actualizar los datos del doctor
                self.editando_doctor.nombre = nombre
                self.editando_doctor.apellido = apellido
                self.editando_doctor.especialidad = especialidad
                self.editando_doctor.telefono = telefono
                self.editando_doctor.correo = correo
                
                # Guardar en la base de datos
                try:
                    if Doctor.actualizar_doctor_bd(self.editando_doctor):
                        QMessageBox.information(
                            self.vista, 
                            "✅ Éxito", 
                            f"Información del Dr. {nombre} {apellido} actualizada correctamente."
                        )
                        
                        self.vista.resultado_text.append(
                            f"✅ DOCTOR ACTUALIZADO EXITOSAMENTE:\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"🆔 N° Junta Médica: {self.editando_doctor.num_junta_medica}\n"
                            f"👨‍⚕️ Nombre: Dr. {nombre} {apellido}\n"
                            f"🏥 Especialidad: {especialidad}\n"
                            f"📞 Teléfono: {telefono}\n"
                            f"📧 Correo: {correo}\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        )
                        
                        # Recargar la lista de doctores
                        self.cargar_doctores()
                        
                    else:
                        QMessageBox.critical(
                            self.vista, 
                            "❌ Error", 
                            "No se pudo actualizar el doctor en la base de datos."
                        )
                        return
                        
                except Exception as e:
                    print(f"Error actualizando doctor: {e}")
                    QMessageBox.critical(
                        self.vista, 
                        "❌ Error", 
                        f"Error al actualizar el doctor en la base de datos:\n{str(e)}"
                    )
                    return
                
                # Limpiar campos y salir del modo edición
                self.vista.num_junta_medica_edit.setReadOnly(False)
                self.editando_doctor = None
                self.limpiar_campos()
                return

            # Si NO estamos editando, pedir N° Junta Medica y cargar datos
            # Mostrar lista de doctores disponibles
            self.vista.resultado_text.append("📋 DOCTORES DISPONIBLES PARA EDITAR:\n" + "="*60 + "\n")
            for doctor in doctores_bd:
                self.vista.resultado_text.append(
                    f"• Nº Junta Médica: {doctor.num_junta_medica}\n"
                    f"  Nombre: Dr. {doctor.nombre} {doctor.apellido}\n"
                    f"  Especialidad: {doctor.especialidad}\n"
                    f"  {'-'*50}\n"
                )
            
            num_junta_medica_a_buscar, ok = QInputDialog.getText(
                self.vista, 
                "Buscar Doctor", 
                "Ingrese el N° Junta Médica del doctor a modificar:"
            )
            
            if not ok or not num_junta_medica_a_buscar.strip():
                return

            num_junta_medica_a_buscar = num_junta_medica_a_buscar.strip()
            
            # Buscar el doctor - CORREGIDO: usar atributos en lugar de índices
            doctor_encontrado = None
            for doctor in doctores_bd:
                # Comparar como strings para evitar problemas de tipos
                if str(doctor.num_junta_medica) == num_junta_medica_a_buscar:
                    doctor_encontrado = doctor
                    break
            
            if not doctor_encontrado:
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    f"No se encontró ningún doctor con el N° Junta Médica: {num_junta_medica_a_buscar}"
                )
                return
            
            # Llenar los campos con los datos encontrados - CORREGIDO: usar atributos
            self.vista.num_junta_medica_edit.setText(str(doctor_encontrado.num_junta_medica))
            self.vista.nombre_edit.setText(doctor_encontrado.nombre)
            self.vista.apellido_edit.setText(doctor_encontrado.apellido)
            self.vista.especialidad_edit.setText(doctor_encontrado.especialidad)
            self.vista.telefono_edit.setText(str(doctor_encontrado.telefono))
            self.vista.correo_edit.setText(doctor_encontrado.correo)
            self.vista.num_junta_medica_edit.setReadOnly(True)  # No permitir editar el Numero de junta medica

            self.editando_doctor = doctor_encontrado  # Guardamos referencia para editar después

            QMessageBox.information(
                self.vista, 
                "Editar Doctor", 
                f"Editando datos del Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido}.\n\n"
                "Modifique los campos que desee y presione nuevamente 'Actualizar Info Doctor' para guardar los cambios."
            )
            
        except Exception as e:
            print(f"Error general en actualizar_info_doctor: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.vista, 
                "❌ Error", 
                f"Error inesperado: {str(e)}"
            )
    
    # Por el momento, no encontrara ninguna cita para el doctor, una vez se haya hecho la conexion con la base de datos será más fácil
    def ver_citas(self):
        """Ver las citas de un doctor específico usando su número de junta médica"""
        self.vista.resultado_text.clear()
        
        try:
            # Obtener doctores desde la base de datos
            doctores_bd = Doctor.obtener_doctores_desde_db()
            
            if not doctores_bd:
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    "No hay doctores registrados en la base de datos.\n"
                    "Primero debe registrar al menos un doctor."
                )
                return
            
            # Mostrar lista de doctores disponibles
            self.vista.resultado_text.append("📋 DOCTORES DISPONIBLES:\n" + "="*60 + "\n")
            for doctor in doctores_bd:
                self.vista.resultado_text.append(
                    f"• ID: {doctor.num_junta_medica}\n"
                    f"  Nombre: Dr. {doctor.nombre} {doctor.apellido}\n"
                    f"  Especialidad: {doctor.especialidad}\n"
                    f"  {'-'*50}\n"
                )
            self.vista.resultado_text.append("\n")
            
            # Pedir el identificador
            identificador, ok = QInputDialog.getText(
                self.vista, 
                "Ver Citas", 
                "Ingrese el Número de Junta Médica del doctor:"
            )
            
            if not ok or not identificador.strip():
                return
            
            identificador = identificador.strip()
            
            # CLAVE: Buscar el doctor comparando como STRING
            doctor_encontrado = None
            
            for doctor in doctores_bd:
                print(f"🔍 DEBUG: Comparando '{identificador}' con '{doctor.num_junta_medica}'")
                
                # Comparar ambos como strings
                if str(doctor.num_junta_medica) == identificador:
                    doctor_encontrado = doctor
                    print(f"✅ Doctor encontrado: {doctor.nombre} {doctor.apellido}")
                    break
            
            if not doctor_encontrado:
                # Crear lista de números disponibles
                nums_disponibles = [d.num_junta_medica for d in doctores_bd]
                
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    f"No se encontró ningún doctor con el Nº Junta Médica: {identificador}\n\n"
                    f"Números disponibles:\n" + 
                    "\n".join([f"• {num} - Dr. {d.nombre} {d.apellido}" for d, num in zip(doctores_bd, nums_disponibles)])
                )
                return
            
            # Convertir a int para la búsqueda en BD (ya que la BD espera int)
            try:
                id_para_bd = int(doctor_encontrado.num_junta_medica)
            except ValueError:
                QMessageBox.critical(
                    self.vista, 
                    "❌ Error", 
                    f"Error al convertir el ID del doctor: {doctor_encontrado.num_junta_medica}"
                )
                return
            
            print(f"🔍 Buscando citas para doctor con ID: {id_para_bd}")
            citas = Doctor.obtener_citas_por_doctor(id_para_bd)
            
            # Mostrar resultados
            self.vista.resultado_text.clear()
            
            if not citas:
                self.vista.resultado_text.append(
                    f"📅 CITAS DEL DR. {doctor_encontrado.nombre.upper()} {doctor_encontrado.apellido.upper()}\n"
                    f"Nº Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                    f"Especialidad: {doctor_encontrado.especialidad}\n"
                    f"{'='*70}\n\n"
                    f"❌ NO TIENE CITAS REGISTRADAS\n\n"
                    f"El Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido} "
                    f"no tiene citas programadas en este momento."
                )
                QMessageBox.information(
                    self.vista, 
                    "ℹ️ Sin Citas", 
                    f"El Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido} no tiene citas registradas."
                )
            else:
                self.vista.resultado_text.append(
                    f"📅 CITAS DEL DR. {doctor_encontrado.nombre.upper()} {doctor_encontrado.apellido.upper()}\n"
                    f"Nº Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                    f"Especialidad: {doctor_encontrado.especialidad}\n"
                    f"{'='*70}\n\n"
                    f"✅ TOTAL DE CITAS ENCONTRADAS: {len(citas)}\n"
                    f"{'='*70}\n\n"
                )
                
                # Mostrar cada cita
                for i, cita in enumerate(citas, 1):
                    try:
                        if isinstance(cita['fecha'], str):
                            fecha_str = cita['fecha']
                        else:
                            fecha_str = cita['fecha'].strftime('%d/%m/%Y')
                    except:
                        fecha_str = str(cita['fecha'])
                    
                    self.vista.resultado_text.append(
                        f"🏥 CITA #{i}\n"
                        f"{'─'*50}\n"
                        f"📅 Fecha: {fecha_str}\n"
                        f"🕐 Hora: {cita['hora_inicio']} - {cita['hora_fin']}\n"
                        f"👤 Paciente: {cita['paciente_nombre']} {cita['paciente_apellido']}\n"
                        f"🩺 Tratamiento: {cita['tratamiento_descripcion']}\n"
                        f"💰 Costo Consulta: {cita['costo']}\n"
                        f"💵 Costo Tratamiento: {cita['tratamiento_costo']}\n"
                        f"📋 Estado: {cita['estado']}\n"
                        f"📞 Teléfono Paciente: {cita['paciente_telefono']}\n"
                        f"🆔 DUI Paciente: {cita['paciente_dui']}\n"
                        f"📅 Fecha: {cita['fecha']}\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    )
                
                QMessageBox.information(
                    self.vista, 
                    "✅ Citas Encontradas", 
                    f"Se encontraron {len(citas)} cita(s) para el Dr. {doctor_encontrado.nombre} {doctor_encontrado.apellido}."
                )
                
        except Exception as e:
            print(f"❌ Error al obtener citas: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.vista, 
                "❌ Error", 
                f"Error al obtener las citas del doctor:\n{str(e)}"
            )
            self.vista.resultado_text.append(f"❌ Error al obtener citas: {str(e)}")

    def obtener_doctores(self):
        try:
            # Verificar conexión a la base de datos
            if not self.conexion_db:
                print("❌ No hay conexión a la base de datos")
                return []
            
            # Consulta SQL
            query = "SELECT * FROM doctores"
            resultado = self.conexion_db.execute(query).fetchall()
            
            print(f"🔍 Doctores encontrados: {len(resultado)}")
            for doctor in resultado:
                print(f"  - {doctor}")
                
            return resultado
            
        except Exception as e:
            print(f"❌ Error al obtener doctores: {e}")
            return []

    def mostrar_listado_doctores(self):
        print("🔍 [DEBUG] Iniciando mostrar_listado_doctores...")
        
        try:
            # Verificar si existe la conexión
            if not hasattr(self, 'conexion') or self.conexion is None:
                print("❌ [DEBUG] No hay conexión a la base de datos")
                self.mostrar_mensaje("Error", "No hay conexión a la base de datos")
                return
            
            print("✅ [DEBUG] Conexión existe")
            
            # Verificar si la tabla existe
            try:
                cursor = self.conexion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doctores'")
                tabla_existe = cursor.fetchone()
                if not tabla_existe:
                    print("❌ [DEBUG] La tabla 'doctores' no existe")
                    self.mostrar_mensaje("Error", "La tabla de doctores no existe")
                    return
                
                print("✅ [DEBUG] La tabla 'doctores' existe")
            except Exception as e:
                print(f"❌ [DEBUG] Error verificando tabla: {e}")
            
            # Contar registros
            try:
                cursor = self.conexion.execute("SELECT COUNT(*) FROM doctores")
                count = cursor.fetchone()[0]
                print(f"📊 [DEBUG] Total de doctores en la tabla: {count}")
                
                if count == 0:
                    print("⚠️ [DEBUG] La tabla está vacía")
                    self.mostrar_mensaje("Información", "No hay doctores registrados")
                    return
                    
            except Exception as e:
                print(f"❌ [DEBUG] Error contando registros: {e}")
                self.mostrar_mensaje("Error", f"Error al consultar la base de datos: {e}")
                return
            
            # Obtener los doctores
            try:
                cursor = self.conexion.execute("SELECT * FROM doctores")
                doctores = cursor.fetchall()
                print(f"📋 [DEBUG] Doctores obtenidos: {len(doctores)}")
                
                for i, doctor in enumerate(doctores):
                    print(f"  {i+1}. {doctor}")
                
                # Aquí deberías mostrar los doctores en tu interfaz
                # self.mostrar_doctores_en_interfaz(doctores)
                
            except Exception as e:
                print(f"❌ [DEBUG] Error obteniendo doctores: {e}")
                self.mostrar_mensaje("Error", f"Error al obtener doctores: {e}")
                
        except Exception as e:
            print(f"❌ [DEBUG] Error general: {e}")
            self.mostrar_mensaje("Error", f"Error inesperado: {e}")
            
def main():
    """Función principal para ejecutar el controlador de doctores"""
    from PyQt6.QtWidgets import QApplication
    from Vistas.DoctorVista import DoctorWindow

    app = QApplication([])
    window = DoctorWindow()
    controlador = ControladorDoctor(window)
    window.show()
    app.exec()  # Sin sys.exit() para permitir continuar

if __name__ == "__main__":
    main()
