def Calculo_Total (salario_base : float, horas_diurnas : int, horas_nocturnas : int, bonos_extra : float, deduccion_adicional : float):
    horas_extra = ((horas_diurnas*6189)*0.25) + ((horas_nocturnas*6189)*0.75)
    auxilio_tranporte = 0

    if salario_base < 2847000:
        auxilio_tranporte = 162000

    bonos = auxilio_tranporte + bonos_extra
    deducciones = ((salario_base+horas_extra+bonos)*0.08) - deduccion_adicional

    return (salario_base+horas_extra+bonos-deducciones)

    
