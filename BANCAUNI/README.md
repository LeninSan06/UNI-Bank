# Simulador de Banco con Reconocimiento Facial

Pequeño simulador en Python (orientado a objetos) que permite crear cuentas, depositar, retirar y transferir. Para operaciones sensibles (retirar/transferir) se activa la cámara y se realiza una verificación facial simple.

- Carpeta: `bank_sim`
- Ejecutables: `main.py` (launcher), `gui.py` (interfaz gráfica)
- Dependencias: `opencv-python`, `numpy`
- Python: 3.8+
- Requisitos: Cámara web disponible para autenticación facial

## Características

✅ Crear cuenta con DNI de 8 dígitos  
✅ Registrar rostro (captura desde cámara)  
✅ Depositar dinero  
✅ Retirar dinero con verificación facial  
✅ Transferir a otras cuentas con verificación facial  
✅ Ver saldo y transacciones  
✅ Acceso administrativo protegido por contraseña  
✅ Eliminar base de datos (función admin)  
✅ Base de datos JSON persistente  
✅ Interfaz gráfica (GUI) con Tkinter  
✅ Terminal (CLI) interactiva  

## 🔧 Instalación

### Requisitos Previos

- **Python 3.8 o superior** instalado
- **pip** (gestor de paquetes de Python)
- **Cámara web** funcional para reconocimiento facial
- **VSCode** (opcional, recomendado)

### 🪟 Instalación en Windows

#### 1. Instalar Python

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, **marca la opción "Add Python to PATH"**
3. Verifica la instalación abriendo **PowerShell** o **CMD**:

```powershell
python --version
pip --version
```

#### 2. Clonar o descargar el repositorio

```powershell
# Si tienes Git instalado
git clone https://github.com/TU_USUARIO/bank-simulator.git
cd bank-simulator

# O descarga el ZIP y extrae
```

#### 3. Instalar dependencias en Windows

**Opción A: Con entorno virtual (recomendado)**

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En PowerShell:
.\venv\Scripts\Activate.ps1

# En CMD:
venv\Scripts\activate.bat

# Instalar dependencias
pip install -r bank_sim/requirements.txt
```

**Opción B: Instalación global (no recomendado)**

```powershell
pip install -r bank_sim/requirements.txt
```

#### 4. Configurar VSCode en Windows

1. Abre el proyecto en VSCode: `code .`
2. Abre la paleta de comandos: `Ctrl + Shift + P`
3. Busca: "Python: Select Interpreter"
4. Elige el intérprete del entorno virtual (`.venv`)
5. Instala la extensión "Python" de Microsoft si no la tienes

#### 5. Ejecutar en Windows

```powershell
# Activar el entorno virtual primero
.\venv\Scripts\Activate.ps1

# Ejecutar la aplicación
python bank_sim/main.py

# O directamente con Python del entorno
python -m bank_sim.main
```

---

### 🐧 Instalación en Linux (Ubuntu/Debian)

#### 1. Instalar Python y pip

```bash
# Actualizar gestor de paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
sudo apt install -y python3 python3-pip python3-venv

# Instalar dependencias del sistema para OpenCV
sudo apt install -y libopencv-dev python3-opencv

# Verificar instalación
python3 --version
pip3 --version
```

#### 2. Clonar o descargar el repositorio

```bash
# Si tienes Git instalado
git clone https://github.com/TU_USUARIO/bank-simulator.git
cd bank-simulator

# O descarga el ZIP y extrae
```

#### 3. Instalar dependencias en Linux

**Opción A: Con entorno virtual (recomendado)**

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r bank_sim/requirements.txt
```

**Opción B: Instalación global (no recomendado)**

```bash
pip3 install -r bank_sim/requirements.txt
```

#### 4. Configurar VSCode en Linux

1. Abre el proyecto en VSCode: `code .`
2. Abre la paleta de comandos: `Ctrl + Shift + P`
3. Busca: "Python: Select Interpreter"
4. Elige el intérprete del entorno virtual (`./venv/bin/python`)
5. Instala la extensión "Python" de Microsoft si no la tienes

#### 5. Ejecutar en Linux

```bash
# Activar el entorno virtual primero
source venv/bin/activate

# Ejecutar la aplicación
python3 bank_sim/main.py

# O directamente
python -m bank_sim.main
```

---

### 📋 Contenido de `requirements.txt`

```
opencv-python==4.8.1.78
numpy==1.24.3
```

Instalar todo de una vez:

```bash
# Windows
pip install -r bank_sim/requirements.txt

# Linux
pip3 install -r bank_sim/requirements.txt
```

---

### ✅ Verificar que todo funciona

```bash
# Probar importación de módulos
python -c "import cv2; import numpy; print('✓ Dependencias OK')"

# O ejecutar los tests
python bank_sim/tests/run_bank_tests.py
```

## Uso

### 🖥️ Opción 1: Interfaz Gráfica (Recomendado)

#### Windows
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar
python bank_sim/main.py
# Luego seleccionar opción "1" para GUI
```

#### Linux
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar
python3 bank_sim/main.py
# Luego seleccionar opción "1" para GUI
```

**Flujo en GUI:**
1. Ingrese DNI en el campo de entrada
2. Seleccione una cuenta (se requiere PIN de 4 dígitos)
3. Operaciones disponibles:
   - 📝 Crear Cuenta: DNI (8 dígitos), Nombre, PIN (4 dígitos)
   - 📷 Registrar Rostro: Captura desde cámara
   - 💰 Depositar: Sin verificación
   - 🚪 Retirar: Con verificación facial (abre cámara)
   - 🔄 Transferir: Con verificación facial (abre cámara)
   - 📊 Ver Transacciones
