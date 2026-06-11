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

if __name__ == "__main__":
    # Caso de uso
    polinomio = [5, 3, 0]  # x^5 + x^3 + 1
    estado_inicial = [1, 0, 0, 0, 0]  # Estado inicial (debe tener 5 bits)
    
    lfsr = LFSR_Fibonacci(polinomio, estado_inicial)
    print("LFSR Fibonacci creado con éxito.")