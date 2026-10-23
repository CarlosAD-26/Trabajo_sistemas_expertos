reglas = [
    {
        "nombre": "R1",
        "condiciones": {"codigo_no_legible"},
        "conclusion": "solicitar_lectura_manual"
    },
    {
        "nombre": "R2",
        "condiciones": {
            "solicitar_lectura_manual",
            "destino_no_identificado"
        },
        "conclusion": "enviar_revision"
    },
    {
        "nombre": "R3",
        "condiciones": {
            "embalaje_danado",
            "contenido_fragil"
        },
        "conclusion": "enviar_revision"
    },
    {
        "nombre": "R4",
        "condiciones": {"peso_fuera_rango"},
        "conclusion": "comprobar_peso"
    },
    {
        "nombre": "R5",
        "condiciones": {
            "comprobar_peso",
            "documentacion_incompleta"
        },
        "conclusion": "retener_temporalmente"
    },
    {
        "nombre": "R6",
        "condiciones": {
            "destino_identificado",
            "sin_incidencias"
        },
        "conclusion": "autorizar_clasificacion"
    },
    {
        "nombre": "R7",
        "condiciones": {
            "documentacion_incompleta",
            "destino_no_identificado"
        },
        "conclusion": "retener_temporalmente"
    }
]