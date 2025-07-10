from datetime import date, time

class Cita:
    """
    Clase que representa una cita en la clínica dental.
    Contiene información sobre el paciente, el doctor, el horario y el estado de la cita.
    """
    def __init__(self, id_cita: str, paciente, doctor, fecha: date, hora_inicio: time, hora_fin: time, costo_cita: float):
        self.id_cita = id_cita                  # Identificador único de la cita
        self.paciente = paciente                # Paciente asociado a la cita
        self.doctor = doctor                    # Doctor asociado a la cita
        self.fecha = fecha                      # Fecha de la cita
        self.hora_inicio = hora_inicio          # Hora de inicio de la cita
        self.hora_fin = hora_fin                # Hora de fin de la cita
        self.costo_cita = costo_cita            # Costo de la cita
        self.estado = "Pendiente"               # Por defecto, la cita está pendiente

    def __str__(self):
        return (
            f"ID Cita: {self.id_cita}\n"
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\n"
            f"Doctor: {self.doctor.nombre} {self.doctor.apellido}\n"
            f"Fecha: {self.fecha.strftime('%d/%m/%Y')}\n"
            f"Hora Inicio: {self.hora_inicio.strftime('%H:%M')}\n"
            f"Hora Fin: {self.hora_fin.strftime('%H:%M')}\n"      
            f"Estado: {self.estado}\n"
            f"Costo: ${self.costo_cita:.2f}\n"
        )
