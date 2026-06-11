class LFSR_Fibonacci:
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
        # El bit de salida es el primer bit (x^n)
        output_bit = self.estado[0]

        # El elemento x^0 (XOR de los bits en las posiciones de los frames)
        constante = self.estado[0] 
        for frame in self.frames:
            constante ^= self.estado[frame]  # XOR con los bits correspondientes a los frames

        # Desplazamos el estado a la izquierda
        for i in range(self.n - 1):
            self.estado[i] = self.estado[i + 1]
        self.estado[-1] = constante  # El nuevo bit de entrada es la constante calculada

        return output_bit

    def generar_secuencia(self, longitud: int) -> list[int]:
        secuencia = []
        for i in range(longitud):
            secuencia.append(self.avance_LFSR())
        return secuencia
    
    def restablecer_estado(self):
        self.estado = list(self.estado_inicial)

    


if __name__ == "__main__":
    # Caso de uso
    polinomio = [5, 3, 0]  # x^5 + x^3 + 1
    estado_inicial = [1, 0, 0, 0, 0]  # Estado inicial (debe tener 5 bits), el primer bit es el más significativo (x^5)
    
    lfsr = LFSR_Fibonacci(polinomio, estado_inicial)

    print(f"Estado inicial: {lfsr.estado}")
    for i in range(10):
        output = lfsr.avance_LFSR()
        print(f"Salida: {output}, Estado después del desplazamiento: {lfsr.estado}")

    # Permite continuar la secuencia de generación hasta el estado inicial para verificar el ciclo completo
    secuencia = lfsr.generar_secuencia(63)
    print(f"Secuencia generada: {secuencia}")

    lfsr.restablecer_estado()
    secuencia_rest = lfsr.generar_secuencia(10)
    print(f"Secuencia después de restablecer el estado: {secuencia_rest}")

    print("LFSR Fibonacci creado con éxito.")