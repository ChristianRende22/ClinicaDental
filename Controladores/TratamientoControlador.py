import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Modelos.TratamientoModelo import Tratamiento
from Vistas.TratamientoVista import AgregarTratamientoDialog
from PyQt6.QtWidgets import QApplication, QDialog

class TratamientoControlador:
    def __init__(self, doctor):
        self.doctor = doctor
        self.vista = None 
        
    def mostrar_vista(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication([])  # Creas QApplication si no existe

        if self.vista is None:
            self.vista = AgregarTratamientoDialog(controlador=self)

        resultado = self.vista.exec()
        # if resultado == QDialog.accepted:
        #     print("Tratamiento agregado correctamente")
        # else:
        #     print("Cancelado o cerrado")

    def crear_tratamiento(self, descripcion, costo, fecha, id_doctor):
        # No creamos un objeto completo, solo los datos necesarios para guardar.
        # La creación real es en insertar_tratamiento
        return {
            'descripcion': descripcion,
            'costo': costo,
            'fecha': fecha,
            'id_doctor': id_doctor
        }
        
    def verificar_doctor(self, carnet):
        if not carnet:
            self.vista.mostrar_mensaje("Validación", "Ingrese el carnet (ID_Doctor).")
            return None

        nombre, apellido = Tratamiento.buscar_doctor_por_codigo(carnet)
        if nombre and apellido:
            self.vista.mostrar_nombre_doctor(f"Nombre Doctor: {nombre} {apellido}")
            return (nombre, apellido)
        else:
            self.vista.mostrar_nombre_doctor("Doctor no encontrado, debe registrarlo.")
            respuesta = self.vista.preguntar_registro_doctor()
            if respuesta:
                self.vista.abrir_registro_doctor()
            return None
        
    def validar_datos(self, descripcion, costo, fecha, carnet_doctor):
        errores = []

        if not descripcion or descripcion.strip() == "":
            errores.append("Debe ingresar la descripción del tratamiento.")

        if costo <= 0:
            errores.append("El costo debe ser mayor a cero.")

        if not fecha or not fecha.isValid():
            errores.append("Debe seleccionar una fecha válida.")

        if not carnet_doctor:
            errores.append("Debe ingresar el carnet del doctor.")

        if errores:
            self.vista.mostrar_mensaje("Errores de Validación", "\n".join(errores))
            return False

        return True
    
    def guardar_tratamiento(self, descripcion, costo, fecha, carnet_doctor):
        id_tratamiento = Tratamiento.insertar_tratamiento(
            id_doctor= carnet_doctor,
            descripcion=descripcion,
            costo=costo,
            fecha=fecha
        )
        return id_tratamiento

def main():
    """Función principal para ejecutar el controlador de tratamientos"""
    from PyQt6.QtWidgets import QApplication
    from Vistas.TratamientoVista import AgregarTratamientoDialog

    # Usar la instancia existente de QApplication si existe
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    controlador = TratamientoControlador(doctor=None)
    vista = AgregarTratamientoDialog(controlador=controlador)
    vista.show()
    app.exec()  # Sin sys.exit() para permitir continuar
    

if __name__ == "__main__":
    main()
