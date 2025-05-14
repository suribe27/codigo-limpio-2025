import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.models import Configuracion
from datetime import date

class ConfiguracionController:
    """Controlador para la gestión de parámetros de configuración"""
    
    @classmethod
    def validate_input(cls, data):
        """Valida los datos de un parámetro de configuración"""
        errors = {}
        
        # Validar nombre_parametro
        if 'nombre_parametro' not in data or not data['nombre_parametro']:
            errors['nombre_parametro'] = "El nombre del parámetro es obligatorio"
        elif len(data['nombre_parametro']) > 50:
            errors['nombre_parametro'] = "El nombre del parámetro no puede exceder los 50 caracteres"
        
        # Validar valor
        if 'valor' not in data:
            errors['valor'] = "El valor es obligatorio"
        else:
            try:
                float(data['valor'])
            except (ValueError, TypeError):
                errors['valor'] = "El valor debe ser un número válido"
        
        return errors
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los parámetros de configuración"""
        return Configuracion.get_all()
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un parámetro de configuración por su ID"""
        try:
            id_num = int(id)
            return Configuracion.get_by_id(id_num)
        except (ValueError, TypeError):
            return None
    
    @classmethod
    def get_by_nombre(cls, nombre_parametro):
        """Obtiene un parámetro de configuración por su nombre"""
        return Configuracion.get_by_nombre(nombre_parametro)
    
    @classmethod
    def get_valor(cls, nombre_parametro):
        """Obtiene el valor de un parámetro de configuración"""
        param = cls.get_by_nombre(nombre_parametro)
        return param.valor if param else None
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo parámetro de configuración"""
        errors = cls.validate_input(data)
        if errors:
            return None, errors
        
        try:
            # Verificar si ya existe un parámetro con el mismo nombre
            if cls.get_by_nombre(data['nombre_parametro']):
                return None, {"nombre_parametro": "Ya existe un parámetro con este nombre"}
            
            # Crear el parámetro
            configuracion = Configuracion(
                nombre_parametro=data['nombre_parametro'],
                valor=float(data['valor']),
                descripcion=data.get('descripcion', '')
            )
            
            # Guardar en la base de datos
            if configuracion.save():
                return configuracion, {}
            else:
                return None, {"db_error": "No se pudo guardar el parámetro en la base de datos"}
        
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def update(cls, id, data):
        """Actualiza un parámetro de configuración existente"""
        # Obtener el parámetro
        configuracion = None
        if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
            configuracion = cls.get_by_id(id)
        else:
            configuracion = cls.get_by_nombre(id)
        
        if not configuracion:
            return None, {"error": "Parámetro de configuración no encontrado"}
        
        # Validar datos
        validation_data = data.copy()
        if 'nombre_parametro' not in validation_data:
            validation_data['nombre_parametro'] = configuracion.nombre_parametro
        if 'valor' not in validation_data:
            validation_data['valor'] = configuracion.valor
            
        errors = cls.validate_input(validation_data)
        if errors:
            return None, errors
        
        try:
            # Verificar si el nombre ya está en uso por otro parámetro
            if 'nombre_parametro' in data and data['nombre_parametro'] != configuracion.nombre_parametro:
                existing = cls.get_by_nombre(data['nombre_parametro'])
                if existing and existing.id != configuracion.id:
                    return None, {"nombre_parametro": "Este nombre ya está asociado a otro parámetro"}
            
            # Actualizar los datos
            configuracion.nombre_parametro = data.get('nombre_parametro', configuracion.nombre_parametro)
            configuracion.valor = float(data.get('valor', configuracion.valor))
            
            if 'descripcion' in data:
                configuracion.descripcion = data['descripcion']
            
            # Guardar los cambios
            if configuracion.save():
                return configuracion, {}
            else:
                return None, {"db_error": "No se pudo actualizar el parámetro en la base de datos"}
            
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def delete(cls, id):
        """Elimina un parámetro de configuración"""
        configuracion = cls.get_by_id(id)
        if not configuracion:
            return False, {"error": "Parámetro de configuración no encontrado"}
        
        try:
            if configuracion.delete():
                return True, {}
            else:
                return False, {"db_error": "No se pudo eliminar el parámetro de configuración"}
        except Exception as e:
            return False, {"error": str(e)}
    
    @classmethod
    def get_configuracion_calculo(cls):
        """Obtiene todos los parámetros necesarios para el cálculo de nómina"""
        params = [
            'valor_hora_extra',
            'porcentaje_hora_diurna',
            'porcentaje_hora_nocturna',
            'limite_smmlv_auxilio',
            'salario_minimo',
            'auxilio_transporte',
            'porcentaje_deducciones',
            'limite_horas_extra',
            'porcentaje_maximo_deducciones'
        ]
        
        result = {}
        for param_name in params:
            param = cls.get_by_nombre(param_name)
            if param:
                result[param_name] = param.valor
            else:
                # Valores por defecto si no existen en la base de datos
                default_values = {
                    'valor_hora_extra': 6189,
                    'porcentaje_hora_diurna': 0.25,
                    'porcentaje_hora_nocturna': 0.75,
                    'limite_smmlv_auxilio': 2,
                    'salario_minimo': 1300000,
                    'auxilio_transporte': 162000,
                    'porcentaje_deducciones': 0.08,
                    'limite_horas_extra': 90,
                    'porcentaje_maximo_deducciones': 0.4
                }
                result[param_name] = default_values.get(param_name)
        
        return result