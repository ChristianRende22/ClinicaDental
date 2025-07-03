from PyQt6.QtWidgets import QApplication
import sys
from modelo import HorarioModel
from vista import HorarioView

class HorarioController:
    def __init__(self):
        self.modelo = HorarioModel()
        self.vista = HorarioView()
        # Inicializar datos
        self.modelo.cargar_doctores()
        # Conectar vista con controlador
        self.vista.conectar_controlador(self)
        # Actualizar vista inicial
        self.actualizar_vista()
    
    def agregar_horario(self):
        # agregar un nuevo horario
        try:
            # Obtener doctores del modelo
            doctores = self.modelo.obtener_doctores()
            # Mostrar diálogo y obtener datos
            datos = self.vista.mostrar_dialogo_agregar(doctores)
            if datos and all(datos.values()):
                # Agregar horario al modelo
                self.modelo.agregar_horario(
                    datos['id_horario'],
                    datos['dia'],
                    datos['hora_inicio'],
                    datos['hora_fin'],
                    datos['doctor'] )
                # Actualizar vista
                self.actualizar_vista()
                
                # Mostrar mensaje de exito
                self.vista.mostrar_mensaje("Exito", "Horario agregado correctamente", "success")
            elif datos:  # Si se recibieron datos pero están incompletos
                self.vista.mostrar_mensaje("Error", "Todos los campos son obligatorios", "error")
                
        except ValueError as e:
            self.vista.mostrar_mensaje("Error", str(e), "error")
        except Exception as e:
            self.vista.mostrar_mensaje("Error", f"Error al agregar horario: {str(e)}", "error")
    
    def eliminar_horario(self):
        #eliminar un horario
        try:
            # Obtener horarios del modelo
            horarios = self.modelo.obtener_horarios()
            if not horarios:
                self.vista.mostrar_mensaje("Error", "No hay horarios registrados", "error")
                return
            # Preparar informacion para el dialogo
            horarios_info = self.vista.obtener_info_horarios_para_eliminar(horarios) 
            # Mostrar dialogo y obtener seleccion
            id_horario = self.vista.mostrar_dialogo_eliminar(horarios_info)
            
            if id_horario:
                # Eliminar del modelo
                if self.modelo.eliminar_horario(id_horario):
                    # Actualizar vista
                    self.actualizar_vista()
                    # Mostrar mensaje de éxito
                    self.vista.mostrar_mensaje("Éxito", "Horario eliminado correctamente", "success")
                else:
                    self.vista.mostrar_mensaje("Error", "No se pudo eliminar el horario", "error")
                    
        except Exception as e:
            self.vista.mostrar_mensaje("Error", f"Error al eliminar horario: {str(e)}", "error")
    
    def actualizar_vista(self):
        #Actualiza la vista con los datos del modelo
        horarios_por_dia = self.modelo.obtener_horarios_agrupados_por_dia()
        self.vista.actualizar_lista_horarios(horarios_por_dia)
    
    def mostrar_ventana(self):
        #ventana principal
        self.vista.show()
    def obtener_vista(self):
        #retorna la vista para acceso externo si es necesario
        return self.vista

def main():
    app = QApplication(sys.argv)
    # Crear controlador (que inicializa modelo y vista)
    controlador = HorarioController()
    # Mostrar ventana
    controlador.mostrar_ventana()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
