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
    bloque = []
    bit_actual = secuencia[0]
    longitud_actual = 1

    for i in range(1, periodo):
        if secuencia[i] == bit_actual:
            longitud_actual += 1
        else:
            bloque.append((bit_actual, longitud_actual))
            bit_actual = secuencia[i]
            longitud_actual = 1
    
    bloque.append((bit_actual, longitud_actual))

    total_bloques = len(bloque)

    racha_unos = {}
    racha_ceros = {}

    for bit, length in bloque:
        if bit == 1:
            racha_unos[length] = racha_unos.get(length, 0) + 1
        else:
            racha_ceros[length] = racha_ceros.get(length, 0) + 1

    distribucion_bloques = []
    bool_distribucion = True

    for k in range(1, longitud):
        rachas_esperadas = 2 ** (longitud - k - 1) if k <= longitud - 2 else 1
        unos = racha_unos.get(k, 0)
        ceros = racha_ceros.get(k, 0)

        cumple = True

        if k <= longitud - 2:
            if unos != rachas_esperadas or ceros != rachas_esperadas:
                cumple = False
                bool_distribucion = False

        distribucion_bloques.append({
            'longitud': k,
            'racha_unos': racha_unos,
            'racha_ceros': racha_ceros,
            'rachas_esperadas': rachas_esperadas if k <= longitud - 2 else "1 uno, 1 cero",
            'cumple': cumple
        })

    resultado['rachas'] = {
        'postulado': 'Distribucion de rachas',
        'bloques_totales': total_bloques,
        'distribución': distribucion_bloques,
        'unos': dict(sorted(racha_unos.items())),
        'ceros': dict(sorted(racha_ceros.items())),
        'passed': bool_distribucion
    }


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
    print("Resultado del Postulado de Distribución de Rachas:", resultado['rachas'])
    print("Resultado del Postulado de Autocorrelación:", resultado['autocorrelación'])