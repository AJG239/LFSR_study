import math
from collections import Counter
from berlekamp_massey import berlekamp_massey


ALPHA = 0.01  # Nivel de significancia

def _igamc(a: float, x: float) -> float:
    if x <= 0:
        return 1.0
    if x < a + 1:
        # Serie
        term = 1.0 / a
        total = term
        for n in range(1, 300):
            term *= x / (a + n)
            total += term
            if abs(term) < 1e-12 * abs(total):
                break
        return 1.0 - total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    else:
        f = 1e-30
        C = f
        D = 1.0 / (x + 1 - a)
        f = C * D
        for n in range(1, 300):
            an = n * (a - n)
            bn = x + 2 * n + 1 - a
            D = bn + an * D
            if abs(D) < 1e-30:
                D = 1e-30
            C = bn + an / C
            if abs(C) < 1e-30:
                C = 1e-30
            D = 1.0 / D
            delta = C * D
            f *= delta
            if abs(delta - 1.0) < 1e-12:
                break
        return f * math.exp(-x + a * math.log(x) - math.lgamma(a))

def test_de_frecuencia(secuentia: list[int]) -> dict:
    longitud = len(secuentia)

    S = sum((2 * bit - 1) for bit in secuentia)
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
        return {
            "test": "Frecuencia por bloque",
            "error": "La secuencia es demasiado corta para el tamaño de bloque especificado."
        }

    chi_cuadrado = 0.0
    for i in range(num_bloques):
        bloque = secuencia[i * tam_boque:(i + 1) * tam_boque]
        prob = sum(bloque) / tam_boque
        chi_cuadrado += (prob - 0.5) ** 2

    chi_cuadrado *= 4 * tam_boque
    p_valor = _igamc(num_bloques / 2.0, chi_cuadrado / 2.0)

    return {
        "test": "Frecuencia por Bloques",
        "chi_cuadrado": chi_cuadrado,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
        "num_bloques": num_bloques,
        "tam_bloque": tam_boque,
    }

def test_rachas(secuencia: list[int]) -> dict:
    longitud = len(secuencia)
    pi = sum(secuencia) / longitud

    tau = 2 / math.sqrt(longitud)

    if abs(pi - 0.5) >= tau:
        return {
            "test": "Test de rachas",
            "error": "Sesgo elevado"
        }
    
    contador = 1
    for i in range(1, longitud):
        if secuencia[i] != secuencia[i - 1]:
            contador += 1
    
    numerador = abs(contador - 2 * longitud * pi * (1 - pi))
    denominador = 2 * math.sqrt(2 * longitud) * pi * (1 - pi)

    if denominador == 0:
        p_valor = 0
    else:
        p_valor = math.erfc(numerador / denominador)

    return {
        "test": "Test de rachas",
        "contador_de_rachas": contador,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
    }
 
def test_de_racha_mas_larga(secuencia: list[int]) -> dict:
    longitud = len(secuencia)
    
    # Parámetros de cálculo con respecto a la longitud de la secuencia
    if longitud < 128:
        return {
            "test": "Racha más larga",
            "error": "La secuencia es demasiado corta (minimo 128 bits)."
        }
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
        
        # Clasificación según la longitud de la racha más larga
        index = racha_maxima - v_offset

        if index < 0:
            index = 0
        elif index > K:
            index = K
        
        rachas[index] += 1

    chi_cuadrado = sum((rachas[i] - numero_bloques * p_valores[i]) ** 2 / (numero_bloques * p_valores[i]) for i in range(K + 1))
    p_valor = _igamc(K / 2.0, chi_cuadrado / 2.0)

    return {
        "test": "Racha más larga",
        "chi_cuadrado": chi_cuadrado,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
    }

def test_serial(secuencia: list[int], m: int = 2) -> dict:
    longitud = len(secuencia)

    def secuencia_phi(phi_secuencia, m_val):
        if m_val == 0:
            return 0

        extension = phi_secuencia + phi_secuencia[:m_val + 1]
        contador = Counter()

        for i in range(longitud):
            patron = tuple(extension[i:i + m_val])
            contador[patron] += 1
        
        total = sum(value ** 2 for value in contador.values())
        return (2 ** m_val / longitud) * total - longitud

    psi_m = secuencia_phi(secuencia, m)
    psi_m1 = secuencia_phi(secuencia, m - 1)
    psi_m2 = secuencia_phi(secuencia, m - 2) if m >= 2 else 0.0

    delta1 = psi_m - psi_m1
    delta2 = psi_m - 2 * psi_m1 + psi_m2

    p_value1 = _igamc(2 ** (m - 2), delta1 / 2.0)
    p_value2 = _igamc(2 ** (m - 3), delta2 / 2.0) if m >= 3 else 1.0

    return {
        "test": f"Serial (m={m})",
        "delta": delta1,
        "p_value": p_value1,
        "p_value2": p_value2,
        "passed": p_value1 >= ALPHA and p_value2 >= ALPHA,
    }


