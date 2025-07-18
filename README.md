🦷 Sistema de Gestión Integral para Clínica Dental

    Un sistema completo de gestión desarrollado en Python con PyQt6 y MySQL, específicamente diseñado para optimizar la administración integral de Dental Smiling.
    El sistema implementa una arquitectura MVC (Modelo-Vista-Controlador) para garantizar un código organizado, mantenible y escalable.

🏥 Descripción del problema

    Dental Smiling es una clínica dental privada que cuenta con:
    •	Personal: 1 directora (Dra. Jacquelin Zepeda) + 2 Doctores + 3 Asistentes
    •	Problema principal: Gestión manual mediante papel, archivos físicos y sistemas de almacenamiento tradicionales.

🏗 Arquitectura del Sistema

    El sistema utiliza arquitectura MVC para cada módulo principal:
        📊 MODELO 
        ├── Gestión de datos y lógica de negocio
        ├── Conexión directa con MySQL
        ├── Validaciones de datos
        └── Operaciones CRUD
        👀 VISTA 
        ├── Interfaces gráficas PyQt6
        ├── Formularios de entrada
        ├── Tablas de visualización
        └── Elementos de navegación
        🎮 CONTROLADOR 
        ├── Lógica de aplicación
        ├── Coordinación entre Modelo y Vista
        ├── Manejo de eventos
        └── Validaciones de entrada
    Módulos con Arquitectura MVC
    •	🔐 Login: Autenticación y control de acceso
    •	📋 Menú: Navegación principal del sistema
    •	👤 Paciente: Gestión integral de pacientes
    •	👨‍⚕️ Doctor: Administración de personal médico
    •	📅 Cita: Sistema de programación de citas
    •	💊 Tratamiento: Gestión de procedimientos médicos
    •	🧾 Factura: Control financiero y facturación
    •	⏰ Horario: Administración de disponibilidad médica

🛠 Tecnologías Utilizadas

    •	Python 3.13.3: Lenguaje de programación principal
    •	PyQt6: Framework para interfaz gráfica moderna
    •	MySQL: Sistema de gestión de base de datos relacional
    •	mysql-connector-python: Conector directo Python-MySQL
    •	DBeaver: Herramienta de administración de base de datos

📋Instrucciones de uso

    1.	Inicio de sesión: 
        •	Usuario: admin
        •	Password: 123456

    2.	Al ejecutarlo, se desplegará la interfaz de inicio de sesión, donde podrá validar la funcionalidad de autenticación de usuarios.
        Una vez cerrada la ventana de inicio de sesión, se abrirá automáticamente la interfaz del menú principal.
        Desde el menú principal, es posible acceder y evaluar el funcionamiento de todos los módulos y modelos del sistema.

📋 Requisitos del Sistema

    Sistema Operativo: 
        •	Windows 10/11 (Soporte principal)
        •	macOS (Compatibilidad extendida)
        Python: Python 3.13.3 o superior
    Base de Datos:
        •	MySQL 5.7 o superior
        •	MySQL Workbench (recomendado)
    dependencia con python: 
        •	PyQt6>=6.0.0
        •	mysql-connector-python>=8.0.0

🚀 Instalación y Configuración

    1. Preparación del Entorno
        Clonar repositorio:
        •	git clone [URL_DEL_REPOSITORIO]
        •	cd clinica-dental
        Crear entorno virtual:
        •	python -m venv venv
        Activar entorno virtual:
        Windows:
        •	venv\Scripts\activate
        # macOS/Linux:
        •	source venv/bin/activate
    2. Instalación de dependencias
        
    3. Configuración de Base de Datos
        •	Instalar MySQL Server y MySQL Workbench
        •	Ejecutar script SQL ubicado en: DB_clinica/GestionClinicaDental.sql
        •	Configurar credenciales en los archivos de modelo
        Configuración de conexión (ajustar según su instalación):
        HOST = 'localhost'
        USER = 'root'  
        PASSWORD = 'tu_password_mysql'
        DATABASE = 'ClinicaDental'
        PORT = 3306
    4. Ejecutar la Aplicación
        •	cd "CLINICA DENTAL/Main"
        •	python ControladorClinica.py

📊 Módulos del Sistema

    👤 Gestión de Pacientes
        Funcionalidades principales:
        •	Crear paciente: Registro completo con validaciones
        •	 Consultar información: Datos personales y médicos
        •	Historial médico: Tratamientos y citas realizadas
        •	Actualizar datos: Modificación de información
        •	Eliminar registro: Con validaciones de integridad
        •	 Búsqueda avanzada: Por nombre, apellido o ID
    👨‍⚕️ Gestión de Doctores
        Funcionalidades principales:
        •	Registro de doctor: Datos profesionales completos
        •	Gestión de especialidades: Registro de áreas médicas
        •	 Administración de horarios: Disponibilidad semanal
        •	Consulta de información: Datos y estadísticas
        •	Actualización de datos: Modificación de información
        •	Eliminación controlada: Con validaciones
    📅 Sistema de Citas
        Funcionalidades principales:
        •	Crear cita: Programación con validaciones
        •	Modificar cita: Cambios de fecha/hora/doctor
        •	 Cancelar cita: Con registro de motivo
        •	Confirmar asistencia: Control de estados
        •	Cálculo automático: Montos según tratamiento
        •	Consulta de agenda: Por doctor y fecha
        Estados de Cita:
            ├── 🟡 Pendiente: Recién programada
            ├── 🟢 Confirmada: Paciente confirmó asistencia  
            ├── ❌ Cancelada: Cita cancelada
            ├── ✅ Asistida: Paciente asistió a la cita
            └── 🔴 Ausente: Paciente no asistió 
    💊 Gestión de Tratamientos
        Funcionalidades principales:
        •	Registro de tratamientos: Procedimientos realizados
        •	Control de costos: Precios por tratamiento
        •	 Consulta de historial: Tratamientos por paciente
        •	Actualización: Modificación de datos
        •	Eliminación: Con validaciones
        •	Reportes: Estadísticas de tratamientos
    🧾 Sistema de Facturación
        Funcionalidades principales:
        •	Generación automática: Facturas basadas en citas
        •	Control de pagos: Estados financieros
        •	Reportes financieros: Ingresos y estadísticas
        •	Consulta de facturas: Por paciente y fecha
        •	Modificación: Ajustes necesarios
        •	Análisis: Indicadores financieros
    ⏰ Control de Horarios
        Funcionalidades Principales:
        •	Definir horarios: Disponibilidad por doctor
        •	Gestión de estados: Disponible/Ocupado/No disponible
        •	Consulta de agenda: Visualización de horarios
        •	Configuración: Días y horas laborales
        •	Reportes: Ocupación y disponibilidad



