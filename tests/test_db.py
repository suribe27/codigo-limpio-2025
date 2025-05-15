import unittest
import sys
import os
from datetime import date, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar las clases de modelo
from src.model.models import Empleado, Liquidacion, Configuracion, inicializar_tablas
from src.model.neon_db import obtener_conexion, liberar_conexion, cerrar_pool

class TestFixtures(unittest.TestCase):
    """Test fixtures para crear tablas y datos básicos para pruebas"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        print("Inicializando entorno de pruebas...")
        # Inicializar las tablas en la base de datos
        inicializar_tablas()
        print("Tablas inicializadas correctamente")
    
    @classmethod
    def tearDownClass(cls):
        """Limpieza después de todas las pruebas"""
        print("Limpiando entorno de pruebas...")
        # Cerrar el pool de conexiones al finalizar todas las pruebas
        cerrar_pool()
        print("Entorno de pruebas limpiado correctamente")

class TestEmpleado(unittest.TestCase):
    """Pruebas para operaciones CRUD de Empleado"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        # Limpiar datos previos de la tabla empleados
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM liquidaciones WHERE TRUE")
        cursor.execute("DELETE FROM empleados WHERE TRUE")
        conn.commit()
        cursor.close()
        liberar_conexion(conn)
    
    def test_insertar_empleado(self):
        """Test para insertar un empleado en la base de datos"""
        # Crear un empleado de prueba
        empleado = Empleado(
            nombre="Juan Pérez",
            documento="1234567890",
            salario_base=1500000,
            fecha_ingreso=date.today() - timedelta(days=180)
        )
        
        # Guardar el empleado en la base de datos
        resultado = empleado.save()
        
        # Verificar que se guardó correctamente
        self.assertTrue(resultado)
        self.assertIsNotNone(empleado.id)
        
        # Verificar que se puede recuperar de la base de datos
        empleado_db = Empleado.get_by_id(empleado.id)
        self.assertIsNotNone(empleado_db)
        self.assertEqual(empleado_db.nombre, "Juan Pérez")
        self.assertEqual(empleado_db.documento, "1234567890")
        self.assertEqual(empleado_db.salario_base, 1500000)
    
    def test_modificar_empleado(self):
        """Test para modificar un empleado en la base de datos"""
        # Crear un empleado de prueba
        empleado = Empleado(
            nombre="María López",
            documento="0987654321",
            salario_base=1800000,
            fecha_ingreso=date.today() - timedelta(days=90)
        )
        
        # Guardar el empleado en la base de datos
        empleado.save()
        
        # Modificar el empleado
        empleado.nombre = "María López García"
        empleado.salario_base = 2000000
        
        # Guardar los cambios
        resultado = empleado.save()
        
        # Verificar que se guardó correctamente
        self.assertTrue(resultado)
        
        # Verificar que los cambios se reflejan en la base de datos
        empleado_db = Empleado.get_by_id(empleado.id)
        self.assertEqual(empleado_db.nombre, "María López García")
        self.assertEqual(empleado_db.salario_base, 2000000)
    
    def test_buscar_empleado(self):
        """Test para buscar un empleado en la base de datos"""
        # Crear varios empleados de prueba
        empleado1 = Empleado(
            nombre="Carlos Ramírez",
            documento="1111111111",
            salario_base=1600000,
            fecha_ingreso=date.today() - timedelta(days=120)
        )
        empleado1.save()
        
        empleado2 = Empleado(
            nombre="Laura Gómez",
            documento="2222222222",
            salario_base=1700000,
            fecha_ingreso=date.today() - timedelta(days=150)
        )
        empleado2.save()
        
        # Buscar por documento
        empleado_doc = Empleado.get_by_documento("1111111111")
        self.assertIsNotNone(empleado_doc)
        self.assertEqual(empleado_doc.nombre, "Carlos Ramírez")
        
        # Buscar todos los empleados
        empleados = Empleado.get_all()
        self.assertEqual(len(empleados), 2)

