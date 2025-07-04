from datetime import datetime
from typing import List

# class Doctor:
#     def __init__(self, id_doctor: str, nombre: str, especialidad: str):
#         self.id_doctor = id_doctor
#         self.nombre = nombre
#         self.especialidad = especialidad
#     def __str__(self):
#         return f"{self.nombre} ({self.especialidad})"

from Modelos.DoctorModelo import Doctor

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

class HorarioModel:
    def __init__(self):
        self.horarios: List[Horario] = []
        self.doctores: List[Doctor] = []
    
    def cargar_doctores(self):
        #Función para cargar doctores - será reemplazada por conexión a BD
        self.doctores = [
            Doctor("D001", "Dra. Pérez", "Odontología"),
            Doctor("D002", "Dr. Gómez", "Ortodoncia"),
            Doctor("D003", "Dra. Martínez", "Cirugía Maxilofacial")
        ]
        return self.doctores
    
    def agregar_horario(self, id_horario: str, dia: str, hora_inicio: str, hora_fin: str, doctor: Doctor):
        """Agrega un nuevo horario después de validaciones"""
        # Validar formato de hora
        try:
            datetime.strptime(hora_inicio, "%H:%M")
            datetime.strptime(hora_fin, "%H:%M")
        except ValueError:
            raise ValueError("Formato de hora inválido. Use HH:MM")
        # Validar ID unico
        if any(h.id_horario == id_horario for h in self.horarios):
            raise ValueError("El ID de horario ya existe")
        # Crear nuevo horario
        nuevo_horario = Horario(id_horario, dia, hora_inicio, hora_fin, doctor)
        # Validar conflictos de horario
        for horario_existente in self.horarios:
            if nuevo_horario.horario_ocupado(horario_existente):
                raise ValueError("El horario ya está ocupado")
        self.horarios.append(nuevo_horario)
        return nuevo_horario
    
    def eliminar_horario(self, id_horario: str):
        #Elimina un horario por ID
        horario_eliminado = None
        for horario in self.horarios:
            if horario.id_horario == id_horario:
                horario_eliminado = horario
                break
        if horario_eliminado:
            self.horarios.remove(horario_eliminado)
            return True
        return False
        
    def obtener_horarios(self):
        #Retorna todos los horarios
        return self.horarios.copy()
    
    def obtener_doctores(self):
        #Retorna todos los doctores
        return self.doctores.copy()
    
    def obtener_horarios_agrupados_por_dia(self):
        #Retorna horarios agrupados por dia
        horarios_por_dia = {}
        for horario in sorted(self.horarios, key=lambda h: h.dia):
            if horario.dia not in horarios_por_dia:
                horarios_por_dia[horario.dia] = []
            horarios_por_dia[horario.dia].append(horario)
        return horarios_por_dia
