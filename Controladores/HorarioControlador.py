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
        
        self.doctores = [
            Doctor("Melisa", "Rivas", "12345678-9", "Cirujano Dentista", 12345678, "correo@gmail.com"),
            Doctor("Carlos", "López", "98765432-1", "Ortodontista", 87654321, "coreo1@gmail.com")
        ]
        self.inicializar_vista()
        
    def inicializar_vista(self):
        """Inicializa la vista con los datos del controlador."""
        self.vista.actualizar_combos(self.doctores) 

    def agregar_horario(self):
        """Agrega un nuevo horario después de validaciones."""
        try:
            datos = self.vista.mostrar_dialogo_agregar(self.doctores)
            if not datos: 
                return
            
            # Validaciones de campos obligatorios
            if not all(datos.values()):
                QMessageBox.warning(self.vista, "❌ Error", "Todos los campos son obligatorios.")
                return

            id_horario = datos['id_horario']
            dia = datos['dia']
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

            # Validar ID único
            if any(h.id_horario == id_horario for h in self.modelo.obtener_horarios()):
                QMessageBox.warning(self.vista, "❌ Error", "El ID de horario ya existe.")
                return
            # Crear el nuevo objeto Horario
            nuevo_horario = Horario(id_horario, dia, hora_inicio, hora_fin, doctor)

            # Validar existencia de horario 
            for horario_existente in self.modelo.obtener_horarios():
                if nuevo_horario.horario_ocupado(horario_existente):
                    QMessageBox.warning(self.vista, "❌ Error", "El doctor ya tiene un horario ocupado en ese día y rango de horas.")
                    return
            
            # Si todas las validaciones pasan, agregar al modelo
            self.modelo.agregar_horario(nuevo_horario)
            # Actualizar vista
            self.actualizar_vista()
            QMessageBox.information(self.vista, "✅ Éxito", "Horario agregado correctamente.")       
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", f"Error al agregar horario: {str(e)}")
    
    def eliminar_horario(self):
        """Elimina un horario."""
        try:
            horarios = self.modelo.obtener_horarios()
            if not horarios:
                QMessageBox.information(self.vista, "ℹ️ Información", "No hay horarios registrados para eliminar.")
                return
            
            # Obtener el ID del horario a eliminar de la vista
            id_horario = self.vista.mostrar_dialogo_eliminar(self.vista.obtener_info_horarios_para_eliminar(horarios))
            if id_horario: 
                if self.modelo.eliminar_horario(id_horario):
                    self.actualizar_vista()
                    QMessageBox.information(self.vista, "✅ Éxito", "Horario eliminado correctamente.")
                else:
                    QMessageBox.warning(self.vista, "❌ Error", "No se encontró el horario para eliminar.")
                    
        except Exception as e:
            QMessageBox.critical(self.vista, "❌ Error", f"Error al eliminar horario: {str(e)}")
    
    def actualizar_vista(self):
        """Actualiza la vista con los datos del modelo."""
        horarios_por_dia = self.modelo.obtener_horarios_agrupados_por_dia()
        self.vista.actualizar_lista_horarios(horarios_por_dia)
 
if __name__ == "__main__":
    from Vistas.HorarioVista import HorarioView # Importar la vista
    app = QApplication(sys.argv)
    window = HorarioView()
    controller = HorarioController(window) # Pasar la instancia de la vista al controlador
    window.show()
    sys.exit(app.exec())