def test_entropia(secuencia: list[int], m: int = 2) -> dict:
    longitud = len(secuencia)

    def phi(m_val):
        if m_val == 0:
            return 0
        
        extension = secuencia + secuencia[:m_val - 1]
        contador = Counter()

        for i in range(longitud):
            patron = tuple(extension[i:i + m_val])
            contador[patron] += 1

        total = 0

        for value in contador.values():
            pi = value / longitud
            if pi > 0:
                total += pi * math.log(pi)

        return total

    phi_m = phi(m)
    phi_m1 = phi(m + 1)

    aprox_entp = phi_m - phi_m1
    chi_cuadrado = 2 * longitud * (math.log(2) - aprox_entp)
    p_valor = _igamc(2 ** (m - 1), chi_cuadrado / 2.0)

    return {
        "test": f"Entropia (m={m})",
        "statistic": chi_cuadrado,
        "p_value": p_valor,
        "passed": p_valor >= ALPHA,
        "approx_entropy": aprox_entp,
    }


def test_complejidad_lineal(secuencia: list[int], M: int = 500) -> dict:
    longitud = len(secuencia)
    num_bloques = longitud // M 

    if num_bloques == 0:
        return {
            "test": "Complejidad lineal",
            "error": "Secuencia demasiado corta."
        }

    mu = M / 2.0 + (9 + (-1) ** (M + 1)) / 36.0 - (M / 3.0 + 2 / 9.0) / (2 ** M)

    cat = 6  # Número de categorías
    val = [0] * (cat + 1)
    complejidades = []

    for i in range(num_bloques):
        bloque = secuencia[i * M: (i + 1) * M]
        res = berlekamp_massey(bloque)
        CL = res["complejidad_lineal"]
        complejidades.append(CL)

        T = (-1) ** M * (CL - mu) + 2 / 9.0

        # Clasificar en categorías
        if T <= -2.5:
            val[0] += 1
        elif T <= -1.5:
            val[1] += 1
        elif T <= -0.5:
            val[2] += 1
        elif T <= 0.5:
            val[3] += 1
        elif T <= 1.5:
            val[4] += 1
        elif T <= 2.5:
            val[5] += 1
        else:
            val[6] += 1

    # Probabilidades teóricas
    prob = [0.010882, 0.03568, 0.11765, 0.24268, 0.24268, 0.11765, 0.23267]

    # Chi-cuadrado
    chi_cuadrado = sum(
        (val[i] - longitud * prob[i]) ** 2 / (longitud * prob[i])
        for i in range(cat + 1)
        if longitud * prob[i] > 0
    )

    p_valor = _igamc(cat / 2.0, chi_cuadrado / 2.0)

    avg_complejidad = sum(complejidades) / len(complejidades) if complejidades else 0

    return {
        "test": f"Complejidad lineal (M={M})",
        "statistic": chi_cuadrado,
        "p_valor": p_valor,
        "passed": p_valor >= ALPHA,
        "complejidad_media": avg_complejidad,
        "complejidad_esperada": mu,
        "numero_bloques": num_bloques,
    }


if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [1, 0, 1, 1, 1, 1, 0, 0, 1, 0]  # Secuencia de ejemplo
    resultado = test_de_frecuencia(secuencia)
    print(resultado)

    resultado = test_de_frecuencia_por_bloques(secuencia, tam_boque=5)
    print(resultado)

    resultado = test_rachas(secuencia)
    print(resultado)

    resultado = test_de_racha_mas_larga(secuencia)
    print(resultado)

    resultado = test_serial(secuencia, m=2)
    print(resultado)

    resultado = test_entropia(secuencia, m=2)
    print(resultado)

    resultado = test_complejidad_lineal(secuencia, M=5)
    print(resultado)
