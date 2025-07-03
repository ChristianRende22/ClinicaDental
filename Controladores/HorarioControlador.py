from PyQt6.QtWidgets import QApplication
from modelo import cargar_doctores, Horario
from vista import HorarioWindow, AgregarHorarioDialog

class Controlador:
    def __init__(self):
        self.doctores = cargar_doctores()
        self.horarios = []
        self.window = HorarioWindow(self.doctores)
        self.window.btn_agregar.clicked.connect(self.agregar_horario)
        self.window.btn_eliminar.clicked.connect(self.eliminar_horario)

    def agregar_horario(self):
        dialog = AgregarHorarioDialog(self.doctores, self.window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                datos = dialog.get_data()
                if not all(datos.values()):
                    self.window.mostrar_error("Error", "Todos los campos son obligatorios")
                    return   
                # Validaciones
                datetime.strptime(datos['hora_inicio'], "%H:%M")
                datetime.strptime(datos['hora_fin'], "%H:%M")
        
                if any(h.id_horario == datos['id_horario'] for h in self.horarios):
                    self.window.mostrar_error("Error", "El ID de horario ya existe")
                    return
        
                nuevo_horario = Horario(**datos)
                for horario_existente in self.horarios:
                    if nuevo_horario.horario_ocupado(horario_existente):
                        self.window.mostrar_error("Error", "El horario ya está ocupado")
                        return
                self.horarios.append(nuevo_horario)
                self.window.actualizar_lista(self.horarios)
                self.window.mostrar_mensaje("Éxito", "Horario agregado correctamente")
            except ValueError as e:
                self.window.mostrar_error("Error", f"Formato de hora inválido: {str(e)}")
            except Exception as e:
                self.window.mostrar_error("Error", f"Error al agregar horario: {str(e)}")

    def eliminar_horario(self):
        """Elimina un horario existente"""
        if not self.horarios:
            self.window.mostrar_error("Error", "No hay horarios registrados")
            return
        items = [f"{h.id_horario} | {h.dia} {h.hora_inicio}-{h.hora_fin} (Dr. {h.doctor.nombre})" 
                for h in self.horarios]
        item, ok = QInputDialog.getItem(
            self.window, "Eliminar Horario", 
            "Seleccione un horario a eliminar:", items, 0, False
        )
        
        if ok and item:
            id_horario = item.split(" | ")[0]
            confirm = QMessageBox.question(
                self.window, "Confirmar",
                f"¿Eliminar el horario {id_horario}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.horarios = [h for h in self.horarios if h.id_horario != id_horario]
                self.window.actualizar_lista(self.horarios)
                self.window.mostrar_mensaje("Éxito", "Horario eliminado")

if __name__ == "__main__":
    app = QApplication([])
    controlador = Controlador()
    controlador.window.show()
    app.exec()
