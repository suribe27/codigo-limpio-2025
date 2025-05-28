import psycopg2
from psycopg2 import pool
import os
from datetime import date
from config import secret_config

# Datos de conexión
PGHOST=secret_config.PGHOST
PGDATABASE=secret_config.PGDATABASE
PGUSER=secret_config.PGUSER
PGPASSWORD=secret_config.PGPASSWORD

# Crear un pool de conexiones para mejor rendimiento
connection_pool = None

def inicializar_pool():
    """Inicializa el pool de conexiones"""
    global connection_pool
    try:
        connection_pool = pool.SimpleConnectionPool(
            1, 10,  # min y max conexiones
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
        print("Pool de conexiones inicializado correctamente")
    except Exception as e:
        print(f"Error al inicializar el pool de conexiones: {e}")
        raise

def obtener_conexion():
    """Obtiene una conexión del pool"""
    if connection_pool is None:
        inicializar_pool()
    return connection_pool.getconn()

def liberar_conexion(conn):
    """Devuelve la conexión al pool"""
    if connection_pool is not None:
        connection_pool.putconn(conn)

def cerrar_pool():
    """Cierra el pool de conexiones"""
    if connection_pool is not None:
        connection_pool.closeall()
        print("Pool de conexiones cerrado")

# Funciones CRUD para empleados
def registrar_empleado(nombre, documento, salario_base, fecha_ingreso):
    """Registra un nuevo empleado en la base de datos"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO empleados (nombre, documento, salario_base, fecha_ingreso) VALUES (%s, %s, %s, %s) RETURNING id",
            (nombre, documento, salario_base, fecha_ingreso)
        )
        id_empleado = cursor.fetchone()[0]
        conn.commit()
        return id_empleado
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

def obtener_empleado(id_empleado=None, documento=None):
    """Obtiene información de un empleado por ID o documento"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        if id_empleado:
            cursor.execute("SELECT * FROM empleados WHERE id = %s", (id_empleado,))
        elif documento:
            cursor.execute("SELECT * FROM empleados WHERE documento = %s", (documento,))
        else:
            raise ValueError("Debe proporcionar un ID o documento")
        
        empleado = cursor.fetchone()
        return empleado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

def listar_empleados():
    """Lista todos los empleados registrados"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empleados ORDER BY nombre")
        empleados = cursor.fetchall()
        return empleados
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

# Funciones para liquidaciones
def registrar_liquidacion(empleado_id, salario_base, horas_diurnas, horas_nocturnas, 
                         bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina):
    """Registra una nueva liquidación de nómina"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO liquidaciones 
               (empleado_id, fecha_liquidacion, salario_base, horas_diurnas, horas_nocturnas, 
                bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (empleado_id, date.today(), salario_base, horas_diurnas, horas_nocturnas, 
             bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina)
        )
        id_liquidacion = cursor.fetchone()[0]
        conn.commit()
        return id_liquidacion
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

def obtener_liquidacion(id_liquidacion):
    """Obtiene información de una liquidación por ID"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.*, e.nombre, e.documento 
            FROM liquidaciones l
            JOIN empleados e ON l.empleado_id = e.id
            WHERE l.id = %s
        """, (id_liquidacion,))
        liquidacion = cursor.fetchone()
        return liquidacion
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

def listar_liquidaciones_empleado(empleado_id):
    """Lista todas las liquidaciones de un empleado"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM liquidaciones 
            WHERE empleado_id = %s
            ORDER BY fecha_liquidacion DESC
        """, (empleado_id,))
        liquidaciones = cursor.fetchall()
        return liquidaciones
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

# Funciones para la configuración
def obtener_configuracion(nombre_parametro):
    """Obtiene el valor de un parámetro de configuración"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT valor FROM configuracion WHERE nombre_parametro = %s", (nombre_parametro,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

def actualizar_configuracion(nombre_parametro, valor, descripcion=None):
    """Actualiza un parámetro de configuración"""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        if descripcion:
            cursor.execute(
                """UPDATE configuracion 
                SET valor = %s, descripcion = %s, fecha_actualizacion = CURRENT_DATE 
                WHERE nombre_parametro = %s""",
                (valor, descripcion, nombre_parametro)
            )
        else:
            cursor.execute(
                """UPDATE configuracion 
                SET valor = %s, fecha_actualizacion = CURRENT_DATE 
                WHERE nombre_parametro = %s""",
                (valor, nombre_parametro)
            )
        
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexion(conn)

# Inicializa el pool al importar el módulo
try:
    inicializar_pool()
except Exception:
    print("No se pudo inicializar la conexión a la base de datos al cargar el módulo")
