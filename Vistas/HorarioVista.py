import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFormLayout, QMessageBox,
    QDialog, QDialogButtonBox, QInputDialog, QComboBox,
    QDateEdit, QCalendarWidget, QTimeEdit
)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont
from typing import List
from Controladores.HorarioControlador import HorarioController
from Modelos.DoctorModelo import Doctor 


class AgregarHorarioDialog(QDialog):
    def __init__(self, doctores: List[Doctor], parent=None):
        super().__init__(parent)
        self.doctores = doctores
        self.setWindowTitle("➕ Agregar Horario")
        self.setModal(True)
        self.resize(600, 500)
        
        # Usar los mismos colores que la ventana principal
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'text_light': '#2b2b2b',   # Dark gray
            'text_dark': '#3c3c3c',    # Slightly lighter gray
            'background': '#f7f8fa',   # Light background
            'surface': '#ffffff'       # White surface
        }
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
            }}
            
            QLineEdit, QComboBox, QDateEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
                border-color: {self.colors['accent']};
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['surface']};
                background-color: {self.colors['secondary']};
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 4px;
                min-width: 120px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QPushButton:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QCalendarWidget {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 12px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: {self.colors['secondary']};
                color: {self.colors['surface']};
                border: none;
                border-radius: 4px;
                padding: 5px;
                margin: 2px;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QCalendarWidget QMenu {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
                border-radius: 4px;
                padding: 2px;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
                selection-color: {self.colors['surface']};
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: {self.colors['secondary']};
            }}
        """)

        self.configurar_ui()
    
    def configurar_ui(self):
        # Crear los layouts principales
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Campo ID Horario con sugerencia de formato H1
        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("Ejemplo: H001, H002, H003, etc.")
        
        # Quitar el campo de fecha ya que la tabla no lo maneja por días específicos
        # self.fecha_edit = QDateEdit()
        
        # Campos de hora
        self.hora_inicio_edit = QTimeEdit()
        self.hora_inicio_edit.setDisplayFormat("HH:mm")
        self.hora_inicio_edit.setTime(QTime(9, 0))  # Hora por defecto 09:00
        
        self.hora_fin_edit = QTimeEdit()
        self.hora_fin_edit.setDisplayFormat("HH:mm")
        self.hora_fin_edit.setTime(QTime(17, 0))  # Hora por defecto 17:00
        
        # ComboBox para seleccionar doctor
        self.doctor_combo = QComboBox()
        for doctor in self.doctores:
            self.doctor_combo.addItem(f"Dr. {doctor.nombre} {doctor.apellido}", doctor)
        
        # Agregar campos al formulario
        form_layout.addRow("🆔 ID Horario:", self.id_edit)
        form_layout.addRow("⏰ Hora Inicio:", self.hora_inicio_edit)
        form_layout.addRow("⏳ Hora Fin:", self.hora_fin_edit)
        form_layout.addRow("👨‍⚕️ Médico:", self.doctor_combo)
        
        # Widget contenedor para el formulario
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        # Personalizar botones
        buttons.setStyleSheet(f"""
            QDialogButtonBox QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['surface']};
                background-color: {self.colors['secondary']};
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 4px;
                min-width: 100px;
            }}
            
            QDialogButtonBox QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QDialogButtonBox QPushButton:pressed {{
                background-color: {self.colors['primary']};
            }}
        """)
        
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_data(self):
        return {
            'id_horario': self.id_edit.text().strip(),
            'hora_inicio': self.hora_inicio_edit.time().toString("HH:mm"),
            'hora_fin': self.hora_fin_edit.time().toString("HH:mm"),
            'doctor': self.doctor_combo.currentData()
        }


class HorarioView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕒 Gestión de Horarios - Clínica Dental")
        self.setGeometry(100, 100, 900, 700)
        
        # Usar exactamente los mismos colores que la ventana principal
        self.colors = {
            'primary': '#130760',      # Dark blue-purple 
            'secondary': '#756f9f',    # Medium purple
            'accent': '#10b8b9',       # Teal
            'text_light': '#2b2b2b',   # Dark gray
            'text_dark': '#3c3c3c',    # Slightly lighter gray
            'background': '#f7f8fa',   # Light background
            'surface': '#ffffff'       # White surface
        }

        self.setup_styles()
        self.configurar_ui()
        self.controlador = HorarioController(self)
        self.conectar_botones()
    
    def setup_styles(self):
        """Configura los estilos idénticos a la ventana principal"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}

            QWidget {{
                background-color: {self.colors['background']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
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
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['surface']};
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
            
            QComboBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QDateEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
        """)
    
    def configurar_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título con el mismo estilo que la ventana principal
        titulo = QLabel("🕒 Sistema de Gestión de Horarios")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        titulo.setStyleSheet(f"color: {self.colors['text_light']}; margin: 10px;")
        layout.addWidget(titulo)
        
        # Botones
        btn_container = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar Horario") 
        self.btn_eliminar = QPushButton("🗑️ Eliminar Horario") 
        btn_container.addWidget(self.btn_agregar)
        btn_container.addWidget(self.btn_eliminar)
        layout.addLayout(btn_container)
        
        # Etiqueta para resultados
        resultado_label = QLabel("📊 Horarios Registrados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(resultado_label)
        
        # Lista de horarios
        self.resultados = QTextEdit()
        self.resultados.setReadOnly(True)
        layout.addWidget(self.resultados)
    
    def conectar_botones(self):
        """Conecta los botones con los métodos del controlador."""
        self.btn_agregar.clicked.connect(self.controlador.agregar_horario)
        self.btn_eliminar.clicked.connect(self.controlador.eliminar_horario)
    
    def actualizar_combos(self, doctores: List[Doctor]):
        """Método para que el controlador actualice los combos."""
        pass 
    
    def mostrar_dialogo_agregar(self, doctores: List[Doctor]):
        """Muestra el diálogo para agregar horario y retorna los datos."""
        dialog = AgregarHorarioDialog(doctores, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_data()
        return None
    
    def mostrar_dialogo_eliminar(self, horarios_info: List[str]):
        """Muestra el diálogo para eliminar horario y retorna el ID seleccionado."""
        if not horarios_info:
            QMessageBox.information(self, "ℹ️ Información", "No hay horarios registrados para eliminar.")
            return None
        
        item, ok = QInputDialog.getItem(
            self, "🗑️ Eliminar horario", 
            "Seleccione un horario a eliminar:", horarios_info, 0, False)
        
        if ok and item:
            id_horario = item.split(" | ")[0]
            
            confirm = QMessageBox.question(
                self, "⚠️ Confirmar Eliminación", 
                f"¿Está seguro que desea eliminar el horario con ID: {id_horario}?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                return id_horario
        
        return None
    
    def actualizar_lista_horarios(self, horarios_por_dia: dict):
        """Actualiza la lista de horarios en la interfaz."""
        self.resultados.clear()
        
        if not horarios_por_dia:
            self.resultados.setPlainText("📋 No hay horarios registrados.")
            return
        
        for dia, horarios in horarios_por_dia.items():
            self.resultados.append(f"\n📅 HORARIOS DE HOY")
            self.resultados.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for horario in sorted(horarios, key=lambda h: h.hora_inicio):
                self.resultados.append(f"   {str(horario)}")
            self.resultados.append("")
    
    def obtener_info_horarios_para_eliminar(self, horarios):
        """Genera la lista de información de horarios para el diálogo de eliminación."""
        return [f"{h.id_horario} |  {h.hora_inicio}-{h.hora_fin} (Dr. {h.doctor.nombre} {h.doctor.apellido})"
                for h in horarios]
    
    def mostrar_mensaje(self, tipo: str, titulo: str, mensaje: str):
        """Muestra mensajes al usuario"""
        if tipo == "error":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "info":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)


#def main():
    #app = QApplication(sys.argv)
    #window = HorarioView()
    #window.show()
    #sys.exit(app.exec())

#if __name__ == "__main__":
   # main()
