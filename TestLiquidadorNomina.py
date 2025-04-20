import unittest
import sys
sys.path.append("src")
from src.model.Calculo_Total import *

class TestLiquidadorNomina(unittest.TestCase):

    def test_normal_1(self):
        salario_base = 2000000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 0

        expected = 1989040

        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertEqual(expected, result)

    def test_normal_2(self):
        salario_base = 1500000
        horas_diurnas = 2
        horas_nocturnas = 1
        bonos_extra = 0
        deduccion_adicional = 0

        expected = 1536157.35

        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_normal_3(self):
        salario_base = 1800000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 300000
        deduccion_adicional = 0

        expected = 2081040

        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_4(self):
        salario_base = 1300000
        horas_diurnas = 36
        horas_nocturnas = 15
        bonos_extra = 100000
        deduccion_adicional = 0

        expected = 1552341.07


        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_5(self):
        salario_base = 2500000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 500000

        expected = 1949040

        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_6(self):
        salario_base = 1700000
        horas_diurnas = 14
        horas_nocturnas = 19
        bonos_extra = 200000
        deduccion_adicional = 0

        expected = 1998106.37

        result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)
    
    
    
    def test_error_1(self):
        salario_base = -1500000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 0

        with self.assertRaises (ErrorSalarioN):

            result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)


    def test_error_2(self):
        salario_base = 3500000
        horas_diurnas = 12
        horas_nocturnas = 12
        bonos_extra = 300000
        deduccion_adicional = 1400000
                    
        with self.assertRaises (ErrorDeduccionesM):

             result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

    
        
        
    def test_error_3(self):
        salario_base = 5000000
        horas_diurnas = 43
        horas_nocturnas = 47
        bonos_extra = 0
        deduccion_adicional = 0
                    
        with self.assertRaises (ErrorHorasExtra):
            
            result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

    def test_error_4(self):
        salario_base = "tres millones"
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 0
                    
        with self.assertRaises (Exception):
            
            result = calculo_total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)
        
        
if __name__ == '__main__':
    # print( Payment.calcularCuota.__doc__)
    unittest.main()