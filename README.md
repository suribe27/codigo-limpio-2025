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



 ---> Instrucciones para ejecutar las pruebas unitarias en el README:


 Instrucciones para Ejecutar las Pruebas Unitarias  

El proyecto incluye un conjunto de pruebas unitarias para garantizar la correcta funcionalidad del cálculo de la nómina. Estas pruebas están definidas en el archivo `TestLiquidadorNomina.py` y se ejecutan con `unittest`.  

Requisitos Previos
Antes de ejecutar las pruebas, asegúrate de tener instalado Python en tu sistema. Puedes verificarlo con el siguiente comando:  

```sh
python --version
```

Pasos para Ejecutar las Pruebas:

1. Abrir la terminal o línea de comandos:
   - En Windows: `cmd` o `PowerShell`  
   - En macOS/Linux: `Terminal`  

2. Navegar al directorio del proyecto:
   Usa el comando `cd` para moverte a la carpeta donde está el proyecto. Por ejemplo:  

   ```sh
   cd ruta/del/proyecto
   ```

3. Ejecutar las pruebas:
   Para correr todas las pruebas unitarias, usa el siguiente comando:  

   ```sh
   python -m unittest TestLiquidadorNomina.py
   ```

4. Ver los resultados
   - Si todas las pruebas pasan, verás un mensaje indicando que las pruebas fueron exitosas.  
   - Si alguna prueba falla, se mostrará un mensaje con detalles sobre el error.  

Ejemplo de Salida Exitosa:
```
.....
----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

Solución de Problemas:
- Si recibes un error indicando que `unittest` no está disponible, asegúrate de estar usando la versión correcta de Python.  
- Si hay errores de importación, revisa que el archivo `TestLiquidadorNomina.py` esté en el mismo directorio o que el módulo `Calculo_Total` esté correctamente referenciado.  



---->  Instrucciones para ejecutar la interfaz de Consola:


El proyecto incluye un archivo `consola.py`, que permite al usuario ingresar datos y calcular la liquidación de nómina de manera interactiva a través de la terminal.  

Requisitos Previos:
Antes de ejecutar la interfaz de consola, asegúrate de tener instalado Python en tu sistema. Puedes verificarlo con el siguiente comando:  

```sh
python --version
```

Pasos para Ejecutar la Interfaz de Consola:

1. Abrir la terminal o línea de comandos:
   - En Windows: `cmd` o `PowerShell`  
   - En macOS/Linux: `Terminal`  

2. Navegar al directorio del proyecto:
   Usa el comando `cd` para moverte a la carpeta donde está el archivo `consola.py`.  

   ```sh
   cd ruta/del/proyecto
   ```

3. Ejecutar el archivo de la interfaz: 
   Para iniciar la aplicación de consola, ejecuta el siguiente comando:  

   ```sh
   python consola.py
   ```

4. Ingresar los datos solicitados:
   La aplicación pedirá que ingreses la siguiente información:  
   - Salario base  
   - Horas extras diurnas  
   - Horas extras nocturnas  
   - Bonos extra  
   - Deducciones adicionales  

   Introduce los valores según se te pida y presiona `Enter` después de cada uno.

5. Ver el resultado:  
   Una vez ingresados los datos, el programa calculará la liquidación de la nómina y mostrará el resultado en pantalla.  

   Ejemplo de salida:
   ```
   Ingrese su salario base: 2000000
   Ingrese sus horas extras diurnas: 5
   Ingrese sus horas extras nocturnas: 2
   Ingrese sus bonos extras: 50000
   Ingrese sus deducciones adicionales: 100000
   El valor total de su nómina es 1,950,320.00
   ```

Manejo de Errores:

Si ingresas datos incorrectos, el sistema mostrará mensajes de error como:  
- Salario base negativo: `¡Error salario negativo!`  
- Deducciones mayores al 40%: `¡Error deducciones mayores al 40%!`  
- Horas extras no permitidas: `¡Error horas extra superior o igual a 90!`  
- Entrada inválida: `¡Error digitación! No puedes ingresar letras, por favor corrija ingresando datos numéricos.`  

Notas Adicionales:

- Para finalizar la ejecución, puedes presionar `Ctrl + C` en la terminal.  
- Si experimentas errores de importación, asegúrate de que los archivos `Calculo_Total.py` y `consola.py` estén en la misma carpeta o correctamente referenciados.  







