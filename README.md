# Liquidador de Nómina 2025

Hecho por:
- Samuel Uribe Salazar
- Valery Monsalve Correa
- Juan Sebastian Pinilla Giraldo (Interfaz gráfica)
- Juan Vallejo (Interfaz gráfica)

Este proyecto ayuda a poder calcular la Liquidación de Nómina de Empleados.

## 📋 Descripción

El sistema permite calcular la liquidación de nómina considerando:
- Salario base
- Horas extras diurnas y nocturnas
- Auxilio de transporte (cuando aplica)
- Bonos adicionales
- Deducciones

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura modular para garantizar un código mantenible, escalable y fácil de entender. Se organiza en los siguientes componentes principales:

### Estructura del Proyecto:

```
/liquidador-nomina-2025
│── AUDIO Y EXCEL/                      # Archivos auxiliares
│   │── CASOS LIQUIDACION NOMINA.xlsx   # Archivo con casos de prueba 
│   │── WhatsApp Ptt...                 # Nota de voz relacionada
│
│── build/                              # Archivos de compilación
│
│── config/                             # Configuración del proyecto
│   │── __pycache__/                    # Caché de Python
│   │── __init__.py                     # Inicializador del módulo
│   │── secret_config.py                # Configuración para conexión a BD
│
│── dist/                               # Distribución compilada
│
│── sql/                                # Scripts SQL
│   │── uso.py                          # Utilidades de base de datos
│
│── src/                                # Código fuente principal
│   │── __pycache__/                    # Caché de Python
│   │── __init__.py                     # Inicializador del módulo
│   │
│   │── controller/                     # Controladores
│   │   │── __pycache__/                # Caché de Python
│   │   │── __init__.py                 # Inicializador del módulo
│   │   │── configuracion_controller.py # Controlador de configuración
│   │   │── empleado_controller.py      # Controlador de empleados
│   │   │── liquidacion_controller.py   # Controlador de liquidación
│   │
│   │── model/                          # Modelos de datos
│   │   │── __pycache__/                # Caché de Python
│   │   │── __init__.py                 # Inicializador del módulo
│   │   │── calculo_total.py            # Lógica de cálculo
│   │   │── models.py                   # Modelos de datos
│   │   │── neon_db.py                  # Conexión a BD Neon
│   │
│   │── view/                           # Interfaces de usuario
│       │── __pycache__/                # Caché de Python
│       │── __init__.py                 # Inicializador del módulo
│       │── consola/                    # Interfaz en consola
│       │   │── main.py                 # Punto de entrada consola
│       │
│       │── gui/                        # Interfaz gráfica
│           │── __init__.py             # Inicializador del módulo
│           │── interfaz_database.py    # UI para base de datos
│
│── tests/                              # Pruebas unitarias
│   │── test_db.py                      # Tests para la base de datos
│   │── TestLiquidadorNomina.py         # Tests para la liquidación
│
│── README.md                           # Documentación del proyecto
```

## 🗄️ Configuración de la Base de Datos (Neon DB)

El proyecto utiliza Neon DB, una base de datos PostgreSQL en la nube, para almacenar información de empleados y liquidaciones. A continuación, se detallan los pasos para configurar y conectar a la base de datos.

### 1. Requisitos

