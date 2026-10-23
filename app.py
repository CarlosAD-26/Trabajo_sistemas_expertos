"""
Interfaz web hecha con Streamlit.
La aplicación permite probar incidencias de paquetes y consultar la ocupación de una zona.
"""

import streamlit as st
# Esta librería sirven para dibujar las gráficas.
import matplotlib.pyplot as plt

# Importamos la lógica del proyecto
from motor import encadenar_hacia_adelante
from reglas import reglas
from logica_difusa import (
    REJILLA, ocupacion_baja, ocupacion_media, ocupacion_alta,
    metodo_mandani, decidir_desvio
)
from main import NOMBRES_HECHOS, NOMBRES_CONCLUSIONES, obtener_nombre

# Configuramos el título y el icono
st.set_page_config(page_title="Panel de gestión logística", page_icon="📦", layout="wide")

# Con este bloque cambiamos algunos colores y estilos de la página.
st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"] {background-color: #000; color: #fff;}
.main-title {font-size: 2.15rem; font-weight: 700; margin-bottom: .2rem;}
.subtitle {color: #cbd5e1; margin-bottom: 1.3rem;}
div[data-testid="stMetric"] {background: #111827; border: 1px solid #374151; color: #fff; padding: 12px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📦 Panel de gestión logística</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistema de apoyo a la decisión para incidencias y ocupación de zonas.</div>', unsafe_allow_html=True)

# Creamos dos pestañas para separar el contenido principal.
tab_incidencias, tab_ocupacion = st.tabs([
    "📋 Incidencias de paquetes", "📊 Ocupación y desvío"
])

# --------------------- ZONA 1: INCIDENCIAS ---------------------
with tab_incidencias:
    st.header("Evaluación de incidencias")
    st.write("Selecciona las situaciones observadas. El sistema aplicará las reglas y explicará sus conclusiones.")

    # Guardamos varios casos de ejemplo para poder cargarlos con un botón.
    ejemplos = {
        "Caso A — Clasificación normal": ["destino_identificado", "sin_incidencias"],
        "Caso B — Paquete P-104": ["codigo_no_legible", "destino_no_identificado"],
        "Caso C — Dos caminos a revisión": ["codigo_no_legible", "destino_no_identificado", "embalaje_danado", "contenido_fragil"],
        "Caso D — Sin conclusión nueva": ["embalaje_danado"],
        "Caso E — Peso y documentación": ["peso_fuera_rango", "documentacion_incompleta"],
    }

    # Carga de ejemplos ejecutada ANTES de renderizar el formulario
    st.markdown("#### Cargar caso de prueba")
    c_sel, c_btn = st.columns([3, 1])
    with c_sel:
        caso = st.selectbox("Selecciona un escenario predefinido", list(ejemplos.keys()), label_visibility="collapsed")
    with c_btn:
        # Al pulsarlo, marcamos los hechos del ejemplo elegido y actualizamos la página.
        if st.button("Cargar ejemplo", use_container_width=True):
            for hecho in NOMBRES_HECHOS:
                st.session_state["hecho_" + hecho] = hecho in ejemplos[caso]
            st.rerun()

    st.divider()

    # El formulario reúne la referencia del paquete y las incidencias observadas.
    with st.form("formulario_incidencias"):
        st.write("**Incidencias observadas**")
        
        izquierda, derecha = st.columns(2)
        seleccionados = []
        for i, (hecho, nombre) in enumerate(NOMBRES_HECHOS.items()):
            # Repartimos las casillas entre dos columnas para que sea más fácil leerlas.
            col = izquierda if i % 2 == 0 else derecha
            with col:
                # Guardamos si cada casilla está marcada para que Streamlit la recuerde.
                if "hecho_" + hecho not in st.session_state:
                    st.session_state["hecho_" + hecho] = False
                
                marcado = st.checkbox(nombre, key="hecho_" + hecho)
                if marcado:
                    seleccionados.append(hecho)

        analizar = st.form_submit_button("Analizar paquete", type="primary", use_container_width=True)

    if analizar:
        # El conjunto evita repetir hechos y el motor aplica las reglas encadenadas.
        iniciales = set(seleccionados)
        finales, traza = encadenar_hacia_adelante(iniciales, reglas)
        # Guardamos el resultado en la sesión para que siga visible al actualizarse la página.
        st.session_state["resultado_incidencias"] = {
            "iniciales": iniciales,
            "conclusiones": finales - iniciales,
            "traza": traza,
        }

    if "resultado_incidencias" in st.session_state:
        # Recuperamos el análisis anterior y mostramos sus datos.
        resultado = st.session_state["resultado_incidencias"]
        iniciales = resultado["iniciales"]
        conclusiones = resultado["conclusiones"]
        traza = resultado["traza"]

        st.divider()
        st.subheader("Resultado de la evaluación")
        c1, c2, c3 = st.columns(3)
        c1.metric("Hechos iniciales", len(iniciales))
        c2.metric("Conclusiones nuevas", len(conclusiones))
        c3.metric("Reglas aplicadas", len(traza))

        # El mensaje cambia según las conclusiones que haya encontrado el sistema.
        if "enviar_revision" in conclusiones or "retener_temporalmente" in conclusiones:
            st.warning("El sistema recomienda revisar o retener el paquete.")
        elif "autorizar_clasificacion" in conclusiones:
            st.success("El sistema recomienda autorizar la clasificación.")
        elif conclusiones:
            st.info("Se han generado acciones que deben completarse.")
        else:
            st.info("No se ha obtenido ninguna conclusión nueva con las reglas actuales.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Información introducida")
            # Convertimos los códigos internos en nombres más fáciles de entender.
            if iniciales:
                for hecho in sorted(iniciales):
                    st.write("• " + obtener_nombre(hecho))
            else:
                st.write("No se seleccionaron hechos.")
        with col2:
            st.markdown("#### Conclusiones del sistema")
            if conclusiones:
                for hecho in sorted(conclusiones):
                    st.write("✅ " + obtener_nombre(hecho))
            else:
                st.write("Sin conclusiones nuevas.")

        st.markdown("#### Explicación de la decisión")
        if traza:
            # La traza explica paso a paso qué reglas se activaron y qué conclusión salió.
            for numero, paso in enumerate(traza, start=1):
                with st.expander(f"Paso {numero} · {paso['regla']} — {obtener_nombre(paso['conclusion_generada'])}", expanded=(numero == 1)):
                    st.write("**Condiciones cumplidas:**")
                    for condicion in paso["condiciones_activadas"]:
                        st.write("• " + obtener_nombre(condicion))
                    st.write("**Conclusión generada:** " + obtener_nombre(paso["conclusion_generada"]))
        else:
            st.write("No se activó ninguna regla. El sistema no inventa conclusiones.")

        with st.expander("Consultar la base de reglas"):
            # Mostramos las reglas en formato legible, uniendo sus condiciones con "Y".
            for regla in reglas:
                condiciones = " Y ".join(obtener_nombre(h) for h in sorted(regla["condiciones"]))
                st.write(f"**{regla['nombre']}:** {condiciones} → {obtener_nombre(regla['conclusion'])}")

# --------------------- ZONA 2: LÓGICA DIFUSA ---------------------
with tab_ocupacion:
    st.header("Control de ocupación de una zona")
    st.write("Compara la regla rígida del 80 % con el resultado gradual de la inferencia difusa.")

    # El deslizador permite elegir un porcentaje entre 0 y 100.
    ocupacion = st.slider("Ocupación actual de la zona (%)", 0, 100, 75, 1)
    # Calculamos la salida difusa y también la decisión de la regla rígida.
    desvio_final, informacion = metodo_mandani(ocupacion)
    baja, media, alta = informacion["activaciones"]
    decision = decidir_desvio(ocupacion)

    col_datos, col_graficos = st.columns([1, 1.25], gap="large")

    with col_datos:
        c1, c2, c3 = st.columns(3)
        c1.metric("Ocupación actual", f"{ocupacion}%")
        c2.metric("Salida difusa (centroide)", f"{desvio_final:.1f}%")
        c3.metric("Regla rígida (> 80%)", "Desviar" if decision else "No desviar")

        # Indicamos si se ha superado el límite fijo del 80 %.
        if decision:
            st.success("La regla rígida se activa porque la ocupación supera el 80 %.")
        else:
            st.warning("La regla rígida no se activa porque la ocupación es del 80 % o menos.")

        st.markdown("#### Grados de pertenencia y reglas activadas")
        st.caption("Los grados están entre 0 y 1 y no representan el porcentaje final de desvío.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ocupación baja", f"{baja:.2f}")
        c2.metric("Ocupación media", f"{media:.2f}")
        c3.metric("Ocupación alta", f"{alta:.2f}")

        with st.expander("Cómo se calcula el resultado"):
            st.write("1. **Fuzzificación:** se calcula la pertenencia a baja, media y alta.")
            st.write("2. **Implicación:** cada regla recorta su conjunto de salida usando el mínimo.")
            st.write("3. **Agregación:** se combinan las salidas usando el máximo.")
            st.write("4. **Desdifusificación:** se calcula el centroide para obtener un único valor.")
        st.caption("La salida difusa es un resultado matemático, no una probabilidad. La regla rígida y la difusa son criterios distintos.")

    with col_graficos:
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.markdown("#### Funciones de pertenencia (Entrada)")
            # Cada curva representa cuándo consideramos la ocupación baja, media o alta.
            fig1, ax1 = plt.subplots(figsize=(4.5, 3))
            ax1.plot(REJILLA, ocupacion_baja(REJILLA), label="Baja")
            ax1.plot(REJILLA, ocupacion_media(REJILLA), label="Media")
            ax1.plot(REJILLA, ocupacion_alta(REJILLA), label="Alta")

            # Esta línea señala el porcentaje que hemos elegido en el deslizador.
            ax1.axvline(ocupacion, linestyle="--", color="gray", label=f"Ocupación = {ocupacion}%")
            ax1.set_xlabel("Ocupación (%)")
            ax1.set_ylabel("Grado de pertenencia")
            ax1.set_xlim(0, 100)
            ax1.set_ylim(0, 1.05)
            ax1.grid(True, alpha=0.25)
            ax1.legend(loc="upper right")
            fig1.tight_layout()
            st.pyplot(fig1, use_container_width=False)

            # Cerramos la figura para liberar recursos después de mostrarla.
            plt.close(fig1)

        with col_graf2:
            st.markdown("#### Salida agregada y centroide")
            # La zona naranja es la salida combinada; la línea roja marca el resultado final.
            fig2, ax2 = plt.subplots(figsize=(4.5, 3))
            ax2.plot(REJILLA, informacion["mu_agg"], label="Salida agregada", color="orange")
            ax2.fill_between(REJILLA, informacion["mu_agg"], alpha=0.2, color="orange")
            ax2.axvline(desvio_final, linestyle="--", color="red", label=f"Centroide = {desvio_final:.1f}%")
            ax2.set_xlabel("Nivel de desvío (%)")
            ax2.set_ylabel("Grado de pertenencia")
            ax2.set_xlim(0, 100)
            ax2.set_ylim(0, 1.05)
            ax2.grid(True, alpha=0.25)
            ax2.legend(loc="upper right")
            fig2.tight_layout()
            st.pyplot(fig2, use_container_width=False)

            plt.close(fig2)
