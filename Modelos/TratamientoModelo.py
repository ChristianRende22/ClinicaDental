class Paciente:
    def __init__(self, id_paciente, nombre, apellido, edad, genero, telefono, correo, direccion):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self):
        return f"{self.nombre} {self.apellido}, {self.edad} años"


class Doctor:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"


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
