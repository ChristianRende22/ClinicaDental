from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,      QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QListWidget, QDialog, QDialogButtonBox, QDoubleSpinBox,
                             QScrollArea, QScrollBar, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List
import re

# Clase temporal para representar el horario de atención del doctor
class Horario:
    """
    Clase que representa un horario de atención del doctor.
    Contiene información sobre el día de la semana y el rango de horas.
    """
    def __init__(self, dia: str, hora_inicio: datetime, hora_fin: datetime):
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __str__(self):
        return f"Horario{{dia='{self.dia}', hora_inicio={self.hora_inicio}, hora_fin={self.hora_fin}}}"

class AgregarHorarioDialog(QDialog):
    """
    Diálogo para agregar un horario de atención del doctor.
    Permite seleccionar el día de la semana y el rango de horas.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⌚ Agregar Horario")        
        self.setModal(True)
        self.resize(450, 350)
               
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #2b2b2b;
                font-family: 'Segoe UI';
                font-size: 14px;
                color: #ffffff;
            }}
            
            QLabel {{
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
            }}
            
            QLineEdit, QTextEdit, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus {{
                border-color: #10b8b9;
                background-color: #404040;
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #756f9f;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
            }}
            
            QPushButton:hover {{
                background-color: #10b8b9;
            }}
        """)

        self.dia_edit = QLineEdit(self)
        self.dia_edit.setPlaceholderText("Día de la semana (ej. Lunes)")
        
        self.hora_inicio_edit = QLineEdit(self)
        self.hora_inicio_edit.setPlaceholderText("Hora inicio (HH:MM)")
        
        self.hora_fin_edit = QLineEdit(self)
        self.hora_fin_edit.setPlaceholderText("Hora fin (HH:MM)")

        layout = QFormLayout()
        layout.addRow("🗓️ Día:", self.dia_edit)
        layout.addRow("⏰ Hora Inicio:", self.hora_inicio_edit)
        layout.addRow("⏳ Hora Fin:", self.hora_fin_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def get_horario(self):
        """Devuelve el horario ingresado como una tupla"""
        dia = self.dia_edit.text().strip()
        hora_inicio = self.hora_inicio_edit.text().strip()
        hora_fin = self.hora_fin_edit.text().strip()
        
        return dia, hora_inicio, hora_fin

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

class DoctorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Doctores - Clínica Dental")
        self.setGeometry(100, 100, 800, 600)

        # Color scheme 
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'background': '#2b2b2b',   # Dark gray
            'surface': '#3c3c3c',      # Slightly lighter gray
            'text_light': '#ffffff',   # White text
            'text_dark': '#e0e0e0'     # Light gray text
        }

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                font-family: 'Segoe UI';
                font-size: 14px;
            }}
            
            QGroupBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: {self.colors['surface']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: {self.colors['surface']};
                color: {self.colors['accent']};
            }}
            
            QLineEdit, QSpinBox, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {self.colors['accent']};
                background-color: #404040;
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
                background-color: {self.colors['secondary']};
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 4px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['accent']};
                
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QTextEdit {{
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_dark']};
                padding: 15px;
                selection-background-color: {self.colors['accent']};
            }}
            
            QTextEdit:focus {{
                border-color: {self.colors['accent']};
            }}
        """)

        self.dui = 0
        self.nombre = ""
        self.apellido = ""
        self.especialidad = ""
        self.telefono = 0
        self.correo = "-"
        self.citas: List["Cita"] = []  # Lista de citas asociadas al doctor
        self.horario: List[Horario] = [] # Lista de horarios del doctor

        # Almacenamos los dotores en una lista
        self.doctores = []
        
        self.editando_doctor = None  # Variable que ocuparemos para actulizar campos de la informacion del doctor

        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario del Doctor"""
        # Creamos el widget central real
        central_widget = QWidget()
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Creamos el scroll 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        # Título con estilo mejorado
        title = QLabel("🏥 Sistema de Gestión de Doctor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
                border: 3px solid {self.colors['accent']};
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        main_layout.addWidget(title)
        
        # Información del paciente
        info_group = QGroupBox("Información del Doctor")
        info_layout = QFormLayout()
        
        self.dui_edit = QLineEdit()
        self.nombre_edit = QLineEdit()
        self.apellido_edit = QLineEdit()
        self.especialidad_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.correo_edit = QLineEdit()

        
        info_layout.addRow("DUI:", self.dui_edit)
        info_layout.addRow("Nombre:", self.nombre_edit)
        info_layout.addRow("Apellido:", self.apellido_edit)
        info_layout.addRow("Especialidad:", self.especialidad_edit)
        info_layout.addRow("Teléfono:", self.telefono_edit)
        info_layout.addRow("Correo:", self.correo_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Botones de acción con iconos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        buttons_row1.setSpacing(10)
        
        self.crear_btn = QPushButton("👤 Crear Doctor")
        self.crear_btn.clicked.connect(self.crear_doctor)
        self.crear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent']};
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['secondary']};
            }}
        """)
        
        self.agregar_horario_btn = QPushButton("🩺 Agregar Horario")
        self.agregar_horario_btn.clicked.connect(self.agregar_horario)
        
        self.ver_cita_btn = QPushButton("📅 Ver Citas")
        self.ver_cita_btn.clicked.connect(self.ver_citas)
        
        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.agregar_horario_btn)
        buttons_row1.addWidget(self.ver_cita_btn)
        
        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        buttons_row2.setSpacing(10)
        
        self.mostrar_info_btn = QPushButton("ℹ️ Mostrar listado de doctores")
        self.mostrar_info_btn.clicked.connect(self.mostrar_info_doctor)
        
        self.suprimir_doctor_btn = QPushButton("📋 Suprimir Doctor")
        self.suprimir_doctor_btn.clicked.connect(self.suprimir_doctor)
        
        # Botón para mostrar todos los historiales
        self.actualizar_info_doctor_btn = QPushButton("📚 Actualizar Info Doctor")
        self.actualizar_info_doctor_btn.clicked.connect(self.actualizar_info_doctor)
        
        buttons_row2.addWidget(self.mostrar_info_btn)
        buttons_row2.addWidget(self.suprimir_doctor_btn)
        buttons_row2.addWidget(self.actualizar_info_doctor_btn)
        
        # Tercer fila de botones 
        buttons_row3 = QHBoxLayout()
        buttons_row3.setSpacing(10)

        self.registrar_diagnostico_btn = QPushButton("📝 Registrar Diagnóstico")
        self.registrar_diagnostico_btn.clicked.connect(self.registrar_diagnostico) 

        buttons_row3.addWidget(self.registrar_diagnostico_btn)

        # Layout vertical para las filas de botones
        buttons_container = QVBoxLayout()
        buttons_container.addLayout(buttons_row1)
        buttons_container.addLayout(buttons_row2)
        buttons_container.addLayout(buttons_row3)
        
        main_layout.addLayout(buttons_container)
        
        # Área de resultados con estilo mejorado y scroll bar
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        resultado_label.setStyleSheet(f"color: {self.colors['accent']};")
        main_layout.addWidget(resultado_label)
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Consolas", 13))
        self.resultado_text.setPlaceholderText("Aquí aparecerán los resultados de las operaciones...")
        
        # Configurar scroll bars con estilo
        self.resultado_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.resultado_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Estilo mejorado para el área de texto y scroll bars
        self.resultado_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                padding: 15px;
            }}
            
            QScrollBar:vertical {{
                background-color: #3c3c3c;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['secondary']};
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QScrollBar::handle:vertical:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            
            QScrollBar:horizontal {{
                background-color: #3c3c3c;
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {self.colors['secondary']};
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QScrollBar::handle:horizontal:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 0px;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)
        
        # Configurar el comportamiento del scroll
        self.resultado_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.resultado_text.setMinimumHeight(200)
        
        main_layout.addWidget(self.resultado_text)
    
    def validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_dui(self, dui: str) -> bool:
        """Valida el formato del DUI (########-#)"""
        patron = r'^\d{8}-\d{1}$'
        return re.match(patron, dui) is not None
    
    def validar_telefono(self, telefono: str) -> bool:
        """Valida que el teléfono tenga al menos 8 dígitos"""
        return telefono.isdigit() and len(telefono) >= 8
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.dui_edit.clear()
        self.telefono_edit.clear()
        self.correo_edit.clear()
        self.especialidad_edit.clear()
        
        # Enfocar el primer campo para facilitar la entrada
        self.nombre_edit.setFocus()
    
    def crear_doctor(self):
        """Crea un nuevo paciente con los datos ingresados"""
        try:
            self.resultado_text.clear()  # Limpia el área de resultados antes de mostrar nuevos datos

            nombre = self.nombre_edit.text().strip().title()
            apellido = self.apellido_edit.text().strip().title()
            especialidad = self.especialidad_edit.text().strip().title()
            dui = self.dui_edit.text().strip()
            telefono_str = self.telefono_edit.text().strip()
            correo = self.correo_edit.text().strip().lower()
            
            # Validaciones básicas
            if not all([nombre, apellido, dui, especialidad]):
                QMessageBox.warning(self, "❌ Error", "Nombre, Apellido, DUI y Especialidad son campos obligatorios")
                return
            
            # Validación DUI
            if not self.validar_dui(dui):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El DUI debe tener el formato: 12345678-9")
                return
            
            # Verificar si ya existe un paciente con el mismo DUI
            for doctor in self.doctores:
                if doctor['dui'] == dui:
                    QMessageBox.warning(self, "❌ Error", 
                                      f"Ya existe un doctor registrado con el DUI: {dui}")
                    return
            
            # Validación teléfono
            if telefono_str and not self.validar_telefono(telefono_str):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El teléfono debe contener al menos 8 dígitos")
                return
            
            telefono = int(telefono_str) if telefono_str else 0
            
            # Validación email
            if correo and not self.validar_email(correo):
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El email no tiene un formato válido")
                return
               
            # Crear datos del nuevo paciente
            nuevo_doctor = {
                'nombre': nombre,
                'apellido': apellido,
                'dui': dui,
                'especialidad': especialidad,
                'telefono': telefono,
                'correo': correo,
                'citas': [],
                'fecha_registro': datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            }
            
            # Agregar a la lista de pacientes registrados
            self.doctores.append(nuevo_doctor)
            
            # Establecer como paciente actual
            self.nombre = nombre
            self.apellido = apellido
            self.especialidad = especialidad
            self.dui = dui
            self.telefono = telefono
            self.correo = correo
            self.citas = []
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "✅ Éxito", 
                                  f"Paciente {nombre} {apellido} creado exitosamente.\n\n"
                                  f"Total de pacientes registrados: {len(self.doctores)}")
            
            # Mostrar información del paciente creado
            self.resultado_text.append(f"Doctor creado: {nombre} {apellido}\n"
                                       f"DUI: {dui}\n"
                                       f"Especialidad: {especialidad}\n"
                                       f"Teléfono: {telefono}\n"
                                       f"Correo: {correo}\n"
                                       f"Fecha de registro: {nuevo_doctor['fecha_registro']}\n")
            
            # Limpiar campos automáticamente para el siguiente paciente
            self.limpiar_campos()
            
        except ValueError as e:
            QMessageBox.warning(self, "❌ Error", f"Error en el formato de los datos: {str(e)}")
    
    def agregar_horario(self):
        """ Abre un diálogo para agregar un horario al doctor """
        dialog = AgregarHorarioDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            dia, hora_inicio, hora_fin = dialog.get_horario()
            
            # Validar que se ingresaron todos los campos
            if not all([dia, hora_inicio, hora_fin]):
                QMessageBox.warning(self, "❌ Error", "Todos los campos son obligatorios")
                return
            
            # Validar formato de horas
            try:
                hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
                hora_fin_dt = datetime.strptime(hora_fin, "%H:%M")
            except ValueError:
                QMessageBox.warning(self, "❌ Error de Formato", 
                                  "El formato de hora debe ser HH:MM (24 horas)")
                return
            
            # Verificar que la hora de inicio sea antes de la hora de fin
            if hora_inicio_dt >= hora_fin_dt:
                QMessageBox.warning(self, "❌ Error", 
                                  "La hora de inicio debe ser anterior a la hora de fin")
                return
            
            # Crear el horario y agregarlo a la lista
            nuevo_horario = Horario(dia, hora_inicio_dt, hora_fin_dt)
            self.horario.append(nuevo_horario)
            
            # Actualizar también en la lista de doctores registrados
            for doctor in self.doctores:
                if doctor['dui'] == self.dui:
                    doctor['horario'].append(nuevo_horario)
                    break
            
            QMessageBox.information(self, "✅ Éxito", 
                                  f"Horario agregado exitosamente para {self.nombre} {self.apellido}")

    def mostrar_info_doctor(self):
        """ Muestra un diálogo con la información de todos los doctores registrados """
        self.resultado_text.clear()  # Limpia el área de resultados antes de mostrar nuevos datos

        if not self.doctores:
            QMessageBox.information(self, "ℹ️ Información", "No hay doctores registrados")
            return
    
        for doctor in self.doctores:
            self.resultado_text.append(f"""- DUI: {doctor['dui']}
Dr. {doctor['nombre']} {doctor['apellido']}
Especialidad: {doctor['especialidad']}
Teléfono: {doctor['telefono']}
Correo: {doctor['correo']}\n""")
            
    def suprimir_doctor(self):
        """
        Permite eliminar un doctor registrado por su DUI.
        Si no se encuentra el doctor, muestra un mensaje de error.
        """
        self.resultado_text.clear()

        if not self.doctores:
            QMessageBox.information(self, "ℹ️ Información", "No hay doctores registrados")
            return

        dui_a_eliminar, ok = QInputDialog.getText(self, "Eliminar Doctor", "Ingrese el DUI del doctor a eliminar:")
        if not ok or not dui_a_eliminar.strip():
            return

        dui_a_eliminar = dui_a_eliminar.strip()
        for doctor in self.doctores:
            if doctor['dui'] == dui_a_eliminar:
                self.doctores.remove(doctor)
                QMessageBox.information(self, "✅ Éxito", f"Doctor con DUI {dui_a_eliminar} eliminado correctamente.")
                self.resultado_text.append(f"Doctor eliminado: {doctor['nombre']} {doctor['apellido']} (DUI: {dui_a_eliminar})\n")
                return

        QMessageBox.warning(self, "❌ Error", f"No se encontró ningún doctor con el DUI: {dui_a_eliminar}")
            

    def actualizar_info_doctor(self):
        """
        Si no estamos editando, pide el DUI, busca el doctor y permite editar sus datos (excepto el DUI).
        Si ya estamos editando, guarda los cambios realizados.
        """
        self.resultado_text.clear()

        if not self.doctores:
            QMessageBox.information(self, "ℹ️ Información", "No hay doctores registrados")
            return

        # Si ya estamos editando, guardar los cambios
        if self.editando_doctor is not None:
            doctor = self.editando_doctor
            doctor['nombre'] = self.nombre_edit.text().strip().title()
            doctor['apellido'] = self.apellido_edit.text().strip().title()
            doctor['especialidad'] = self.especialidad_edit.text().strip().title()
            doctor['telefono'] = int(self.telefono_edit.text().strip()) if self.telefono_edit.text().strip().isdigit() else 0
            doctor['correo'] = self.correo_edit.text().strip().lower()

            QMessageBox.information(self, "✅ Éxito", "Información del doctor actualizada correctamente.")
            self.resultado_text.append(
                f"Doctor actualizado:\n"
                f"DUI: {doctor['dui']}\n"
                f"Nombre: {doctor['nombre']}\n"
                f"Apellido: {doctor['apellido']}\n"
                f"Especialidad: {doctor['especialidad']}\n"
                f"Teléfono: {doctor['telefono']}\n"
                f"Correo: {doctor['correo']}\n"
            )
            self.dui_edit.setReadOnly(False)
            self.editando_doctor = None  # Salimos del modo edición
            self.limpiar_campos()
            return

        # Si NO estamos editando, pedir DUI y cargar datos
        dui_a_buscar, ok = QInputDialog.getText(self, "Buscar Doctor", "Ingrese el DUI del doctor a modificar:")
        if not ok or not dui_a_buscar.strip():
            return

        dui_a_buscar = dui_a_buscar.strip()
        for doctor in self.doctores:
            if doctor['dui'] == dui_a_buscar:
                # Llenar los campos con los datos encontrados
                self.dui_edit.setText(doctor['dui'])
                self.nombre_edit.setText(doctor['nombre'])
                self.apellido_edit.setText(doctor['apellido'])
                self.especialidad_edit.setText(doctor['especialidad'])
                self.telefono_edit.setText(str(doctor['telefono']))
                self.correo_edit.setText(doctor['correo'])
                self.dui_edit.setReadOnly(True)  # No permitir editar el DUI

                self.editando_doctor = doctor  # Guardamos referencia para editar después

                QMessageBox.information(self, "Editar Doctor", 
                    "Modifique los campos que desee y presione nuevamente 'Actualizar Info Doctor' para guardar los cambios.")
                return

        QMessageBox.warning(self, "❌ Error", f"No se encontró ningún doctor con el DUI: {dui_a_buscar}")

    # Por el momento, no encontrara ninguna cita para el doctor, una vez se haya hecho la conexion con la base de datos será más fácil
    def ver_citas(self):
        self.resultado_text.clear()
        # Pide el DUI del doctor a consultar
        dui, ok = QInputDialog.getText(self, "Ver Citas", "Ingrese el DUI del doctor:")
        if not ok or not dui.strip():
            return
        for doctor in self.doctores:
            if doctor['dui'] == dui.strip():
                if not doctor.get('citas'):
                    self.resultado_text.append("No hay citas registradas para este doctor.")
                    return
                self.resultado_text.append(f"Citas del Dr. {doctor['nombre']} {doctor['apellido']}:")
                for cita in doctor['citas']:
                    self.resultado_text.append(str(cita))
                return
        QMessageBox.warning(self, "❌ Error", "No se encontró el doctor con ese DUI.")

    # Este metodo sera para que el doctor pueda registrar un diagnostico a un paciente, sin embargo se implementara mas adelante.
    # Especialmente, cuando se haga la conexion con la base de datos
    # def registrar_diagnostico(self):


def main():
    
    app = QApplication([])
    window = DoctorWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
