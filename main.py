"""
==================================================
Interfaz de Consola - Sistema Experto y Lógica Difusa
==================================================
"""

from motor import encadenar_hacia_adelante
from reglas import reglas
from logica_difusa import metodo_mandani, decidir_desvio

# Mapeo de identificadores a descripciones legibles
NOMBRES_HECHOS = {
    "codigo_no_legible": "Código de paquete no legible",
    "destino_no_identificado": "Destino no identificado",
    "destino_identificado": "Destino identificado",
    "embalaje_danado": "Embalaje dañado",
    "contenido_fragil": "Contenido frágil",
    "peso_fuera_rango": "Peso fuera del rango permitido",
    "documentacion_incompleta": "Documentación incompleta",
    "sin_incidencias": "Paquete sin incidencias",
}

NOMBRES_CONCLUSIONES = {
    "solicitar_lectura_manual": "Solicitar lectura manual",
    "enviar_revision": "Enviar paquete a revisión",
    "comprobar_peso": "Comprobar el peso del paquete",
    "retener_temporalmente": "Retener temporalmente",
    "autorizar_clasificacion": "Autorizar clasificación",
}


def obtener_nombre(clave):
    if clave in NOMBRES_HECHOS:
        return NOMBRES_HECHOS[clave]
    if clave in NOMBRES_CONCLUSIONES:
        return NOMBRES_CONCLUSIONES[clave]
    return clave.replace("_", " ").capitalize()


def zona_sistema_experto():
    print("\n" + "=" * 50)
    print("        ZONA 1: EVALUACIÓN DE INCIDENCIAS")
    print("=" * 50)
    print("Seleccione los hechos observados introduciendo sus números separados por comas:")
    
    lista_hechos = list(NOMBRES_HECHOS.items())
    for idx, (clave, descripcion) in enumerate(lista_hechos, 1):
        print(f"  [{idx}] {descripcion}")

    entrada = input("\nOpciones seleccionadas (ej. 1,2) o presione Enter para ninguna: ").strip()
    
    hechos_iniciales = set()
    if entrada:
        indices = [i.strip() for i in entrada.split(",") if i.strip().isdigit()]
        for idx_str in indices:
            idx = int(idx_str) - 1
            if 0 <= idx < len(lista_hechos):
                hechos_iniciales.add(lista_hechos[idx][0])

    print("\n--- HECHOS INICIALES ---")
    if hechos_iniciales:
        for h in sorted(hechos_iniciales):
            print(f" • {obtener_nombre(h)}")
    else:
        print(" Ninguno seleccionado.")

    # Ejecución del motor
    hechos_finales, traza = encadenar_hacia_adelante(hechos_iniciales, reglas)
    conclusiones = hechos_finales - hechos_iniciales

    print("\n--- TRAZA DE INFERENCIA ---")
    if traza:
        for paso_num, paso in enumerate(traza, 1):
            print(f"Paso {paso_num}: Regla {paso['regla']}")
            conds = [obtener_nombre(c) for c in paso["condiciones_activadas"]]
            print(f"  Condiciones: {' Y '.join(conds)}")
            print(f"  → Conclusión: {obtener_nombre(paso['conclusion_generada'])}\n")
    else:
        print(" No se activó ninguna regla.")

    print("--- CONCLUSIONES FINALES ---")
    if conclusiones:
        for c in sorted(conclusiones):
            print(f" ✅ {obtener_nombre(c)}")
    else:
        print(" Sin conclusiones nuevas.")


def zona_logica_difusa():
    print("\n" + "=" * 50)
    print("        ZONA 2: CONTROL DE OCUPACIÓN (DIFUSA)")
    print("=" * 50)
    
    while True:
        try:
            val = input("Introduzca la ocupación actual de la zona (0-100 %): ").strip()
            ocupacion = float(val)
            if 0 <= ocupacion <= 100:
                break
            print("Por favor, introduzca un valor entre 0 y 100.")
        except ValueError:
            print("Entrada no válida. Debe ser un número.")

    # Inferencia difusa y regla rígida
    desvio_final, info = metodo_mandani(ocupacion)
    baja, media, alta = info["activaciones"]
    regla_rigida = decidir_desvio(ocupacion)

    print(f"\nOcupación evaluada: {ocupacion}%")
    print("\n--- GRADOS DE PERTENENCIA ---")
    print(f" • Baja:  {baja:.2f}")
    print(f" • Media: {media:.2f}")
    print(f" • Alta:  {alta:.2f}")

    print("\n--- COMPARATIVA DE DECISIÓN ---")
    print(f" • Regla rígida (> 80%): {'DESVIAR PAQUETES' if regla_rigida else 'NO DESVIAR'}")
    print(f" • Salida difusa (centroide): Nivel de desvío = {desvio_final:.2f}%")


def main():
    while True:
        print("\n" + "=" * 50)
        print("    SISTEMA EXPERTO DE GESTIÓN LOGÍSTICA")
        print("=" * 50)
        print("1. Evaluar paquete (Sistema Experto)")
        print("2. Evaluar ocupación de zona (Lógica Difusa)")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            zona_sistema_experto()
        elif opcion == "2":
            zona_logica_difusa()
        elif opcion == "3":
            print("\nSaliendo del sistema...")
            break
        else:
            print("Opción inválida. Seleccione 1, 2 o 3.")


if __name__ == "__main__":
    main()