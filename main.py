import streamlit as st
import pandas as pd
import math

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="YAXAL ENGINEERING AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado ligero para headers
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
st.sidebar.caption("PMO & Engineering Assistant v1.1")

# MENÚ DE NAVEGACIÓN ACTUALIZADO (OPCIÓN B)
menu_opcion = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "📊 Dashboard PMO",
        "💧 Ingeniería Hidráulica & PTAR",
        "☀️ Energía Solar & Bombeo",  # NUEVO
        "👨‍🏭 Soldadura & Metalmecánica", # NUEVO
        "📝 Gestión de Minutas e IA"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Estado:** Fase Gratuita")

# ---------------------------------------------------------
# MÓDULO 1: DASHBOARD PMO (Mantenido)
# ---------------------------------------------------------
if menu_opcion == "📊 Dashboard PMO":
    st.markdown('<p class="main-header">Control de Proyectos - PMO Yaxal</p>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Proyectos Activos", "5")
    col2.metric("Propuestas en Cotización", "8")
    col3.metric("Unidades PTAR/Solar", "3")
    col4.metric("Compromisos Pendientes", "12")

    st.subheader("Estado de Proyectos en Ejecución (Simulación)")
    df_proyectos = pd.DataFrame({
        "ID Proyecto": ["YAX-001", "YAX-002", "YAX-003"],
        "Cliente": ["Residencial Campestre", "Industrial Park QRO", "Campo Agrícola"],
        "Unidad": ["Ósmosis Residencial", "PTAR Industrial", "Bombeo Solar"],
        "Estado": ["En Diseño", "Instalación", "Cotización"]
    })
    st.dataframe(df_proyectos, use_container_width=True)

# ---------------------------------------------------------
# MÓDULO 2: INGENIERÍA HIDRÁULICA & PTAR (Mantenido)
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
        # Fórmulas
        q_lps = q_gpm * 0.0630902
        diam_m = diamb_pulg * 0.0254
        hf_m = 10.67 * (longitud_m) * ((q_lps / 1000)**1.852) / ((coef_c**1.852) * (diam_m**4.87))
        
        st.metric("Pérdida por Fricción (hf)", f"{hf_m:.2f} m")
        st.caption(f"Caudal equivalente: {q_lps:.2f} L/s")

# ---------------------------------------------------------
# MÓDULO 3: ENERGÍA SOLAR & BOMBEO (COMPLETO E INTEGRAL)
# ---------------------------------------------------------
elif menu_opcion == "☀️ Energía Solar & Bombeo":
    st.markdown('<p class="main-header">☀️ Ingeniería Fotovoltaica & Dimensionamiento Solar</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Cálculo integral de demanda energética, área requerida, peso, cableado y recomendaciones técnicas.</p>', unsafe_allow_html=True)
    st.markdown("---")

    tab_solar1, tab_solar2 = st.tabs(["📐 Proyecto Solar Integral (Interconectado)", "💧 Bombeo Solar Directo"])

    with tab_solar1:
        st.subheader("1. Parámetros del Proyecto y Consumo")
        
        c_in1, c_in2, c_in3 = st.columns(3)
        with c_in1:
            consumo_bimestral_kwh = st.number_input("Consumo Bimestral CFE (kWh):", min_value=50, value=1200, step=50)
            tipo_tarifa = st.selectbox("Tarifa CFE:", ["PDBT (Baja Tensión)", "GDBT (Gran Demanda Baja Tensión)", "DAC (Doméstica Alto Consumo)"])
        with c_in2:
            hsp_localidad = st.slider("Horas Sol Pico (HSP) promedio diarias:", 3.5, 7.0, 5.5, help="Ej: Mérida/Yucatán = 5.6, Querétaro = 5.4, CDMX = 5.0")
            porcentaje_cobertura = st.slider("Porcentaje de consumo a mitigar (%):", 50, 100, 95)
        with c_in3:
            potencia_modulo_w = st.selectbox("Potencia de Panel Comercial (Wp):", [450, 550, 580, 670], index=1)
            eficiencia_modulo = st.number_input("Eficiencia del panel (%):", value=21.3)

        st.markdown("---")
        st.subheader("2. Resultados del Dimensionamiento Energético y Físico")

        # --- CÁLCULOS MATEMÁTICOS DE INGENIERÍA ---
        # 1. Demanda Energética
        consumo_diario_promedio = (consumo_bimestral_kwh / 60) * (porcentaje_cobertura / 100) # kWh/día
        factor_perdidas_sistema = 0.80 # 20% pérdidas (temperatura, cableado, ineficiencia del inversor, suciedad)
        potencia_dc_requerida_kw = consumo_diario_promedio / (hsp_localidad * factor_perdidas_sistema)
        
        # 2. Número de Módulos
        num_paneles_exacto = (potencia_dc_requerida_kw * 1000) / potencia_modulo_w
        num_paneles_comercial = math.ceil(num_paneles_exacto)
        potencia_instalada_real_kw = (num_paneles_comercial * potencia_modulo_w) / 1000
        
        # 3. Área y Peso Físico Requerido
        # Un panel promedio de 550W mide approx 2.27m x 1.13m = 2.56 m² y pesa approx 27.5 kg
        area_por_panel_m2 = (potencia_modulo_w / 1000) / (eficiencia_modulo / 100) # Cálculo real por eficiencia
        area_total_requerida_m2 = num_paneles_comercial * area_por_panel_m2 * 1.25 # 25% extra para pasillos de mantenimiento y sombras
        peso_por_panel_kg = 28.0 # Panel + Estructura de aluminio aproximado
        peso_total_estructura_kg = num_paneles_comercial * peso_por_panel_kg

        # 4. Dimensionamiento Eléctrico (Inversor y Cableado)
        potencia_inversor_kw = math.ceil(potencia_instalada_real_kw * 0.90) # Inversor dimensionado a relación 1.1 DC/AC
        amperaje_ac_220v = (potencia_inversor_kw * 1000) / (220 * 1.732 * 0.9) # Trifásico / Bifásico 220V
        calibre_cable_sugerido = "Calibre 10 AWG (THHN/THWN)" if amperaje_ac_220v < 30 else "Calibre 8 AWG" if amperaje_ac_220v < 45 else "Calibre 6 AWG o mayor"
        
        # --- DESPLIEGUE DE RESULTADOS ---
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        col_res1.metric("Demanda Diaria Requerida", f"{consumo_diario_promedio:.2f} kWh/día")
        col_res2.metric("Potencia Total Instalada", f"{potencia_instalada_real_kw:.2f} kWp")
        col_res3.metric("Módulos Solares (Paneles)", f"{num_paneles_comercial} unidades", f"Módulos de {potencia_modulo_w}W")
        col_res4.metric("Inversor Recomendado", f"{potencia_inversor_kw:.1f} kW AC")

        st.markdown("### 🏢 Análisis de Espacio y Carga en Techo")
        col_esp1, col_esp2, col_esp3 = st.columns(3)
        col_esp1.metric("Área Mínima de Techo/Terreno", f"{area_total_requerida_m2:.1f} m²", "Incluye pasillos de sombra")
        col_esp2.metric("Peso Estimado sobre Losa", f"{peso_total_estructura_kg:.1f} kg", f"~{(peso_total_estructura_kg/area_total_requerida_m2):.1f} kg/m²")
        col_esp3.metric("Generación Mensual Estimada", f"{(potencia_instalada_real_kw * hsp_localidad * 30 * factor_perdidas_sistema):.0f} kWh/mes")

        st.markdown("### ⚡ Recomendaciones Técnicas e Inclinación")
        st.info(f"""
        * **Orientación Recomendada:** Orientar los paneles exactamente hacia el **SUR** (Azimut 180°).
        * **Ángulo de Inclinación Óptimo:** Para el sur de México (ej. Yucatán) se recomienda **15° a 20°**. Para el centro/norte entre **20° y 30°**.
        * **Protecciones Eléctricas:** Interruptor termomagnético en AC de **{math.ceil(amperaje_ac_220v * 1.25)} Amperios**.
        * **Cableado Sugerido (Salida AC):** {calibre_cable_sugerido}.
        * **Cableado Fotovoltaico (DC):** Cable Solar 4mm² (12 AWG) o 6mm² (10 AWG) con protección UV e conectores MC4.
        """)

    with tab_solar2:
        st.subheader("2. Dimensionamiento de Bombeo Solar Directo (Agua)")
        st.write("Calcula la arreglo fotovoltaico directo para operar bombas de agua en plantas PTAR o pozos sin red eléctrica.")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            hp_bomba = st.number_input("Potencia de la Bomba (HP):", value=3.0, step=0.5)
            voltaje_bomba = st.selectbox("Tipo de Motor / Alimentación:", ["220V Trifásico", "220V Monofásico", "440V Trifásico"])
        
        with col_b2:
            watts_motor = hp_bomba * 746
            watts_array_dc = (watts_motor / 0.85) * 1.35 # 35% de sobredimensionamiento para picos de arranque y radiación baja
            num_paneles_bomba = math.ceil(watts_array_dc / 550)
            
            st.metric("Potencia DC Fotovoltaica Total", f"{(watts_array_dc/1000):.2f} kWp")
            st.success(f"**Paneles Solares Requeridos:** {num_paneles_bomba} paneles de 550W")
            st.caption("Requiere un Variador de Frecuencia (VFD) Solar o Controlador de Bombeo MPPT.")
# ---------------------------------------------------------
# MÓDULO 4: SOLDADURA & METALMECÁNICA (NUEVO)
# ---------------------------------------------------------
elif menu_opcion == "👨‍🏭 Soldadura & Metalmecánica":
    st.markdown('<p class="main-header">👨‍🏭 Cálculos de Soldadura y Materiales</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Estimador de consumo de electrodos y pesos de acero.</p>', unsafe_allow_html=True)
    st.markdown("---")

    tab_w1, tab_w2 = st.tabs(["Consumo de Soldadura", "Peso de Materiales"])

    with tab_w1:
        st.subheader("Estimador de Kilos de Electrodo (SMAW / Filete 1g/2g)")
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            tipo_filete_pulg = st.selectbox("Tamaño del Filete de Soldadura (Pierna - Pulgadas):", ["1/8\"", "3/16\"", "1/4\"", "5/16\"", "3/8\"", "1/2\""])
            longitud_soldadura_m = st.number_input("Longitud total del cordón a soldar (m):", min_value=0.1, value=10.0, step=1.0)
            
            # Factores de peso aproximado de metal depositado por metro lineal (kg/m) para filete estándar
            # Asumiendo refuerzo ligero y eficiencia de electrodo E7018 (aprox 65-70%)
            tabla_pesos_filete = {
                "1/8\"": 0.08,   "3/16\"": 0.18,  "1/4\"": 0.32,
                "5/16\"": 0.50,  "3/8\"": 0.72,   "1/2\"": 1.28
            }
            
        with col_w2:
            # Peso de metal depositado puro
            peso_depositado_kg = tabla_pesos_filete[tipo_filete_pulg] * longitud_soldadura_m
            
            # Eficiencia de electrodo revestido (SMAW) - Incluye colillas y escoria (aprox 65%)
            eficiencia_smaw = 0.65
            
            # Kilos de electrodo a comprar
            peso_electrodo_requerido = peso_depositado_kg / eficiencia_smaw
            
            st.metric("Metal Depositado Puro", f"{peso_depositado_kg:.2f} kg")
            st.success(f"**Kilos de Electrodo E7018 a Comprar:** {peso_electrodo_requerido:.1f} kg")
            st.caption("Nota: Cálculo estimado para filete de una pasada sin desperdicio excesivo.")

    with tab_w2:
        st.subheader("Peso de Placa de Acero A36")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            largo_m = st.number_input("Largo de Placa (m):", value=2.44)
            ancho_m = st.number_input("Ancho de Placa (m):", value=1.22)
            espesor_mm = st.number_input("Espesor de Placa (mm):", value=6.35, help="1/4\" = 6.35mm, 1/2\" = 12.7mm")
        
        with col_p2:
            # Densidad del acero = 7850 kg/m3
            volumen_m3 = largo_m * ancho_m * (espesor_mm / 1000)
            peso_placa_kg = volumen_m3 * 7850
            
            st.metric("Peso Total de la Placa", f"{peso_placa_kg:.2f} kg")

# ---------------------------------------------------------
# MÓDULO 5: GESTIÓN DE MINUTAS (Mantenido)
# ---------------------------------------------------------
elif menu_opcion == "📝 Gestión de Minutas e IA":
    st.markdown('<p class="main-header">Transcripción de Reuniones y Compromisos</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.text_area("Pega aquí las notas transcritas de obra o reunión:")
    if st.button("Extraer Compromisos (IA)"):
        st.info("Función lista para conectar con IA en Colab.")
