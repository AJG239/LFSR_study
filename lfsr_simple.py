def lfsr_4(estado_inicial, num_pasos):
    estado = estado_inicial & 0xF
    output = []

    for i in range(num_pasos):
        bit_salida = (estado >> 3) & 1
        nuevo = ((estado >> 3) ^ (estado >> 2)) & 1
        estado = ((estado << 1) | nuevo) & 0xF
        output.append(bit_salida)
    
    return output


def periodo(estado_inicial = 0b0001):
    bits_lfsr = lfsr_4(estado_inicial, num_pasos=4)
    referencia = bits_lfsr[:4]

    for i in range(1, len(bits_lfsr) - 4):
        if bits_lfsr[i:i+4] == referencia:
            return i
        
    return None

if __name__ == "__main__":
    secuencia = lfsr_4(estado_inicial=0b0001, num_pasos=20)
    print("Secuencia generada con estado inicial 0001: " + "".join(str(b) for b in secuencia))
    print("Período: " + str(periodo(0b0001)))