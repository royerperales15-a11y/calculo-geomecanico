import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de página para móvil
st.set_page_config(page_title="GeoMinería Pro", layout="centered")

st.title("⚒️ Geomecánica: Diseño de Sostenimiento")
st.markdown("---")

# --- ENTRADA DE DATOS (Organizada en columnas para móvil) ---
st.subheader("📋 Parámetros de Terreno")
col1, col2 = st.columns(2)

with col1:
    s1 = st.number_input("σ1 (MPa)", value=32.0, help="Tensión principal mayor")
    s2 = st.number_input("σ2 (MPa)", value=16.0, help="Tensión principal menor")
    sci = st.number_input("σci (MPa)", value=110.0, help="Resistencia roca intacta")

with col2:
    gr = st.number_input("γr (KN/m³)", value=27.0, help="Peso específico roca")
    base = st.number_input("Ancho Galería (m)", value=4.0)
    alt = st.number_input("Altura Galería (m)", value=4.0)

# --- LÓGICA DE CÁLCULO (Según imágenes 2 y 4) ---
# Tensión máxima (Ec. 18)
sigma_max = 3 * s1 - s2 #

# Radio equivalente 'a'
r = base / 2
area_galeria = (np.pi * r**2 / 2) + (base * (alt / 2))
a_radio = np.sqrt(area_galeria / np.pi) #

# Radio de zona plástica 'Rf' (Ec. 17)
rf = a_radio * (0.49 + 1.25 * (sigma_max / sci)) #

# Resultados de diseño
sexc = rf - a_radio #
p_ton = (gr * base * sexc * 1.0) / 10 #
lp = sexc + 1.0 # Longitud mínima del perno

# --- VISUALIZACIÓN DE RESULTADOS ---
st.markdown("---")
st.subheader("📊 Resultados de Diseño")

# Tarjetas de métricas
m1, m2, m3 = st.columns(3)
m1.metric("Sexc", f"{sexc:.2f} m")
m2.metric("Peso P", f"{p_ton:.1f} t")
m3.metric("Lp (Perno)", f"{lp:.2f} m")

# Gráfico de la sección
st.subheader("📐 Sección Transversal")
fig, ax = plt.subplots(figsize=(6, 5))
# Galería
rect = plt.Rectangle((-base/2, 0), base, alt/2, color='red', fill=False, lw=3, label='Galería')
ax.add_patch(rect)
t = np.linspace(0, np.pi, 100)
ax.plot(r*np.cos(t), (alt/2) + r*np.sin(t), color='red', lw=3)

# Zonas de influencia
c_rf = plt.Circle((0, alt/2), rf, color='green', fill=False, ls='--', lw=2, label=f'Rf = {rf:.2f}m')
ax.add_artist(c_rf)

ax.set_aspect('equal')
ax.set_xlim(-rf-1, rf+1)
ax.set_ylim(-0.5, alt+2)
ax.legend()
st.pyplot(fig)
