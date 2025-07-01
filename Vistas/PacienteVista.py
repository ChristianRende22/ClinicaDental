from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QLineEdit, QSpinBox, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QListWidget, QDialog, QDialogButtonBox, QDoubleSpinBox,
                             QScrollArea, QScrollBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar las clases del controlador
from Controladores.PacienteControlador import PacienteControlador, Tratamiento, Cita, Doctor

from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate


class AgregarTratamientoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🩺 Agregar Tratamiento")
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
            
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
                border-color: #10b8b9;
                background-color: #404040;
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #756f9f;
                background-color: #756f9f;
                border-radius: 3px;
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: #10b8b9;
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
                transform: rotate(45deg);
            }}
            
            QCalendarWidget {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #756f9f;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: #130760;
            }}
            
            QCalendarWidget QMenu {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
            }}
            
            QCalendarWidget QSpinBox:focus {{
                border-color: #10b8b9;
            }}
            
            QCalendarWidget QAbstractItemView {{
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #10b8b9;
                selection-color: #ffffff;
                border: none;
                outline: none;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                color: #ffffff;
                background-color: #3c3c3c;
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: #666666;
            }}
            
            QCalendarWidget QWidget {{
                alternate-background-color: #404040;
            }}
            
            QCalendarWidget QHeaderView::section {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QCalendarWidget QTableView {{
                gridline-color: #555555;
                background-color: #3c3c3c;
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
        
        layout = QFormLayout()
        
        self.id_edit = QLineEdit()
        self.descripcion_edit = QTextEdit()
        self.descripcion_edit.setMaximumHeight(80)
        self.costo_edit = QDoubleSpinBox()
        self.costo_edit.setMaximum(99999.99)
        self.costo_edit.setPrefix("$")
        
        # Cambiar a QDateEdit con calendario popup
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDisplayFormat("dd/MM/yyyy")
        self.fecha_edit.setDate(QDate.currentDate())
        
        self.estado_edit = QLineEdit()
        self.doctor_nombre_edit = QLineEdit()
        self.doctor_apellido_edit = QLineEdit()
        
        layout.addRow("ID Tratamiento:", self.id_edit)
        layout.addRow("Descripción:", self.descripcion_edit)
        layout.addRow("Costo:", self.costo_edit)
        layout.addRow("Fecha:", self.fecha_edit)
        layout.addRow("Estado:", self.estado_edit)
        layout.addRow("Nombre Doctor:", self.doctor_nombre_edit)
        layout.addRow("Apellido Doctor:", self.doctor_apellido_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_tratamiento(self):
        doctor = Doctor(self.doctor_nombre_edit.text(), self.doctor_apellido_edit.text())
        
        # Convertir QDate a string en formato DD/MM/YYYY
        fecha_qdate = self.fecha_edit.date()
        fecha_str = fecha_qdate.toString("dd/MM/yyyy")
        
        return Tratamiento(
            self.id_edit.text(),
            self.descripcion_edit.toPlainText(),
            self.costo_edit.value(),
            fecha_str,
            self.estado_edit.text(),
            doctor
        )

class AgregarCitaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📅 Agregar Cita")
        self.setModal(True)
        self.resize(450, 300)
        
      
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
            
            QLineEdit, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid #756f9f;
                border-radius: 6px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }}
            
            QLineEdit:focus, QDoubleSpinBox:focus {{
                border-color: #10b8b9;
                background-color: #404040;
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #756f9f;
                background-color: #756f9f;
                border-radius: 3px;
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: #10b8b9;
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
                transform: rotate(45deg);
            }}
            
            QCalendarWidget {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #756f9f;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: #130760;
            }}
            
            QCalendarWidget QMenu {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
            }}
            
            QCalendarWidget QSpinBox:focus {{
                border-color: #10b8b9;
            }}
            
            QCalendarWidget QAbstractItemView {{
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #10b8b9;
                selection-color: #ffffff;
                border: none;
                outline: none;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                color: #ffffff;
                background-color: #3c3c3c;
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: #666666;
            }}
            
            QCalendarWidget QWidget {{
                alternate-background-color: #404040;
            }}
            
            QCalendarWidget QHeaderView::section {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QCalendarWidget QTableView {{
                gridline-color: #555555;
                background-color: #3c3c3c;
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
        
        layout = QFormLayout()
        
        self.id_edit = QLineEdit()
        self.hora_inicio_edit = QLineEdit()
        self.hora_inicio_edit.setPlaceholderText("DD/MM/YYYY HH:MM")
        self.hora_fin_edit = QLineEdit()
        self.hora_fin_edit.setPlaceholderText("DD/MM/YYYY HH:MM")
        self.costo_edit = QDoubleSpinBox()
        self.costo_edit.setMaximum(99999.99)
        self.costo_edit.setPrefix("$")
        self.estado_edit = QLineEdit()
        self.doctor_nombre_edit = QLineEdit()
        self.doctor_apellido_edit = QLineEdit()
        
        layout.addRow("ID Cita:", self.id_edit)
        layout.addRow("Hora Inicio:", self.hora_inicio_edit)
        layout.addRow("Hora Fin:", self.hora_fin_edit)
        layout.addRow("Costo:", self.costo_edit)
        layout.addRow("Estado:", self.estado_edit)
        layout.addRow("Nombre Doctor:", self.doctor_nombre_edit)
        layout.addRow("Apellido Doctor:", self.doctor_apellido_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)
    
    def get_cita(self):
        doctor = Doctor(self.doctor_nombre_edit.text(), self.doctor_apellido_edit.text())
        return Cita(
            self.id_edit.text(),
            self.hora_inicio_edit.text(),
            self.hora_fin_edit.text(),
            self.costo_edit.value(),
            self.estado_edit.text(),
            doctor
        )

class VentanaInfoPaciente(QDialog):
    def __init__(self, paciente, controlador, parent=None):
        super().__init__(parent)
        self.paciente = paciente
        self.controlador = controlador
        self.setWindowTitle(f"📋 Información de {paciente.nombre} {paciente.apellido}")
        self.setModal(True)
        self.resize(800, 600)
        
        # Aplicar el mismo estilo que la ventana principal
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
            
            QTextEdit {{
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 2px solid #756f9f;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                padding: 15px;
                selection-background-color: #10b8b9;
            }}
            
            QTextEdit:focus {{
                border-color: #10b8b9;
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #756f9f;
                background-color: #756f9f;
                border-radius: 3px;
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: #10b8b9;
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid #ffffff;
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
                transform: rotate(45deg);
            }}
            
            QCalendarWidget {{
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #756f9f;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: #10b8b9;
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: #130760;
            }}
            
            QCalendarWidget QMenu {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #756f9f;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
            }}
            
            QCalendarWidget QSpinBox:focus {{
                border-color: #10b8b9;
            }}
            
            QCalendarWidget QAbstractItemView {{
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #10b8b9;
                selection-color: #ffffff;
                border: none;
                outline: none;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                color: #ffffff;
                background-color: #3c3c3c;
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: #666666;
            }}
            
            QCalendarWidget QWidget {{
                alternate-background-color: #404040;
            }}
            
            QCalendarWidget QHeaderView::section {{
                background-color: #756f9f;
                color: #ffffff;
                border: none;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QCalendarWidget QTableView {{
                gridline-color: #555555;
                background-color: #3c3c3c;
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
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Título de la ventana
        titulo = QLabel(f"👤 Información Completa del Paciente")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        titulo.setStyleSheet("""
            QLabel {
                color: #10b8b9;
                background-color: #3c3c3c;
                border: 2px solid #10b8b9;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        # Área de texto para mostrar la información
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFont(QFont("Consolas", 13))
        
        # Generar y mostrar la información del paciente
        info_completa = self._generar_info_detallada()
        self.info_text.setText(info_completa)
        
        layout.addWidget(self.info_text)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        
        cerrar_btn = QPushButton("❌ Cerrar")
        cerrar_btn.clicked.connect(self.reject)
        
        seleccionar_btn = QPushButton("✅ Seleccionar Paciente")
        seleccionar_btn.clicked.connect(self.seleccionar_paciente)
        seleccionar_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b8b9;
            }
            QPushButton:hover {
                background-color: #0d9a9b;
            }
        """)
        
        historial_btn = QPushButton("📋 Ver Historial Completo")
        historial_btn.clicked.connect(self.mostrar_historial_completo)
        
        botones_layout.addWidget(historial_btn)
        botones_layout.addWidget(seleccionar_btn)
        botones_layout.addWidget(cerrar_btn)
        
        layout.addLayout(botones_layout)
        self.setLayout(layout)
    
    def _generar_info_detallada(self):
        """Genera información detallada del paciente"""
        edad = self.controlador.calcular_edad(self.paciente.fecha_nacimiento)
        dui_label = "DUI del Responsable" if edad < 18 else "DUI"
        edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else " (Mayor de edad)")
        
        separador = "=" * 70
        info = f"""
{separador}
🏥 INFORMACIÓN DETALLADA DEL PACIENTE - CLÍNICA DENTAL
{separador}

👤 DATOS PERSONALES:
   ▪ Nombre Completo: {self.paciente.nombre} {self.paciente.apellido}
   ▪ Edad: {edad_info}
   ▪ Fecha de Nacimiento: {self.paciente.fecha_nacimiento.strftime('%d/%m/%Y')}
   ▪ {dui_label}: {self.paciente.dui}
   ▪ Teléfono: {self.controlador.formatear_telefono(self.paciente.telefono)}
   ▪ Correo Electrónico: {self.paciente.correo if self.paciente.correo else 'No especificado'}
   ▪ Fecha de Registro: {self.paciente.fecha_registro}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${self.paciente.saldo_pendiente:,.2f}
   ▪ Estado de Pago: {'🔴 Pendiente de pago' if self.paciente.saldo_pendiente > 0 else '🟢 Al día'}

📊 RESUMEN MÉDICO:
   ▪ Tratamientos Realizados: {len(self.paciente.historial_medico)}
   ▪ Citas Agendadas: {len(self.paciente.citas)}
   ▪ Costo Total Tratamientos: ${self.paciente.calcular_total_tratamientos():,.2f}
   ▪ Costo Total Citas: ${self.paciente.calcular_total_citas():,.2f}
   ▪ Balance Total: ${self.paciente.get_balance_total():,.2f}

🩺 ÚLTIMOS TRATAMIENTOS:
"""
        
        if not self.paciente.historial_medico:
            info += "   📝 No hay tratamientos registrados.\n"
        else:
            for i, tratamiento in enumerate(self.paciente.historial_medico[-3:], 1):  # Últimos 3
                estado_icon = self.controlador.get_estado_icon(tratamiento.estado)
                info += f"""   {i}. {tratamiento.descripcion}
      💵 ${tratamiento.costo:,.2f} | 📅 {tratamiento.fecha_realizacion}
      {estado_icon} {tratamiento.estado} | 👨‍⚕️ Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
"""
        
        info += f"""
📅 PRÓXIMAS CITAS:
"""
        
        if not self.paciente.citas:
            info += "   📝 No hay citas programadas.\n"
        else:
            for i, cita in enumerate(self.paciente.citas[-3:], 1):  # Últimas 3
                estado_icon = self.controlador.get_estado_icon(cita.estado)
                info += f"""   {i}. ID: {cita.id_cita}
      ⏰ {cita.hora_inicio} - {cita.hora_fin}
      💵 ${cita.costo_cita:,.2f} | {estado_icon} {cita.estado}
      👨‍⚕️ Dr. {cita.doctor.nombre} {cita.doctor.apellido}
"""
        
        info += f"""
⏰ Consulta realizada: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

💡 OPCIONES DISPONIBLES:
   • Seleccionar Paciente: Establecer como paciente actual para trabajar
   • Ver Historial Completo: Mostrar todos los tratamientos y citas
   • Cerrar: Volver a la ventana principal

{separador}
"""
        return info
    
    def seleccionar_paciente(self):
        """Selecciona este paciente como el actual en el controlador"""
        self.controlador.paciente_actual = self.paciente
        QMessageBox.information(self, "✅ Paciente Seleccionado", 
                              f"Paciente {self.paciente.nombre} {self.paciente.apellido} "
                              f"ha sido seleccionado como paciente actual.\n\n"
                              f"Ahora puede usar todas las funciones (agregar tratamientos, "
                              f"citas, consultar historial, etc.) con este paciente.")
        self.accept()
    
    def mostrar_historial_completo(self):
        """Muestra el historial completo del paciente"""
        historial = self._generar_historial_completo()
        self.info_text.setText(historial)
    
    def _generar_historial_completo(self):
        """Genera el historial médico completo del paciente"""
        edad = self.controlador.calcular_edad(self.paciente.fecha_nacimiento)
        edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else "")
        
        separador_principal = "=" * 70
        separador_seccion = "-" * 50
        
        historial = f"""
{separador_principal}
📋 HISTORIAL MÉDICO COMPLETO
{separador_principal}

👤 Paciente: {self.paciente.nombre} {self.paciente.apellido} - {edad_info}
📅 Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_seccion}
🩺 TODOS LOS TRATAMIENTOS ({len(self.paciente.historial_medico)})
{separador_seccion}
"""
        
        if not self.paciente.historial_medico:
            historial += "\n   📝 No hay tratamientos registrados en el historial.\n"
        else:
            for i, tratamiento in enumerate(self.paciente.historial_medico, 1):
                estado_icon = self.controlador.get_estado_icon(tratamiento.estado)
                historial += f"""
   ┌─ Tratamiento #{i:02d}
   │ 🆔 ID: {tratamiento.id_tratamiento}
   │ 📄 Descripción: {tratamiento.descripcion}
   │ 💵 Costo: ${tratamiento.costo:,.2f}
   │ 📅 Fecha: {tratamiento.fecha_realizacion}
   │ {estado_icon} Estado: {tratamiento.estado}
   │ 👨‍⚕️ Doctor: Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        historial += f"""
{separador_seccion}
📅 TODAS LAS CITAS ({len(self.paciente.citas)})
{separador_seccion}
"""
        
        if not self.paciente.citas:
            historial += "\n   📝 No hay citas programadas.\n"
        else:
            for i, cita in enumerate(self.paciente.citas, 1):
                estado_icon = self.controlador.get_estado_icon(cita.estado)
                historial += f"""
   ┌─ Cita #{i:02d}
   │ 🆔 ID: {cita.id_cita}
   │ ⏰ Inicio: {cita.hora_inicio}
   │ ⏰ Fin: {cita.hora_fin}
   │ 💵 Costo: ${cita.costo_cita:,.2f}
   │ {estado_icon} Estado: {cita.estado}
   │ 👨‍⚕️ Doctor: Dr. {cita.doctor.nombre} {cita.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        # Resumen financiero
        total_tratamientos = self.paciente.calcular_total_tratamientos()
        total_citas = self.paciente.calcular_total_citas()
        total_general = total_tratamientos + total_citas
        
        historial += f"""
{separador_seccion}
💰 RESUMEN FINANCIERO DETALLADO
{separador_seccion}

   📊 Estadísticas Completas:
   ▪ Total de Tratamientos: {len(self.paciente.historial_medico)} - ${total_tratamientos:,.2f}
   ▪ Total de Citas: {len(self.paciente.citas)} - ${total_citas:,.2f}
   ▪ Subtotal General: ${total_general:,.2f}
   ▪ Saldo Pendiente: ${self.paciente.saldo_pendiente:,.2f}
   
   💳 Balance Final: ${self.paciente.get_balance_total():,.2f}

{separador_principal}
"""
        return historial

class PacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pacientes - Clínica Dental")
        self.setGeometry(100, 100, 900, 700)
        
        # Inicializar el controlador
        self.controlador = PacienteControlador()
        
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
            
            QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
                border-color: {self.colors['accent']};
                background-color: #404040;
            }}
            
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid {self.colors['secondary']};
                background-color: {self.colors['secondary']};
                border-radius: 3px;
            }}
            
            QDateEdit::drop-down:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QDateEdit::down-arrow {{
                image: none;
                border: 2px solid {self.colors['text_light']};
                width: 6px;
                height: 6px;
                border-top: none;
                border-left: none;
                margin-top: -2px;
                transform: rotate(45deg);
            }}
            
            QCalendarWidget {{
                background-color: {self.colors['background']};
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }}
            
            QCalendarWidget QToolButton {{
                background-color: {self.colors['secondary']};
                color: {self.colors['text_light']};
                border: none;
                border-radius: 4px;
                padding: 8px;
                margin: 2px;
                font-weight: bold;
                min-width: 50px;
            }}
            
            QCalendarWidget QToolButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QCalendarWidget QToolButton:pressed {{
                background-color: {self.colors['primary']};
            }}
            
            QCalendarWidget QMenu {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
                border-radius: 4px;
            }}
            
            QCalendarWidget QSpinBox {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                border: 1px solid {self.colors['secondary']};
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
                min-width: 80px;
            }}
            
            QCalendarWidget QSpinBox:focus {{
                border-color: {self.colors['accent']};
            }}
            
            QCalendarWidget QAbstractItemView {{
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
                selection-color: {self.colors['text_light']};
                border: none;
                outline: none;
                gridline-color: #555555;
            }}
            
            QCalendarWidget QAbstractItemView:enabled {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
            }}
            
            QCalendarWidget QAbstractItemView:disabled {{
                color: #666666;
            }}
            
            QCalendarWidget QWidget {{
                alternate-background-color: #404040;
            }}
            
            QCalendarWidget QHeaderView::section {{
                background-color: {self.colors['secondary']};
                color: {self.colors['text_light']};
                border: none;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QCalendarWidget QTableView {{
                gridline-color: #555555;
                background-color: {self.colors['surface']};
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
        
        self.init_ui()
    
    def init_ui(self):
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
        title = QLabel("🏥 Sistema de Gestión de Pacientes")
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
        info_group = QGroupBox("Información del Paciente")
        info_layout = QFormLayout()
        
        self.nombre_edit = QLineEdit()
        self.apellido_edit = QLineEdit()

        self.edad_edit = QDateEdit()
        self.edad_edit.setCalendarPopup(True)
        self.edad_edit.setDisplayFormat("dd/MM/yyyy")
        self.edad_edit.setDate(QDate.currentDate())
        # Conectar señal para actualizar el label del DUI cuando cambie la fecha
        self.edad_edit.dateChanged.connect(self.actualizar_label_dui)
        
        self.dui_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.correo_edit = QLineEdit()
        self.saldo_edit = QDoubleSpinBox()
        self.saldo_edit.setPrefix("$")
        self.saldo_edit.setMaximum(99999.99)
        
        info_layout.addRow("Nombre:", self.nombre_edit)
        info_layout.addRow("Apellido:", self.apellido_edit)
        info_layout.addRow("Fecha de Nacimiento:", self.edad_edit)
        
        # Crear el label del DUI que se actualizará dinámicamente
        self.dui_label = QLabel("DUI:")
        info_layout.addRow(self.dui_label, self.dui_edit)
        
        info_layout.addRow("Teléfono:", self.telefono_edit)
        info_layout.addRow("Correo:", self.correo_edit)
        info_layout.addRow("Saldo Pendiente:", self.saldo_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Botones de acción con iconos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Primera fila de botones
        buttons_row1 = QHBoxLayout()
        buttons_row1.setSpacing(10)
        
        self.crear_btn = QPushButton("👤 Crear Paciente")
        self.crear_btn.clicked.connect(self.crear_paciente)
        
        self.agregar_tratamiento_btn = QPushButton("🩺 Agregar Tratamiento")
        self.agregar_tratamiento_btn.clicked.connect(self.agregar_tratamiento)
        
        self.agregar_cita_btn = QPushButton("📅 Agregar Cita")
        self.agregar_cita_btn.clicked.connect(self.agregar_cita)
        
        buttons_row1.addWidget(self.crear_btn)
        buttons_row1.addWidget(self.agregar_tratamiento_btn)
        buttons_row1.addWidget(self.agregar_cita_btn)
        
        # Segunda fila de botones
        buttons_row2 = QHBoxLayout()
        buttons_row2.setSpacing(10)
        
        self.consultar_historial_btn = QPushButton("📋 Consultar Historial")
        self.consultar_historial_btn.clicked.connect(self.consultar_historial)
        
        self.mostrar_info_btn = QPushButton("ℹ️ Mostrar Info Paciente")
        self.mostrar_info_btn.clicked.connect(self.mostrar_info_paciente)
        
        # Botón para mostrar todos los historiales
        self.mostrar_todos_btn = QPushButton("📚 Todos los Historiales")
        self.mostrar_todos_btn.clicked.connect(self.mostrar_todos_historiales)
        
        buttons_row2.addWidget(self.consultar_historial_btn)
        buttons_row2.addWidget(self.mostrar_info_btn)
        buttons_row2.addWidget(self.mostrar_todos_btn)
        
        # Tercera fila de botones
        buttons_row3 = QHBoxLayout()
        buttons_row3.setSpacing(10)
        
        # Botón para buscar paciente por DUI
        self.buscar_dui_btn = QPushButton("🔍 Buscar por DUI")
        self.buscar_dui_btn.clicked.connect(self.buscar_paciente_por_dui)
        
        buttons_row3.addWidget(self.buscar_dui_btn)
        
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
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada para agregar un nuevo paciente"""
        self.nombre_edit.clear()
        self.apellido_edit.clear()
        self.edad_edit.setDate(QDate.currentDate())
        self.dui_edit.clear()
        self.telefono_edit.clear()
        self.correo_edit.clear()
        self.saldo_edit.setValue(0.0)
        
        # Enfocar el primer campo para facilitar la entrada
        self.nombre_edit.setFocus()
    
    def crear_paciente(self):
        """Crea un nuevo paciente con los datos ingresados"""
        try:
            nombre = self.nombre_edit.text().strip()
            apellido = self.apellido_edit.text().strip()
            
            # Convertir QDate a datetime
            fecha_qdate = self.edad_edit.date()
            fecha_nacimiento = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
            
            dui = self.dui_edit.text().strip()
            telefono_str = self.telefono_edit.text().strip()
            correo = self.correo_edit.text().strip()
            saldo_pendiente = self.saldo_edit.value()
            
            # Validación del teléfono
            telefono = 0
            if telefono_str:
                if not self.controlador.validar_telefono(telefono_str):
                    QMessageBox.warning(self, "❌ Error de Formato", 
                                      "El teléfono debe contener al menos 8 dígitos")
                    return
                telefono = int(telefono_str)
            
            # Crear paciente usando el controlador
            exito, mensaje = self.controlador.crear_paciente(
                nombre, apellido, fecha_nacimiento, dui, telefono, correo, saldo_pendiente
            )
            
            if exito:
                # Mostrar mensaje de éxito
                total_pacientes = len(self.controlador.get_todos_los_pacientes())
                QMessageBox.information(self, "✅ Éxito", 
                                      f"{mensaje}\n\n"
                                      f"Total de pacientes registrados: {total_pacientes}")
                
                # Mostrar información del paciente creado
                self.resultado_text.setText(self._generar_info_completa())
                
                # Limpiar campos automáticamente para el siguiente paciente
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "❌ Error", mensaje)
                
        except ValueError as e:
            QMessageBox.warning(self, "❌ Error", f"Error en el formato de los datos: {str(e)}")
    
    def mostrar_todos_historiales(self):
        """Muestra todos los historiales de los pacientes registrados"""
        pacientes = self.controlador.get_todos_los_pacientes()
        if not pacientes:
            QMessageBox.information(self, "ℹ️ Información", 
                                  "No hay pacientes registrados en el sistema.")
            return
        
        historial_completo = self._generar_historial_todos_pacientes()
        self.resultado_text.setText(historial_completo)
    
    def _generar_historial_todos_pacientes(self) -> str:
        """Genera el historial de todos los pacientes registrados"""
        separador_principal = "=" * 80
        separador_paciente = "-" * 60
        
        pacientes = self.controlador.get_todos_los_pacientes()
        
        historial = f"""
{separador_principal}
🏥 HISTORIALES MÉDICOS COMPLETOS - CLÍNICA DENTAL
{separador_principal}

📊 RESUMEN GENERAL:
   ▪ Total de Pacientes Registrados: {len(pacientes)}
   ▪ Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_principal}
"""
        
        # Mostrar cada paciente
        for i, paciente in enumerate(pacientes, 1):
            edad = self.controlador.calcular_edad(paciente.fecha_nacimiento)
            dui_label = "DUI del Responsable" if edad < 18 else "DUI"
            edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else "")
            
            total_tratamientos = paciente.calcular_total_tratamientos()
            total_citas = paciente.calcular_total_citas()
            
            historial += f"""
{separador_paciente}
👤 PACIENTE #{i:02d}: {paciente.nombre} {paciente.apellido}
{separador_paciente}

📋 INFORMACIÓN PERSONAL:
   ▪ Nombre Completo: {paciente.nombre} {paciente.apellido}
   ▪ Edad: {edad_info}
   ▪ {dui_label}: {paciente.dui}
   ▪ Teléfono: {self.controlador.formatear_telefono(paciente.telefono)}
   ▪ Correo: {paciente.correo if paciente.correo else 'No especificado'}
   ▪ Fecha de Registro: {paciente.fecha_registro}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${paciente.saldo_pendiente:,.2f}
   ▪ Total Tratamientos: ${total_tratamientos:,.2f}
   ▪ Total Citas: ${total_citas:,.2f}
   ▪ Balance Total: ${paciente.get_balance_total():,.2f}

🩺 TRATAMIENTOS ({len(paciente.historial_medico)}):
"""
            
            if not paciente.historial_medico:
                historial += "   📝 No hay tratamientos registrados.\n"
            else:
                for j, tratamiento in enumerate(paciente.historial_medico, 1):
                    estado_icon = self.controlador.get_estado_icon(tratamiento.estado)
                    historial += f"""   {j}. {tratamiento.descripcion}
      💵 ${tratamiento.costo:,.2f} | 📅 {tratamiento.fecha_realizacion}
      {estado_icon} {tratamiento.estado} | 👨‍⚕️ Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
"""
            
            historial += f"""
📅 CITAS ({len(paciente.citas)}):
"""
            
            if not paciente.citas:
                historial += "   📝 No hay citas programadas.\n"
            else:
                for j, cita in enumerate(paciente.citas, 1):
                    estado_icon = self.controlador.get_estado_icon(cita.estado)
                    historial += f"""   {j}. ID: {cita.id_cita}
      ⏰ {cita.hora_inicio} - {cita.hora_fin}
      💵 ${cita.costo_cita:,.2f} | {estado_icon} {cita.estado}
      👨‍⚕️ Dr. {cita.doctor.nombre} {cita.doctor.apellido}
"""
            
            historial += "\n"
        
        # Resumen general
        total_pacientes = len(pacientes)
        total_tratamientos_general = sum(len(p.historial_medico) for p in pacientes)
        total_citas_general = sum(len(p.citas) for p in pacientes)
        total_dinero_tratamientos = sum(p.calcular_total_tratamientos() for p in pacientes)
        total_dinero_citas = sum(p.calcular_total_citas() for p in pacientes)
        total_saldos_pendientes = sum(p.saldo_pendiente for p in pacientes)
        
        historial += f"""
{separador_principal}
📈 ESTADÍSTICAS GENERALES DE LA CLÍNICA
{separador_principal}

👥 PACIENTES:
   ▪ Total de Pacientes: {total_pacientes}
   
🩺 TRATAMIENTOS:
   ▪ Total de Tratamientos: {total_tratamientos_general}
   ▪ Ingresos por Tratamientos: ${total_dinero_tratamientos:,.2f}
   
📅 CITAS:
   ▪ Total de Citas: {total_citas_general}
   ▪ Ingresos por Citas: ${total_dinero_citas:,.2f}
   
💰 FINANCIERO:
   ▪ Saldos Pendientes: ${total_saldos_pendientes:,.2f}
   ▪ Ingresos Totales: ${(total_dinero_tratamientos + total_dinero_citas):,.2f}
   ▪ Balance General: ${(total_dinero_tratamientos + total_dinero_citas + total_saldos_pendientes):,.2f}

{separador_principal}
"""
        return historial
    
    def agregar_tratamiento(self):
        """Abre un diálogo para agregar un tratamiento"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        dialog = AgregarTratamientoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            tratamiento = dialog.get_tratamiento()
            if self.controlador.agregar_tratamiento_a_paciente(tratamiento):
                QMessageBox.information(self, "✅ Éxito", "Tratamiento agregado exitosamente")
            else:
                QMessageBox.warning(self, "❌ Error", "No se pudo agregar el tratamiento")
    
    def agregar_cita(self):
        """Abre un diálogo para agregar una cita"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        dialog = AgregarCitaDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            cita = dialog.get_cita()
            if self.controlador.agregar_cita_a_paciente(cita):
                QMessageBox.information(self, "✅ Éxito", "Cita agregada exitosamente")
            else:
                QMessageBox.warning(self, "❌ Error", "No se pudo agregar la cita")
    
    def consultar_historial(self):
        """Consulta y muestra el historial médico del paciente"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        historial = self._generar_historial_detallado()
        self.resultado_text.setText(historial)
    
    def mostrar_info_paciente(self):
        """Muestra la información básica del paciente"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            QMessageBox.warning(self, "❌ Error", "Debe crear un paciente primero")
            return
        
        self.resultado_text.setText(self._generar_info_completa())
    
    def buscar_paciente_por_dui(self):
        """Busca un paciente por su DUI y abre una ventana con su información"""
        from PyQt6.QtWidgets import QInputDialog
        
        dui, ok = QInputDialog.getText(self, '🔍 Buscar Paciente', 
                                      'Ingrese el DUI del paciente:')
        
        if ok and dui.strip():
            dui = dui.strip()
            pacientes = self.controlador.get_todos_los_pacientes()
            paciente_encontrado = None
            
            # Buscar el paciente por DUI
            for paciente in pacientes:
                if paciente.dui == dui:
                    paciente_encontrado = paciente
                    break
            
            if paciente_encontrado:
                # Abrir ventana con información del paciente
                ventana_info = VentanaInfoPaciente(paciente_encontrado, self.controlador, self)
                ventana_info.exec()
            else:
                QMessageBox.warning(self, "❌ No Encontrado", 
                                  f"No se encontró ningún paciente con DUI: {dui}")
        elif ok:
            QMessageBox.warning(self, "❌ Error", "Debe ingresar un DUI válido")
    
    def actualizar_label_dui(self):
        """Actualiza el label del DUI basado en la edad del paciente"""
        fecha_qdate = self.edad_edit.date()
        fecha_nacimiento = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
        edad = self.controlador.calcular_edad(fecha_nacimiento)
        
        if edad < 18:
            self.dui_label.setText("DUI del Responsable:")
            self.dui_edit.setPlaceholderText("DUI del padre, madre o tutor legal")
        else:
            self.dui_label.setText("DUI:")
            self.dui_edit.setPlaceholderText("Documento único de identidad")
    
    def _generar_info_completa(self) -> str:
        """Genera la información completa del paciente con formato mejorado"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            return "No hay paciente seleccionado"
        
        edad = self.controlador.calcular_edad(paciente_actual.fecha_nacimiento)
        dui_label = "DUI del Responsable" if edad < 18 else "DUI"
        edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else " (Mayor de edad)")
            
        separador = "=" * 60
        info = f"""
{separador}
🏥 INFORMACIÓN DEL PACIENTE - CLÍNICA DENTAL
{separador}

👤 DATOS PERSONALES:
   ▪ Nombre Completo: {paciente_actual.nombre} {paciente_actual.apellido}
   ▪ Edad: {edad_info}
   ▪ {dui_label}: {paciente_actual.dui}
   ▪ Teléfono: {self.controlador.formatear_telefono(paciente_actual.telefono)}
   ▪ Correo Electrónico: {paciente_actual.correo if paciente_actual.correo else 'No especificado'}

💰 INFORMACIÓN FINANCIERA:
   ▪ Saldo Pendiente: ${paciente_actual.saldo_pendiente:,.2f}
   ▪ Estado: {'🔴 Pendiente de pago' if paciente_actual.saldo_pendiente > 0 else '🟢 Al día'}

📊 RESUMEN MÉDICO:
   ▪ Tratamientos Realizados: {len(paciente_actual.historial_medico)}
   ▪ Citas Agendadas: {len(paciente_actual.citas)}
   ▪ Costo Total Tratamientos: ${paciente_actual.calcular_total_tratamientos():,.2f}
   ▪ Costo Total Citas: ${paciente_actual.calcular_total_citas():,.2f}

⏰ Última Actualización: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}
{separador}
"""
        return info
    
    def _generar_historial_detallado(self) -> str:
        """Genera el historial médico detallado con formato mejorado"""
        paciente_actual = self.controlador.get_paciente_actual()
        if not paciente_actual:
            return "No hay paciente seleccionado"
        
        edad = self.controlador.calcular_edad(paciente_actual.fecha_nacimiento)
        dui_label = "DUI del Responsable" if edad < 18 else "DUI"
        edad_info = f"{edad} años" + (" (Menor de edad)" if edad < 18 else "")
            
        separador_principal = "=" * 60
        separador_seccion = "-" * 40
        
        historial = f"""
{separador_principal}
📋 HISTORIAL MÉDICO COMPLETO
{separador_principal}

👤 Paciente: {paciente_actual.nombre} {paciente_actual.apellido} - {edad_info}
📅 Fecha de Consulta: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}

{separador_seccion}
🩺 TRATAMIENTOS REALIZADOS ({len(paciente_actual.historial_medico)})
{separador_seccion}
"""
        
        if not paciente_actual.historial_medico:
            historial += "\n   📝 No hay tratamientos registrados en el historial.\n"
        else:
            for i, tratamiento in enumerate(paciente_actual.historial_medico, 1):
                estado_icon = self.controlador.get_estado_icon(tratamiento.estado)
                historial += f"""
   ┌─ Tratamiento #{i:02d}
   │ 🆔 ID: {tratamiento.id_tratamiento}
   │ 📄 Descripción: {tratamiento.descripcion}
   │ 💵 Costo: ${tratamiento.costo:,.2f}
   │ 📅 Fecha: {tratamiento.fecha_realizacion}
   │ {estado_icon} Estado: {tratamiento.estado}
   │ 👨‍⚕️ Doctor: Dr. {tratamiento.doctor.nombre} {tratamiento.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        historial += f"""
{separador_seccion}
📅 CITAS PROGRAMADAS ({len(paciente_actual.citas)})
{separador_seccion}
"""
        
        if not paciente_actual.citas:
            historial += "\n   📝 No hay citas programadas.\n"
        else:
            for i, cita in enumerate(paciente_actual.citas, 1):
                estado_icon = self.controlador.get_estado_icon(cita.estado)
                historial += f"""
   ┌─ Cita #{i:02d}
   │ 🆔 ID: {cita.id_cita}
   │ ⏰ Inicio: {cita.hora_inicio}
   │ ⏰ Fin: {cita.hora_fin}
   │ 💵 Costo: ${cita.costo_cita:,.2f}
   │ {estado_icon} Estado: {cita.estado}
   │ 👨‍⚕️ Doctor: Dr. {cita.doctor.nombre} {cita.doctor.apellido}
   └─────────────────────────────────────────────────
"""
        
        # Resumen financiero
        total_tratamientos = paciente_actual.calcular_total_tratamientos()
        total_citas = paciente_actual.calcular_total_citas()
        total_general = total_tratamientos + total_citas
        
        historial += f"""
{separador_seccion}
💰 RESUMEN FINANCIERO
{separador_seccion}

   📊 Estadísticas:
   ▪ Total de Tratamientos: {len(paciente_actual.historial_medico)} - ${total_tratamientos:,.2f}
   ▪ Total de Citas: {len(paciente_actual.citas)} - ${total_citas:,.2f}
   ▪ Subtotal General: ${total_general:,.2f}
   ▪ Saldo Pendiente: ${paciente_actual.saldo_pendiente:,.2f}
   
   💳 Balance Final: ${paciente_actual.get_balance_total():,.2f}

{separador_principal}
"""
        return historial

def main():
    app = QApplication([])
    window = PacienteWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
