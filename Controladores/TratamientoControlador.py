from Modelos.Tratamiento import Tratamiento
from Modelos.Tratamiento import Doctor

class TratamientoControlador:
    def __init__(self, vista):
        self.vista = vista
        self.paciente = vista.paciente

    def crear_tratamiento(self, id_tratamiento, descripcion, costo, fecha, estado, doctor_nombre, doctor_apellido, paciente):
        doctor = Doctor(doctor_nombre, doctor_apellido)
        return Tratamiento(
            id_tratamiento=id_tratamiento,
            descripcion=descripcion,
            costo=costo,
            fecha=fecha,
            estado=estado,
            doctor=doctor,
            paciente=paciente
        )
