import math

def postulados_golomb(secuencia: list[int], longitud: int = None) -> dict:
    resultado = {}
    periodo = len(secuencia)

    if longitud is None:
        # Sacar la longitud del LFSR a partir del periodo dado por la secuencia
        longitud = int(math.log2(periodo + 1))

    # Primer postulado: Balance
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

    # Segundo postulado: rachas


    # Tercer postulado: autocorrelación
    valores_coincidentes = []
    secuencia_copia = [2 ** n - 1 for n in secuencia]

    for k in range(periodo):
        correlacion = sum(
            secuencia_copia[i] * secuencia[(i + k) % periodo] for i in range(periodo) 
        )
        valores_coincidentes.append(correlacion)

    comp_coincidencia = True
    if valores_coincidentes[0] != periodo:
        comp_coincidencia = False
    
    for k in range(1, periodo):
        if valores_coincidentes[k] != -1:
            comp_coincidencia = False
            break

    resultado['autocorrelación'] = {
        'postulado': 'Autocorrelación',
        'C(0)': valores_coincidentes[0],
        'C(0) esperados': periodo,
        'C(k)': valores_coincidentes[1:6],
        'passed': comp_coincidencia
    }

    return resultado

if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [0, 0, 0, 0, 1, 0, 1]  # Secuencia de bits de ejemplo
    resultado = postulados_golomb(secuencia)
    print("Resultado del Postulado de Balance:", resultado['balance'])

    print("Resultado del Postulado de Autocorrelación:", resultado['autocorrelación'])