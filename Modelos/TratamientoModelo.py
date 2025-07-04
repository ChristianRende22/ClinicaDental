class Tratamiento:
    def __init__(self, id_tratamiento, descripcion, costo, fecha, estado, doctor, paciente):
        self.id_tratamiento = id_tratamiento
        self.descripcion = descripcion
        self.costo = costo
        self.fecha = fecha
        self.estado = estado
        self.doctor = doctor
        self.paciente = paciente

    def __str__(self):
        return (f"Tratamiento ID: {self.id_tratamiento} \n " 
                f"Descripción: '{self.descripcion}' \n "
                f"Costo: ${self.costo:,.2f} \n " 
                f"Fecha de realización: {self.fecha} \n " 
                f"Estado: '{self.estado}' \n "
                f"Doctor: {self.doctor} \n " 
                f"Paciente: {self.paciente.nombre} {self.paciente.apellido}")
