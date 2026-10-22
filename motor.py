def encadenar_hacia_adelante(hechos_iniciales, reglas):
   
    hechos = set(hechos_iniciales)
    
    traza = []
    
    while True:
        hay_novedad = False
        
        for regla in reglas:
            condiciones = regla["condiciones"]
            conclusion = regla["conclusion"]
            
            if condiciones.issubset(hechos) and conclusion not in hechos:
                hechos.add(conclusion)
                
                traza.append({
                    "regla": regla["nombre"],
                    "condiciones_activadas": list(condiciones),
                    "conclusion_generada": conclusion
                })
                
                hay_novedad = True
                
        if not hay_novedad:
            break
            
    return hechos, traza

