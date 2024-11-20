import random
from typing import Optional, Tuple

def es_primo(n: int, k: int = 10) -> bool:
    """Prueba de primalidad de Miller-Rabin para verificar si un número es primo."""
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Descomponer n-1 como 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Realizar k pruebas
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generar_primo(bits: int) -> int:
    """Genera un número primo aleatorio de 'bits' bits."""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Asegurar que n tenga el tamaño adecuado y sea impar
        if es_primo(n):
            return n

def mcd(a: int, b: int) -> int:
    """Calcula el máximo común divisor de dos números."""
    while b != 0:
        a, b = b, a % b
    return abs(a)

def inverso_modular(e: int, phi: int) -> Optional[int]:
    """Calcula el inverso modular de e módulo phi usando el algoritmo extendido de Euclides."""
    t, newt = 0, 1
    r, newr = phi, e
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return None  # No existe inverso modular
    if t < 0:
        t += phi
    return t

def generar_llaves(bits: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Genera un par de llaves pública y privada para RSA."""
    p = generar_primo(bits // 2)
    q = generar_primo(bits // 2)
    while q == p:
        q = generar_primo(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Elegir e tal que 1 < e < phi y mcd(e, phi) = 1
    e = 65537  # Valor comúnmente utilizado para e
    if mcd(e, phi) != 1:
        e = random.randrange(2, phi)
        while mcd(e, phi) != 1:
            e = random.randrange(2, phi)
    d = inverso_modular(e, phi)
    if d is None:
        raise Exception("No se pudo calcular el inverso modular.")
    llave_publica = (e, n)
    llave_privada = (d, n)
    return llave_publica, llave_privada

def encriptar(mensaje: int, llave_publica: Tuple[int, int]) -> int:
    """Encripta un mensaje usando la llave pública de RSA."""
    e, n = llave_publica
    if mensaje < 0 or mensaje >= n:
        raise ValueError("El mensaje debe ser un entero positivo menor que n.")
    return pow(mensaje, e, n)

def desencriptar(cifrado: int, llave_privada: Tuple[int, int]) -> int:
    """Desencripta un mensaje encriptado usando la llave privada de RSA."""
    d, n = llave_privada
    if cifrado < 0 or cifrado >= n:
        raise ValueError("El cifrado debe ser un entero positivo menor que n.")
    return pow(cifrado, d, n)

def texto_a_bloques(texto: str, bloque_size: int) -> list:
    """Convierte un texto en una lista de bloques de enteros."""
    texto_bytes = texto.encode('utf-8')
    bloques = []
    for i in range(0, len(texto_bytes), bloque_size):
        bloque = texto_bytes[i:i+bloque_size]
        bloque_int = int.from_bytes(bloque, byteorder='big')
        bloques.append(bloque_int)
    return bloques

def bloques_a_texto(bloques: list, bloque_size: int) -> str:
    """Convierte una lista de bloques de enteros a texto."""
    texto_bytes = b''
    for bloque in bloques:
        bloque_bytes = bloque.to_bytes(bloque_size, byteorder='big')
        texto_bytes += bloque_bytes
    return texto_bytes.decode('utf-8', errors='ignore')

def encriptar_mensaje(texto: str, llave_publica: Tuple[int, int]) -> list:
    """Encripta un mensaje de texto completo."""
    e, n = llave_publica
    bloque_size = (n.bit_length() - 1) // 8
    bloques = texto_a_bloques(texto, bloque_size)
    encriptados = [encriptar(bloque, llave_publica) for bloque in bloques]
    return encriptados

def desencriptar_mensaje(encriptados: list, llave_privada: Tuple[int, int]) -> str:
    """Desencripta un mensaje encriptado completo."""
    d, n = llave_privada
    bloque_size = (n.bit_length() - 1) // 8
    bloques = [desencriptar(cifrado, llave_privada) for cifrado in encriptados]
    texto = bloques_a_texto(bloques, bloque_size)
    return texto

def main():
    bits = 2048  # Tamaño de las llaves en bits
    print("Generando llaves RSA de 2048 bits...")
    llave_publica, llave_privada = generar_llaves(bits)
    print("Llaves generadas exitosamente.")

    mensaje = ("Este es un mensaje muy largo y complejo para probar el sistema de encriptación RSA. "
               "Incluye diferentes caracteres como números (1234567890), símbolos (!@#$%^&*), y más texto "
               "para asegurar que el sistema pueda manejar grandes cantidades de datos sin problemas.")

    print("\nMensaje original:")
    print(mensaje)

    print("\nEncriptando mensaje...")
    encriptados = encriptar_mensaje(mensaje, llave_publica)
    print("Mensaje encriptado exitosamente.")

    print("\nDesencriptando mensaje...")
    mensaje_desencriptado = desencriptar_mensaje(encriptados, llave_privada)
    print("Mensaje desencriptado exitosamente.")

    print("\nMensaje desencriptado:")
    print(mensaje_desencriptado)

    # Verificar que el mensaje original y el desencriptado sean iguales
    if mensaje == mensaje_desencriptado:
        print("\nLa encriptación y desencriptación fueron exitosas.")
    else:
        print("\nHubo un error en el proceso de encriptación/desencriptación.")

if __name__ == "__main__":
    main()
