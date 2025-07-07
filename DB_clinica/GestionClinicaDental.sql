-- Crear la base de datos
create database if not exists ClinicaDental;

-- CREACION DE TABLAS Y RELACIONES
CREATE TABLE ClinicaDental.Paciente (
	ID_Paciente INTEGER auto_increment PRIMARY KEY,
	Nombre varchar(50) NOT NULL,
	Apellido varchar(50) NOT NULL,
	Fecha_Nacimiento DATE NOT NULL,
	DUI varchar(10) UNIQUE, -- ESTO PUEDE SER NULL, POR LOS PACIENTES QUE SON MENORES DE EDAD
	Telefono CHAR(8),
	Correo VARCHAR(25)
);

-- Tabla: historial médico
CREATE TABLE ClinicaDental.Historial_Medico (
	ID_Historial INTEGER auto_increment PRIMARY KEY,
	ID_Paciente INTEGER NOT NULL,
	Fecha_Creacion DATE NOT NULL,
	Notas_Generales varchar(100),
	Estado ENUM('Activo', 'Archivado') DEFAULT 'Activo',
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE
);

-- Tabla: Doctor
CREATE TABLE ClinicaDental.Doctor (
	ID_Doctor varchar(50) PRIMARY KEY,
	Nombre varchar(50) NOT NULL,
	Apellido varchar(50) NOT NULL,
	Especialidad varchar(50) NOT NULL,
	Telefono CHAR(8) NOT NULL,
	Correo varchar(25) NOT NULL,
	Contrasena varchar(255) NOT NULL
);

-- Tabla: Horario
CREATE TABLE ClinicaDental.Horario (
	ID_Horario INTEGER auto_increment PRIMARY KEY,
	ID_Doctor INTEGER NOT NULL,
	Fecha DATE NOT NULL,
	Hora_Inicio TIME NOT NULL,
	Hora_Fin TIME NOT NULL,
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE
);

-- Tabla: Cita
CREATE TABLE ClinicaDental.Cita (
	ID_Cita INTEGER auto_increment PRIMARY KEY,
	ID_Paciente INTEGER NOT NULL,
	ID_Doctor INTEGER NOT NULL,
	ID_Tratamiento INTEGER NOT NULL,
	Fecha DATETIME NOT NULL,
	Hora_Inicio TIME NOT NULL,
	Hora_Fin TIME NOT NULL,
	Estado ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Ausente', 'Asistida') DEFAULT 'Pendiente',
	Costo DECIMAL(10,2) NOT NULL,
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE
);

-- Tabla: Tratamiento
CREATE TABLE ClinicaDental.Tratamiento (
	ID_Tratamiento INTEGER auto_increment PRIMARY KEY,
	ID_Doctor INTEGER NOT NULL,
	Descripcion TEXT NOT NULL,
	Costo DECIMAL(10,2) NOT NULL,
	Fecha DATETIME NOT NULL,
	Estado ENUM('Pendiente', 'En Progreso', 'Finalizado') DEFAULT 'Pendiente',
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE,
	FOREIGN KEY (ID_Doctor) REFERENCES Doctor(ID_Doctor) ON DELETE CASCADE
);

-- Tabla: Factura
CREATE TABLE ClinicaDental.Factura (
	ID_Factura INTEGER auto_increment PRIMARY KEY,
	ID_Paciente INTEGER NOT NULL,
	Fecha_Emision DATE NOT NULL,
	Monto_Total DECIMAL(10,2) NOT NULL,
	Estado_Pago ENUM('Pendiente', 'Pagada', 'Vencida') DEFAULT 'Pendiente',
	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE
);

-- Tabla: Asistente
CREATE TABLE ClinicaDental.Asistente (
	ID_Asistente INTEGER auto_increment PRIMARY KEY,
	Nombre varchar(50) NOT NULL,
	Apellido varchar(50) NOT NULL,
	Telefono varchar(15) NOT NULL,
	Correo varchar(100) NOT NULL,
	Contrasena varchar(255) NOT NULL
);

-- Tabla: Tratamiento_Factura
CREATE TABLE ClinicaDental.Tratamiento_Factura (
	ID_Tratamiento INTEGER NOT NULL,
	ID_Factura INTEGER NOT NULL,
	PRIMARY KEY (ID_Tratamiento, ID_Factura),
  	FOREIGN KEY (ID_Tratamiento) REFERENCES Tratamiento(ID_Tratamiento) ON DELETE CASCADE,
  	FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura) ON DELETE CASCADE
);

-- Tabla: Asistente_Paciente
CREATE TABLE ClinicaDental.Asistente_Paciente (
	ID_Asistente INTEGER NOT NULL,
	ID_Paciente INTEGER NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Paciente),
  	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
  	FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente) ON DELETE CASCADE
);

