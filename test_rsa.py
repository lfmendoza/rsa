import unittest
from rsa import (
    es_primo,
    generar_primo,
    mcd,
    inverso_modular,
    generar_llaves,
    encriptar,
    desencriptar,
    encriptar_mensaje,
    desencriptar_mensaje
)

class TestRSA(unittest.TestCase):

    def test_es_primo(self):
        self.assertTrue(es_primo(2))
        self.assertTrue(es_primo(13))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(15))

    def test_generar_primo(self):
        primo = generar_primo(16)
        self.assertTrue(es_primo(primo))
        self.assertEqual(primo.bit_length(), 16)

    def test_mcd(self):
        self.assertEqual(mcd(54, 24), 6)
        self.assertEqual(mcd(17, 31), 1)
        self.assertEqual(mcd(0, 5), 5)
        self.assertEqual(mcd(5, 0), 5)

    def test_inverso_modular(self):
        self.assertEqual(inverso_modular(3, 11), 4)
        self.assertEqual(inverso_modular(7, 40), 23)
        self.assertIsNone(inverso_modular(2, 4))

    def test_generar_llaves(self):
        llave_publica, llave_privada = generar_llaves(512)
        self.assertIsNotNone(llave_publica)
        self.assertIsNotNone(llave_privada)
        self.assertNotEqual(llave_publica[0], llave_privada[0])

    def test_encriptar_y_desencriptar(self):
        llave_publica, llave_privada = generar_llaves(512)
        mensaje = 123456789
        encriptado = encriptar(mensaje, llave_publica)
        desencriptado = desencriptar(encriptado, llave_privada)
        self.assertEqual(mensaje, desencriptado)

    def test_encriptar_mensaje_completo(self):
        llave_publica, llave_privada = generar_llaves(512)
        mensaje = "Mensaje de prueba para encriptación completa."
        encriptado = encriptar_mensaje(mensaje, llave_publica)
        desencriptado = desencriptar_mensaje(encriptado, llave_privada)
        self.assertEqual(mensaje, desencriptado)

    def test_mensajes_grandes(self):
        llave_publica, llave_privada = generar_llaves(1024)
        mensaje = ("Este es un mensaje muy largo y complejo que contiene una gran cantidad de información. "
                   "Se utiliza para probar el sistema RSA en situaciones de carga pesada y asegurar que "
                   "funcione correctamente incluso con mensajes de gran tamaño.")
        encriptado = encriptar_mensaje(mensaje, llave_publica)
        desencriptado = desencriptar_mensaje(encriptado, llave_privada)
        self.assertEqual(mensaje, desencriptado)

if __name__ == '__main__':
    unittest.main()
