import math

def postulados_golomb(secuencia: list[int], longitud: int = None) -> dict:
    resultado = {}
    periodo = len(secuencia)

    if longitud is None:
        # Sacar la longitud del LFSR a partir del periodo dado por la secuencia
        longitud = int(math.log2(periodo + 1))

    unos = sum(secuencia)
    ceros = periodo - unos

    resultado['balance'] = {
        'postulado': 'Balance',
        'unos': unos,
        'ceros': ceros,
        'diferencia': abs(unos - ceros),
        'unos_esperados': (2** (longitud - 1)),
        'ceros_esperados': 2 ** (longitud - 1) - 1,
        'passed': abs(unos - ceros) == 1
    }

    return resultado

if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [0, 0, 0, 0, 1, 0, 1]  # Secuencia de bits de ejemplo
    resultado = postulados_golomb(secuencia)
    print("Resultado del Postulado de Balance:", resultado['balance'])