def encadenar_hacia_adelante(hechos_iniciales, reglas):
    hechos = set(hechos_iniciales)
    traza = []
    reglas_registradas = set()

    while True:
        hay_novedad = False

        for regla in reglas:
            condiciones = regla["condiciones"]
            conclusion = regla["conclusion"]
            nombre = regla["nombre"]

            if condiciones.issubset(hechos):

                # Registrar la regla aunque la conclusión ya exista
                if nombre not in reglas_registradas:
                    traza.append({
                        "regla": nombre,
                        "condiciones_activadas": list(condiciones),
                        "conclusion_generada": conclusion
                    })
                    reglas_registradas.add(nombre)

                # Añadir solo los hechos que sean nuevos
                if conclusion not in hechos:
                    hechos.add(conclusion)
                    hay_novedad = True

        if not hay_novedad:
            break

    return hechos, traza
