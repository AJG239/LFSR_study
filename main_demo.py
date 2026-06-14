from lfsr_fibonacci import LFSR_Fibonacci
from lfsr_galois import LFSR_Galois
from berlekamp_massey import berlekamp_massey
from generador_combinado import generador_combinacional
from propiedades_golomb import postulados_golomb
from nist_tests import test_de_frecuencia, test_de_frecuencia_por_bloques, test_rachas, test_de_racha_mas_larga, test_serial, test_entropia, test_complejidad_lineal

def run_nist_tests(secuencia, label):
    print(f"NIST: {label}")
    resultados = [
        test_de_frecuencia(secuencia),
        test_de_frecuencia_por_bloques(secuencia, tam_boque=128),
        test_rachas(secuencia),
        test_de_racha_mas_larga(secuencia),
        test_serial(secuencia, m=2),
        test_entropia(secuencia, m=2),
        test_complejidad_lineal(secuencia, M=500),
    ]
    for prueba in resultados:
        nombre = prueba.get('test', 'desconocido')
        passed = prueba.get('passed', False)
        p_valor = prueba.get('p_value', prueba.get('p_valor', None))
        if p_valor is not None:
            print(f"  {nombre}: {'PASADO' if passed else 'FALLADO'} (p={p_valor:.5f})")
        else:
            print(f"  {nombre}: {'PASADO' if passed else 'FALLADO'}")
    return resultados


def main():
    fib = LFSR_Fibonacci([4, 1, 0], [1, 0, 0, 0])
    seq_fib = fib.generar_secuencia(15)
    gal = LFSR_Galois([4, 1, 0], [1, 0, 0, 0])
    seq_gal = gal.generar_secuencia(15)
    print('Fibonacci:', ''.join(map(str, seq_fib)))
    print('Galois:   ', ''.join(map(str, seq_gal)))

    n = 5
    lfsr = LFSR_Fibonacci([5, 2, 0], [1] + [0] * (n - 1))
    seq = lfsr.generar_secuencia(2**n - 1)
    resultados = postulados_golomb(seq, n)
    ok = resultados['balance']['passed'] and resultados['rachas']['passed'] and resultados['autocorrelación']['passed']
    print('Golomb:', 'PASADO' if ok else 'FALLADO')

    gen = generador_combinacional()
    gen_seq = gen.generar_secuencia(2000)
    bm = berlekamp_massey(gen_seq)
    print('Generador combinacional CL:', bm['complejidad_lineal'])

    seq_nist = LFSR_Fibonacci(
        [16, 5, 3, 2, 0],
        [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0],
    ).generar_secuencia(2000)
    run_nist_tests(seq_nist, 'LFSR simple')


if __name__ == '__main__':
    main()
