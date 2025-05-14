import sys
sys.path.append("src")
from model.neon_db import obtener_configuracion, registrar_liquidacion

class ErrorSalarioN(Exception):
    """¡Error salario negativo! Ingresaste el dato del salario base negativo, por favor ingreselo correctamente"""

class ErrorDeduccionesM(Exception):
    """¡Error deducciones mayores al 40%! Sus deducciones son mayores al 40% del salario, por favor verifique y corrija."""

class ErrorHorasExtra(Exception):
    """¡Error horas extra superior o igual a 90! Sus horas extras son mayores o iguales a 90, lo cual no está permitido. Por favor verifique y corrija."""

class ErrorHorasNegativas(Exception):
    """¡Error horas negativas! No puede ingresar una cantidad de horas extra negativa."""

class ErrorBonosNegativos(Exception):
    """¡Error bonos negativos! El valor de los bonos adicionales no puede ser negativo."""

class ErrorDeduccionNegativa(Exception):
    """¡Error deducción adicional negativa! El valor de la deducción adicional no puede ser negativo."""

def obtener_parametros_configuracion():
    """Obtiene los parámetros de configuración desde la base de datos"""
    try:
        valor_hora_extra = obtener_configuracion('valor_hora_extra')
        porcentaje_hora_diurna = obtener_configuracion('porcentaje_hora_diurna')
        porcentaje_hora_nocturna = obtener_configuracion('porcentaje_hora_nocturna')
        limite_smmlv_auxilio = obtener_configuracion('limite_smmlv_auxilio')
        salario_minimo = obtener_configuracion('salario_minimo')
        auxilio_transporte = obtener_configuracion('auxilio_transporte')
        porcentaje_deducciones = obtener_configuracion('porcentaje_deducciones')
        limite_horas_extra = obtener_configuracion('limite_horas_extra')
        porcentaje_maximo_deducciones = obtener_configuracion('porcentaje_maximo_deducciones')
        
        # Si algún valor no existe en la base de datos, usar valores por defecto
        if valor_hora_extra is None:
            valor_hora_extra = 6189
        if porcentaje_hora_diurna is None:
            porcentaje_hora_diurna = 0.25
        if porcentaje_hora_nocturna is None:
            porcentaje_hora_nocturna = 0.75
        if limite_smmlv_auxilio is None:
            limite_smmlv_auxilio = 2
        if salario_minimo is None:
            salario_minimo = 1300000
        if auxilio_transporte is None:
            auxilio_transporte = 162000
        if porcentaje_deducciones is None:
            porcentaje_deducciones = 0.08
        if limite_horas_extra is None:
            limite_horas_extra = 90
        if porcentaje_maximo_deducciones is None:
            porcentaje_maximo_deducciones = 0.4
            
        return {
            'valor_hora_extra': valor_hora_extra,
            'porcentaje_hora_diurna': porcentaje_hora_diurna,
            'porcentaje_hora_nocturna': porcentaje_hora_nocturna,
            'limite_smmlv_auxilio': limite_smmlv_auxilio,
            'salario_minimo': salario_minimo,
            'auxilio_transporte': auxilio_transporte,
            'porcentaje_deducciones': porcentaje_deducciones,
            'limite_horas_extra': limite_horas_extra,
            'porcentaje_maximo_deducciones': porcentaje_maximo_deducciones
        }
    except Exception as e:
        print(f"Error obteniendo configuración: {e}")
        # Si hay error, usar valores por defecto
        return {
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

def validaciones(salario_base, horas_diurnas, horas_nocturnas, deduccion_adicional):
    """Realiza las validaciones necesarias para el cálculo de nómina"""
    config = obtener_parametros_configuracion()
    
    # Validar horas extra
    if horas_diurnas < 0 or horas_nocturnas < 0:
        raise ErrorHorasNegativas("¡Error horas negativas! No puede ingresar una cantidad de horas extra negativa.")
    
    if horas_diurnas + horas_nocturnas >= config['limite_horas_extra']:
        raise ErrorHorasExtra(f"¡Error horas extra superior o igual a {config['limite_horas_extra']}! Sus horas extras son mayores o iguales a {config['limite_horas_extra']}, lo cual no está permitido. Por favor verifique y corrija.")

    # Validar salario base
    if salario_base < 0:
        raise ErrorSalarioN("¡Error salario negativo! Ingresaste el dato del salario base negativo, por favor ingreselo correctamente")

    # Validar deducción adicional
    if deduccion_adicional < 0:
        raise ErrorDeduccionNegativa("¡Error deducción adicional negativa! El valor de la deducción adicional no puede ser negativo.")

    # Calcular valores para verificar deducciones
    horas_extra = ((horas_diurnas * config['valor_hora_extra']) * config['porcentaje_hora_diurna']) + \
                 ((horas_nocturnas * config['valor_hora_extra']) * config['porcentaje_hora_nocturna'])
    
    # Calcular auxilio de transporte
    auxilio_transporte = 0
    if salario_base < (config['salario_minimo'] * config['limite_smmlv_auxilio']):
        auxilio_transporte = config['auxilio_transporte']
    
    bonos = auxilio_transporte + 0  # Suposición de que bonos_extra es 0 por ahora
    deducciones = ((salario_base + horas_extra + bonos) * config['porcentaje_deducciones']) + deduccion_adicional
    
    # Las deducciones no pueden ser mayor al porcentaje máximo del salario base
    if deducciones > (salario_base * config['porcentaje_maximo_deducciones']):
        raise ErrorDeduccionesM(f"¡Error deducciones mayores al {config['porcentaje_maximo_deducciones']*100}%! Sus deducciones son mayores al {config['porcentaje_maximo_deducciones']*100}% del salario, por favor verifique y corrija.")

def calculo_total(salario_base: float, horas_diurnas: int, horas_nocturnas: int, bonos_extra: float, deduccion_adicional: float, empleado_id=None):
    """
    Calcula el total de la nómina
    
    Args:
        salario_base: Salario base del empleado
        horas_diurnas: Número de horas extras diurnas
        horas_nocturnas: Número de horas extras nocturnas
        bonos_extra: Bonificaciones adicionales
        deduccion_adicional: Deducciones adicionales
        empleado_id: ID del empleado en la base de datos (opcional)
        
    Returns:
        float: El valor total de la nómina
    """
    if bonos_extra < 0:
        raise ErrorBonosNegativos("¡Error bonos negativos! El valor de los bonos adicionales no puede ser negativo.")

    validaciones(salario_base, horas_diurnas, horas_nocturnas, deduccion_adicional)
    
    # Obtener parámetros de configuración
    config = obtener_parametros_configuracion()

    # Si pasa la validación, realizamos el cálculo
    horas_extra = ((horas_diurnas * config['valor_hora_extra']) * config['porcentaje_hora_diurna']) + \
                 ((horas_nocturnas * config['valor_hora_extra']) * config['porcentaje_hora_nocturna'])
    
    # Calcular auxilio de transporte
    auxilio_transporte = 0
    if salario_base < (config['salario_minimo'] * config['limite_smmlv_auxilio']):
        auxilio_transporte = config['auxilio_transporte']

    bonos = auxilio_transporte + bonos_extra
    deducciones = ((salario_base + horas_extra + bonos) * config['porcentaje_deducciones']) + deduccion_adicional
    
    total_nomina = salario_base + horas_extra + bonos - deducciones
    
    # Si se proporciona el ID del empleado, registrar la liquidación en la base de datos
    if empleado_id:
        try:
            registrar_liquidacion(
                empleado_id=empleado_id,
                salario_base=salario_base,
                horas_diurnas=horas_diurnas,
                horas_nocturnas=horas_nocturnas,
                bonos_extra=bonos_extra,
                deduccion_adicional=deduccion_adicional,
                auxilio_transporte=auxilio_transporte,
                total_nomina=total_nomina
            )
        except Exception as e:
            print(f"Error al registrar la liquidación en la base de datos: {e}")
    
    return total_nomina