class TestLiquidacion(unittest.TestCase):
    """Pruebas para operaciones CRUD de Liquidacion"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        # Limpiar datos previos de las tablas
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM liquidaciones WHERE TRUE")
        cursor.execute("DELETE FROM empleados WHERE TRUE")
        conn.commit()
        cursor.close()
        liberar_conexion(conn)
        
        # Crear un empleado para las pruebas
        self.empleado = Empleado(
            nombre="Ana Martínez",
            documento="3333333333",
            salario_base=1900000,
            fecha_ingreso=date.today() - timedelta(days=200)
        )
        self.empleado.save()
    
    def test_insertar_liquidacion(self):
        """Test para insertar una liquidación en la base de datos"""
        # Crear una liquidación de prueba
        liquidacion = Liquidacion(
            empleado_id=self.empleado.id,
            salario_base=1900000,
            horas_diurnas=10,
            horas_nocturnas=5,
            bonos_extra=100000,
            deduccion_adicional=50000,
            auxilio_transporte=0,
            total_nomina=1950000
        )
        
        # Guardar la liquidación
        resultado = liquidacion.save()
        
        # Verificar que se guardó correctamente
        self.assertTrue(resultado)
        self.assertIsNotNone(liquidacion.id)
        
        # Verificar que se puede recuperar de la base de datos
        liquidacion_db = Liquidacion.get_by_id(liquidacion.id)
        self.assertIsNotNone(liquidacion_db)
        self.assertEqual(liquidacion_db.empleado_id, self.empleado.id)
        self.assertEqual(liquidacion_db.salario_base, 1900000)
    
    def test_modificar_liquidacion(self):
        """Test para modificar una liquidación en la base de datos"""
        # Crear una liquidación de prueba
        liquidacion = Liquidacion(
            empleado_id=self.empleado.id,
            salario_base=1900000,
            horas_diurnas=8,
            horas_nocturnas=4,
            bonos_extra=80000,
            deduccion_adicional=30000,
            auxilio_transporte=0,
            total_nomina=1950000
        )
        
        # Guardar la liquidación
        liquidacion.save()
        
        # Modificar la liquidación
        liquidacion.horas_diurnas = 12
        liquidacion.bonos_extra = 120000
        liquidacion.total_nomina = 2050000
        
        # Guardar los cambios
        resultado = liquidacion.save()
        
        # Verificar que se guardó correctamente
        self.assertTrue(resultado)
        
        # Verificar que los cambios se reflejan en la base de datos
        liquidacion_db = Liquidacion.get_by_id(liquidacion.id)
        self.assertEqual(liquidacion_db.horas_diurnas, 12)
        self.assertEqual(liquidacion_db.bonos_extra, 120000)
        self.assertEqual(liquidacion_db.total_nomina, 2050000)
    
    def test_buscar_liquidacion_empleado(self):
        """Test para buscar liquidaciones de un empleado"""
        # Crear varias liquidaciones para el mismo empleado
        liquidacion1 = Liquidacion(
            empleado_id=self.empleado.id,
            salario_base=1900000,
            horas_diurnas=5,
            horas_nocturnas=3,
            bonos_extra=50000,
            deduccion_adicional=20000,
            auxilio_transporte=0,
            total_nomina=1930000,
            fecha_liquidacion=date.today() - timedelta(days=30)
        )
        liquidacion1.save()
        
        liquidacion2 = Liquidacion(
            empleado_id=self.empleado.id,
            salario_base=1900000,
            horas_diurnas=7,
            horas_nocturnas=2,
            bonos_extra=60000,
            deduccion_adicional=25000,
            auxilio_transporte=0,
            total_nomina=1935000
        )
        liquidacion2.save()
        
        # Buscar todas las liquidaciones del empleado
        liquidaciones = Liquidacion.get_by_empleado(self.empleado.id)
        self.assertEqual(len(liquidaciones), 2)

class TestConfiguracion(unittest.TestCase):
    """Pruebas para operaciones CRUD de Configuracion"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        # No es necesario limpiar la tabla de configuración, ya que contiene valores por defecto
        # que deben mantenerse para el correcto funcionamiento de la aplicación
        pass
    
    def test_modificar_configuracion(self):
        """Test para modificar un parámetro de configuración"""
        # Obtener un parámetro de configuración
        config = Configuracion.get_by_nombre('salario_minimo')
        self.assertIsNotNone(config)
        
        # Guardar el valor original para restaurarlo después
        valor_original = config.valor
        
        # Modificar el valor
        config.valor = 1400000
        resultado = config.save()
        
        # Verificar que se guardó correctamente
        self.assertTrue(resultado)
        
        # Verificar que el cambio se refleja en la base de datos
        config_db = Configuracion.get_by_nombre('salario_minimo')
        self.assertEqual(config_db.valor, 1400000)
        
        # Restaurar el valor original
        config.valor = valor_original
        config.save()
    
    def test_buscar_configuracion(self):
        """Test para buscar parámetros de configuración"""
        # Buscar por nombre
        config = Configuracion.get_by_nombre('auxilio_transporte')
        self.assertIsNotNone(config)
        self.assertEqual(config.nombre_parametro, 'auxilio_transporte')
        
        # Verificar que existen todos los parámetros necesarios
        params = ['valor_hora_extra', 'porcentaje_hora_diurna', 'porcentaje_hora_nocturna', 
                 'salario_minimo', 'auxilio_transporte', 'limite_smmlv_auxilio', 
                 'porcentaje_deducciones', 'limite_horas_extra', 'porcentaje_maximo_deducciones']
        
        for param in params:
            config = Configuracion.get_by_nombre(param)
            self.assertIsNotNone(config)
    
    def test_listar_configuraciones(self):
        """Test para listar todos los parámetros de configuración"""
        # Obtener todos los parámetros
        configs = Configuracion.get_all()
        
        # Debería haber al menos 9 parámetros de configuración
        self.assertGreaterEqual(len(configs), 9)

if __name__ == '__main__':
    unittest.main()