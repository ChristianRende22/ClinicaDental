# CONTROLADORES
### ¿Que tiene que ir en el controlador?

Cada uno de las entidades llevara su propio controlador y dentro de este iran la clase de la entidad en donde iran los atributos de la clase y sus funciones respectivas. 

Las funciones que se pongan dentro de la clase seran las que se llamaran dentro de la vista de la entidad correspondiente. 

##### Por ejemplo
``` python
# Actualmente - DoctorVista.py
class Doctor:
    def __init__(self, nombre, apellido, dui, especialidad, telefono, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.dui = dui
        self.especialidad = especialidad
        self.telefono = telefono
        self.correo = correo
        self.citas: List["Cita"] = [] 
        self.horario = []
    # ... toda la logica de la vista

# Corregido - En DoctorControlador.py
class Doctor:
    def __init__(self, nombre, apellido, dui, especialidad, telefono, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.dui = dui
        self.especialidad = especialidad
        self.telefono = telefono
        self.correo = correo
        self.citas: List["Cita"] = [] 
        self.horario = []
    # ... metodos necesarios ...
    # Validadores y metodos como crear doctor, registrar horario, etc

```


Esto se repetira con todos los entidades

