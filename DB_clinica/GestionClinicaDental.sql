-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ClinicaDental;
USE ClinicaDental;

-- Tabla: Paciente
CREATE TABLE Paciente (
	ID_Paciente INT AUTO_INCREMENT PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	Apellido VARCHAR(50) NOT NULL,
	Fecha_Nacimiento DATE NOT NULL,
	DUI VARCHAR(10) ,
	Telefono CHAR(8),
	Correo VARCHAR(25)
);

-- Tabla: Doctor
CREATE TABLE Doctor (
	ID_Doctor VARCHAR(10) UNIQUE PRIMARY key NOT NULL,
	Nombre VARCHAR(50) ,
	Apellido VARCHAR(50) ,
	Especialidad VARCHAR(50) ,
	Telefono CHAR(8)  ,
	Correo VARCHAR(25) ,
	Contrasena VARCHAR(255) 
);

-- Tabla: Horario
CREATE TABLE Horario (
	ID_Horario VARCHAR(10) PRIMARY KEY,
	ID_Doctor VARCHAR(10) NOT NULL,
	Hora_Inicio TIME NOT NULL,
	Hora_Fin TIME NOT NULL,
	Disponible BOOLEAN DEFAULT TRUE,
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE
);

-- Tabla: Historial_Medico
CREATE TABLE Historial_Medico (
	ID_Historial INT AUTO_INCREMENT PRIMARY KEY,
	ID_Paciente INT NOT NULL,
	Fecha_Creacion DATE NOT NULL,
	Notas_Generales VARCHAR(100),
	Estado ENUM('Activo', 'Archivado') DEFAULT 'Activo',
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE
);

-- Tabla: Tratamiento
CREATE TABLE Tratamiento (
	ID_Tratamiento INT AUTO_INCREMENT PRIMARY KEY,
	ID_Doctor VARCHAR(10) NOT NULL,
	Descripcion TEXT NOT NULL,
	Costo DECIMAL(10,2) NOT NULL,
	Fecha DATETIME NOT NULL,
	Estado ENUM('Pendiente', 'En Progreso', 'Finalizado') DEFAULT 'Pendiente',
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE
);

-- Tabla: Cita
CREATE TABLE Cita (
	ID_Cita INT AUTO_INCREMENT PRIMARY KEY,
	ID_Paciente INT NOT NULL,
	ID_Doctor VARCHAR(10) NOT NULL,
	ID_Tratamiento INT NOT NULL,
	Fecha DATETIME NOT NULL,
	Hora_Inicio TIME NOT NULL,
	Hora_Fin TIME NOT NULL,
	Estado ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Ausente', 'Asistida') DEFAULT 'Pendiente',
	Costo DECIMAL(10,2) NOT NULL,
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE,
	FOREIGN KEY (ID_Tratamiento) REFERENCES Tratamiento(ID_Tratamiento) ON DELETE CASCADE
);

-- Tabla: Factura
CREATE TABLE Factura (
    ID_Factura INT AUTO_INCREMENT PRIMARY KEY,
    ID_Factura_Custom VARCHAR(50),
    ID_Paciente INT,
    Fecha_Emision DATETIME,
    Descripcion_Servicio TEXT,
    Monto_Servicio DECIMAL(10,2),
    Monto_Total DECIMAL(10,2),
    Estado_Pago VARCHAR(20),
    FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente)
);
-- Tabla: Asistente
CREATE TABLE Asistente (
	ID_Asistente INT AUTO_INCREMENT PRIMARY KEY,
	Nombre VARCHAR(50) NOT NULL,
	Apellido VARCHAR(50) NOT NULL,
	Telefono VARCHAR(15) NOT NULL,
	Correo VARCHAR(100) NOT NULL,
	Contrasena VARCHAR(255) NOT NULL
);

-- Tablas de relación
CREATE TABLE Tratamiento_Factura (
	ID_Tratamiento INT NOT NULL,
	ID_Factura INT NOT NULL,
	PRIMARY KEY (ID_Tratamiento, ID_Factura),
	FOREIGN KEY (ID_Tratamiento) REFERENCES Tratamiento(ID_Tratamiento) ON DELETE CASCADE,
	FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura) ON DELETE CASCADE
);

CREATE TABLE Asistente_Paciente (
	ID_Asistente INT NOT NULL,
	ID_Paciente INT NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Paciente),
	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE
);