4. ⚙️ Acceso Admin: Botón "Ingresar como Admin"
   - Contraseña: `S0lx@dm1n&str4d?r"z!`
   - Opciones admin:
     - 👁️ Ver Rostros Registrados
     - 🗑️ Eliminar Base de Datos

### 📱 Opción 2: Terminal (CLI)

#### Windows
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar
python bank_sim/main.py
# Luego seleccionar opción "2" para CLI
```

#### Linux
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar
python3 bank_sim/main.py
# Luego seleccionar opción "2" para CLI
```

**Flujo en CLI:**
1. Crear cuenta
2. Registrar rostro
3. Depositar dinero
4. Retirar o Transferir (requiere verificación facial en vivo)

### 🎯 Ejecutar directamente

#### GUI directo
```bash
# Windows
python bank_sim/gui.py

# Linux
python3 bank_sim/gui.py
```

#### CLI directo
```bash
# Windows
python -c "from bank_sim.main import run_cli; run_cli()"

# Linux
python3 -c "from bank_sim.main import run_cli; run_cli()"
```

### 🧪 Ejecutar pruebas

```bash
# Windows
python bank_sim/tests/run_bank_tests.py

# Linux
python3 bank_sim/tests/run_bank_tests.py
```

## Estructura

```
bank_sim/
├── bank.py              # Lógica de cuentas y operaciones
├── face_auth.py         # Autenticación facial con OpenCV
├── gui.py               # Interfaz gráfica (Tkinter)
├── main.py              # Launcher CLI/GUI
├── requirements.txt     # Dependencias
├── README.md            # Este archivo
├── db/                  # Carpeta de base de datos (se crea automáticamente)
├── faces/               # Carpeta para fotos de registro (se crea automáticamente)
└── tests/               # Pruebas unitarias
    ├── run_bank_tests.py
    └── test_bank.py
```

## Notas y Solución de Problemas

### ⚠️ Problemas comunes

#### Error: "ModuleNotFoundError: No module named 'cv2'"

**Solución:**
```bash
# Windows
pip install opencv-python

# Linux
pip3 install opencv-python
```

#### Error: "No module named 'numpy'"

**Solución:**
```bash
# Windows
pip install numpy

# Linux
pip3 install numpy
```

#### Error: "Camera not available" o problemas con cámara

- Verifica que tu cámara esté conectada
- En Linux, instala: `sudo apt install -y cheese` (para probar cámara)
- Verifica permisos de cámara en tu SO

#### VSCode no reconoce Python

1. Abre paleta de comandos: `Ctrl + Shift + P`
2. Busca: "Python: Select Interpreter"
3. Elige el intérprete correcto (debe estar en la carpeta `venv`)

#### Error en Windows: "cannot find vcvarsall.bat"

Instala Microsoft C++ Build Tools:
- Descarga desde: https://visualstudio.microsoft.com/downloads/
- Selecciona "Desktop development with C++"

### 📋 Sobre la funcionalidad

- El método de verificación facial usa **ORB** (feature matching); es simple y no reemplaza sistemas robustos.
- Los datos se guardan en `db/bank_db.json` automáticamente.
- Las fotos de referencia se guardan en `faces/{dni}.jpg`
- PIN requerido: 4 dígitos numéricos
- DNI requerido: 8 dígitos numéricos
- Contraseña admin: `S0lx@dm1n&str4d?r"z!`

### 🔐 Seguridad

- **PIN local**: Cada usuario tiene un PIN de 4 dígitos
- **Verificación facial**: Para retirar/transferir
- **Contraseña admin**: Para acceso administrativo
- **Base de datos JSON**: Almacenada localmente (no encriptada)

> **Nota**: Este es un simulador educativo. No usar en producción sin implementar medidas de seguridad robustas.

### 📚 Estructura de datos

#### Cliente (Client)
```json
{
  "dni": "12345678",
  "name": "Juan Pérez",
  "balance": 1000.50,
  "face_image": "faces/12345678.jpg",
  "pin": "1234",
  "transactions": ["Depósito: $100", "Retiro: $50"]
}
```

#### Base de datos (`db/bank_db.json`)
```json
{
  "clients": [
    { "dni": "12345678", "name": "Juan Pérez", ... },
    { "dni": "87654321", "name": "María García", ... }
  ]
}
```

### 🛠️ Desarrollo

Para contribuir o modificar el código:

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/bank-simulator.git
cd bank-simulator

# 2. Crea una rama para tu feature
git checkout -b feature/mi-feature

# 3. Haz cambios y commits
git add bank_sim/
git commit -m "Agregar nueva característica"

# 4. Sube tu rama
git push origin feature/mi-feature

# 5. Crea un Pull Request en GitHub
```

### 📞 Soporte

Si tienes problemas:

1. Verifica que Python 3.8+ esté instalado: `python --version`
2. Verifica que pip esté actualizado: `pip install --upgrade pip`
3. Borra la carpeta `venv` y crea una nueva
4. Reinstala las dependencias: `pip install -r bank_sim/requirements.txt`

¡IMPORTANTE!

Para ingresar como administrador use la contraseña siguiente:

S0lx@dm1n&str4d?r"z!


Ejecutar:

```bash
# Windows
python bank_sim/main.py

# Linux
python3 bank_sim/main.py
```
