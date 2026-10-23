def encadenar_hacia_adelante(hechos_iniciales, reglas):
    # Copiamos los hechos iniciales para no modificar los originales
    hechos = set(hechos_iniciales)
    
    # Lista para guardar el historial de reglas aplicadas
    traza = []
    
    # Bucle principal: se repite mientras descubramos nuevos hechos
    while True:
        hay_novedad = False
        
        # Revisamos cada regla una por una
        for regla in reglas:
            condiciones = regla["condiciones"]
            conclusion = regla["conclusion"]
            
            # Si se cumplen las condiciones y la conclusión es nueva
            if condiciones.issubset(hechos) and conclusion not in hechos:
                # Añadimos la conclusión a nuestros hechos
                hechos.add(conclusion)
                
                # Guardamos el paso en el historial (traza)
                traza.append({
                    "regla": regla["nombre"],
                    "condiciones_activadas": list(condiciones),
                    "conclusion_generada": conclusion
                })
                
                # Avisamos de que ha habido cambios en esta vuelta
                hay_novedad = True
                
        # Si revisamos todas las reglas y no hay nada nuevo, terminamos
        if not hay_novedad:
            break
            
    # Devolvemos todos los hechos encontrados y el recorrido realizado
    return hechos, traza