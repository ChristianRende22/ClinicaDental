from typing import List
class Doctor:
    def __init__(self, id_doctor: str, nombre: str, especialidad: str):
        self.id_doctor = id_doctor
        self.nombre = nombre
        self.especialidad = especialidad
    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"

class Horario:
    def __init__(self, id_horario: str, dia: str, hora_inicio: str, hora_fin: str, doctor: Doctor):
        self.id_horario = id_horario
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.doctor = doctor
        self.disponible = True

    def __str__(self):
        status = "✅ Disponible" if self.disponible else "❌ Ocupado"
        return (f"🆔 ID Horario: {self.id_horario}\n"
                f"📅 Día: {self.dia} | ⏰ {self.hora_inicio} - {self.hora_fin}\n"
                f"👨‍⚕️ Médico: {self.doctor}\n"
                f" {status}\n"
                )

    def horario_ocupado(self, otro_horario):
        if self.doctor.id_doctor != otro_horario.doctor.id_doctor or self.dia != otro_horario.dia:
            return False
        def hora_a_minutos(hora):
            h, m = map(int, hora.split(':'))
            return h * 60 + m
    
        inicio1 = hora_a_minutos(self.hora_inicio)
        fin1 = hora_a_minutos(self.hora_fin)
        inicio2 = hora_a_minutos(otro_horario.hora_inicio)
        fin2 = hora_a_minutos(otro_horario.hora_fin)
        return max(inicio1, inicio2) < min(fin1, fin2)

def cargar_doctores() -> List[Doctor]:
    """Función de ejemplo para cargar doctores"""
    return [
        Doctor("D001", "Dra. Pérez", "Odontología"),
        Doctor("D002", "Dr. Gómez", "Ortodoncia"),
        Doctor("D003", "Dra. Martínez", "Cirugía Maxilofacial")
    ]
