import sys
import os

# Soporte para PyInstaller: permite que encuentre correctamente el paquete model
if hasattr(sys, '_MEIPASS'):
    # Si es una aplicación compilada, agrega la ruta temporal usada por PyInstaller
    sys.path.append(os.path.join(sys._MEIPASS, "src"))
else:
    # Si es ejecución normal (desarrollo)
    sys.path.append("src")

from model.Calculo_Total import *

from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.core.window import Window

# Configuración de la ventana principal
Window.size = (Window.width, Window.height)  # Usa el tamaño actual de la ventana
Window.maximize()  # Maximiza la ventana
Window.clearcolor = (1, 1, 1, 1)  # Color de fondo blanco

# Clase principal de la interfaz de usuario
class NominaApp(BoxLayout):
    def __init__(self, **kwargs):
        # Inicializa el diseño vertical
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # Agrega los campos necesarios con sus textos guía (hint_text)
        self.agregar_campo("Salario Base", "Ingrese su salario (Ej: 100000)", 'salario_input')
        self.agregar_campo("Horas Extra Diurnas", "Ej: 2", 'horas_diurnas_input')
        self.agregar_campo("Horas Extra Nocturnas", "Ej: 3", 'horas_nocturnas_input')
        self.agregar_campo("Bonos Extra", "Ej: 50000", 'bonos_input')
        self.agregar_campo("Deducciones Adicionales", "Ej: 15000", 'deduccion_input')

        # Botón principal para calcular la nómina
        self.calcular_button = Button(
            text='Calcular Nómina', 
            background_color=(0.3, 0.6, 1, 1), 
            size_hint_y=None, height=50
        )
        self.calcular_button.bind(on_press=self.calcular_nomina)
        self.add_widget(self.calcular_button)

        # Etiqueta para mostrar el resultado del cálculo
        self.result_label = Label(
            text='', color=(0, 0, 0, 1),  
            font_size='22sp', size_hint_y=None, height=60
        )
        self.add_widget(self.result_label)

        # Muestra mensaje de bienvenida al iniciar
        Clock.schedule_once(lambda dt: self.mostrar_bienvenida(), 0.1)

    def agregar_campo(self, titulo, hint_text, atributo):
        # Crea una etiqueta con el título del campo
        self.add_widget(Label(text=titulo, size_hint_y=None, height=30, color=(0, 0, 0, 1)))

        # Crea el campo de entrada (TextInput)
        campo = TextInput(hint_text=hint_text, multiline=False, size_hint_y=None, height=40)
        setattr(self, atributo, campo)

        # Crea una etiqueta para mostrar errores
        error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=20)
        setattr(self, f'{atributo}_error', error_label)

        # Asocia evento de perder foco al validador
        campo.bind(focus=self.on_focus)

        # Agrega los elementos a la interfaz
        self.add_widget(campo)
        self.add_widget(error_label)

    def on_focus(self, instance, value):
        # Valida el campo al perder el foco (cuando value es False)
        if not value:
            self.validar_campo(instance)

    def mostrar_bienvenida(self):
        # Crea una ventana modal para dar la bienvenida al usuario
        popup = ModalView(size_hint=(1, 1), background_color=(0, 0, 0, 0.4), auto_dismiss=False)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # Mensaje explicativo
        mensaje = Label(
            text='Bienvenido al Calculador de Nómina 2025.\n\nEste programa le permite calcular el total de su pago incluyendo horas extra, bonos y deducciones.',
            color=(1, 1, 1, 1),
            font_size='16sp',
            halign='center'
        )

        # Botón para cerrar el mensaje
        cerrar_btn = Button(
            text='Entendido',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1)
        )
        cerrar_btn.bind(on_press=popup.dismiss)

        # Añade componentes y muestra la ventana
        layout.add_widget(mensaje)
        layout.add_widget(cerrar_btn)
        popup.add_widget(layout)
        popup.open()

    def calcular_nomina(self, instance):
        error_found = False  # Marca si se encuentra un error

        # Diccionario de mensajes de error por campo
        error_messages = {
            'salario_input_error': "Por favor, ingrese un salario válido, solo números positivos",
            'horas_diurnas_input_error': "Por favor, ingrese horas extra diurnas válidas, solo números positivos o 0 si no tiene",
            'horas_nocturnas_input_error': "Por favor, ingrese horas extra nocturnas válidas, solo números positivos o 0 si no tiene",
            'bonos_input_error': "Por favor, ingrese bonos válidos, solo números positivos o 0 si no tiene",
            'deduccion_input_error': "Por favor, ingrese deducciones válidas, solo números positivos o 0 si no tiene",
        }

        # Validación de todos los campos
        for key, error_message in error_messages.items():
            campo = getattr(self, key.replace("_error", ""))
            error_label = getattr(self, key)
            
            if not self.validar_campo(campo):
                error_label.text = error_message
                error_found = True
            else:
                error_label.text = ""

        # Si hubo errores, no continuar
        if error_found:
            return

        try:
            # Se convierten los valores ingresados
            salario_base = float(self.salario_input.text)
            horas_diurnas = int(self.horas_diurnas_input.text)
            horas_nocturnas = int(self.horas_nocturnas_input.text)
            bonos_extra = float(self.bonos_input.text)
            deduccion_adicional = float(self.deduccion_input.text)

            # Se llama a la función de cálculo
            resultado = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)
            self.result_label.text = f'El valor total de su nómina es {resultado:.2f}'

        # Captura de errores personalizados definidos en model.Calculo_Total
        except ErrorSalarioN as ex:
            self.result_label.text = str(ex)
        except ErrorDeduccionesM as ex:
            self.result_label.text = str(ex)
        except ErrorHorasExtra as ex:
            self.result_label.text = str(ex)
        # Errores por datos no numéricos
        except ValueError:
            self.result_label.text = '¡Error! Ingrese solo valores numéricos.'
        # Captura de errores inesperados
        except Exception as ex:
            self.result_label.text = f'Error inesperado: {str(ex)}'

    def validar_campo(self, campo):
        # Retorna True si el campo tiene un número válido (puede contener un punto)
        return campo.text.strip().replace(".", "", 1).isdigit()

class MainApp(App):
    def build(self):
        self.title = "Calculadora Nómina"  # Cambia el título de la ventana
        return NominaApp()


if __name__ == '__main__':
    MainApp().run()