- Cuenta en Neon DB (https://neon.tech/)
- Librería psycopg2 para la conexión a PostgreSQL

Para instalar las dependencias:

```sh
pip install psycopg2-binary
```

### 2. Configuración del archivo secret_config.py

El archivo `secret_config.py` ubicado en la carpeta `config/` debe configurarse con los datos de conexión a su base de datos Neon. Este archivo NO contiene datos privados por defecto, solo la estructura para configurarlos.

Ejemplo del contenido de `secret_config.py`:

```python
# Configuración de conexión a Neon DB
# Sustituya estos valores con los proporcionados en su dashboard de Neon

DB_CONFIG = {
    'host': 'ep-xyz-123.us-east-2.aws.neon.tech',  # Host de Neon DB
    'database': 'nomina',      # Nombre de la base de datos
    'user': 'usuario_neon',    # Usuario de Neon
    'password': 'su_contraseña_segura',  # Contraseña
    'port': 5432,              # Puerto estándar de PostgreSQL
    'sslmode': 'require'       # Requerido para conexiones seguras a Neon
}

# Constantes del sistema (no modificar)
VALOR_HORA_BASE = 6189  # Valor base para el cálculo de horas extras
PORCENTAJE_SALUD_PENSION = 0.08  # 8% de deducciones obligatorias
SALARIO_MINIMO_2025 = 1423500  # Salario mínimo 2025
AUXILIO_TRANSPORTE = 162000  # Valor auxilio de transporte
```

**Importante**: No comparta su archivo `secret_config.py` con datos reales en repositorios públicos.

### 3. Creación de la Base de Datos en Neon

Para configurar su base de datos en Neon:

1. Cree una cuenta en Neon DB (https://neon.tech/) y cree un nuevo proyecto.
   
2. En el dashboard de Neon, cree una nueva base de datos llamada `nomina`.

3. Obtenga las credenciales de conexión desde su panel de control y actualice `secret_config.py`.

4. Para inicializar las tablas necesarias, ejecute:
   ```sh
   python sql/uso.py --init-db
   ```

El script `neon_db.py` se encargará de establecer la conexión con Neon DB y gestionar las operaciones de base de datos requeridas por el sistema.

## 🚀 Instrucciones de Ejecución

### Interfaz de Consola (Simulación sin Base de Datos)

Esta interfaz permite realizar simulaciones de cálculo de nómina sin necesidad de conexión a base de datos:

1. Navegar al directorio del proyecto:
   ```sh
   cd ruta/del/proyecto
   ```

2. Ejecutar la interfaz de consola simple:
   ```sh
   python src/view/consola/main.py
   ```

3. Siga las instrucciones en pantalla para ingresar:
   - Salario base
   - Horas extras diurnas y nocturnas
   - Bonos extra
   - Deducciones adicionales
   
   El sistema calculará y mostrará el valor total de la nómina.

### Interfaz de Consola con Base de Datos

Esta interfaz permite gestionar la información en la base de datos Neon DB:

1. Asegúrese de haber configurado correctamente `secret_config.py` con sus credenciales de base de datos.

2. Ejecutar la interfaz de base de datos:
   ```sh
   python interfaz_database.py
   ```

3. La interfaz le permitirá:
   - Gestionar empleados (crear, consultar, actualizar)
   - Registrar liquidaciones
   - Consultar histórico de liquidaciones

### Interfaz Gráfica (GUI con Kivy)

Esta interfaz proporciona una experiencia visual para el cálculo de nómina sin conexión a base de datos.

#### 🚀 Requisitos Previos
Antes de ejecutar la aplicación, asegúrese de tener instalado:
- **Python 3.8+**
- **Kivy**

Si no tiene Kivy instalado:
```sh
pip install kivy
```

#### Ejecución
- Desde la carpeta **raíz** del proyecto, ejecute:
```sh
python src/view/gui/kivy_gui.py
```

- Alternativamente, puede ejecutar el archivo compilado desde:
```
dist/kivy_gui/kivy_gui.exe
```

## 🧪 Ejecución de Pruebas Unitarias

Para verificar el correcto funcionamiento del sistema:

1. Pruebas del módulo de cálculo:
   ```sh
   python -m unittest tests/TestLiquidadorNomina.py
   ```

2. Pruebas de la conexión a base de datos:
   ```sh
   python -m unittest tests/test_db.py
   ```

## 📊 Fórmulas de Cálculo

### Horas Extra
```
horas_extra = ((horas_diurnas*6189)*0.25) + ((horas_nocturnas*6189)*0.75)
```

### Auxilio de Transporte
```
auxilio_tranporte = 0
if salario_base < 2847000:  # 2 SMMVL
    auxilio_tranporte = 162000
```

### Bonos
```
bonos = auxilio_tranporte + bonos_extra
```

### Deducciones
```
deducciones = ((salario_base+horas_extra+bonos)*0.08) + deduccion_adicional
```

### Liquidación Final
```
total = salario_base + horas_extra + bonos - deducciones
```

## ⚠️ Validaciones

El sistema realiza las siguientes validaciones:
- Salario base no puede ser negativo (`ErrorSalarioN`)
- Las deducciones no pueden superar el 40% del salario (`ErrorDeduccionesM`)
- Las horas extras no pueden ser mayores o iguales a 90 (`ErrorHorasExtra`)

## 👥 Autores

- **Samuel Uribe Salazar**: Desarrollo core
- **Valery Monsalve Correa**: Desarrollo core
- **Juan Sebastian Pinilla Giraldo**: Interfaz gráfica
- **Juan Vallejo**: Interfaz gráfica





