import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.models import Empleado, Liquidacion, Configuracion
from datetime import date

class Controller:
    """Clase base para los controladores de la aplicación"""
    
    @classmethod
    def validate_input(cls, data):
        """Método para validar los datos de entrada"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los registros"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un registro por su ID"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo registro"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def update(cls, id, data):
        """Actualiza un registro existente"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    @classmethod
    def delete(cls, id):
        """Elimina un registro"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")


class EmpleadoController(Controller):
    """Controlador para la gestión de empleados"""
    
    @classmethod
    def validate_input(cls, data):
        """Valida los datos de un empleado"""
        errors = {}
        
        # Validar nombre
        if 'nombre' not in data or not data['nombre']:
            errors['nombre'] = "El nombre es obligatorio"
        elif len(data['nombre']) > 100:
            errors['nombre'] = "El nombre no puede exceder los 100 caracteres"
        
        # Validar documento
        if 'documento' not in data or not data['documento']:
            errors['documento'] = "El documento es obligatorio"
        elif len(data['documento']) > 20:
            errors['documento'] = "El documento no puede exceder los 20 caracteres"
        
        # Validar salario base
        if 'salario_base' not in data:
            errors['salario_base'] = "El salario base es obligatorio"
        else:
            try:
                salario = float(data['salario_base'])
                if salario <= 0:
                    errors['salario_base'] = "El salario base debe ser mayor que cero"
            except (ValueError, TypeError):
                errors['salario_base'] = "El salario base debe ser un número válido"
        
        # Validar fecha de ingreso
        if 'fecha_ingreso' not in data or not data['fecha_ingreso']:
            errors['fecha_ingreso'] = "La fecha de ingreso es obligatoria"
        else:
            try:
                if isinstance(data['fecha_ingreso'], str):
                    date.fromisoformat(data['fecha_ingreso'])
            except ValueError:
                errors['fecha_ingreso'] = "La fecha de ingreso debe tener un formato válido (YYYY-MM-DD)"
        
        return errors
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los empleados"""
        return Empleado.get_all()
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un empleado por su ID"""
        try:
            id_num = int(id)
            return Empleado.get_by_id(id_num)
        except (ValueError, TypeError):
            return None
    
    @classmethod
    def get_by_documento(cls, documento):
        """Obtiene un empleado por su documento"""
        return Empleado.get_by_documento(documento)
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo empleado"""
        errors = cls.validate_input(data)
        if errors:
            return None, errors
        
        try:
            # Verificar si ya existe un empleado con el mismo documento
            if cls.get_by_documento(data['documento']):
                return None, {"documento": "Ya existe un empleado con este documento"}
            
            # Crear el empleado
            empleado = Empleado(
                nombre=data['nombre'],
                documento=data['documento'],
                salario_base=float(data['salario_base']),
                fecha_ingreso=data['fecha_ingreso']
            )
            
            # Guardar en la base de datos
            if empleado.save():
                return empleado, {}
            else:
                return None, {"db_error": "No se pudo guardar el empleado en la base de datos"}
        
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def update(cls, id, data):
        """Actualiza un empleado existente"""
        # Obtener el empleado
        empleado = cls.get_by_id(id)
        if not empleado:
            return None, {"error": "Empleado no encontrado"}
        
        # Validar los datos
        errors = cls.validate_input(data)
        if errors:
            return None, errors
        
        try:
            # Verificar si el documento ya está en uso por otro empleado
            if 'documento' in data and data['documento'] != empleado.documento:
                existing = cls.get_by_documento(data['documento'])
                if existing and existing.id != empleado.id:
                    return None, {"documento": "Este documento ya está asociado a otro empleado"}
            
            # Actualizar los datos
            empleado.nombre = data.get('nombre', empleado.nombre)
            empleado.documento = data.get('documento', empleado.documento)
            empleado.salario_base = float(data.get('salario_base', empleado.salario_base))
            
            if 'fecha_ingreso' in data:
                empleado.fecha_ingreso = data['fecha_ingreso']
            
            # Guardar los cambios
            if empleado.save():
                return empleado, {}
            else:
                return None, {"db_error": "No se pudo actualizar el empleado en la base de datos"}
            
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def delete(cls, id):
        """Elimina un empleado"""
        empleado = cls.get_by_id(id)
        if not empleado:
            return False, {"error": "Empleado no encontrado"}
        
        try:
            if empleado.delete():
                return True, {}
            else:
                return False, {"db_error": "No se pudo eliminar el empleado"}
        except Exception as e:
            return False, {"error": str(e)}