#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
from datetime import date, datetime
import traceback

# Importar los módulos de conexión a la base de datos y los modelos
from model.neon_db import inicializar_pool, cerrar_pool
from model.models import Empleado, Liquidacion, Configuracion, inicializar_tablas

class InterfazSimple:
    """Interfaz de consola simplificada para gestión de datos con Neon DB"""
    
    def __init__(self):
        """Inicializa la interfaz y la conexión a la base de datos"""
        try:
            # Inicializar la conexión a la base de datos
            print("Conectando a la base de datos Neon DB...")
            inicializar_pool()
            
            # Inicializar las tablas si no existen
            print("Verificando tablas en la base de datos...")
            inicializar_tablas()
            
            print("¡Conexión establecida correctamente!")
        except Exception as e:
            print(f"Error al inicializar la conexión a la base de datos: {e}")
            print(traceback.format_exc())
            sys.exit(1)
    
    def __del__(self):
        """Cierra la conexión al finalizar"""
        try:
            cerrar_pool()
        except:
            pass
    
    #=========================================================================
    # Funciones de utilidad para la interfaz de usuario
    #=========================================================================
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal"""
        if os.name == 'nt':  # Para Windows
            os.system('cls')
        else:  # Para Unix/Linux/MacOS
            os.system('clear')
    
    def pausa(self):
        """Pausa la ejecución hasta que el usuario presione Enter"""
        input("\nPresione Enter para continuar...")
    
    def obtener_opcion(self, min_valor, max_valor):
        """Solicita al usuario una opción numérica dentro de un rango"""
        while True:
            try:
                opcion = input("\nOpción: ").strip()
                opcion = int(opcion)
                
                if min_valor <= opcion <= max_valor:
                    return opcion
                else:
                    print(f"¡Error! Ingrese un número entre {min_valor} y {max_valor}")
            except ValueError:
                print("¡Error! Ingrese un número válido")
    
    def obtener_entero(self, mensaje):
        """Solicita al usuario un número entero"""
        while True:
            try:
                valor = input(mensaje).strip()
                return int(valor)
            except ValueError:
                print("¡Error! Ingrese un número entero válido")
    
    def obtener_float(self, mensaje):
        """Solicita al usuario un número de punto flotante"""
        while True:
            try:
                valor = input(mensaje).strip().replace(',', '.')
                return float(valor)
            except ValueError:
                print("¡Error! Ingrese un número válido")
    
    def obtener_texto(self, mensaje):
        """Solicita al usuario un texto no vacío"""
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("¡Error! El texto no puede estar vacío")
    
    def obtener_fecha(self, mensaje):
        """Solicita al usuario una fecha en formato YYYY-MM-DD"""
        while True:
            try:
                fecha_str = input(mensaje).strip()
                
                # Validar formato
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
                    print("¡Error! El formato debe ser YYYY-MM-DD")
                    continue
                    
                # Convertir a objeto date
                año, mes, dia = map(int, fecha_str.split('-'))
                fecha = date(año, mes, dia)
                
                return fecha
            except ValueError:
                print("¡Error! Fecha inválida")
    
    #=========================================================================
    # Menú principal
    #=========================================================================
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        while True:
            self.limpiar_pantalla()
            print("=" * 50)
            print("SISTEMA DE GESTIÓN DE NÓMINA".center(50))
            print("=" * 50)
            print("\nSeleccione una opción:")
            print("1. Gestionar Empleados")
            print("2. Gestionar Liquidaciones")
            print("3. Configuración del Sistema")
            print("0. Salir")
            
            opcion = self.obtener_opcion(0, 3)
            
            if opcion == 1:
                self.menu_empleados()
            elif opcion == 2:
                self.menu_liquidaciones()
            elif opcion == 3:
                self.menu_configuracion()
            elif opcion == 0:
                print("\nGracias por usar el sistema. ¡Hasta pronto!")
                sys.exit(0)
    
    #=========================================================================
    # Menú y funciones para Empleados
    #=========================================================================
    
    def menu_empleados(self):
        """Menú de gestión de empleados"""
        while True:
            self.limpiar_pantalla()
            print("=" * 50)
            print("GESTIÓN DE EMPLEADOS".center(50))
            print("=" * 50)
            print("\nSeleccione una opción:")
            print("1. Registrar nuevo empleado")
            print("2. Modificar empleado")
            print("3. Buscar empleado")
            print("4. Listar todos los empleados")
            print("0. Volver al menú principal")
            
            opcion = self.obtener_opcion(0, 4)
            
            if opcion == 0:
                return
            elif opcion == 1:
                self.registrar_empleado()
            elif opcion == 2:
                self.modificar_empleado()
            elif opcion == 3:
                self.buscar_empleado()
            elif opcion == 4:
                self.listar_empleados()
    
    def registrar_empleado(self):
        """Función para registrar un nuevo empleado"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("REGISTRAR NUEVO EMPLEADO".center(50))
        print("=" * 50)
        
        try:
            nombre = self.obtener_texto("Nombre del empleado: ")
            documento = self.obtener_texto("Documento de identidad: ")
            
            # Verificar si ya existe un empleado con ese documento
            empleado_existente = Empleado.get_by_documento(documento)
            if empleado_existente:
                print(f"\n¡Error! Ya existe un empleado con el documento {documento}")
                self.pausa()
                return
            
            salario_base = self.obtener_float("Salario base: ")
            fecha_ingreso = self.obtener_fecha("Fecha de ingreso (YYYY-MM-DD): ")
            
            # Crear y guardar el nuevo empleado
            empleado = Empleado(nombre, documento, salario_base, fecha_ingreso)
            if empleado.save():
                print(f"\n¡Empleado '{nombre}' registrado exitosamente con ID {empleado.id}!")
            else:
                print("\n¡Error al registrar el empleado!")
                
        except Exception as e:
            print(f"\n¡Error al registrar empleado: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def modificar_empleado(self):
        """Función para modificar un empleado existente"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("MODIFICAR EMPLEADO".center(50))
        print("=" * 50)
        
        # Primero, buscar el empleado
        empleado = self.seleccionar_empleado("Seleccione el empleado a modificar")
        if not empleado:
            return
        
        try:
            print(f"\nModificando empleado: {empleado.nombre} (ID: {empleado.id})")
            print("\n¿Qué dato desea modificar?")
            print("1. Nombre")
            print("2. Documento")
            print("3. Salario base")
            print("4. Fecha de ingreso")
            print("0. Cancelar")
            
            opcion = self.obtener_opcion(0, 4)
            
            if opcion == 0:
                return
                
            if opcion == 1:
                nuevo_valor = self.obtener_texto("Nuevo nombre: ")
                empleado.nombre = nuevo_valor
            elif opcion == 2:
                nuevo_valor = self.obtener_texto("Nuevo documento: ")
                # Verificar si el documento ya existe para otro empleado
                empleado_existente = Empleado.get_by_documento(nuevo_valor)
                if empleado_existente and empleado_existente.id != empleado.id:
                    print(f"\n¡Error! Ya existe otro empleado con el documento {nuevo_valor}")
                    self.pausa()
                    return
                empleado.documento = nuevo_valor
            elif opcion == 3:
                nuevo_valor = self.obtener_float("Nuevo salario base: ")
                empleado.salario_base = nuevo_valor
            elif opcion == 4:
                nuevo_valor = self.obtener_fecha("Nueva fecha de ingreso (YYYY-MM-DD): ")
                empleado.fecha_ingreso = nuevo_valor
            
            # Guardar los cambios
            if empleado.save():
                print("\n¡Empleado actualizado exitosamente!")
            else:
                print("\n¡Error al actualizar el empleado!")
                
        except Exception as e:
            print(f"\n¡Error al modificar empleado: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def buscar_empleado(self):
        """Función para buscar un empleado por diferentes criterios"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("BUSCAR EMPLEADO".center(50))
        print("=" * 50)
        
        print("\nBuscar por:")
        print("1. ID")
        print("2. Documento")
        print("3. Nombre (búsqueda parcial)")
        print("0. Cancelar")
        
        opcion = self.obtener_opcion(0, 3)
        
        if opcion == 0:
            return
        
        try:
            empleados = []
            
            if opcion == 1:
                id_empleado = self.obtener_entero("ID del empleado: ")
                empleado = Empleado.get_by_id(id_empleado)
                if empleado:
                    empleados = [empleado]
            elif opcion == 2:
                documento = self.obtener_texto("Documento del empleado: ")
                empleado = Empleado.get_by_documento(documento)
                if empleado:
                    empleados = [empleado]
            elif opcion == 3:
                nombre_parcial = self.obtener_texto("Nombre del empleado (puede ser parcial): ").lower()
                todos_empleados = Empleado.get_all()
                # Filtrar los empleados cuyo nombre contiene la búsqueda
                empleados = [e for e in todos_empleados if nombre_parcial in e.nombre.lower()]
            
            # Mostrar resultados
            if empleados:
                self.mostrar_empleados(empleados)
            else:
                print("\nNo se encontraron empleados con los criterios especificados.")
                
        except Exception as e:
            print(f"\n¡Error al buscar empleado: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def listar_empleados(self):
        """Función para listar todos los empleados"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("LISTADO DE EMPLEADOS".center(50))
        print("=" * 50)
        
        try:
            empleados = Empleado.get_all()
            if empleados:
                self.mostrar_empleados(empleados)
            else:
                print("\nNo hay empleados registrados en el sistema.")
                
        except Exception as e:
            print(f"\n¡Error al listar empleados: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def mostrar_empleados(self, empleados):
        """Muestra una lista de empleados en formato tabular"""
        print("\n{:<5} {:<30} {:<15} {:<15} {:<12}".format("ID", "Nombre", "Documento", "Salario Base", "Fecha Ingreso"))
        print("-" * 80)
        
        for empleado in empleados:
            print("{:<5} {:<30} {:<15} ${:<14,.0f} {}".format(
                empleado.id,
                empleado.nombre,
                empleado.documento,
                empleado.salario_base,
                empleado.fecha_ingreso.strftime("%Y-%m-%d")
            ))
    
    def seleccionar_empleado(self, mensaje="Seleccione un empleado"):
        """Permite al usuario seleccionar un empleado de la lista o buscarlo"""
        while True:
            print(f"\n{mensaje}:")
            print("1. Ver lista de empleados")
            print("2. Buscar por ID")
            print("3. Buscar por documento")
            print("0. Cancelar")
            
            opcion = self.obtener_opcion(0, 3)
            
            if opcion == 0:
                return None
            
            if opcion == 1:
                # Mostrar lista de empleados
                empleados = Empleado.get_all()
                if not empleados:
                    print("\nNo hay empleados registrados en el sistema.")
                    self.pausa()
                    continue
                
                self.mostrar_empleados(empleados)
                id_empleado = self.obtener_entero("\nIngrese el ID del empleado (0 para cancelar): ")
                if id_empleado == 0:
                    continue
                
                empleado = Empleado.get_by_id(id_empleado)
                if empleado:
                    return empleado
                else:
                    print(f"\nNo se encontró un empleado con ID {id_empleado}")
                    self.pausa()
            
            elif opcion == 2:
                # Buscar por ID
                id_empleado = self.obtener_entero("ID del empleado: ")
                empleado = Empleado.get_by_id(id_empleado)
                if empleado:
                    return empleado
                else:
                    print(f"\nNo se encontró un empleado con ID {id_empleado}")
                    self.pausa()
            
            elif opcion == 3:
                # Buscar por documento
                documento = self.obtener_texto("Documento del empleado: ")
                empleado = Empleado.get_by_documento(documento)
                if empleado:
                    return empleado
                else:
                    print(f"\nNo se encontró un empleado con documento {documento}")
                    self.pausa()
    
    #=========================================================================
    # Menú y funciones para Liquidaciones
    #=========================================================================
    
    def menu_liquidaciones(self):
        """Menú de gestión de liquidaciones"""
        while True:
            self.limpiar_pantalla()
            print("=" * 50)
            print("GESTIÓN DE LIQUIDACIONES".center(50))
            print("=" * 50)
            print("\nSeleccione una opción:")
            print("1. Crear nueva liquidación")
            print("2. Modificar liquidación")
            print("3. Buscar liquidación")
            print("4. Ver liquidaciones por empleado")
            print("0. Volver al menú principal")
            
            opcion = self.obtener_opcion(0, 4)
            
            if opcion == 0:
                return
            elif opcion == 1:
                self.crear_liquidacion()
            elif opcion == 2:
                self.modificar_liquidacion()
            elif opcion == 3:
                self.buscar_liquidacion()
            elif opcion == 4:
                self.listar_liquidaciones_empleado()
    
    def crear_liquidacion(self):
        """Función para crear una nueva liquidación"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("CREAR NUEVA LIQUIDACIÓN".center(50))
        print("=" * 50)
        
        # Primero, seleccionar el empleado
        empleado = self.seleccionar_empleado("Seleccione el empleado para la liquidación")
        if not empleado:
            return
        
        try:
            print(f"\nCreando liquidación para: {empleado.nombre} (ID: {empleado.id})")
            print(f"Salario base: ${empleado.salario_base:,.0f}")
            
            # Obtener parámetros para la liquidación
            horas_diurnas = self.obtener_entero("Horas extras diurnas: ")
            horas_nocturnas = self.obtener_entero("Horas extras nocturnas: ")
            bonos_extra = self.obtener_float("Bonificaciones adicionales: ")
            deduccion_adicional = self.obtener_float("Deducciones adicionales: ")
            
            # Calcular auxilios y valores según la configuración
            salario_minimo = Configuracion.get_by_nombre('salario_minimo').valor
            limite_auxilio = Configuracion.get_by_nombre('limite_smmlv_auxilio').valor
            auxilio_transporte = Configuracion.get_by_nombre('auxilio_transporte').valor if empleado.salario_base <= (salario_minimo * limite_auxilio) else 0
            
            # Calcular total de nómina (simplificado)
            valor_hora_extra = Configuracion.get_by_nombre('valor_hora_extra').valor
            porcentaje_hora_diurna = Configuracion.get_by_nombre('porcentaje_hora_diurna').valor
            porcentaje_hora_nocturna = Configuracion.get_by_nombre('porcentaje_hora_nocturna').valor
            porcentaje_deducciones = Configuracion.get_by_nombre('porcentaje_deducciones').valor
            
            # Cálculo de horas extras
            valor_horas_diurnas = horas_diurnas * valor_hora_extra * (1 + porcentaje_hora_diurna)
            valor_horas_nocturnas = horas_nocturnas * valor_hora_extra * (1 + porcentaje_hora_nocturna)
            
            # Deducciones básicas (salud y pensión)
            deducciones_base = empleado.salario_base * porcentaje_deducciones
            
            # Total de la nómina
            total_nomina = (empleado.salario_base + valor_horas_diurnas + valor_horas_nocturnas + 
                           bonos_extra + auxilio_transporte - deducciones_base - deduccion_adicional)
            
            # Mostrar resumen de la liquidación
            print("\n--- Resumen de la Liquidación ---")
            print(f"Salario base: ${empleado.salario_base:,.0f}")
            print(f"Valor horas extras diurnas: ${valor_horas_diurnas:,.0f}")
            print(f"Valor horas extras nocturnas: ${valor_horas_nocturnas:,.0f}")
            print(f"Bonificaciones: ${bonos_extra:,.0f}")
            print(f"Auxilio de transporte: ${auxilio_transporte:,.0f}")
            print(f"Deducciones base: ${deducciones_base:,.0f}")
            print(f"Deducciones adicionales: ${deduccion_adicional:,.0f}")
            print(f"Total nómina: ${total_nomina:,.0f}")
            
            confirmar = input("\n¿Desea guardar esta liquidación? (s/n): ").strip().lower()
            if confirmar == 's':
                # Crear y guardar la liquidación
                liquidacion = Liquidacion(
                    empleado.id, empleado.salario_base, horas_diurnas, horas_nocturnas,
                    bonos_extra, deduccion_adicional, auxilio_transporte, total_nomina
                )
                
                if liquidacion.save():
                    print(f"\n¡Liquidación registrada exitosamente con ID {liquidacion.id}!")
                else:
                    print("\n¡Error al registrar la liquidación!")
            else:
                print("\nOperación cancelada.")
                
        except Exception as e:
            print(f"\n¡Error al crear liquidación: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def modificar_liquidacion(self):
        """Función para modificar una liquidación existente"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("MODIFICAR LIQUIDACIÓN".center(50))
        print("=" * 50)
        
        # Buscar la liquidación a modificar
        liquidacion_id = self.obtener_entero("ID de la liquidación a modificar (0 para cancelar): ")
        if liquidacion_id == 0:
            return
        
        liquidacion = Liquidacion.get_by_id(liquidacion_id)
        if not liquidacion:
            print(f"\nNo se encontró una liquidación con ID {liquidacion_id}")
            self.pausa()
            return
        
        try:
            # Mostrar información actual
            empleado = Empleado.get_by_id(liquidacion.empleado_id)
            print(f"\nModificando liquidación ID {liquidacion.id} del empleado {empleado.nombre}")
            print(f"Fecha: {liquidacion.fecha_liquidacion}")
            print(f"Salario base: ${liquidacion.salario_base:,.0f}")
            print(f"Horas extras diurnas: {liquidacion.horas_diurnas}")
            print(f"Horas extras nocturnas: {liquidacion.horas_nocturnas}")
            print(f"Bonificaciones: ${liquidacion.bonos_extra:,.0f}")
            print(f"Deducciones adicionales: ${liquidacion.deduccion_adicional:,.0f}")
            print(f"Auxilio de transporte: ${liquidacion.auxilio_transporte:,.0f}")
            print(f"Total nómina: ${liquidacion.total_nomina:,.0f}")
            
            print("\n¿Qué dato desea modificar?")
            print("1. Horas extras diurnas")
            print("2. Horas extras nocturnas")
            print("3. Bonificaciones")
            print("4. Deducciones adicionales")
            print("0. Cancelar")
            
            opcion = self.obtener_opcion(0, 4)
            
            if opcion == 0:
                return
                
            # Obtener nuevos valores
            if opcion == 1:
                liquidacion.horas_diurnas = self.obtener_entero("Nuevas horas extras diurnas: ")
            elif opcion == 2:
                liquidacion.horas_nocturnas = self.obtener_entero("Nuevas horas extras nocturnas: ")
            elif opcion == 3:
                liquidacion.bonos_extra = self.obtener_float("Nuevas bonificaciones: ")
            elif opcion == 4:
                liquidacion.deduccion_adicional = self.obtener_float("Nuevas deducciones adicionales: ")
            
            # Recalcular el total de la nómina
            valor_hora_extra = Configuracion.get_by_nombre('valor_hora_extra').valor
            porcentaje_hora_diurna = Configuracion.get_by_nombre('porcentaje_hora_diurna').valor
            porcentaje_hora_nocturna = Configuracion.get_by_nombre('porcentaje_hora_nocturna').valor
            porcentaje_deducciones = Configuracion.get_by_nombre('porcentaje_deducciones').valor
            
            valor_horas_diurnas = liquidacion.horas_diurnas * valor_hora_extra * (1 + porcentaje_hora_diurna)
            valor_horas_nocturnas = liquidacion.horas_nocturnas * valor_hora_extra * (1 + porcentaje_hora_nocturna)
            deducciones_base = liquidacion.salario_base * porcentaje_deducciones
            
            liquidacion.total_nomina = (liquidacion.salario_base + valor_horas_diurnas + valor_horas_nocturnas + 
                                       liquidacion.bonos_extra + liquidacion.auxilio_transporte - 
                                       deducciones_base - liquidacion.deduccion_adicional)
            
            # Mostrar resumen actualizado
            print("\n--- Resumen Actualizado ---")
            print(f"Horas extras diurnas: {liquidacion.horas_diurnas}")
            print(f"Horas extras nocturnas: {liquidacion.horas_nocturnas}")
            print(f"Bonificaciones: ${liquidacion.bonos_extra:,.0f}")
            print(f"Deducciones adicionales: ${liquidacion.deduccion_adicional:,.0f}")
            print(f"Total nómina recalculado: ${liquidacion.total_nomina:,.0f}")
            
            confirmar = input("\n¿Desea guardar estos cambios? (s/n): ").strip().lower()
            if confirmar == 's':
                # Guardar los cambios
                if liquidacion.save():
                    print("\n¡Liquidación actualizada exitosamente!")
                else:
                    print("\n¡Error al actualizar la liquidación!")
            else:
                print("\nOperación cancelada.")
                
        except Exception as e:
            print(f"\n¡Error al modificar liquidación: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def buscar_liquidacion(self):
        """Función para buscar una liquidación por su ID"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("BUSCAR LIQUIDACIÓN".center(50))
        print("=" * 50)
        
        liquidacion_id = self.obtener_entero("ID de la liquidación (0 para cancelar): ")
        if liquidacion_id == 0:
            return
        
        try:
            liquidacion = Liquidacion.get_by_id(liquidacion_id)
            if liquidacion:
                empleado = Empleado.get_by_id(liquidacion.empleado_id)
                
                print("\n--- Información de la Liquidación ---")
                print(f"ID: {liquidacion.id}")
                print(f"Empleado: {empleado.nombre} (ID: {empleado.id})")
                print(f"Documento: {empleado.documento}")
                print(f"Fecha: {liquidacion.fecha_liquidacion}")
                print(f"Salario base: ${liquidacion.salario_base:,.0f}")
                print(f"Horas extras diurnas: {liquidacion.horas_diurnas}")
                print(f"Horas extras nocturnas: {liquidacion.horas_nocturnas}")
                print(f"Bonificaciones: ${liquidacion.bonos_extra:,.0f}")
                print(f"Deducciones adicionales: ${liquidacion.deduccion_adicional:,.0f}")
                print(f"Auxilio de transporte: ${liquidacion.auxilio_transporte:,.0f}")
                print(f"Total nómina: ${liquidacion.total_nomina:,.0f}")
            else:
                print(f"\nNo se encontró una liquidación con ID {liquidacion_id}")
                
        except Exception as e:
            print(f"\n¡Error al buscar liquidación: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    def listar_liquidaciones_empleado(self):
        """Función para listar todas las liquidaciones de un empleado"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("LIQUIDACIONES POR EMPLEADO".center(50))
        print("=" * 50)
        
        # Seleccionar el empleado
        empleado = self.seleccionar_empleado("Seleccione un empleado para ver sus liquidaciones")
        if not empleado:
            return
        
        try:
            liquidaciones = Liquidacion.get_by_empleado(empleado.id)
            if liquidaciones:
                print(f"\nLiquidaciones del empleado: {empleado.nombre} (ID: {empleado.id})")
                print("\n{:<5} {:<12} {:<15} {:<15} {:<15}".format(
                    "ID", "Fecha", "Horas Extras", "Bonos", "Total"
                ))
                print("-" * 65)
                
                for liq in liquidaciones:
                    horas_totales = liq.horas_diurnas + liq.horas_nocturnas
                    print("{:<5} {:<12} {:<15} ${:<14,.0f} ${:<14,.0f}".format(
                        liq.id,
                        liq.fecha_liquidacion.strftime("%Y-%m-%d"),
                        horas_totales,
                        liq.bonos_extra,
                        liq.total_nomina
                    ))
            else:
                print(f"\nEl empleado {empleado.nombre} no tiene liquidaciones registradas.")
                
        except Exception as e:
            print(f"\n¡Error al listar liquidaciones: {e}")
            print(traceback.format_exc())
        
        self.pausa()
    
    #=========================================================================
    # Menú y funciones para Configuración
    #=========================================================================
    
    def menu_configuracion(self):
        """Menú de configuración del sistema"""
        while True:
            self.limpiar_pantalla()
            print("=" * 50)
            print("CONFIGURACIÓN DEL SISTEMA".center(50))
            print("=" * 50)
            print("\nSeleccione una opción:")
            print("1. Ver parámetros de configuración")
            print("2. Modificar parámetro")
            print("0. Volver al menú principal")
            
            opcion = self.obtener_opcion(0, 2)
            
            if opcion == 0:
                return
            elif opcion == 1:
                self.listar_configuraciones()
            elif opcion == 2:
                self.modificar_configuracion()

    def listar_configuraciones(self):
        """Función para listar todos los parámetros de configuración"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("PARÁMETROS DE CONFIGURACIÓN".center(50))
        print("=" * 50)
        
        try:
            configuraciones = Configuracion.get_all()
            if configuraciones:
                print("\n{:<5} {:<30} {:<15} {:<30}".format("ID", "Parámetro", "Valor", "Descripción"))
                print("-" * 80)
                
                for config in configuraciones:
                    if 'porcentaje' in config.nombre_parametro.lower():
                        valor_formateado = f"{config.valor * 100:.2f}%"
                    elif config.valor >= 1000:
                        valor_formateado = f"${config.valor:,.0f}"
                    else:
                        valor_formateado = str(config.valor)
                    
                    print("{:<5} {:<30} {:<15} {:<30}".format(
                        config.id,
                        config.nombre_parametro,
                        valor_formateado,
                        config.descripcion[:30] if config.descripcion else ""
                    ))
            else:
                print("\nNo hay parámetros de configuración registrados.")
                
        except Exception as e:
            print(f"\n¡Error al listar configuraciones: {e}")
            print(traceback.format_exc())
        
        self.pausa()

    def modificar_configuracion(self):
        """Función para modificar un parámetro de configuración"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("MODIFICAR PARÁMETRO DE CONFIGURACIÓN".center(50))
        print("=" * 50)
        
        try:
            configuraciones = Configuracion.get_all()
            if not configuraciones:
                print("\nNo hay parámetros de configuración registrados.")
                self.pausa()
                return
            
            print("\n{:<5} {:<30} {:<15} {:<30}".format("ID", "Parámetro", "Valor", "Descripción"))
            print("-" * 80)
            
            for config in configuraciones:
                if 'porcentaje' in config.nombre_parametro.lower():
                    valor_formateado = f"{config.valor * 100:.2f}%"
                elif config.valor >= 1000:
                    valor_formateado = f"${config.valor:,.0f}"
                else:
                    valor_formateado = str(config.valor)
                
                print("{:<5} {:<30} {:<15} {:<30}".format(
                    config.id,
                    config.nombre_parametro,
                    valor_formateado,
                    config.descripcion[:30] if config.descripcion else ""
                ))
            
            config_id = self.obtener_entero("\nID del parámetro a modificar (0 para cancelar): ")
            if config_id == 0:
                return
            
            config = next((c for c in configuraciones if c.id == config_id), None)
            if not config:
                print(f"\nNo se encontró un parámetro con ID {config_id}")
                self.pausa()
                return
            
            print(f"\nModificando: {config.nombre_parametro}")
            print(f"Valor actual: {config.valor}")
            print(f"Descripción: {config.descripcion}")
            
            if 'porcentaje' in config.nombre_parametro.lower():
                nuevo_valor = self.obtener_float(f"Nuevo valor (en porcentaje, actual: {config.valor * 100:.2f}%): ") / 100
            else:
                nuevo_valor = self.obtener_float(f"Nuevo valor (actual: {config.valor}): ")
            
            confirmar = input("\n¿Desea guardar este cambio? (s/n): ").strip().lower()
            if confirmar == 's':
                config.valor = nuevo_valor
                if config.save():
                    print(f"\n¡Parámetro '{config.nombre_parametro}' actualizado exitosamente!")
                else:
                    print("\n¡Error al actualizar el parámetro!")
            else:
                print("\nOperación cancelada.")
                
        except Exception as e:
            print(f"\n¡Error al modificar configuración: {e}")
            print(traceback.format_exc())
        
        self.pausa()

if __name__ == "__main__":
    app = InterfazSimple()
    app.mostrar_menu_principal()

