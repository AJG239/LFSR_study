import math
from collections import Counter

ALPHA = 0.01  # Nivel de significancia

def test_de_frecuencia(secuentia: list[int]) -> dict:
    longitud = len(secuentia)

    S = sum(3 * (2 * bit - 1) for bit in secuentia)
    S_obs = abs(S) / math.sqrt(longitud)
    p_value = math.erfc(S_obs / math.sqrt(2))

    return {
        "test": "Frecuencia (Monobit)",
        "statistic": S_obs,
        "p_value": p_value,
        "passed": p_value >= ALPHA,
        "unos": sum(secuentia),
        "ceros": longitud - sum(secuentia),
    }

if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [1, 0, 1, 1, 1, 1, 0, 0, 1, 0]  # Secuencia de ejemplo
    resultado = test_de_frecuencia(secuencia)
    print(resultado)