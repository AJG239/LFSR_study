from a51_estructura import A51_estructura

class A51(A51_estructura):
    
    LONGITUD_CLAVE = 64
    LONGITUD_FRAME = 22
    CICLO_WARM_UP = 100
    
    def __init__(self, clave: int, frame: int): # Partimos de los tres registros a cero
        super().__init__(0, 0, 0)
        self._cargar(clave, self.LONGITUD_CLAVE)
        self._cargar(frame, self.LONGITUD_FRAME)
        self._calentar()
 
    def _avanzar_todos(self): # Avanza los tres registros sin aplicar la mayoría (carga inicial)
        self.r1 = self._avanzar(self.r1, self.R_1_taps, self.R_1_mascara)
        self.r2 = self._avanzar(self.r2, self.R_2_taps, self.R_2_mascara)
        self.r3 = self._avanzar(self.r3, self.R_3_taps, self.R_3_mascara)
 
    def _cargar(self, valor: int, n_bits: int):
        """
        Introduce los n_bits menos significativos de 'valor' en los tres
        registros, empezando por el bit 0. Cada bit se hace XOR en el
        bit 0 de los tres registros tras un avance forzado.
        """
        for i in range(n_bits):
            bit = (valor >> i) & 1
            self._avanzar_todos()
            self.r1 ^= bit
            self.r2 ^= bit
            self.r3 ^= bit
 
    def _calentar(self):
        # 100 ciclos con regla de mayoría descartando la salida
        for _ in range(self.CICLO_WARM_UP):
            self.step()
 
 
if __name__ == "__main__":
    clave = 0x123456789ABCDEF0   # ejemplo, no significativo
    frame = 0x1FFFFF             # 22 bits
 
    alg_cifrado = A51(clave=clave, frame=frame)
    bits = alg_cifrado.generar(228)
 
    print(f"Clave de sesión: 0x{clave:016X}")
    print(f"Frame: 0x{frame:06X}")
    print()
    print("Secuencia cifrante de un frame GSM (228 bits):")
    print("  " + "".join(str(b) for b in bits))
        
        