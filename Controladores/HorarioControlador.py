import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from typing import List

from Modelos.HorarioModelo import Horario, HorarioModel
from Modelos.DoctorModelo import Doctor 
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QApplication
from PyQt6.QtCore import QDateTime 

class HorarioController:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = HorarioModel() 
        
        # Cargar doctores desde la base de datos
        self.doctores = []
        self.cargar_datos_desde_bd()
        self.inicializar_vista()
        
    def cargar_datos_desde_bd(self):
        """Carga todos los datos necesarios desde la base de datos"""
        try:
            # Cargar doctores desde la base de datos
            self.doctores = self.modelo.obtener_doctores()
            print(f"Doctores cargados desde BD: {len(self.doctores)}")
            
        except Exception as e:
            print(f"Error al cargar datos desde BD: {e}")
            # Doctores de respaldo si hay error en la BD
            self.doctores = [
                Doctor("Melisa", "Rivas", "12345678-9", "Cirujano Dentista", 12345678, "correo@gmail.com"),
                Doctor("Carlos", "López", "98765432-1", "Ortodontista", 87654321, "correo1@gmail.com")
            ]
        
    def inicializar_vista(self):
        """Inicializa la vista con los datos del controlador."""
        self.vista.actualizar_combos(self.doctores)
        self.actualizar_vista()

    def agregar_horario(self):
        """Agrega un nuevo horario después de validaciones."""
        try:
            # Generar el siguiente ID automáticamente
            siguiente_id = self.modelo.generar_siguiente_id()
            print(f"ID generado automáticamente: {siguiente_id}")
            
            # Mostrar IDs existentes para debugging
            ids_existentes = self.modelo.obtener_ids_existentes()
            print(f"IDs existentes en BD: {ids_existentes}")
            
            datos = self.vista.mostrar_dialogo_agregar(self.doctores, siguiente_id)
            if not datos: 
                return
            
            # Validaciones de campos obligatorios
            if not all([datos['id_horario'], datos['hora_inicio'], datos['hora_fin'], datos['doctor']]):
                QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios.")
                return

            id_horario = datos['id_horario']
            hora_inicio = datos['hora_inicio']
            hora_fin = datos['hora_fin']
            doctor = datos['doctor'] 

            # Validar formato de hora 
            try:
                datetime.strptime(hora_inicio, "%H:%M")
                datetime.strptime(hora_fin, "%H:%M")
            except ValueError:
                QMessageBox.warning(self.vista, "❌ Error", "Formato de hora inválido. Use HH:MM (ej. 09:00).")
                return
            
            # Validar que la hora de inicio sea anterior a la hora de fin
            if datetime.strptime(hora_inicio, "%H:%M") >= datetime.strptime(hora_fin, "%H:%M"):
                QMessageBox.warning(self.vista, "❌ Error", "La hora de fin debe ser posterior a la hora de inicio.")
                return

            # Validar ID único usando el nuevo método del modelo
            if not self.modelo.verificar_id_disponible(id_horario):
                QMessageBox.warning(self.vista, "❌ Error", 
                                  f"El ID de horario '{id_horario}' ya existe.\n"
                                  f"IDs existentes: {', '.join(ids_existentes)}")
                return

            # Crear el nuevo objeto Horario
            nuevo_horario = Horario(id_horario, hora_inicio, hora_fin, doctor)

            # Validar conflicto de horarios 
            horarios_existentes = self.modelo.obtener_horarios()
            for horario_existente in horarios_existentes:
                if nuevo_horario.horario_ocupado(horario_existente):
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      f"El doctor {doctor.nombre} {doctor.apellido} ya tiene un horario "
                                      f"ocupado en ese rango de horas.")
                    return
            
            # Si todas las validaciones pasan, agregar al modelo (que insertará en BD)
            if self.modelo.agregar_horario(nuevo_horario):
                # Actualizar vista
                self.actualizar_vista()
                QMessageBox.information(self.vista, "✅ Éxito", 
                                      f"Horario agregado correctamente en la base de datos.\n"
                                      f"ID: {nuevo_horario.id_horario}\n"
                                      f"Siguiente ID disponible será: {self.modelo.generar_siguiente_id()}")
            else:
                QMessageBox.critical(self.vista, "❌ Error", 
                                   "Error al guardar el horario en la base de datos.")
                                   
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", f"Error al agregar horario: {str(e)}")
    
    def eliminar_horario(self):
        """Elimina un horario."""
        try:
            # Obtener horarios actualizados de la base de datos
            horarios = self.modelo.obtener_horarios()
            if not horarios:
                QMessageBox.information(self.vista, "ℹ️ Información", "No hay horarios registrados para eliminar.")
                return
            
            # Obtener el ID del horario a eliminar de la vista
            id_horario = self.vista.mostrar_dialogo_eliminar(self.vista.obtener_info_horarios_para_eliminar(horarios))
            if id_horario: 
                if self.modelo.eliminar_horario(id_horario):
                    self.actualizar_vista()
                    QMessageBox.information(self.vista, "✅ Éxito", 
                                          f"Horario {id_horario} eliminado correctamente de la base de datos.")
                else:
                    QMessageBox.warning(self.vista, "❌ Error", 
                                      "No se pudo eliminar el horario de la base de datos.")
                    
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", f"Error al eliminar horario: {str(e)}")
    
    def actualizar_vista(self):
        """Actualiza la vista con los datos del modelo."""
        horarios_por_dia = self.modelo.obtener_horarios_agrupados_por_dia()
        self.vista.actualizar_lista_horarios(horarios_por_dia)

    def recargar_datos(self):
        """Recarga todos los datos desde la base de datos"""
        self.cargar_datos_desde_bd()
        self.actualizar_vista()
 
def main():
    """Función principal para ejecutar el controlador de horarios"""
    from Vistas.HorarioVista import HorarioView
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication([])
    window = HorarioView()
    controller = HorarioController(window)
    window.show()
    app.exec()  # Sin sys.exit() para permitir continuar

if __name__ == "__main__":
    main()
