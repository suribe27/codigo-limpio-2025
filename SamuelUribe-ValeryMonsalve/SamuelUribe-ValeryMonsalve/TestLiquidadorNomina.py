import unittest
import Calculo_Total

class TestLiquidadorNomi(unittest.TestCase):

    def test_normal_1(self):
        salario_base = 2000000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 0

        expected = 1989040

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertEqual(expected, result)

    def test_normal_2(self):
        salario_base = 1500000
        horas_diurnas = 2
        horas_nocturnas = 1
        bonos_extra = 0
        deduccion_adicional = 0

        expected = 1536157.35

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_normal_3(self):
        salario_base = 1800000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 300000
        deduccion_adicional = 0

        expected = 2081040

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_4(self):
        salario_base = 1300000
        horas_diurnas = 36
        horas_nocturnas = 55
        bonos_extra = 100000
        deduccion_adicional = 0

        expected = 1723157.47

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_5(self):
        salario_base = 2500000
        horas_diurnas = 0
        horas_nocturnas = 0
        bonos_extra = 0
        deduccion_adicional = 500000

        expected = 2949040

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

    def test_extraordinario_6(self):
        salario_base = 1700000
        horas_diurnas = 14
        horas_nocturnas = 19
        bonos_extra = 200000
        deduccion_adicional = 0

        expected = 1998106.37

        result = Calculo_Total.Calculo_Total(salario_base, horas_diurnas, horas_nocturnas, bonos_extra, deduccion_adicional)

        self.assertAlmostEqual(expected, result, 2)

if __name__ == '__main__':
    unittest.main()

#holaaa