-- Tabla: Asistente_Cita
CREATE TABLE ClinicaDental.Asistente_Cita (
	ID_Asistente INTEGER NOT NULL,
	ID_Cita INTEGER NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Cita),
  	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
  	FOREIGN KEY (ID_Cita) REFERENCES Cita(ID_Cita) ON DELETE CASCADE
);

-- Tabla: Asistente_Factura
CREATE TABLE ClinicaDental.Asistente_Factura (
	ID_Asistente INTEGER NOT NULL,
	ID_Factura INTEGER NOT NULL,
	PRIMARY KEY (ID_Asistente, ID_Factura),
  	FOREIGN KEY (ID_Asistente) REFERENCES Asistente(ID_Asistente) ON DELETE CASCADE,
  	FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura) ON DELETE CASCADE
);

-- INGRESO DE REGISTROS - SEGUNDA PARTE
INSERT INTO ClinicaDental.Paciente (Nombre, Apellido, Fecha_Nacimiento, DUI, Telefono, Correo) VALUES
('Laura', 'Mendoza', '1991-04-12', '12345678-9', '70112233', 'laura.mendoza@correo.com'),
('Ricardo', 'Vásquez', '1987-09-23', '23456789-0', '70223344', 'ricardo.vas@correo.com'),
('Carla', 'López', '1995-06-15', '34567890-1', '70334455', 'carla.lopez@correo.com');

INSERT INTO ClinicaDental.Doctor (Nombre, Apellido, Especialidad, Telefono, Correo, Contrasena) VALUES
('Daniela', 'Pineda', 'Odontología General', '71112233', 'daniela.pineda@doc.com', 'clave123'),
('Luis', 'Zelaya', 'Ortodoncia', '72223344', 'luis.zelaya@doc.com', 'clave234'),
('Rebeca', 'García', 'Endodoncia', '73334455', 'rebeca.garcia@doc.com', 'clave345');

INSERT INTO ClinicaDental.Historial_Medico (ID_Paciente, Fecha_Creacion, Notas_Generales) VALUES
(4, '2024-05-01', 'Paciente con caries recurrentes.'),
(5, '2024-06-10', 'Evaluación inicial.'),
(6, '2024-07-05', 'Control de ortodoncia.');

INSERT INTO ClinicaDental.Horario (ID_Doctor, Dia, Hora_Inicio, Hora_Fin, Disponible) VALUES
(1, '2025-07-01', '08:00:00', '12:00:00', TRUE),
(2, '2025-07-01', '13:00:00', '17:00:00', TRUE),
(3, '2025-07-02', '08:00:00', '12:00:00', FALSE);

INSERT INTO ClinicaDental.Cita (ID_Paciente, ID_Doctor, Fecha, Estado, Costo) VALUES
(4, 1, '2025-07-01 09:00:00', 'confirmada', 20.00),
(5, 2, '2025-07-01 14:30:00', 'pendiente', 45.00),
(6, 3, '2025-07-02 10:00:00', 'confirmada', 60.00);

INSERT INTO ClinicaDental.Tratamiento (ID_Paciente, ID_Doctor, Descripcion, Costo, Fecha, Estado) VALUES
(4, 1, 'Limpieza dental general', 20.00, '2025-07-01 09:30:00', 'finalizado'),
(5, 2, 'Colocación de brackets', 450.00, '2025-07-01 15:00:00', 'en_progreso'),
(6, 3, 'Tratamiento de conducto', 250.00, '2025-07-02 10:30:00', 'pendiente');

INSERT INTO ClinicaDental.Factura (ID_Paciente, Fecha_Emision, Monto_Total, Estado_Pago) VALUES
(4, '2025-07-01', 20.00, 'pagada'),
(5, '2025-07-01', 450.00, 'pendiente'),
(6, '2025-07-02', 250.00, 'pendiente');

INSERT INTO ClinicaDental.Asistente (Nombre, Apellido, Telefono, Correo, Contrasena) VALUES
('Ivonne', 'Morales', '70445566', 'ivonne.morales@clinicadental.com', 'asist123'),
('Pedro', 'Luna', '70556677', 'pedro.luna@clinicadental.com', 'asist234'),
('Tatiana', 'Ramos', '70667788', 'tatiana.ramos@clinicadental.com', 'asist345');

INSERT INTO ClinicaDental.Tratamiento_Factura (ID_Tratamiento, ID_Factura) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO ClinicaDental.Asistente_Paciente (ID_Asistente, ID_Paciente) VALUES
(1, 4),
(2, 5),
(3, 6);

INSERT INTO ClinicaDental.Asistente_Cita (ID_Asistente, ID_Cita) VALUES
(1, 4),
(2, 5),
(3, 6);

INSERT INTO ClinicaDental.Asistente_Factura (ID_Asistente, ID_Factura) VALUES
(1, 1),
(2, 2),
(3, 3);
