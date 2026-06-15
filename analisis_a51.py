from a51 import A51
from berlekamp_massey import berlekamp_massey
from nist_tests import test_complejidad_lineal, test_de_frecuencia, test_de_frecuencia_por_bloques, test_de_racha_mas_larga, test_entropia, test_rachas, test_serial



def analizar_bm(n_bits=2000, clave=0x123456789ABCDEF0, frame=0):
    secuencia = A51(clave=clave, frame=frame).generar(n_bits)
    resultado = berlekamp_massey(secuencia)
    print(f"BM A5/1: bits={n_bits} L={resultado['complejidad_lineal']}")


def analizar_nist(n_bits=100000, clave=0x123456789ABCDEF0, frame=0):
    secuencia = A51(clave=clave, frame=frame).generar(n_bits)

    pruebas = [
        ("freq", test_de_frecuencia),
        ("bloques", lambda s: test_de_frecuencia_por_bloques(s, tam_boque=128)),
        ("rachas", test_rachas),
        ("racha_larga", test_de_racha_mas_larga),
        ("serial", lambda s: test_serial(s, m=2)),
        ("entropia", lambda s: test_entropia(s, m=2)),
        ("lincomp", lambda s: test_complejidad_lineal(s, M=500)),
    ]

    print("NIST A5/1:")
    for nombre, fn in pruebas:
        resultado = fn(secuencia)
        p = resultado.get("p_value", resultado.get("p_valor", None))
        ok = "PASADO" if resultado.get("passed", False) else "FALLADO"
        if p is None:
            print(f"  {nombre}: {ok}")
        else:
            print(f"  {nombre}: {ok}  p={p:.4g}")


if __name__ == "__main__":
    analizar_bm(n_bits=2000)
    analizar_nist(n_bits=100000, clave=0x123456789ABCDEF0, frame=0)

