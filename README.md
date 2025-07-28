# 🦷 Sistema de Gestión Integral para Clínica Dental

Sistema completo de gestión desarrollado en **Python** con **PyQt6** y **MySQL**, diseñado para optimizar la administración integral de la clínica **Dental Smiling**. Este software digitaliza todos los procesos clave: gestión de pacientes, doctores, citas, tratamientos, horarios y facturación, eliminando el uso de papel y mejorando la eficiencia operativa.

Implementa una arquitectura **MVC (Modelo-Vista-Controlador)** para asegurar modularidad, mantenimiento sencillo y escalabilidad del sistema.

---

## 🧾 Tabla de Contenidos

- [🏥 Descripción del problema](#🏥-descripción-del-problema)
- [🎗 Arquitectura del sistema](#🎗-arquitectura-del-sistema)
- [📊 Módulos del sistema](#📊-módulos-del-sistema)
- [🛠 Tecnologías utilizadas](#🛠-tecnologías-utilizadas)
- [📋 Requisitos del sistema](#📋-requisitos-del-sistema)
- [🚀 Instalación y configuración](#🚀-instalación-y-configuración)
- [📋 Instrucciones de uso](#📋-instrucciones-de-uso)
- [🙌 Autores](#🙌-autores)

---

## 🏥 Descripción del problema

**Dental Smiling**, ubicada en El Salvador, es una clínica dental privada con:

- 1 directora (Dra. Jacquelin Zepeda)
- 2 doctores
- 3 asistentes

**Problema principal**: la gestión se realizaba de forma manual mediante archivos físicos, lo cual dificultaba el control, seguimiento y eficiencia administrativa.

**Objetivo del sistema**: modernizar el manejo de la clínica dental mediante un sistema digital centralizado que controle todos los procesos clave.

---

## 🎗 Arquitectura del sistema

El proyecto está organizado bajo el patrón **MVC (Modelo - Vista - Controlador)** para separar las responsabilidades y facilitar el mantenimiento del sistema.

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


## 📊 Módulos del sistema

Cada módulo es independiente y sigue la estructura MVC.

### 🔐 Login
- Verificación de credenciales.
- Acceso controlado por roles.

### 👤 Pacientes
- CRUD de pacientes.
- Historial médico.
- Búsqueda por campos personalizados.

### 👨‍⚕️ Doctores
- Registro y eliminación.
- Gestión de horarios y especialidades.

### 🗓 Citas
- Programar, cancelar y modificar citas.
- Estados: Pendiente, Confirmada, Cancelada, Asistida, Ausente.
- Consulta de agenda y cálculo automático de costos.

### 💊 Tratamientos
- Registro de tratamientos.
- Actualización de precios.
- Consulta y eliminación.

### 🧾 Facturación
- Generación de facturas basada en tratamientos.
- Control de pagos.
- Reportes detallados.

### ⏰ Horarios
- Configuración de disponibilidad médica.
- Visualización de horarios por doctor.
- Cálculo de ocupación y reporte de disponibilidad.

---

## 🛠 Tecnologías Utilizadas

* **Python 3.13.3**
* **PyQt6**
* **MySQL**
* **mysql-connector-python**
* **DBeaver** (para administración de base de datos)

---

## 📋 Instrucciones de uso

1. **Inicio de la aplicación**:

  * Ejecuta el archivo `ControladorClinica.py` para iniciar el sistema.

2. **Inicio de sesión**:

  * Ingresa el nombre de usuario de asistente.
  * La contraseña corresponde al nombre de usuario seguido de `123`.  
    Ejemplo: Si el usuario es `asistente1`, la contraseña será `asistente1123`.

3. Tras iniciar sesión:

  * Se abrirá el menú principal desde donde puedes acceder y gestionar todos los módulos y funcionalidades del sistema.

## 📋 Requisitos del sistema

- **Sistema operativo**:
  - Windows 10/11 (principal)
  - macOS (compatibilidad extendida)
- **Python**: versión 3.13.3 o superior
- **MySQL**: versión 5.7 o superior
- **Dependencias**:
  ```bash
  pip install -r requirements.txt
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
* Ejecutar script SQL ubicado en: `DB/GestionClinicaDental.sql`
* **🎯 Nueva Configuración Centralizada**: La configuración se encuentra en la carpeta `Config`:

```python
# Config/database_config.py
class DatabaseConfig:
    HOST = 'localhost'
    PORT = 3307 o 3306
    USER = 'root'
    PASSWORD = '1234'
    DATABASE = 'ClinicaDental'
```

**✅ Ventajas de la nueva configuración:**
- Un solo archivo para toda la configuración de BD
- Manejo de errores mejorado
- Eliminación de código duplicado
- Fácil cambio entre ambientes (desarrollo/producción)

**🧪 Probar configuración:**
```bash
cd Config
python database_config.py
```

Ver documentación completa en: `Config/README_CONFIGURACION.md`

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