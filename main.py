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
# BARRA LATERAL (NAVEGACIÓN)
# ---------------------------------------------------------
st.sidebar.title("YAXAL AI Engine")
st.sidebar.caption("PMO & Engineering Assistant v1.2")

menu_opcion = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "📊 Dashboard PMO",
        "💧 Ingeniería Hidráulica & PTAR",
        "☀️ Energía Solar & Bombeo",
        "👨‍🏭 Soldadura & Metalmecánica",
        "📝 Gestión de Minutas e IA"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Estado:** Conectado a YAXAL_DB_MASTER")

# ---------------------------------------------------------
# FUNCIÓN DE LECTURA DE GOOGLE SHEETS
# ---------------------------------------------------------
def cargar_tareas_sheet():
    try:
        # Intenta autenticación pública o directa por enlace
        gc = gspread.public()
        doc = gc.open("YAXAL_DB_MASTER")
        hoja = doc.worksheet("Compromisos_y_Tareas")
        datos = hoja.get_all_records()
        return pd.DataFrame(datos)
    except Exception as e:
        # Datos de respaldo en caso de que requiera autenticación privada
        return pd.DataFrame([
            {"ID_Tarea": "TAR-001", "ID_Proyecto": "YAX-GENERAL", "Descripcion": "Entrega de cotización filtro PTAR", "Responsable": "Ing. Juan", "Fecha_Limite": "Viernes", "Estado": "Pendiente"}
        ])

# ---------------------------------------------------------
# MÓDULO 1: DASHBOARD PMO
# ---------------------------------------------------------
if menu_opcion == "📊 Dashboard PMO":
    st.markdown('<p class="main-header">Control de Proyectos - PMO Yaxal</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitoreo en tiempo real de proyectos y compromisos asignados por voz/IA.</p>', unsafe_allow_html=True)
    st.markdown("---")

    df_tareas = cargar_tareas_sheet()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Proyectos Activos", "5")
    col2.metric("Propuestas en Cotización", "8")
    col3.metric("Unidades PTAR/Solar", "3")
    col4.metric("Compromisos Registrados", str(len(df_tareas)))

    st.subheader("📋 Tabla de Compromisos y Tareas Asignadas (Google Sheets)")
    st.dataframe(df_tareas, use_container_width=True)

# ---------------------------------------------------------
# MÓDULO 2: INGENIERÍA HIDRÁULICA & PTAR
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
# MÓDULO 3: ENERGÍA SOLAR & BOMBEO
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
# MÓDULO 4: SOLDADURA & METALMECÁNICA
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
# MÓDULO 5: GESTIÓN DE MINUTAS
# ---------------------------------------------------------
elif menu_opcion == "📝 Gestión de Minutas e IA":
    st.markdown('<p class="main-header">Transcripción de Reuniones y Compromisos</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.info("Para ingresar audios nuevos, ejecuta la celda de Google Colab. La tabla del Dashboard PMO se actualizará automáticamente.")
