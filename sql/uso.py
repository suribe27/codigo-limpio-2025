import psycopg2

# Datos de conexión
PGHOST='ep-snowy-lab-a4mk1kuj-pooler.us-east-1.aws.neon.tech'
PGDATABASE='liquidador_nomina'
PGUSER='neondb_owner'
PGPASSWORD='npg_Tg1KxQSat3Yl'

# Establecer conexión
try:
    conn = psycopg2.connect(host=PGHOST, database=PGDATABASE, user=PGUSER, password=PGPASSWORD)
    print("Conexión exitosa a la base de datos")
    
    # Crear un cursor
    cursor = conn.cursor()
    
    # Crear tabla empleados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS empleados (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        documento VARCHAR(20) UNIQUE NOT NULL,
        salario_base FLOAT NOT NULL,
        fecha_ingreso DATE NOT NULL
    )
    ''')
    
    # Crear tabla liquidaciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS liquidaciones (
        id SERIAL PRIMARY KEY,
        empleado_id INTEGER REFERENCES empleados(id),
        fecha_liquidacion DATE NOT NULL,
        salario_base FLOAT NOT NULL,
        horas_diurnas INTEGER NOT NULL,
        horas_nocturnas INTEGER NOT NULL,
        bonos_extra FLOAT NOT NULL,
        deduccion_adicional FLOAT NOT NULL,
        auxilio_transporte FLOAT NOT NULL,
        total_nomina FLOAT NOT NULL
    )
    ''')
    
    # Crear tabla configuracion
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS configuracion (
        id SERIAL PRIMARY KEY,
        nombre_parametro VARCHAR(50) UNIQUE NOT NULL,
        valor FLOAT NOT NULL,
        descripcion TEXT,
        fecha_actualizacion DATE NOT NULL
    )
    ''')
    
    # Insertar configuraciones iniciales
    cursor.execute('''
    INSERT INTO configuracion (nombre_parametro, valor, descripcion, fecha_actualizacion)
    VALUES 
        ('valor_hora_extra', 6189, 'Valor actual de la hora extra en Colombia', CURRENT_DATE),
        ('porcentaje_hora_diurna', 0.25, 'Multiplicador para horas extras diurnas', CURRENT_DATE),
        ('porcentaje_hora_nocturna', 0.75, 'Multiplicador para horas extras nocturnas', CURRENT_DATE),
        ('salario_minimo', 1300000, 'Salario mínimo mensual legal vigente', CURRENT_DATE),
        ('auxilio_transporte', 162000, 'Valor del auxilio de transporte', CURRENT_DATE),
        ('limite_smmlv_auxilio', 2, 'Límite en SMMLV para recibir auxilio de transporte', CURRENT_DATE),
        ('porcentaje_deducciones', 0.08, 'Porcentaje base de deducciones', CURRENT_DATE),
        ('limite_horas_extra', 90, 'Límite máximo de horas extra permitidas', CURRENT_DATE),
        ('porcentaje_maximo_deducciones', 0.4, 'Porcentaje máximo permitido de deducciones', CURRENT_DATE)
    ON CONFLICT (nombre_parametro) DO NOTHING
    ''')
    
    # Confirmar los cambios
    conn.commit()
    print("Tablas creadas exitosamente")
    
except Exception as e:
    print(f"Error al conectar o crear tablas: {e}")
    
finally:
    # Cerrar cursor y conexión
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
        print("Conexión cerrada")