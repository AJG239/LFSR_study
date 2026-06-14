from lfsr_fibonacci import LFSR_Fibonacci

class generador_combinacional:
    polinomio_1 =[5, 2, 0]
    polinomio_2 =[7, 1, 0]
    polinomio_3 =[11, 2, 0]

    periodo_1 = 2**5 - 1
    periodo_2 = 2**7 - 1
    periodo_3 = 2**11 - 1

    def __init__(self, estado_inicial: tuple = None):
        if estado_inicial is None:
            estado_inicial_1 = [1, 0, 1, 0, 1]
            estado_inicial_2 = [1, 1, 0, 0, 1, 0, 1]
            estado_inicial_3 = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        else:
            estado_inicial_1, estado_inicial_2, estado_inicial_3 = estado_inicial

        self.lfsr1 = LFSR_Fibonacci(self.polinomio_1, estado_inicial_1)
        self.lfsr2 = LFSR_Fibonacci(self.polinomio_2, estado_inicial_2)
        self.lfsr3 = LFSR_Fibonacci(self.polinomio_3, estado_inicial_3)


    @staticmethod
    def combinar(x_1: int, x_2: int, x_3: int) -> int:
        return (x_1 & x_2) ^ x_3
    
    def step(self) -> int:
        """
        Genera un bit de salida:
        1. Cada LFSR avanza un paso
        2. Se toman los bits de salida
        3. Se combinan con la función no lineal
        """
        x1 = self.lfsr1.avance_LFSR()
        x2 = self.lfsr2.avance_LFSR()
        x3 = self.lfsr3.avance_LFSR()
        return self.combinar(x1, x2, x3)
    
    def generar_secuencia(self, length: int) -> list[int]: # Genera una secuencia de n bits
        return [self.step() for _ in range(length)]
    
    
    def reset(self):
        """Reinicia todos los LFSR a sus semillas originales."""
        self.lfsr1.restablecer_estado()
        self.lfsr2.restablecer_estado()
        self.lfsr3.restablecer_estado()
    def periodos_teoricos(self) -> int:
        return self.periodo_1 * self.periodo_2 * self.periodo_3

    def info(self) -> str: # Información del generador
        return (
            f"Generador Combinacional de 3 LFSR\n"
            f"  LFSR1: {self.lfsr1.representacion_polinmio()} (n=5, periodo={self.periodo_1})\n"
            f"  LFSR2: {self.lfsr2.representacion_polinmio()} (n=7, periodo={self.periodo_2})\n"
            f"  LFSR3: {self.lfsr3.representacion_polinmio()} (n=11, periodo={self.periodo_3})\n"
            f"  Función: f(x1,x2,x3) = (x1 AND x2) XOR x3\n"
            f"  Periodo teórico: {self.periodo_1} * {self.periodo_2} * {self.periodo_3} = {self.periodos_teoricos():,}"
        )