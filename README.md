# Análisis comparativo de algoritmos basados en LFSR

Código del Trabajo de Fin de Grado *«Análisis comparativo de algoritmos basados en LFSR: caracterización matemática y criptográfica»*, del Grado en Matemática Computacional (U-tad).

El proyecto implementa en Python los componentes fundamentales de los cifrados de flujo basados en registros de desplazamiento con retroalimentación lineal (LFSR) y los analiza con dos herramientas clásicas del criptoanálisis: el algoritmo de Berlekamp-Massey y un subconjunto de la suite estadística NIST SP 800-22. El recorrido va del LFSR aislado —vulnerable— a dos estrategias de protección por no linealidad: un generador combinacional y el cifrado A5/1 de GSM.

## Requisitos

- Python 3.10 o superior.
- Sin dependencias externas: el proyecto utiliza únicamente la biblioteca estándar (`math` y `collections`).

## Uso

El punto de entrada es `main_demo.py`, que reproduce todas las demostraciones del trabajo con un único comando:

```bash
python3 main_demo.py
```

La ejecución muestra, en orden: la generación de m-secuencias con las dos configuraciones del LFSR, la verificación de los postulados de Golomb, la complejidad lineal del generador combinacional, los tests NIST sobre un LFSR aislado y, finalmente, el análisis de Berlekamp-Massey y NIST sobre la salida del cifrado A5/1.

Cada módulo puede ejecutarse también de forma independiente para validar el componente que implementa. Por ejemplo:

```bash
python3 lfsr_fibonacci.py      # genera una m-secuencia y verifica su periodo
python3 berlekamp_massey.py    # reconstruye un LFSR a partir de su salida
python3 a51.py                 # genera un frame de secuencia cifrante de A5/1
```

## Estructura del proyecto

| Módulo | Descripción |
|--------|-------------|
| `lfsr_fibonacci.py` | LFSR en configuración de Fibonacci (retroalimentación externa). |
| `lfsr_galois.py` | LFSR en configuración de Galois (retroalimentación interna). |
| `lfsr_simple.py` | LFSR de cuatro etapas en representación entera, como puente hacia A5/1. |
| `propiedades_golomb.py` | Verificación de los tres postulados de pseudoaleatoriedad de Golomb. |
| `berlekamp_massey.py` | Algoritmo de Berlekamp-Massey: reconstruye el polinomio de retroalimentación y calcula la complejidad lineal. |
| `generador_combinado.py` | Generador combinacional de tres LFSR con una función booleana no lineal. |
| `a51_estructura.py` | Arquitectura de A5/1 (tres LFSR con control irregular de reloj por mayoría), sin inicialización. |
| `a51.py` | Cifrado A5/1 completo, con carga de clave, carga de frame y calentamiento. |
| `nist_tests.py` | Subconjunto de siete tests de la suite NIST SP 800-22. |
| `analisis_a51.py` | Aplica Berlekamp-Massey y los tests NIST a la salida de A5/1. |
| `main_demo.py` | Punto de entrada que integra y ejecuta todas las demostraciones. |

## Componentes

### LFSR y propiedades de Golomb

Las clases `LFSR_Fibonacci` y `LFSR_Galois` implementan las dos realizaciones canónicas de un mismo polinomio de retroalimentación. Sobre las m-secuencias que generan, `propiedades_golomb.py` verifica el equilibrio, la distribución de rachas y la autocorrelación.

### Berlekamp-Massey

`berlekamp_massey.py` reconstruye el LFSR de menor longitud capaz de generar una secuencia dada. Aplicado a un LFSR aislado, recupera su polinomio completo a partir de un número reducido de bits, lo que demuestra por qué un registro lineal no puede emplearse como cifrado.

### Generador combinacional

`generador_combinado.py` combina tres LFSR de longitudes coprimas mediante la función no lineal `f(x1, x2, x3) = (x1 AND x2) XOR x3`. Su complejidad lineal es muy superior a la de los registros individuales, lo que ilustra el efecto de la no linealidad frente a Berlekamp-Massey.

### A5/1

La implementación de A5/1 sigue una construcción incremental. `a51_estructura.py` reproduce la arquitectura de los tres LFSR (de 19, 22 y 23 bits) con la regla de mayoría que controla el avance irregular, partiendo de un estado interno cargado manualmente. `a51.py` hereda esa arquitectura y añade la fase de inicialización oficial: carga de la clave de sesión (64 bits), carga del frame (22 bits) y 100 ciclos de calentamiento.

### Tests NIST

`nist_tests.py` implementa siete tests de la suite NIST SP 800-22: frecuencia (monobit), frecuencia por bloques, rachas, racha más larga de unos, serial, entropía aproximada y complejidad lineal. Sobre la salida de un LFSR y de A5/1, el único test que detecta la estructura subyacente es el de complejidad lineal, mientras que el resto se superan: superar los tests estadísticos no garantiza la seguridad de un cifrado.

## Licencia

Código desarrollado con fines académicos en el marco de un Trabajo de Fin de Grado.

## Autor

Alejandro Jiménez García — Grado en Matemática Computacional, U-tad (2026).
