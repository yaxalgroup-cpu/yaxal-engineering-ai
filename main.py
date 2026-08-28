import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="YAXAL ENGINEERING AI", page_icon="⚙️", layout="wide")

st.sidebar.title("YAXAL AI Engine")
st.sidebar.caption("PMO & Engineering Assistant v1.0")

menu_opcion = st.sidebar.radio(
    "Selecciona un Módulo:",
    ["📊 Dashboard PMO", "💧 Ingeniería Hidráulica", "⚙️ Metalmecánica & Estructuras", "📝 Gestión de Minutas e IA"]
)

if menu_opcion == "📊 Dashboard PMO":
    st.title("Control de Proyectos - PMO Yaxal")
    col1, col2, col3 = st.columns(3)
    col1.metric("Proyectos Activos", "5")
    col2.metric("Propuestas en Cotización", "8")
    col3.metric("PTAR / Ósmosis", "3")
    
    st.subheader("Listado de Proyectos")
    df_proyectos = pd.DataFrame({
        "ID Proyecto": ["YAX-001", "YAX-002"],
        "Cliente": ["Residencial Campestre", "Industrial Park"],
        "Estado": ["En Diseño", "En Instalación"]
    })
    st.dataframe(df_proyectos, use_container_width=True)

elif menu_opcion == "💧 Ingeniería Hidráulica":
    st.title("Cálculo Hidráulico - Hazen-Williams")
    q_gpm = st.number_input("Caudal (GPM):", value=50.0)
    longitud_m = st.number_input("Longitud de Tubería (m):", value=100.0)
    diamb_pulg = st.number_input("Diámetro Interno (Pulgadas):", value=2.0)
    coef_c = st.selectbox("Coeficiente C:", [150, 140, 120])
    
    q_lps = q_gpm * 0.0630902
    diam_m = diamb_pulg * 0.0254
    hf_m = 10.67 * (longitud_m) * ((q_lps / 1000)**1.852) / ((coef_c**1.852) * (diam_m**4.87))
    st.metric("Pérdida por Fricción Estimada (m)", f"{hf_m:.2f} m")

elif menu_opcion == "⚙️ Metalmecánica & Estructuras":
    st.title("Estimador de Peso de Placa de Acero")
    largo = st.number_input("Largo (m):", value=2.44)
    ancho = st.number_input("Ancho (m):", value=1.22)
    espesor = st.number_input("Espesor (mm):", value=6.35)
    peso = (largo * ancho * (espesor / 1000)) * 7850
    st.success(f"Peso Estimado: {peso:.2f} kg")

elif menu_opcion == "📝 Gestión de Minutas e IA":
    st.title("Notas y Compromisos de Obra")
    st.text_area("Pega aquí las notas de la reunión o levantamiento:")
    if st.button("Extraer Tareas"):
        st.info("Función lista para vincular con IA en el siguiente paso.")
