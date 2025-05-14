import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.neon_db import obtener_conexion, liberar_conexion
from datetime import date

class Model:
    """Clase base para los modelos de la aplicación"""
    
    @classmethod
    def create_table(cls):
        """Método para crear la tabla correspondiente al modelo"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los registros de la tabla"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un registro por su ID"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    def save(self):
        """Guarda o actualiza un registro en la base de datos"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    def delete(self):
        """Elimina un registro de la base de datos"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")

class Empleado(Model):
    """Modelo para la tabla empleados"""
    
    def __init__(self, nombre, documento, salario_base, fecha_ingreso, id=None):
        self.id = id
        self.nombre = nombre
        self.documento = documento
        self.salario_base = salario_base
        self.fecha_ingreso = fecha_ingreso if isinstance(fecha_ingreso, date) else date.fromisoformat(fecha_ingreso)
    
    @classmethod
    def create_table(cls):
        """Crea la tabla empleados en la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                documento VARCHAR(20) UNIQUE NOT NULL,
                salario_base FLOAT NOT NULL,
                fecha_ingreso DATE NOT NULL
            )
            ''')
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al crear tabla empleados: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los empleados de la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, documento, salario_base, fecha_ingreso FROM empleados ORDER BY nombre")
            empleados = []
            for row in cursor.fetchall():
                id, nombre, documento, salario_base, fecha_ingreso = row
                empleados.append(cls(nombre, documento, salario_base, fecha_ingreso, id))
            return empleados
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un empleado por su ID"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, documento, salario_base, fecha_ingreso FROM empleados WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                id, nombre, documento, salario_base, fecha_ingreso = row
                return cls(nombre, documento, salario_base, fecha_ingreso, id)
            return None
        except Exception as e:
            print(f"Error al obtener empleado: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_documento(cls, documento):
        """Obtiene un empleado por su documento"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, documento, salario_base, fecha_ingreso FROM empleados WHERE documento = %s", (documento,))
            row = cursor.fetchone()
            if row:
                id, nombre, documento, salario_base, fecha_ingreso = row
                return cls(nombre, documento, salario_base, fecha_ingreso, id)
            return None
        except Exception as e:
            print(f"Error al obtener empleado por documento: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def save(self):
        """Guarda o actualiza un empleado en la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            if self.id:
                # Actualizar un empleado existente
                cursor.execute(
                    "UPDATE empleados SET nombre = %s, documento = %s, salario_base = %s, fecha_ingreso = %s WHERE id = %s",
                    (self.nombre, self.documento, self.salario_base, self.fecha_ingreso, self.id)
                )
            else:
                # Insertar un nuevo empleado
                cursor.execute(
                    "INSERT INTO empleados (nombre, documento, salario_base, fecha_ingreso) VALUES (%s, %s, %s, %s) RETURNING id",
                    (self.nombre, self.documento, self.salario_base, self.fecha_ingreso)
                )
                self.id = cursor.fetchone()[0]
            
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al guardar empleado: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def delete(self):
        """Elimina un empleado de la base de datos"""
        if not self.id:
            return False
        
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleados WHERE id = %s", (self.id,))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)

class Liquidacion(Model):
    """Modelo para la tabla liquidaciones"""
    
    def __init__(self, empleado_id, salario_base, horas_diurnas, horas_nocturnas, 
                 bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina, 
                 fecha_liquidacion=None, id=None):
        self.id = id
        self.empleado_id = empleado_id
        self.fecha_liquidacion = fecha_liquidacion or date.today()
        self.salario_base = salario_base
        self.horas_diurnas = horas_diurnas
        self.horas_nocturnas = horas_nocturnas
        self.bonos_extra = bonos_extra
        self.deduccion_adicional = deduccion_adicional
        self.auxilio_transporte = auxilio_transporte
        self.total_nomina = total_nomina
    
    @classmethod
    def create_table(cls):
        """Crea la tabla liquidaciones en la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
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
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al crear tabla liquidaciones: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las liquidaciones de la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                       horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina 
                FROM liquidaciones 
                ORDER BY fecha_liquidacion DESC
            """)
            liquidaciones = []
            for row in cursor.fetchall():
                (id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                 horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina) = row
                liquidaciones.append(cls(
                    empleado_id, salario_base, horas_diurnas, horas_nocturnas, 
                    bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina, 
                    fecha_liquidacion, id
                ))
            return liquidaciones
        except Exception as e:
            print(f"Error al obtener liquidaciones: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene una liquidación por su ID"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                       horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina 
                FROM liquidaciones 
                WHERE id = %s
            """, (id,))
            row = cursor.fetchone()
            if row:
                (id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                 horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina) = row
                return cls(
                    empleado_id, salario_base, horas_diurnas, horas_nocturnas, 
                    bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina, 
                    fecha_liquidacion, id
                )
            return None
        except Exception as e:
            print(f"Error al obtener liquidación: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_empleado(cls, empleado_id):
        """Obtiene las liquidaciones de un empleado"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                       horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina 
                FROM liquidaciones 
                WHERE empleado_id = %s
                ORDER BY fecha_liquidacion DESC
            """, (empleado_id,))
            liquidaciones = []
            for row in cursor.fetchall():
                (id, empleado_id, fecha_liquidacion, salario_base, horas_diurnas, 
                 horas_nocturnas, bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina) = row
                liquidaciones.append(cls(
                    empleado_id, salario_base, horas_diurnas, horas_nocturnas, 
                    bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina, 
                    fecha_liquidacion, id
                ))
            return liquidaciones
        except Exception as e:
            print(f"Error al obtener liquidaciones por empleado: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def save(self):
        """Guarda o actualiza una liquidación en la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            if self.id:
                # Actualizar una liquidación existente
                cursor.execute("""
                    UPDATE liquidaciones 
                    SET empleado_id = %s, fecha_liquidacion = %s, salario_base = %s, 
                        horas_diurnas = %s, horas_nocturnas = %s, bonos_extra = %s, 
                        deduccion_adicional = %s, auxilio_transporte = %s, total_nomina = %s
                    WHERE id = %s
                """, (
                    self.empleado_id, self.fecha_liquidacion, self.salario_base, 
                    self.horas_diurnas, self.horas_nocturnas, self.bonos_extra, 
                    self.deduccion_adicional, self.auxilio_transporte, self.total_nomina,
                    self.id
                ))
            else:
                # Insertar una nueva liquidación
                cursor.execute("""
                    INSERT INTO liquidaciones 
                    (empleado_id, fecha_liquidacion, salario_base, horas_diurnas, horas_nocturnas, 
                     bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    self.empleado_id, self.fecha_liquidacion, self.salario_base, 
                    self.horas_diurnas, self.horas_nocturnas, self.bonos_extra, 
                    self.deduccion_adicional, self.auxilio_transporte, self.total_nomina
                ))
                self.id = cursor.fetchone()[0]
            
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al guardar liquidación: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def delete(self):
        """Elimina una liquidación de la base de datos"""
        if not self.id:
            return False
        
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM liquidaciones WHERE id = %s", (self.id,))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar liquidación: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)

class Configuracion(Model):
    """Modelo para la tabla configuracion"""
    
    def __init__(self, nombre_parametro, valor, descripcion=None, fecha_actualizacion=None, id=None):
        self.id = id
        self.nombre_parametro = nombre_parametro
        self.valor = valor
        self.descripcion = descripcion
        self.fecha_actualizacion = fecha_actualizacion or date.today()
    
    @classmethod
    def create_table(cls):
        """Crea la tabla configuración en la base de datos"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
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
            parametros_iniciales = [
                ('valor_hora_extra', 6189, 'Valor actual de la hora extra en Colombia'),
                ('porcentaje_hora_diurna', 0.25, 'Multiplicador para horas extras diurnas'),
                ('porcentaje_hora_nocturna', 0.75, 'Multiplicador para horas extras nocturnas'),
                ('salario_minimo', 1300000, 'Salario mínimo mensual legal vigente'),
                ('auxilio_transporte', 162000, 'Valor del auxilio de transporte'),
                ('limite_smmlv_auxilio', 2, 'Límite en SMMLV para recibir auxilio de transporte'),
                ('porcentaje_deducciones', 0.08, 'Porcentaje base de deducciones'),
                ('limite_horas_extra', 90, 'Límite máximo de horas extra permitidas'),
                ('porcentaje_maximo_deducciones', 0.4, 'Porcentaje máximo permitido de deducciones')
            ]
            
            for param in parametros_iniciales:
                nombre, valor, descripcion = param
                cursor.execute('''
                INSERT INTO configuracion (nombre_parametro, valor, descripcion, fecha_actualizacion)
                VALUES (%s, %s, %s, CURRENT_DATE)
                ON CONFLICT (nombre_parametro) DO NOTHING
                ''', (nombre, valor, descripcion))
            
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al crear tabla configuracion: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los parámetros de configuración"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre_parametro, valor, descripcion, fecha_actualizacion 
                FROM configuracion 
                ORDER BY nombre_parametro
            """)
            configuraciones = []
            for row in cursor.fetchall():
                id, nombre_parametro, valor, descripcion, fecha_actualizacion = row
                configuraciones.append(cls(nombre_parametro, valor, descripcion, fecha_actualizacion, id))
            return configuraciones
        except Exception as e:
            print(f"Error al obtener configuraciones: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_nombre(cls, nombre_parametro):
        """Obtiene un parámetro de configuración por su nombre"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre_parametro, valor, descripcion, fecha_actualizacion 
                FROM configuracion 
                WHERE nombre_parametro = %s
            """, (nombre_parametro,))
            row = cursor.fetchone()
            if row:
                id, nombre_parametro, valor, descripcion, fecha_actualizacion = row
                return cls(nombre_parametro, valor, descripcion, fecha_actualizacion, id)
            return None
        except Exception as e:
            print(f"Error al obtener configuración por nombre: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un parámetro de configuración por su ID"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre_parametro, valor, descripcion, fecha_actualizacion 
                FROM configuracion 
                WHERE id = %s
            """, (id,))
            row = cursor.fetchone()
            if row:
                id, nombre_parametro, valor, descripcion, fecha_actualizacion = row
                return cls(nombre_parametro, valor, descripcion, fecha_actualizacion, id)
            return None
        except Exception as e:
            print(f"Error al obtener configuración: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def save(self):
        """Guarda o actualiza un parámetro de configuración"""
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            if self.id:
                # Actualizar un parámetro existente
                cursor.execute("""
                    UPDATE configuracion 
                    SET nombre_parametro = %s, valor = %s, descripcion = %s, fecha_actualizacion = CURRENT_DATE
                    WHERE id = %s
                """, (self.nombre_parametro, self.valor, self.descripcion, self.id))
            else:
                # Insertar un nuevo parámetro
                cursor.execute("""
                    INSERT INTO configuracion (nombre_parametro, valor, descripcion, fecha_actualizacion)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                    ON CONFLICT (nombre_parametro) DO UPDATE 
                    SET valor = EXCLUDED.valor, descripcion = EXCLUDED.descripcion, fecha_actualizacion = CURRENT_DATE
                    RETURNING id
                """, (self.nombre_parametro, self.valor, self.descripcion))
                self.id = cursor.fetchone()[0]
            
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al guardar configuración: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)
    
    def delete(self):
        """Elimina un parámetro de configuración"""
        if not self.id:
            return False
        
        conn = None
        cursor = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM configuracion WHERE id = %s", (self.id,))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al eliminar configuración: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                liberar_conexion(conn)

# Función para inicializar todas las tablas
def inicializar_tablas():
    """Crea todas las tablas en la base de datos"""
    Empleado.create_table()
    Liquidacion.create_table()
    Configuracion.create_table()
    print("Tablas inicializadas correctamente")

if __name__ == "__main__":
    inicializar_tablas()