"""
==================================================
Script de lógica difusa
==================================================
"""

import numpy as np

REJILLA = np.linspace(0, 100, 1001)


def pertenencia_triangular(x, a, b, c):
    """Triángulo con vértices a <= b <= c, pico en b (μ=1). Acepta escalares o arrays."""
    x = np.asarray(x, dtype=float)
    subida = np.where(b > a, (x - a) / (b - a) if b > a else 0.0, (x >= b).astype(float))
    bajada = np.where(c > b, (c - x) / (c - b) if c > b else 0.0, (x <= b).astype(float))
    return np.clip(np.minimum(subida, bajada), 0.0, 1.0)


def pertenencia_trapezoidal(x, a, b, c, d):
    """Trapecio con a <= b <= c <= d, meseta (μ=1) entre b y c. Acepta escalares o arrays."""
    x = np.asarray(x, dtype=float)
    subida = (x - a) / (b - a) if b > a else (x >= b).astype(float)
    bajada = (d - x) / (d - c) if d > c else (x <= c).astype(float)
    return np.clip(np.minimum(subida, bajada), 0.0, 1.0)


# ========================= Conjuntos difusos =========================
# Entrada: ocupación (%)
def ocupacion_baja(o):  return pertenencia_trapezoidal(o, 0, 0, 20, 40)
def ocupacion_media(o): return pertenencia_triangular(o, 20, 50, 80)
def ocupacion_alta(o):  return pertenencia_trapezoidal(o, 60, 80, 100, 100)

# Salida: desvío (%)
def desvio_bajo(d):  return pertenencia_trapezoidal(d, 0, 0, 20, 40)
def desvio_medio(d): return pertenencia_triangular(d, 20, 50, 80)
def desvio_alto(d):  return pertenencia_trapezoidal(d, 60, 80, 100, 100)


# ========================= Metodo de Mandani =========================

def metodo_mandani(ocupacion, rejilla=REJILLA):
    """
    Inferencia Mamdani:
      D1: SI ocupación es baja  ENTONCES desvío es bajo
      D2: SI ocupación es media ENTONCES desvío es medio
      D3: SI ocupación es alta  ENTONCES desvío es alto
    Devuelve el desvío d* (centroide discreto) y el detalle del cálculo.
    """
    if not 0 <= ocupacion <= 100:
        raise ValueError("La ocupación debe estar en [0, 100].")

    # 1) Fuzzificación: grado de activación (fuerza) de cada regla
    w1 = float(ocupacion_baja(ocupacion))
    w2 = float(ocupacion_media(ocupacion))
    w3 = float(ocupacion_alta(ocupacion))

    # 2) Implicación (recorte con mínimo) de cada consecuente
    r1 = np.minimum(w1, desvio_bajo(rejilla))
    r2 = np.minimum(w2, desvio_medio(rejilla))
    r3 = np.minimum(w3, desvio_alto(rejilla))

    # 3) Agregación (máximo) de las reglas
    mu_agg = np.maximum.reduce([r1, r2, r3])

    # 4) Defuzzificación: centroide  d* ≈ Σ d_j·μ_agg(d_j) / Σ μ_agg(d_j)
    area = np.sum(mu_agg)
    d_star = np.sum(rejilla * mu_agg) / area if area > 0 else 0.0

    return d_star, {"activaciones": (w1, w2, w3), "mu_agg": mu_agg}


def decidir_desvio(ocupacion, umbral=80):
    """Regla nítida original: SI ocupación > 80 ENTONCES desviar_paquetes."""
    return ocupacion > umbral


#Prueba funcion difusa
"""
if __name__ == "__main__":
    for o in [75, 80, 81]:
        d, info = metodo_mandani(o)
        w = tuple(round(v, 2) for v in info["activaciones"])
        print(f"ocupación={o:>3}% -> desvío d*={d:6.2f}%  "
              f"(baja, media, alta)={w}  desviar>80: {decidir_desvio(o)}")
"""

"""
    Resultado: 
    ocupación= 75% -> desvío d*= 74.75%  (baja, media, alta)=(0.0, 0.17, 0.75)  desviar>80: False
    ocupación= 80% -> desvío d*= 84.47%  (baja, media, alta)=(0.0, 0.0, 1.0)  desviar>80: False
    ocupación= 81% -> desvío d*= 84.47%  (baja, media, alta)=(0.0, 0.0, 1.0)  desviar>80: True

    Cuando el porcentaje de ocupación es menor o igual a 80 da como resultado falso. A parir del 81 el resultado es verdadero.
    Pienso que la regla es correcta debido a que 80 representa el limite que puede tolerar la zona antes de que se llene. El contenido que exceda de ese 
    porcentaje será desviado para no seguir llenando la zona.
"""