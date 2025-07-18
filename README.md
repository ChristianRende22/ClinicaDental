# 🦷 Sistema de Gestión Integral para Clínica Dental

Sistema completo de gestión desarrollado en **Python** con **PyQt6** y **MySQL**, diseñado para optimizar la administración integral de **Dental Smiling**.
Implementa arquitectura **MVC (Modelo-Vista-Controlador)** para un código organizado, mantenible y escalable.

---

## 🏥 Descripción del problema

**Dental Smiling** es una clínica dental privada que cuenta con:

* **Personal**: 1 directora (Dra. Jacquelin Zepeda) + 2 doctores + 3 asistentes
* **Problema principal**: Gestión manual mediante papel, archivos físicos y almacenamiento tradicional

---

## 🎗 Arquitectura del Sistema

El sistema utiliza **arquitectura MVC** para cada módulo principal:

```
📈 MODELO
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
```

### Módulos Implementados

* 🔐 Login: Autenticación y control de acceso
* 📋 Menú: Navegación principal
* 👤 Paciente: Gestión de pacientes
* 👨‍⚕️ Doctor: Administración del personal médico
* 🗕 Cita: Programación de citas
* 💊 Tratamiento: Gestión de tratamientos
* 🧾 Factura: Control financiero y facturación
* ⏰ Horario: Administración de horarios médicos

---

## 🛠 Tecnologías Utilizadas

* **Python 3.13.3**
* **PyQt6**
* **MySQL**
* **mysql-connector-python**
* **DBeaver** (para administración de base de datos)

---

## 📋 Instrucciones de uso

1. **Inicio de sesión**:

   * **Usuario**: admin
   * **Password**: 123456

2. Al ejecutar la aplicación:

   * Se desplegará la interfaz de inicio de sesión, donde podrá validar la funcionalidad de autenticación de usuarios.
   * Una vez cerrada la ventana de inicio de sesión, se abrirá automáticamente la interfaz del menú principal.
   * Desde el menú principal, es posible acceder y evaluar el funcionamiento de todos los módulos y modelos del sistema.
---

## 📋 Requisitos del Sistema

* **Sistema Operativo**:

  * Windows 10/11 (principal)
  * macOS (compatibilidad extendida)
* **Python**: 3.13.3 o superior
* **Base de Datos**:

  * MySQL 5.7 o superior
  * MySQL Workbench (recomendado)
* **Dependencias Python**:

  * PyQt6>=6.0.0
  * mysql-connector-python>=8.0.0

---

## 🚀 Instalación y Configuración

### 1. Preparación del Entorno

```bash
git clone [URL_DEL_REPOSITORIO]
cd clinica-dental
python -m venv venv
```

Activar entorno virtual:

* **Windows**:

```bash
venv\Scripts\activate
```

* **macOS/Linux**:

```bash
source venv/bin/activate
```

### 2. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos

* Instalar MySQL Server y MySQL Workbench
* Ejecutar script SQL ubicado en: `DB_clinica/GestionClinicaDental.sql`
* Configurar credenciales en el archivo del modelo:

```python
HOST = 'localhost'
USER = 'root'
PASSWORD = 'tu_password_mysql'
DATABASE = 'ClinicaDental'
PORT = 3306 o 3307
```

### 4. Ejecutar la Aplicación

```bash
cd "CLINICA DENTAL/Main"
python ControladorClinica.py
```

---

## 📊 Módulos del Sistema

### 👤 Gestión de Pacientes

* Crear, consultar, actualizar y eliminar pacientes
* Historial médico y búsqueda avanzada

### 👨‍⚕️ Gestión de Doctores

* Registro y consulta de doctores
* Gestión de especialidades y horarios
* Administración de datos y eliminación segura

### 🗕 Sistema de Citas

* Programación, modificación y cancelación de citas
* Confirmación de asistencia y estados:

  * 🟡 Pendiente
  * 🟢 Confirmada
  * ❌ Cancelada
  * ✅ Asistida
  * 🔴 Ausente
* Consulta de agenda y cálculo de costos

### 💊 Gestión de Tratamientos

* Registro y consulta de tratamientos
* Control de costos
* Actualización
* Eliminación
* Reportes


### 🧾 Sistema de Facturación

* Generación automática
* Control de pagos
* Consulta de facturas
* Modificación

### Control de horarios
* Definir horarios: Disponibilidad por doctor
* Gestión de estados
* Visualización de horarios
* Configuración de días y horas laborales
* Reportes: Ocupación y disponibilidad


## Autores 
- **Christian Renderos** 
- **Melisa Rivas** 
- **Lorena Arriola** 
- **Alisson Quijano** 