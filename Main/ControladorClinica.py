# Script consolidado que ejecuta todos los controladores
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Controladores.CitaControlador as ej1
import Controladores.DoctorControlador as ej2
import Controladores.FacturaControlador as ej3
import Controladores.HorarioControlador as ej4
import Controladores.LoginControlador as ej5
import Controladores.MenuControlador as ej6
import Controladores.PacienteControlador as ej7
import Controladores.TratamientoControlador as ej8

# Script consolidado que ejecuta todos los controladores
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication

import Controladores.CitaControlador as Cita
import Controladores.DoctorControlador as Dcotor
import Controladores.FacturaControlador as Factura
import Controladores.HorarioControlador as Horario
import Controladores.LoginControlador as Login
import Controladores.MenuControlador as Menu
import Controladores.PacienteControlador as Paciente
import Controladores.TratamientoControlador as Tratamiento
def ejecutar_controlador_secuencial(modulo, nombre):
    """Ejecuta un controlador y espera a que se cierre para continuar"""
    print(f"====== {nombre} ======")
    try:
        # Ejecutar el controlador - cada uno maneja su propia QApplication
        modulo.main()
        print(f"✅ {nombre} completado")
        
    except Exception as e:
        print(f"❌ Error en {nombre}: {e}")


def main():
    """Función principal que ejecuta todos los controladores en secuencia"""
    print("🚀 Iniciando ejecución secuencial de controladores...")
    print("📋 Se ejecutará un controlador a la vez. Cierre la ventana para continuar al siguiente.\n")
    
    controladores = [        
        (Login, " - Sistema de Login"),        
        (Menu, " - Menú Principal"),
        (Cita, " - Gestión de Citas"),        
        (Paciente, " - Gestión de Pacientes"),
        (Dcotor, " - Gestión de Doctores"), 
        (Factura, " - Gestión de Facturas"),
        (Horario, "  - Gestión de Horarios"),
        (Tratamiento, " - Gestión de Tratamientos")
    ]
    
    for modulo, nombre in controladores:
        ejecutar_controlador_secuencial(modulo, nombre)
        print(f"🔄 Continuando al siguiente controlador...\n")
    
    print("🎉 Todos los controladores han sido ejecutados!")

if __name__ == "__main__":
    main()
