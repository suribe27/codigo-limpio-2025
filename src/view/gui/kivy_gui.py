import sys
sys.path.append("src")
from model.Calculo_Total import *

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class NominaApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text='Salario Base:'))
        self.salario_input = TextInput(multiline=False)
        self.add_widget(self.salario_input)

        self.add_widget(Label(text='Horas Extra Diurnas:'))
        self.horas_diurnas_input = TextInput(multiline=False)
        self.add_widget(self.horas_diurnas_input)

        self.add_widget(Label(text='Horas Extra Nocturnas:'))
        self.horas_nocturnas_input = TextInput(multiline=False)
        self.add_widget(self.horas_nocturnas_input)

        self.add_widget(Label(text='Bonos Extra:'))
        self.bonos_input = TextInput(multiline=False)
        self.add_widget(self.bonos_input)

        self.add_widget(Label(text='Deducciones Adicionales:'))
        self.deduccion_input = TextInput(multiline=False)
        self.add_widget(self.deduccion_input)

        self.calcular_button = Button(text='Calcular Nómina')
        self.calcular_button.bind(on_press=self.calcular_nomina)
        self.add_widget(self.calcular_button)

        self.result_label = Label(text='')
        self.add_widget(self.result_label)

    def calcular_nomina(self, instance):
        try:
            salario_base = float(self.salario_input.text)
            horas_diurnas = int(self.horas_diurnas_input.text)
            horas_nocturnas = int(self.horas_nocturnas_input.text)
            bonos_extra = float(self.bonos_input.text)
            deduccion_adicional = float(self.deduccion_input.text)
            
            resultado = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)
            self.result_label.text = f'El valor total de su nómina es {resultado:.2f}'
        
        except ErrorSalarioN as ex:
            self.result_label.text = str(ex)
        except ErrorDeduccionesM as ex:
            self.result_label.text = str(ex)
        except ErrorHorasExtra as ex:
            self.result_label.text = str(ex)
        except ValueError:
            self.result_label.text = '¡Error! Ingrese solo valores numéricos.'
        except Exception as ex:
            self.result_label.text = f'Error inesperado: {str(ex)}'

class MainApp(App):
    def build(self):
        return NominaApp()

if __name__ == '__main__':
    MainApp().run()
