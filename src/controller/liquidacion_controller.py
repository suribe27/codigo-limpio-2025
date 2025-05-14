import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.models import Liquidacion, Empleado
from model.calculo_total import calculo_total, ErrorSalarioN, ErrorDeduccionesM, ErrorHorasExtra, ErrorHorasNegativas, ErrorBonosNegativos, ErrorDeduccionNegativa
from datetime import date

class LiquidacionController:
    """Controlador para la gestión de liquidaciones de nómina"""
    
    @classmethod
    def validate_input(cls, data):
        """Valida los datos de una liquidación"""
        errors = {}
        
        # Validar empleado_id
        if 'empleado_id' not in data:
            errors['empleado_id'] = "El ID del empleado es obligatorio"
        else:
            try:
                empleado_id = int(data['empleado_id'])
                empleado = Empleado.get_by_id(empleado_id)
                if not empleado:
                    errors['empleado_id'] = "El empleado especificado no existe"
            except (ValueError, TypeError):
                errors['empleado_id'] = "El ID del empleado debe ser un número válido"
        
        # Validar salario_base
        if 'salario_base' not in data:
            errors['salario_base'] = "El salario base es obligatorio"
        else:
            try:
                salario = float(data['salario_base'])
                if salario < 0:
                    errors['salario_base'] = "El salario base no puede ser negativo"
            except (ValueError, TypeError):
                errors['salario_base'] = "El salario base debe ser un número válido"
        
        # Validar horas_diurnas
        if 'horas_diurnas' not in data:
            errors['horas_diurnas'] = "Las horas diurnas son obligatorias"
        else:
            try:
                horas = int(data['horas_diurnas'])
                if horas < 0:
                    errors['horas_diurnas'] = "Las horas diurnas no pueden ser negativas"
            except (ValueError, TypeError):
                errors['horas_diurnas'] = "Las horas diurnas deben ser un número entero válido"
        
        # Validar horas_nocturnas
        if 'horas_nocturnas' not in data:
            errors['horas_nocturnas'] = "Las horas nocturnas son obligatorias"
        else:
            try:
                horas = int(data['horas_nocturnas'])
                if horas < 0:
                    errors['horas_nocturnas'] = "Las horas nocturnas no pueden ser negativas"
            except (ValueError, TypeError):
                errors['horas_nocturnas'] = "Las horas nocturnas deben ser un número entero válido"
        
        # Validar bonos_extra
        if 'bonos_extra' not in data:
            errors['bonos_extra'] = "Los bonos extra son obligatorios"
        else:
            try:
                bonos = float(data['bonos_extra'])
                if bonos < 0:
                    errors['bonos_extra'] = "Los bonos extra no pueden ser negativos"
            except (ValueError, TypeError):
                errors['bonos_extra'] = "Los bonos extra deben ser un número válido"
        
        # Validar deduccion_adicional
        if 'deduccion_adicional' not in data:
            errors['deduccion_adicional'] = "La deducción adicional es obligatoria"
        else:
            try:
                deduccion = float(data['deduccion_adicional'])
                if deduccion < 0:
                    errors['deduccion_adicional'] = "La deducción adicional no puede ser negativa"
            except (ValueError, TypeError):
                errors['deduccion_adicional'] = "La deducción adicional debe ser un número válido"
        
        return errors
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las liquidaciones"""
        return Liquidacion.get_all()
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene una liquidación por su ID"""
        try:
            id_num = int(id)
            return Liquidacion.get_by_id(id_num)
        except (ValueError, TypeError):
            return None
    
    @classmethod
    def get_by_empleado(cls, empleado_id):
        """Obtiene las liquidaciones de un empleado"""
        try:
            id_num = int(empleado_id)
            return Liquidacion.get_by_empleado(id_num)
        except (ValueError, TypeError):
            return []
    
    @classmethod
    def create(cls, data):
        """Crea una nueva liquidación"""
        errors = cls.validate_input(data)
        if errors:
            return None, errors
        
        try:
            # Convertir los datos
            empleado_id = int(data['empleado_id'])
            salario_base = float(data['salario_base'])
            horas_diurnas = int(data['horas_diurnas'])
            horas_nocturnas = int(data['horas_nocturnas'])
            bonos_extra = float(data['bonos_extra'])
            deduccion_adicional = float(data['deduccion_adicional'])
            
            # Calcular el total de la nómina
            try:
                total_nomina = calculo_total(
                    salario_base, 
                    horas_diurnas, 
                    horas_nocturnas, 
                    bonos_extra, 
                    deduccion_adicional
                )
                
                # Determinar auxilio de transporte (reutilizando lógica de calculo_total)
                from src.model.calculo_total import obtener_parametros_configuracion
                config = obtener_parametros_configuracion()
                auxilio_transporte = 0
                if salario_base < (config['salario_minimo'] * config['limite_smmlv_auxilio']):
                    auxilio_transporte = config['auxilio_transporte']
                
                # Crear la liquidación
                liquidacion = Liquidacion(
                    empleado_id=empleado_id,
                    salario_base=salario_base,
                    horas_diurnas=horas_diurnas,
                    horas_nocturnas=horas_nocturnas,
                    bonos_extra=bonos_extra,
                    deduccion_adicional=deduccion_adicional,
                    auxilio_transporte=auxilio_transporte,
                    total_nomina=total_nomina
                )
                
                # Guardar en la base de datos
                if liquidacion.save():
                    return liquidacion, {}
                else:
                    return None, {"db_error": "No se pudo guardar la liquidación en la base de datos"}
                
            except (ErrorSalarioN, ErrorDeduccionesM, ErrorHorasExtra, 
                   ErrorHorasNegativas, ErrorBonosNegativos, ErrorDeduccionNegativa) as e:
                return None, {"calculo_error": str(e)}
            
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def update(cls, id, data):
        """Actualiza una liquidación existente"""
        # Obtener la liquidación
        liquidacion = cls.get_by_id(id)
        if not liquidacion:
            return None, {"error": "Liquidación no encontrada"}
        
        # Validar los datos
        errors = cls.validate_input(data)
        if errors:
            return None, errors
        
        try:
            # Actualizar los datos
            liquidacion.empleado_id = int(data.get('empleado_id', liquidacion.empleado_id))
            liquidacion.salario_base = float(data.get('salario_base', liquidacion.salario_base))
            liquidacion.horas_diurnas = int(data.get('horas_diurnas', liquidacion.horas_diurnas))
            liquidacion.horas_nocturnas = int(data.get('horas_nocturnas', liquidacion.horas_nocturnas))
            liquidacion.bonos_extra = float(data.get('bonos_extra', liquidacion.bonos_extra))
            liquidacion.deduccion_adicional = float(data.get('deduccion_adicional', liquidacion.deduccion_adicional))
            
            # Recalcular el total de la nómina
            try:
                total_nomina = calculo_total(
                    liquidacion.salario_base, 
                    liquidacion.horas_diurnas, 
                    liquidacion.horas_nocturnas, 
                    liquidacion.bonos_extra, 
                    liquidacion.deduccion_adicional
                )
                
                # Determinar auxilio de transporte
                from src.model.calculo_total import obtener_parametros_configuracion
                config = obtener_parametros_configuracion()
                auxilio_transporte = 0
                if liquidacion.salario_base < (config['salario_minimo'] * config['limite_smmlv_auxilio']):
                    auxilio_transporte = config['auxilio_transporte']
                
                liquidacion.auxilio_transporte = auxilio_transporte
                liquidacion.total_nomina = total_nomina
                
                # Guardar los cambios
                if liquidacion.save():
                    return liquidacion, {}
                else:
                    return None, {"db_error": "No se pudo actualizar la liquidación en la base de datos"}
                
            except (ErrorSalarioN, ErrorDeduccionesM, ErrorHorasExtra,
                   ErrorHorasNegativas, ErrorBonosNegativos, ErrorDeduccionNegativa) as e:
                return None, {"calculo_error": str(e)}
            
        except Exception as e:
            return None, {"error": str(e)}
    
    @classmethod
    def delete(cls, id):
        """Elimina una liquidación"""
        liquidacion = cls.get_by_id(id)
        if not liquidacion:
            return False, {"error": "Liquidación no encontrada"}
        
        try:
            if liquidacion.delete():
                return True, {}
            else:
                return False, {"db_error": "No se pudo eliminar la liquidación"}
        except Exception as e:
            return False, {"error": str(e)}