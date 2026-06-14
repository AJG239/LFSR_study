import math
from collections import Counter

ALPHA = 0.01  # Nivel de significancia

def test_de_frecuencia(secuentia: list[int]) -> dict:
    longitud = len(secuentia)

    S = sum(3 * (2 * bit - 1) for bit in secuentia)
    S_obs = abs(S) / math.sqrt(longitud)
    p_valor = math.erfc(S_obs / math.sqrt(2))

    return {
        "test": "Frecuencia (Monobit)",
        "chi_cuadrado": S_obs,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
        "unos": sum(secuentia),
        "ceros": longitud - sum(secuentia),
    }

def test_de_frecuencia_por_bloques(secuencia: list[int], tam_boque: int = 128) -> dict:
    longitud = len(secuencia)
    num_bloques = longitud // tam_boque

    if num_bloques == 0:
        raise ValueError("La secuencia es demasiado corta para el tamaño de bloque especificado.")

    proporciones = []
    for i in range(num_bloques):
        bloque = secuencia[i * tam_boque:(i + 1) * tam_boque]
        proporciones.append(sum(bloque) / tam_boque)

    chi_cuadrado = sum((p - 0.5) ** 2 for p in proporciones) * (4 * tam_boque)
    p_valor = math.erfc(math.sqrt(chi_cuadrado / 2))

    return {
        "test": "Frecuencia por Bloques",
        "chi_cuadrado": chi_cuadrado,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
        "num_bloques": num_bloques,
        "tam_bloque": tam_boque,
    }

def test_de_rachas(secuencia: list[int]) -> dict:
    longitud = len(secuencia)
    
    # Parámetros de cálculo con respecto a la longitud de la secuencia
    if longitud < 128:
        raise ValueError("La secuencia es demasiado corta (minimo 128 bits).")
    elif longitud < 6272:
       longitud_bloque, K = 8, 3
       numero_bloques = longitud // longitud_bloque
       p_valores = [0.2148, 0.3672, 0.2305, 0.1875]
       v_offset = 1
    elif longitud < 750000:   
       longitud_bloque, K = 128, 5
       numero_bloques = longitud // longitud_bloque
       p_valores = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
       v_offset = 4
    else: 
        longitud_bloque, K = 10000, 6
        numero_bloques = longitud// longitud_bloque
        p_valores = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
        v_offset = 10
    
    # Contar la racha más larga
    rachas = [0] * (K + 1)

    for i in range(numero_bloques):
        bloque = secuencia[i * longitud_bloque: (i + 1) * longitud_bloque]
        racha_maxima = 0
        racha_actual = 0

        for b in bloque:
            if b == 1:
                racha_actual += 1
                racha_maxima = max(racha_maxima, racha_actual)
            else:
                racha_actual = 0
        
        # Clasificaciones en 
        index = racha_maxima - rachas

        if index < 0:
            index = 0
        elif index > K:
            index = K
        
        rachas[index] += 1

    chi_cuadrado = sum((rachas[i] - numero_bloques * p_valores[i]) ** 2 / (numero_bloques * p_valores[i]) for i in range(K + 1))
    p_valor = math.erfc(math.sqrt(chi_cuadrado / 2))

    return {
        "test": "Rachas",
        "chi_cuadrado": chi_cuadrado,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
    }

if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [1, 0, 1, 1, 1, 1, 0, 0, 1, 0]  # Secuencia de ejemplo
    resultado = test_de_frecuencia(secuencia)
    print(resultado)

    resultado = test_de_frecuencia_por_bloques(secuencia, tam_boque=5)
    print(resultado)

    resultado = test_de_rachas(secuencia)
    print(resultado)

    resultado = test_de_rachas(secuencia)
    print(resultado)