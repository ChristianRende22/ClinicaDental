class Doctor:
    def __init__(self, nombre, apellido, dui, especialidad, telefono, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.dui = dui
        self.especialidad = especialidad
        self.telefono = telefono
        self.correo = correo
        self.citas = [] 
        self.horario = []

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.especialidad})"

    def mostrar_citas(self, resultado_text):
        """Muestra todas las citas asociadas a este doctor en el QTextEdit resultado_text."""
        if not self.citas:
            resultado_text.append(f"No hay citas registradas para el Dr. {self.nombre} {self.apellido}.")
            return
        resultado_text.append(f"Citas del Dr. {self.nombre} {self.apellido}:")
        for cita in self.citas:
            resultado_text.append(str(cita))
        resultado_text.append("")
