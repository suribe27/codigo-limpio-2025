import sys
sys.path.append("src")
from model.calculo_total import *

try:
    
    salario_base = float(input("Ingrese su salario base: "))
    horas_diurnas = int(input("Ingrese sus horas extras diurnas: "))
    horas_nocturnas = int(input("Ingrese sus horas extras nocturnas: "))
    bonos_extra = float(input("Ingrese sus bonos extras: "))
    deduccion_adicional = float(input("Ingrese sus deducciones adicionales: "))

    nomina = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

    print (f"El valor total de su nomina es {nomina}")

except ErrorSalarioN as ex:
    print( str(ex))
    
except ErrorDeduccionesM as ex:
    print( str(ex))

  
except ErrorHorasExtra as ex:
    print( str(ex))
    
except Exception as ex:
    print( str(ex))
    print("¡Error digitacion! No puedes ingresar letras, por favor corrija ingresando datos numericos. ")