class LFSR_Galois:
    def __init__(self, polinomio: list[int], estado_inicial: list[int]):
        # Longitud del LFSR
        self.n = max(polinomio)

        # Sacamos los grados de los términos del polinomio, ordenados de mayor a menor
        self.frames = sorted([grado for grado in polinomio if 0 < grado < self.n], reverse=True)

        # Validar el estado inicial
        if len(estado_inicial) != self.n:
            raise ValueError(f"El estado inicial debe tener exactamente {self.n} bits.")
        
        
        # Validar que el estado inicial no sea nulo
        if all(bit == 0 for bit in estado_inicial):
            raise ValueError("El estado inicial no puede ser el estado nulo.")
        
        # Copiamos el estado_inicial para no modificar la variable original
        self.estado = list(estado_inicial)
        self.estado_inicial = list(estado_inicial)

        # Guardamos el polinomio
        self.polinomio = sorted(polinomio, reverse=True)

    def avance_LFSR(self) -> int:
       return 0

    def generar_secuencia(self, longitud: int) -> list[int]:
        secuencia = []
        for i in range(longitud):
            secuencia.append(self.avance_LFSR())
        return secuencia
    
    def restablecer_estado(self):
        self.estado = list(self.estado_inicial)

    def verificar_periodo_maximo(self) -> dict:    
        # Restablecemos al estado inicial para comprobar si la secuencia generada alcanza el periodo máximo
        self.restablecer_estado()
        periodo_maximo = (2 ** self.n) - 1

        # Generamos 2^n para verificar si se repite el estado inicial
        secuencia = self.generar_secuencia(periodo_maximo + 1)

        periodo = periodo_maximo
        for pos in range (1, periodo_maximo + 1):
            # Verificamos si el estado inicial se repite en la secuencia generada
            if secuencia[pos] == self.estado_inicial[0] and secuencia[pos:pos+self.n] == self.estado_inicial:
                periodo = pos
                break

        return {"periodo_maximo": periodo_maximo, "periodo_encontrado": periodo, "es_maximo": periodo == periodo_maximo}

    def representacion_polinmio(self) -> str:
        terminos = []
        for grado in self.polinomio:
            if grado == 0:
                terminos.append("1")
            elif grado == 1:
                terminos.append("x")
            else:
                terminos.append(f"x^{grado}")
        return " + ".join(terminos)

if __name__ == "__main__":
    # Caso de uso
    polinomio = [5, 3, 0]  # x^5 + x^3 + 1
    estado_inicial = [1, 0, 0, 0, 0]  # Estado inicial (debe tener 5 bits), el primer bit es el más significativo (x^5)
    
    lfsr = LFSR_Galois(polinomio, estado_inicial)

    print(f"Polinomio de retroalimentación: {lfsr.representacion_polinmio()}")

    print(f"Estado inicial: {lfsr.estado}")
    for i in range(10):
        output = lfsr.avance_LFSR()
        print(f"Salida: {output}, Estado después del desplazamiento: {lfsr.estado}")

    # Permite continuar la secuencia de generación hasta el estado inicial para verificar el ciclo completo
    secuencia = lfsr.generar_secuencia(21)
    print(f"Secuencia generada: {secuencia}")

    lfsr.restablecer_estado()
    secuencia_rest = lfsr.generar_secuencia(10)
    print(f"Secuencia después de restablecer el estado: {secuencia_rest}")

    resultado = lfsr.verificar_periodo_maximo()
    print(f"Resultados del verificación de periodo máximo: {resultado}")

    print("LFSR Galois creado con éxito.")