class A51_estructura:
    # Máscaras de longitud de cada registro
    R_1_mascara = 0x07FFFF   # 19 bits
    R_2_mascara = 0x3FFFFF   # 22 bits
    R_3_mascara = 0x7FFFFF   # 23 bits

    # Posiciones de los taps de cada registro o valores del polinomio
    R_1_taps = 0x072000   # bits 13, 16, 17, 18
    R_2_taps = 0x300000   # bits 20, 21
    R_3_taps = 0x700080   # bits 7, 20, 21, 22

    # Bits de control para la regla de mayoría
    control_bit_R_1 = 8
    control_bit_R_2 = 10
    control_bit_R_3 = 10

    # Bits de salida (los más significativos de cada registro)
    output_R_1 = 18
    output_R_2 = 21
    output_R_3 = 22

    def __init__(self, r1, r2, r3):
        self.r1 = r1 & self.R_1_mascara
        self.r2 = r2 & self.R_2_mascara
        self.r3 = r3 & self.R_3_mascara

    @staticmethod
    def _paridad(x): # Devuelve el XOR de todos los bits de x
        x ^= x >> 16
        x ^= x >> 8
        x ^= x >> 4
        x ^= x >> 2
        x ^= x >> 1
        return x & 1
        
    @classmethod
    def _avanzar(cls, reg, taps, mask): # Avanza un registro un ciclo aplicando la realimentación
        bit_nuevo = cls._paridad(reg & taps)
        return ((reg << 1) & mask) | bit_nuevo

    def step(self):
        c_1 = (self.r1 >> self.control_bit_R_1) & 1
        c_2 = (self.r2 >> self.control_bit_R_2) & 1
        c_3 = (self.r3 >> self.control_bit_R_3) & 1

        mayor = (c_1 &  c_2) | (c_2 & c_3) | (c_1 & c_3)

        if c_1 == mayor:
            self.r1 = self._avanzar(self.r1, self.R_1_taps, self.R_1_mascara)
        if c_2 == mayor:
            self.r2 = self._avanzar(self.r2, self.R_2_taps, self.R_2_mascara)
        if c_3 == mayor:
            self.r3 = self._avanzar(self.r3, self.R_3_taps, self.R_3_mascara)

        bit_1 = (self.r1 >> self.output_R_1) & 1
        bit_2 = (self.r2 >> self.output_R_2) & 1
        bit_3 = (self.r3 >> self.output_R_3) & 1

        return bit_1 ^ bit_2 ^ bit_3

    def generar(self, n_bits): # Devuelve n bits de entrada
        return [self.step() for _ in range(n_bits)]

if __name__ == "__main__":
    # Estado interno fijado a mano para probar la arquitectura.
    # Los valores no representan ninguna clave concreta: solo sirven
    # para verificar que el control por mayoría produce una salida
    # razonable.
    alg_cifrado = A51_estructura(
        r1=0b1010101010101010101,        # 19 bits
        r2=0b1100110011001100110011,     # 22 bits
        r3=0b11110000111100001111000,    # 23 bits
    )

    bits = alg_cifrado.generar(64)

    print("Primeros 64 bits de salida (estado inicial fijo):")
    print("  " + "".join(str(b) for b in bits))

