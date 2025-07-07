from Modelos.DoctorModelo import Doctor
from Modelos.TratamientoModelo import Tratamiento

class TratamientoControlador:
    def __init__(self, vista):
        self.vista = vista
        self.paciente = vista.paciente

    def crear_tratamiento(self, id_tratamiento, descripcion, costo, fecha, estado, doctor_nombre, doctor_apellido, paciente):
        
        doctor = Doctor(doctor_nombre, doctor_apellido, dui=None, especialidad=None, telefono=None, correo=None)
        
        return Tratamiento(
            id_tratamiento=id_tratamiento,
            descripcion=descripcion,
            costo=costo,
            fecha=fecha,
            estado=estado,
            doctor=doctor,
            paciente=paciente
        )
        
    def verificar_doctor(self, carnet):
        if not carnet:
            self.vista.mostrar_mensaje("Validación", "Ingrese el carnet del doctor.")
            return None
        
        doctores_simulados = {
            "DOC123": "Juan Pérez",
            "DOC456": "María López",
            "DOC789": "Carlos Gómez"
        }
        
        nombre = doctores_simulados.get(carnet)
        if nombre:
            self.vista.mostrar_nombre_doctor(f"Nombre Doctor: {nombre}")
            return nombre
        else:
            self.vista.mostrar_nombre_doctor("Doctor no encontrado, debe registrarlo.")
            respuesta = self.vista.preguntar_registro_doctor()
            if respuesta:
                self.vista.abrir_registro_doctor()
            return None
        
    def validar_datos(self, tratamiento, costo, fecha, estado, carnet_doctor, nombre_doctor):
        errores = []

        # Validar tratamiento
        if not tratamiento:
            errores.append("Debe seleccionar un tratamiento.")

        # Validar costo
        if costo <= 0:
            errores.append("El costo debe ser mayor a cero.")

        # Validar fecha (asumimos fecha es QDate)
        if not fecha or not fecha.isValid():
            errores.append("Debe seleccionar una fecha válida.")

        # Validar estado
        estados_validos = ['Pendiente', 'En_Progreso', 'Finalizado']
        if estado not in estados_validos:
            errores.append(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")

        # Validar carnet y nombre doctor
        if not carnet_doctor:
            errores.append("Debe ingresar el carnet del doctor.")
        if not nombre_doctor or nombre_doctor.startswith("Doctor no encontrado"):
            errores.append("Debe verificar un doctor válido.")

        if errores:
            self.vista.mostrar_mensaje("Errores de Validación", "\n".join(errores))
            return False

        return True
