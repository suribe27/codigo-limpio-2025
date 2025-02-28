Samuel Uribe Salazar
Valery Monsalve Correa

Este proyecto ayuda a poder calcular la Liquidación de Nomina de Empleados.

Entradas

salario_base = es el salario base de un usuario en float
horas_diurnas = son las horas diurnas que realizo un usuario en int
horas_nocturnas = son las horas nocturnas que realizo un usuario en int
bonos_extra = son los bonos extra que le fueron asignados a un usuario en float
deduccion_adicional = son las deducciones adicionales que se le hacen a un usuario en float

---------------------------------------------------------------------

Calculos

horas_extra = ((horas_diurnas*6189)*0.25) + ((horas_nocturnas*6189)*0.75)

Para el total de horas extra se multiplica la cantidad de hora según la hora del dia en que se haga por la cantidad que paga ese tiempo y se suman las 2, dando un total en float.

   auxilio_tranporte = 0

    if salario_base < 2847000:
        auxilio_tranporte = 162000

Si el salario base de una persona es menor a 2 SMMVL se la asigna un auxilio de transporte.

 bonos = auxilio_tranporte + bonos_extra

A la variable bonos se le asigna la sumatoria del auxilio de transporte si existe y el total de los bonos extra

 deducciones = ((salario_base+horas_extra+bonos)*0.08) + deduccion_adicional

Para calcular las deducciones se suma todos los ingresos, se suman y se multiplican por el 8% y luego, si existe, se le suma una deducción adicional.

---------------------------------------------------------------------

Salida

return (salario_base+horas_extra+bonos-deducciones)

Para poder dar el resultado final, se suma el salario, la ganancia de las horas extras y bonos, y se le resta las deducciones.
