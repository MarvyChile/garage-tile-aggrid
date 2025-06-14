import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Garage Tile Designer – Clickable Grid Final")

# 1. Unidad y cálculo de medidas
unidad = st.selectbox("Selecciona unidad", ["metros", "centímetros"])
factor = 1 if unidad == "metros" else 0.01
min_val = 1.0 if unidad == "metros" else 10.0
ancho_input = st.number_input(f"Ancho ({unidad})", min_value=min_val, value=4.0 if unidad == "metros" else 400.0, step=1.0)
largo_input = st.number_input(f"Largo ({unidad})", min_value=min_val, value=6.0 if unidad == "metros" else 600.0, step=1.0)
ancho_m, largo_m = ancho_input * factor, largo_input * factor
area_m2 = round(ancho_m * largo_m, 2)
st.markdown(f"**Área:** {area_m2} m²")

# 2. Bordillos y esquineros
incluir_bordillos = st.checkbox("Agregar bordillos", value=True)
incluir_esquineros = st.checkbox("Agregar esquineros", value=True)
pos_bord = st.multiselect(
    "Posiciones bordillo", ["Arriba", "Abajo", "Izquierda", "Derecha"],
    default=["Arriba", "Abajo", "Izquierda", "Derecha"]
)

# 3. Colores disponibles\ ncolores = {
    "Blanco": "#FFFFFF", "Negro": "#000000", "Gris": "#B0B0B0", "Gris Oscuro": "#4F4F4F",
    "Azul": "#0070C0", "Celeste": "#00B0F0", "Amarillo": "#FFFF00", "Verde": "#00B050", "Rojo": "#FF0000"
}
lista_colores = list(colores.keys())

# 4. Inicializar DataFrame
dp = 0.4  # 40 cm
cols_cnt = math.ceil(ancho_m / dp)
rows_cnt = math.ceil(largo_m / dp)
if 'df' not in st.session_state or st.session_state.df.shape != (rows_cnt, cols_cnt):
    st.session_state.df = pd.DataFrame([["Blanco"] * cols_cnt for _ in range(rows_cnt)])
df = st.session_state.df

# 5. Color base\ ncolor_base = st.selectbox("Color base", lista_colores, index=0)
if st.button("Aplicar color base"):
    st.session_state.df.iloc[:, :] = color_base
    df = st.session_state.df

# 6. Cuadrícula clicable
st.subheader("Diseño personalizado: haz clic para pintar")
for r in range(rows_cnt):
    cols_ui = st.columns(cols_cnt)
    for c in range(cols_cnt):
        val = df.iat[r, c]
        hexcol = colores.get(val, "#FFFFFF")
        if cols_ui[c].button("", key=f"cell_{r}_{c}"):
            st.session_state.df.iat[r, c] = color_base
            df = st.session_state.df
        cols_ui[c].markdown(
            f"""
            <div style="width:25px; height:25px; background:{hexcol};
                        border:1px solid {'white' if color_base=='Negro' else 'black'};
                        margin-top:-25px;"></div>
            """,
            unsafe_allow_html=True
        )

# 7. Render gráfico final
fig, ax = plt.subplots(figsize=(cols_cnt/5, rows_cnt/5))
for y in range(rows_cnt):
    for x in range(cols_cnt):
        c = df.iat[y, x]
        ax.add_patch(plt.Rectangle((x, rows_cnt-1-y), 1, 1,
                                   facecolor=colores.get(c, "#FFFFFF"),
                                   edgecolor="white" if color_base=='Negro' else "black"))
# Bordillos\ nif incluir_bordillos:
    if "Arriba" in pos_bord: ax.add_patch(plt.Rectangle((0, rows_cnt), cols_cnt, 0.15, facecolor="black"))
    if "Abajo" in pos_bord: ax.add_patch(plt.Rectangle((0, -0.15), cols_cnt, 0.15, facecolor="black"))
    if "Izquierda" in pos_bord: ax.add_patch(plt.Rectangle((-0.15, 0), 0.15, rows_cnt, facecolor="black"))
    if "Derecha" in pos_bord: ax.add_patch(plt.Rectangle((cols_cnt, 0), 0.15, rows_cnt, facecolor="black"))
# Esquineros
if incluir_esquineros:
    s = 0.15
    for (x, y) in [(0, 0), (0, rows_cnt), (cols_cnt, 0), (cols_cnt, rows_cnt)]:
        ax.add_patch(plt.Rectangle((x-s/2, y-s/2), s, s, facecolor="black"))
ax.set_xlim(-0.5, cols_cnt+0.5); ax.set_ylim(-0.5, rows_cnt+0.5);
ax.set_aspect('equal'); ax.axis('off')
st.pyplot(fig)

# 8. Conteo material
total = rows_cnt * cols_cnt
bord_count = sum([cols_cnt if side in ["Arriba","Abajo"] else rows_cnt for side in pos_bord]) - 2*len(pos_bord)
esq_count = 4 if incluir_esquineros else 0
st.markdown(f"**Total palmetas:** {total}")
st.markdown(f"**Bordillos:** {bord_count}")
st.markdown(f"**Esquineros:** {esq_count}")
st.markdown(f"**Dimensiones:** {cols_cnt} x {rows_cnt}")
