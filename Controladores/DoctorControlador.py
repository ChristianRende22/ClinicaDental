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
                    num_junta_medica=doctor_dict['num_junta_medica'],
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
                if not all([data['id_horario'], data['hora_inicio'], data['hora_fin'], data['doctor']]):
                    QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios")
                    return
                
                # Mostrar el resultado en el área de texto
                self.vista.resultado_text.append(f"""
🕒 Horario agregado exitosamente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ID Horario: {data['id_horario']}
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
            print(f"Error detallado: {e}") 

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
        Si no se encuentra el doctor, muestra un mensaje de error.
        """
        self.vista.resultado_text.clear()

        if not self.doctores:
            QMessageBox.information(self.vista, "ℹ️ Información", "No hay doctores registrados")
            return

        num_junta_medica_a_eliminar, ok = QInputDialog.getText(self.vista, "Eliminar Doctor", "Ingrese el DUI del doctor a eliminar:")
        if not ok or not num_junta_medica_a_eliminar.strip():
            return

        num_junta_medica_a_eliminar = num_junta_medica_a_eliminar.strip()
        for doctor in self.doctores:
            if doctor['num_junta_medica'] == num_junta_medica_a_eliminar:
                self.doctores.remove(doctor)
                QMessageBox.information(self.vista, "✅ Éxito", f"Doctor con N° Junta Medica {num_junta_medica_a_eliminar} eliminado correctamente.")
                self.vista.resultado_text.append(f"Doctor eliminado: {doctor['nombre']} {doctor['apellido']} (N° Junta Medica: {num_junta_medica_a_eliminar})\n")
                return

        QMessageBox.warning(self.vista, "❌ Error", f"No se encontró ningún doctor con el N° Junta Medica: {num_junta_medica_a_eliminar}")
            

    def actualizar_info_doctor(self):
        """
        Si no estamos editando, pide el N° Junta Medica, busca el doctor y permite editar sus datos (excepto el N° Junta Medica).
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
                f"N° Junta Medica: {doctor['num_junta_medica']}\n"
                f"Nombre: {doctor['nombre']}\n"
                f"Apellido: {doctor['apellido']}\n"
                f"Especialidad: {doctor['especialidad']}\n"
                f"Teléfono: {doctor['telefono']}\n"
                f"Correo: {doctor['correo']}\n"
            )
            self.vista.num_junta_medica_edit.setReadOnly(False)
            self.editando_doctor = None  # Salimos del modo edición
            self.limpiar_campos()
            return

        # Si NO estamos editando, pedir N° Junta Medica y cargar datos
        num_junta_medica_a_buscar, ok = QInputDialog.getText(self.vista, "Buscar Doctor", "Ingrese el N° Junta Medica del doctor a modificar:")
        if not ok or not num_junta_medica_a_buscar.strip():
            return

        num_junta_medica_a_buscar = num_junta_medica_a_buscar.strip()
        for doctor in self.doctores:
            if doctor['num_junta_medica'] == num_junta_medica_a_buscar:
                # Llenar los campos con los datos encontrados
                self.vista.num_junta_medica_edit.setText(doctor['num_junta_medica'])
                self.vista.nombre_edit.setText(doctor['nombre'])
                self.vista.apellido_edit.setText(doctor['apellido'])
                self.vista.especialidad_edit.setText(doctor['especialidad'])
                self.vista.telefono_edit.setText(str(doctor['telefono']))
                self.vista.correo_edit.setText(doctor['correo'])
                self.vista.num_junta_medica_edit.setReadOnly(True)  # No permitir editar el Numero de junta medica

                self.editando_doctor = doctor  # Guardamos referencia para editar después

                QMessageBox.information(self.vista, "Editar Doctor", 
                    "Modifique los campos que desee y presione nuevamente 'Actualizar Info Doctor' para guardar los cambios.")
                return

        QMessageBox.warning(self.vista, "❌ Error", f"No se encontró ningún doctor con el N° Junta Medica: {num_junta_medica_a_buscar}")

    # Por el momento, no encontrara ninguna cita para el doctor, una vez se haya hecho la conexion con la base de datos será más fácil
    def ver_citas(self):
        """Ver las citas de un doctor específico por su número de junta médica"""
        self.vista.resultado_text.clear()
        
        try:
            # Primero mostrar todos los doctores disponibles
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
            self.vista.resultado_text.append("📋 DOCTORES DISPONIBLES:\n" + "="*50 + "\n")
            for doctor in doctores_bd:
                self.vista.resultado_text.append(
                    f"• N° Junta Médica: {doctor.num_junta_medica}\n"
                    f"  Nombre: Dr. {doctor.nombre} {doctor.apellido}\n"
                    f"  Especialidad: {doctor.especialidad}\n"
                    f"  {'-'*40}\n"
                )
            self.vista.resultado_text.append("\n")
            
            # Pedir el número de junta médica del doctor
            num_junta_medica, ok = QInputDialog.getText(
                self.vista, 
                "Ver Citas", 
                "Seleccione un N° Junta Médica de la lista anterior:"
            )
            
            if not ok or not num_junta_medica.strip():
                return
            
            num_junta_medica = num_junta_medica.strip()
            
            # Validar que sea un número
            try:
                num_junta_int = int(num_junta_medica)
            except ValueError:
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    "El número de junta médica debe ser un número válido"
                )
                return
            
            # Verificar que el doctor existe
            doctor_encontrado = None
            
            for doctor in doctores_bd:
                if doctor.num_junta_medica == num_junta_int:
                    doctor_encontrado = doctor
                    break
            
            if not doctor_encontrado:
                QMessageBox.warning(
                    self.vista, 
                    "❌ Error", 
                    f"No se encontró ningún doctor con el N° Junta Médica: {num_junta_medica}\n\n"
                    f"Doctores disponibles:\n" + 
                    "\n".join([f"• {d.num_junta_medica} - Dr. {d.nombre} {d.apellido}" for d in doctores_bd])
                )
                return
            
            # Obtener las citas del doctor
            print(f"🔍 Buscando citas para doctor ID: {num_junta_int}")
            citas = Doctor.obtener_citas_por_doctor(num_junta_int)
            
            # Limpiar y mostrar resultados
            self.vista.resultado_text.clear()
            
            # Mostrar resultados
            if not citas:
                self.vista.resultado_text.append(
                    f"📅 CITAS DEL DR. {doctor_encontrado.nombre.upper()} {doctor_encontrado.apellido.upper()}\n"
                    f"N° Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                    f"Especialidad: {doctor_encontrado.especialidad}\n"
                    f"{'='*60}\n\n"
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
                # Mostrar las citas encontradas
                self.vista.resultado_text.append(
                    f"📅 CITAS DEL DR. {doctor_encontrado.nombre.upper()} {doctor_encontrado.apellido.upper()}\n"
                    f"N° Junta Médica: {doctor_encontrado.num_junta_medica}\n"
                    f"Especialidad: {doctor_encontrado.especialidad}\n"
                    f"{'='*60}\n\n"
                    f"✅ TOTAL DE CITAS ENCONTRADAS: {len(citas)}\n"
                    f"{'='*60}\n"
                )
                
                # Mostrar cada cita
                for i, cita in enumerate(citas, 1):
                    self.vista.resultado_text.append(
                        f"🏥 CITA #{i}\n"
                        f"{'─'*40}\n"
                        f"• ID Cita: {cita['id_cita']}\n"
                        f"• Fecha: {cita['fecha']}\n"
                        f"• Horario: {cita['hora_inicio']} - {cita['hora_fin']}\n"
                        f"• Estado: {cita['estado']}\n"
                        f"• Paciente: {cita['paciente_nombre']} {cita['paciente_apellido']}\n"
                        f"• DUI Paciente: {cita['paciente_dui']}\n"
                        f"• Teléfono Paciente: {cita['paciente_telefono']}\n"
                        f"• Tratamiento: {cita['tratamiento_descripcion']}\n"
                        f"• Costo Consulta: {cita['costo']}\n"
                        f"• Costo Tratamiento: {cita['tratamiento_costo']}\n"
                        f"{'─'*40}\n\n"
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
                f"Error al obtener las citas del doctor:\n{str(e)}\n\n"
                "Verifique:\n"
                "• La conexión a la base de datos\n"
                "• Que la base de datos esté funcionando\n"
                "• Que existan doctores y citas registradas"
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
