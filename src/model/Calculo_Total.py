class ErrorSalarioN(Exception):
    """¡Error salario negativo! Ingresaste el dato del salario base negativo, por favor ingreselo correctamente"""

class ErrorDeduccionesM(Exception):
    """¡Error deduciones mayores al 40%! Sus deducciones son mayores al 40% del salario, por favor verifique y corrija."""

class ErrorHorasExtra(Exception):
    """¡Error horas extra superior o igual a 90! Sus horas extras son mayores o iguales a 90, lo cual no esta permitido. Por favor verifique y corrija."""

def validaciones(salario_base, horas_diurnas, horas_nocturnas, deduccion_adicional):
    # Validar horas extra
    if horas_diurnas + horas_nocturnas >= 90:
        raise ErrorHorasExtra("¡Error horas extra superior o igual a 90! Sus horas extras son mayores o iguales a 90, lo cual no esta permitido. Por favor verifique y corrija.")
    
    # Validar salario base
    if salario_base < 0:
        raise ErrorSalarioN("¡Error salario negativo! Ingresaste el dato del salario base negativo, por favor ingreselo correctamente")

    # Validar deducciones mayores al 40% del salario
    horas_extra = ((horas_diurnas*6189)*0.25) + ((horas_nocturnas*6189)*0.75)
    auxilio_tranporte = 0
    if salario_base < 2847000:
        auxilio_tranporte = 162000
    bonos = auxilio_tranporte + 0  # Suposición de que bonos_extra es 0 por ahora, si es otro valor, ajusta
    deducciones = ((salario_base + horas_extra + bonos) * 0.08) + deduccion_adicional
    if deducciones > (salario_base * 0.40):
        raise ErrorDeduccionesM("¡Error deduciones mayores al 40%! Sus deducciones son mayores al 40% del salario, por favor verifique y corrija.")

def calculo_total(salario_base: float, horas_diurnas: int, horas_nocturnas: int, bonos_extra: float, deduccion_adicional: float):
    validaciones(salario_base, horas_diurnas, horas_nocturnas, deduccion_adicional)

    # Si pasa la validación, realizamos el cálculo
    horas_extra = ((horas_diurnas * 6189) * 0.25) + ((horas_nocturnas * 6189) * 0.75)
    auxilio_tranporte = 0

    if salario_base < 2847000:
        auxilio_tranporte = 162000

    bonos = auxilio_tranporte + bonos_extra
    deducciones = ((salario_base + horas_extra + bonos) * 0.08) + deduccion_adicional

    return (salario_base + horas_extra + bonos - deducciones)
