from model import Calculo_Total

try:
    
    salario_base = float(input("Ingrese su salario base: "))
    horas_diurnas = int(input("Ingrese sus horas extras diurnas: "))
    horas_nocturnas = int(input("Ingrese sus horas extras nocturnas: "))
    bonos_extra = float(input("Ingrese sus bonos extras: "))
    deduccion_adicional = float(input("Ingrese sus deducciones adicionales: "))

    nomina = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

    print (f"El valor total de su nomina es {nomina}")

except Calculo_Total.ErrorSalarioN as ex:
    print( str(ex))
    
except Calculo_Total.ErrorDeduccionesM as ex:
    print( str(ex))

  
except Calculo_Total.ErrorHorasExtra as ex:
    print( str(ex))
    
except Exception as ex:
    print( str(ex))
    print("¡Error digitacion! No puedes ingresar letras, por favor corrija ingresando datos numericos. ")