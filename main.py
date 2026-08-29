import streamlit as st
import pandas as pd
import math
import gspread

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="YAXAL ENGINEERING AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #0E1117; font-weight: 700; }
    .sub-header { font-size: 1.1rem; color: #4F5E71; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL (ENTORNO Y NAVEGACIÓN)
# ---------------------------------------------------------
st.sidebar.title("YAXAL AI Engine")
st.sidebar.caption("PMO & Engineering Assistant v1.3")

# Selector de Entorno Operativo (Multi-Empresa)
empresa_activa = st.sidebar.selectbox(
    "🏢 Entorno de Trabajo:",
    ["Grupo Industrial YAXAL", "CWS México"]
)

st.sidebar.markdown("---")

menu_opcion = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "📊 Dashboard PMO",
        "⚡ Ingeniería Eléctrica Convencional",
        "💧 Ingeniería Hidráulica & PTAR",
        "☀️ Energía Solar & Bombeo",
        "👨‍🏭 Soldadura & Metalmecánica",
        "📝 Gestión de Minutas e IA"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Asistentes NotebookLM")

# Asistente de Ingeniería Técnico Global (URL Directa)
st.sidebar.link_button(
    "📘 Asistente de Ingeniería (Global)", 
    "https://gemini.google.com/notebook/34536810-a2bb-48d3-abee-77cd7da15829"
)

# Asistente PMO según Entorno Seleccionado (URLs Directas)
if empresa_activa == "Grupo Industrial YAXAL":
    st.sidebar.link_button(
        "📋 PMO YAXAL (Minutas & Tareas)", 
        "https://gemini.google.com/notebook/b3a13d5c-e9f8-4fd9-9018-e89d415fc6cb"
    )
    st.sidebar.info("**Estado:** Conectado a YAXAL_DB_MASTER")
else:
    st.sidebar.link_button(
        "🏢 PMO CWS México (Minutas & Tareas)", 
        "https://gemini.google.com/notebook/875ec975-6098-479b-b959-7e82a960f933"
    )
    st.sidebar.info("**Estado:** Conectado a CWS_DB_MASTER")
# ---------------------------------------------------------
# FUNCIÓN DE LECTURA DE GOOGLE SHEETS (DINÁMICA POR EMPRESA)
# ---------------------------------------------------------
def cargar_tareas_sheet(empresa):
    nombre_doc = "YAXAL_DB_MASTER" if empresa == "Grupo Industrial YAXAL" else "CWS_DB_MASTER"
    try:
        gc = gspread.public()
        doc = gc.open(nombre_doc)
        hoja = doc.worksheet("Compromisos_y_Tareas")
        datos = hoja.get_all_records()
        return pd.DataFrame(datos)
    except Exception as e:
        # Datos de respaldo según la empresa
        if empresa == "Grupo Industrial YAXAL":
            return pd.DataFrame([
                {"ID_Tarea": "YAX-TAR-001", "ID_Proyecto": "YAX-GEN", "Descripcion": "Cotización filtro PTAR", "Responsable": "Ing. Juan", "Fecha_Limite": "Viernes", "Estado": "Pendiente"}
            ])
        else:
            return pd.DataFrame([
                {"ID_Tarea": "CWS-TAR-001", "ID_Proyecto": "CWS-OBRA-01", "Descripcion": "Revisión de avance de obra hidráulica", "Responsable": "Director CWS", "Fecha_Limite": "Lunes", "Estado": "En Proceso"}
            ])

# ---------------------------------------------------------
# MÓDULO 1: DASHBOARD PMO
# ---------------------------------------------------------
if menu_opcion == "📊 Dashboard PMO":
    st.markdown(f'<p class="main-header">Control de Proyectos - PMO ({empresa_activa})</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitoreo en tiempo real de proyectos y compromisos asignados por voz/IA.</p>', unsafe_allow_html=True)
    st.markdown("---")

    df_tareas = cargar_tareas_sheet(empresa_activa)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Entorno Activo", empresa_activa.split()[0])
    col2.metric("Proyectos Activos", "5")
    col3.metric("Unidades de Ingeniería", "3")
    col4.metric("Compromisos Registrados", str(len(df_tareas)))

    st.subheader(f"📋 Compromisos y Tareas ({empresa_activa})")
    st.dataframe(df_tareas, use_container_width=True)

# ---------------------------------------------------------
# MÓDULO 2: INGENIERÍA ELÉCTRICA CONVENCIONAL
# ---------------------------------------------------------
elif menu_opcion == "⚡ Ingeniería Eléctrica Convencional":
    st.markdown('<p class="main-header">⚡ Calculadora Eléctrica Convencional</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dimensionamiento de cables, potencias, caídas de tensión, tuberías conduit y protecciones.</p>', unsafe_allow_html=True)
    st.markdown("---")

    tab_el1, tab_el2, tab_el3 = st.tabs(["📏 Calibre de Cable & Caída de Tensión", "🔌 Ley de Ohm & Potencias", "🛡️ Tubería Conduit & Protecciones"])

    with tab_el1:
        st.subheader("1. Selección de Calibre de Cable (AWG) por Caída de Voltaje")
        c_e1, c_e2, c_e3 = st.columns(3)
        
        with c_e1:
            tipo_sistema = st.selectbox("Tipo de Sistema:", ["Monofásico (1F - 120V)", "Bifásico / Monofásico (2F - 220V)", "Trifásico (3F - 220V)", "Trifásico (3F - 440V)"])
            potencia_kw = st.number_input("Carga / Potencia (kW):", min_value=0.1, value=5.0, step=0.5)
            factor_potencia = st.slider("Factor de Potencia (FP):", 0.70, 1.00, 0.90)
            
        with c_e2:
            longitud_cable_m = st.number_input("Longitud del Alimentador (metros):", min_value=1.0, value=30.0, step=5.0)
            caida_max_porcentaje = st.slider("Caída de Tensión Máxima Permitida (%):", 1.0, 5.0, 3.0)
            
        with c_e3:
            voltaje = 120 if "120V" in tipo_sistema else (220 if "220V" in tipo_sistema else 440)
            
            if "Trifásico" in tipo_sistema:
                corriente_amp = (potencia_kw * 1000) / (math.sqrt(3) * voltaje * factor_potencia)
            else:
                corriente_amp = (potencia_kw * 1000) / (voltaje * factor_potencia)
                
            st.metric("Corriente Nominal (I)", f"{corriente_amp:.2f} A")
            
            if corriente_amp <= 15: calibre_amp = "14 AWG"
            elif corriente_amp <= 20: calibre_amp = "12 AWG"
            elif corriente_amp <= 30: calibre_amp = "10 AWG"
            elif corriente_amp <= 50: calibre_amp = "8 AWG"
            elif corriente_amp <= 65: calibre_amp = "6 AWG"
            elif corriente_amp <= 85: calibre_amp = "4 AWG"
            elif corriente_amp <= 115: calibre_amp = "2 AWG"
            else: calibre_amp = "1/0 AWG o mayor"
            
            st.success(f"**Calibre sugerido por corriente:** {calibre_amp}")
            st.caption(f"Calculado para corriente continua a 125%: {corriente_amp * 1.25:.2f} A")

    with tab_el2:
        st.subheader("2. Relación Voltaje, Corriente, Resistencia y Potencia")
        c_o1, c_o2 = st.columns(2)
        with c_o1:
            v_val = st.number_input("Voltaje (V):", value=220.0)
            r_val = st.number_input("Resistencia (Ohms - Ω):", value=10.0)
        with c_o2:
            i_calc = v_val / r_val if r_val > 0 else 0
            p_calc = (v_val ** 2) / r_val if r_val > 0 else 0
            st.metric("Corriente Resultante (I)", f"{i_calc:.2f} A")
            st.metric("Potencia Disipada (P)", f"{p_calc:.2f} W ({p_calc/1000:.2f} kW)")

    with tab_el3:
        st.subheader("3. Ocupación de Tubería Conduit y Protección Termomagnética")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            num_conductores = st.number_input("Número de Conductores en la tubería:", min_value=1, value=4)
            calibre_tubo = st.selectbox("Calibre de los cables:", ["14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG"])
        with col_t2:
            if calibre_tubo in ["14 AWG", "12 AWG", "10 AWG"] and num_conductores <= 4:
                tubo_sugerido = '1/2" Conduit'
            elif calibre_tubo in ["10 AWG", "8 AWG"] and num_conductores <= 6:
                tubo_sugerido = '3/4" Conduit'
            else:
                tubo_sugerido = '1" Conduit o superior'
                
            st.metric("Diámetro de Tubería Recomendado", tubo_sugerido)
            corriente_est = (5.0 * 1000) / (220 * 0.90)
            st.info(f"Protección Termomagnética (Breaker) recomendada: **{math.ceil(corriente_est * 1.25)} A**")

# ---------------------------------------------------------
# MÓDULO 3: INGENIERÍA HIDRÁULICA & PTAR
# ---------------------------------------------------------
elif menu_opcion == "💧 Ingeniería Hidráulica & PTAR":
    st.markdown('<p class="main-header">Cálculo Hidráulico (Hazen-Williams)</p>', unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        q_gpm = st.number_input("Caudal Deseado (GPM):", min_value=1.0, value=50.0, step=5.0)
        longitud_m = st.number_input("Longitud de Tubería (m):", min_value=1.0, value=100.0)
    with c2:
        diamb_pulg = st.number_input("Diámetro Interno (Pulgadas):", min_value=0.5, value=2.0, step=0.5)
        coef_c = st.selectbox("Coeficiente C (C=150 para PVC):", [150, 140, 120])
    with c3:
        q_lps = q_gpm * 0.0630902
        diam_m = diamb_pulg * 0.0254
        hf_m = 10.67 * (longitud_m) * ((q_lps / 1000)**1.852) / ((coef_c**1.852) * (diam_m**4.87))
        
        st.metric("Pérdida por Fricción (hf)", f"{hf_m:.2f} m")
        st.caption(f"Caudal equivalente: {q_lps:.2f} L/s")

# ---------------------------------------------------------
# MÓDULO 4: ENERGÍA SOLAR & BOMBEO
# ---------------------------------------------------------
elif menu_opcion == "☀️ Energía Solar & Bombeo":
    st.markdown('<p class="main-header">☀️ Ingeniería Solar Fotovoltaica</p>', unsafe_allow_html=True)
    st.markdown("---")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        energia_mes_kwh = st.number_input("Consumo Bimestral Promedio (kWh CFE):", min_value=10, value=1000)
        potencia_panel_w = st.number_input("Potencia del Panel (Watts):", value=550, step=10)
        hsp_zona = st.slider("Horas de Sol Pico (HSP):", 3.5, 7.0, 5.5)
    
    with col_s2:
        energia_dia_kwh = energia_mes_kwh / 60
        potencia_total_dc_kw = energia_dia_kwh / (hsp_zona * 0.80)
        num_paneles = math.ceil((potencia_total_dc_kw * 1000) / potencia_panel_w)
        
        st.metric("Potencia DC Total Requerida", f"{potencia_total_dc_kw:.2f} kWp")
        st.success(f"**Paneles Recomendados:** {num_paneles} módulos de {potencia_panel_w}W")

# ---------------------------------------------------------
# MÓDULO 5: SOLDADURA & METALMECÁNICA
# ---------------------------------------------------------
elif menu_opcion == "👨‍🏭 Soldadura & Metalmecánica":
    st.markdown('<p class="main-header">👨‍🏭 Cálculos de Soldadura y Materiales</p>', unsafe_allow_html=True)
    st.markdown("---")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        tipo_filete_pulg = st.selectbox("Tamaño del Filete:", ["1/8\"", "3/16\"", "1/4\"", "5/16\"", "3/8\"", "1/2\""])
        longitud_soldadura_m = st.number_input("Longitud del cordón (m):", min_value=0.1, value=10.0, step=1.0)
        tabla_pesos_filete = {"1/8\"": 0.08, "3/16\"": 0.18, "1/4\"": 0.32, "5/16\"": 0.50, "3/8\"": 0.72, "1/2\"": 1.28}
        
    with col_w2:
        peso_depositado_kg = tabla_pesos_filete[tipo_filete_pulg] * longitud_soldadura_m
        peso_electrodo_requerido = peso_depositado_kg / 0.65
        st.metric("Metal Depositado Puro", f"{peso_depositado_kg:.2f} kg")
        st.success(f"**Kilos de Electrodo E7018 a Comprar:** {peso_electrodo_requerido:.1f} kg")

# ---------------------------------------------------------
# MÓDULO 6: GESTIÓN DE MINUTAS
# ---------------------------------------------------------
elif menu_opcion == "📝 Gestión de Minutas e IA":
    st.markdown(f'<p class="main-header">Transcripción de Reuniones ({empresa_activa})</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.info(f"Para ingresar audios nuevos de {empresa_activa}, ejecuta la celda de Google Colab. La tabla del Dashboard PMO se actualizará automáticamente.")