CREATE TABLE Asistente_Cita (
	ID_Asistente INT NOT NULL,
	ID_Cita INT NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Cita),
	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Cita) REFERENCES Cita(ID_Cita) ON DELETE CASCADE
);

CREATE TABLE Asistente_Factura (
	ID_Asistente INT NOT NULL,
	ID_Factura INT NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Factura),
	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura) ON DELETE CASCADE
);


INSERT INTO Paciente (Nombre, Apellido, Fecha_Nacimiento, Telefono, Correo) VALUES
('Laura', 'Mendoza', '1991-04-12', '70112233', 'laura.mendoza@correo.com'),
('Ricardo', 'Vásquez', '1987-09-23', '70223344', 'ricardo.vas@correo.com'),
('Carla', 'López', '1995-06-15', '70334455', 'carla.lopez@correo.com');

INSERT INTO Doctor (ID_Doctor, Nombre, Apellido, Especialidad, Telefono, Correo, Contrasena) VALUES
(1234, 'Daniela', 'Pineda', 'Odontología General', '71112233', 'daniela.pineda@doc.com', 'clave123'),
(2345, 'Luis', 'Zelaya', 'Ortodoncia', '72223344', 'luis.zelaya@doc.com', 'clave234'),
(3456, 'Rebeca', 'García', 'Endodoncia', '73334455', 'rebeca.garcia@doc.com', 'clave345');

INSERT INTO Historial_Medico (ID_Paciente, Fecha_Creacion, Notas_Generales) VALUES
(1, '2024-05-01', 'Paciente con caries recurrentes.'),
(2, '2024-06-10', 'Evaluación inicial.'),
(3, '2024-07-05', 'Control de ortodoncia.');

INSERT INTO Horario (ID_Horario,ID_Doctor, Hora_Inicio, Hora_Fin, Disponible) VALUES
("H001",1234,  '08:00:00', '12:00:00', TRUE),
("H002",2345, '13:00:00', '17:00:00', TRUE),
("H003",3456, '08:00:00', '12:00:00', FALSE);


INSERT INTO Tratamiento (ID_Doctor, Descripcion, Costo, Fecha, Estado) VALUES
(1234, 'Limpieza dental general', 20.00, '2025-07-01 09:30:00', 'Finalizado'),
(2345, 'Colocación de brackets', 450.00, '2025-07-01 15:00:00', 'En Progreso'),
(3456, 'Tratamiento de conducto', 250.00, '2025-07-02 10:30:00', 'Pendiente');


INSERT INTO Cita (ID_Paciente, ID_Doctor, ID_Tratamiento, Fecha, Hora_Inicio, Hora_Fin, Estado, Costo) VALUES
(1, 1234, 1, '2025-07-01 09:00:00', '09:00:00', '09:30:00', 'Confirmada', 20.00),
(2, 2345, 2, '2025-07-01 14:30:00', '14:30:00', '15:00:00', 'Pendiente', 45.00),
(3, 3456, 3, '2025-07-02 10:00:00', '10:00:00', '10:30:00', 'Confirmada', 60.00);

INSERT INTO Factura (
    ID_Paciente, ID_Factura_Custom, Fecha_Emision, 
    Descripcion_Servicio, Monto_Servicio, Monto_Total, Estado_Pago) VALUES
(1, 'FAC-1-20250718145401', '2025-07-01', 'Limpieza dental', 20.00, 20.00, 'Pagada'),
(2, 'FAC-2-20250718145402', '2025-07-01', 'Ortodoncia', 450.00, 450.00, 'Pendiente'),
(3, 'FAC-3-20250718145403', '2025-07-02', 'Extracción', 250.00, 250.00, 'Pendiente');


INSERT INTO Asistente (Nombre, Apellido, Telefono, Correo, Contrasena) VALUES
('Ivonne', 'Morales', '70445566', 'ivonne.morales@clinicadental.com', 'asist123'),
('Pedro', 'Luna', '70556677', 'pedro.luna@clinicadental.com', 'asist234'),
('Tatiana', 'Ramos', '70667788', 'tatiana.ramos@clinicadental.com', 'asist345');


INSERT INTO Tratamiento_Factura (ID_Tratamiento, ID_Factura) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Asistente_Paciente (ID_Asistente, ID_Paciente) VALUES
(1, 1),
(2, 2),
(3, 3);


INSERT INTO Asistente_Cita (ID_Asistente, ID_Cita) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Asistente_Factura (ID_Asistente, ID_Factura) VALUES
(1, 1),
(2, 2),
(3, 3);
