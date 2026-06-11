def berlekamp_massey(secuencia: list[int]) -> dict:
    # Longitud de la secuencia
    longitud = len(secuencia)
    
    # Antes de empezar se necesita el polinomio de retroalimentación inicial, que es x^0 (1)
    polinomio_retroalimentacion = [0] * (longitud + 1)  
    polinomio_retroalimentacion[0] = 1 

    # Se necesita un polinomio auxiliar para almacenar el polinomio de retroalimentación anterior
    polinomio_auxiliar = [0] * (longitud + 1)
    polinomio_auxiliar[0] = 1

    complejidad_lineal = 0
    pasos = 1
    cambios_discrepancia = 1  # En GF(2) siempre es 1 cuando existe un cambio

    for i in range(longitud):
        """
            El proceso de sigue los siguientes pasos:
            1. Calcular la discrepancia (discrepancia) para el bit actual
            2. Si la discrepancia es 0, simplemente se incrementa el contador de pasos
            3. Si la discrepancia es 1, se actualiza el polinomio
            4. Se actualiza el polinomio de retroalimentación y el polinomio auxiliar
        """

        discrepancia = secuencia[i]  # El bit actual de la secuencia
        for j in range(1, complejidad_lineal + 1):
            discrepancia ^= (polinomio_retroalimentacion[j] & secuencia[i - j])  # XOR para calcular la discrepancia

        if discrepancia == 0:
            pasos += 1
        else:
            polinomio_temporal = list(polinomio_retroalimentacion)  # Guardamos el polinomio actual antes de actualizarlo

            # Actualizamos el polinomio de retroalimentación
            for j in range(longitud + 1 - pasos):
                polinomio_retroalimentacion[j + pasos] ^= polinomio_auxiliar[j]  # XOR para actualizar el polinomio de retroalimentación
            
            if 2 * complejidad_lineal <= i:
                complejidad_lineal = i + 1 - complejidad_lineal
                polinomio_auxiliar = list(polinomio_temporal)  # Actualizamos el polinomio auxiliar con el antiguo polinomio de retroalimentación
                pasos = discrepancia 
                cambios_discrepancia = 1
            else:
                cambios_discrepancia += 1
    
    polinomio_resultante = polinomio_retroalimentacion[:complejidad_lineal + 1]  # El polinomio resultante es el polinomio de retroalimentación hasta la complejidad lineal

    return {
        "complejidad_lineal": complejidad_lineal,
        "polinomio": polinomio_resultante,
        "pasos": pasos,
        "cambios_discrepancia": cambios_discrepancia
    }

if __name__ == "__main__":
    # Ejemplo de uso
    secuencia = [1, 0, 0, 0, 0, 1, 0, 1, 0, 1]  # Secuencia de bits de ejemplo
    resultado = berlekamp_massey(secuencia)
    print("Complejidad Lineal:", resultado["complejidad_lineal"])
    print("Polinomio Resultante:", resultado["polinomio"])
    print("Pasos:", resultado["pasos"])
    print("Cambios de Discrepancia:", resultado["cambios_discrepancia"])
    
    if resultado['polinomio'] == [1, 0, 1, 0, 0, 0]:  # Polinomio x^2 + 1
        print("El polinomio resultante es el mismo que el polinomio de retroalimentación utilizado en el LFSR.")
    else:
        print("El polinomio resultante no coincide con el polinomio de retroalimentación utilizado en el LFSR.")



