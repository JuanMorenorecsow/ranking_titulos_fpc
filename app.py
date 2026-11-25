import os
import unicodedata
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ranking por Títulos del FPC", page_icon="🏆", layout="centered")

# ---------------------------------------------------------------
# TORNEOS: (nombre, organizador, archivo de imagen en /imagenes)
# ---------------------------------------------------------------
TORNEOS = [
    ("Liga Anual",          "FPC · DIMAYOR", "liga_anual.png", "Temporadas 1948 – 2001"),
    ("Liga Semestral",      "FPC · DIMAYOR", "liga_semestral.png", "Temporadas 2002 – presente"),
    ("Copa Colombia",       "FPC · DIMAYOR", "copa_colombia.png", ""),
    ("Superliga",           "FPC · DIMAYOR", "superliga.png", ""),
    ("Copa Libertadores",   "CONMEBOL",      "libertadores.png", ""),
    ("Copa Sudamericana",   "CONMEBOL",      "sudamericana.png", ""),
    ("Recopa Sudamericana", "CONMEBOL",      "recopa.png", ""),
]
CARPETA_IMG = "imagenes"
NOMBRES = [t[0] for t in TORNEOS]
EXTENSIONES = (".png", ".jpg", ".jpeg", ".webp")


def buscar_imagen(archivo):
    """Busca la imagen sin importar mayúsculas, extensión doble o ubicación de la carpeta."""
    base = archivo.lower()
    for ext in EXTENSIONES:
        if base.endswith(ext):
            base = base[: -len(ext)]

    raiz = Path(__file__).resolve().parent
    # Busca la carpeta "imagenes" (cualquier mayúscula/acento) o, si no existe, usa la raíz
    carpetas = [raiz] + [
        d for d in raiz.iterdir()
        if d.is_dir() and unicodedata.normalize("NFKD", d.name).encode("ascii", "ignore").decode().lower() == "imagenes"
    ]
    for carpeta in carpetas:
        for f in carpeta.iterdir():
            if not f.is_file():
                continue
            nombre = f.name.lower()
            while nombre.endswith(EXTENSIONES):
                for ext in EXTENSIONES:
                    if nombre.endswith(ext):
                        nombre = nombre[: -len(ext)]
                        break
            if nombre == base:
                return str(f)
    return None


# ---------------------------------------------------------------
# DATOS: títulos por equipo, en el mismo orden de TORNEOS.
# ⚠️ Cifras de referencia: verifícalas y corrígelas aquí.
# ---------------------------------------------------------------
DATOS = {
    "Atlético Nacional":      [7, 11, 4, 3, 2, 0, 1],
    "Millonarios":            [14, 3, 1, 1, 0, 0, 0],
    "Independiente Santa Fe": [5, 3, 1, 2, 0, 1, 1],
    "Junior":                 [4, 5, 2, 3, 0, 0, 0],
    "América de Cali":        [13, 3, 0, 0, 0, 0, 0],
    "Deportivo Cali":         [4, 2, 1, 0, 0, 0, 0],
    "Once Caldas":            [0, 3, 0, 0, 1, 0, 0],
    "Independiente Medellín": [2, 3, 0, 1, 0, 0, 0],
    "Deportes Tolima":        [1, 3, 0, 1, 0, 0, 0],
}

# ---------------------------------------------------------------
# ESTILO
# ---------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

#MainMenu, header, footer {visibility: hidden;}
.stApp {
    background: radial-gradient(ellipse at 50% 0%, #0d1b3a 0%, #060b1a 60%, #04070f 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f2f2f2;
}
.block-container {max-width: 680px; padding-top: 2.2rem;}

.eyebrow {text-align:center; color:#c9a43a; letter-spacing:.35em; font-size:.75rem;
          display:flex; align-items:center; justify-content:center; gap:14px;}
.eyebrow::before, .eyebrow::after {content:""; width:48px; height:1px; background:#c9a43a55;}
.titulo {text-align:center; font-family:'Barlow Condensed',sans-serif; font-weight:800;
         font-size:3.4rem; line-height:1.05; text-transform:uppercase; color:#fff; margin:.3rem 0 .2rem;}
.titulo span {background:linear-gradient(180deg,#f3d77a,#b8932f); -webkit-background-clip:text;
              -webkit-text-fill-color:transparent;}
.portada {min-height:62vh; display:flex; flex-direction:column; justify-content:center; padding-top:2rem;}
.portada .titulo {font-size:3.6rem; line-height:1.02; margin:1rem 0;}
.portada .copa {text-align:center; font-size:3.4rem; margin-bottom:.4rem;}
.portada .sub {text-align:center; color:#a9b1c6; font-size:1rem; max-width:460px; margin:.4rem auto 2rem;}
.periodo {text-align:center; color:#f3d77a; font-size:.8rem; letter-spacing:.25em; text-transform:uppercase;
          border:1px solid #c9a43a66; border-radius:999px; padding:6px 18px; width:fit-content;
          margin:-.6rem auto 1.2rem; background:#c9a43a14;}
.linea {width:110px; height:1px; background:#c9a43a88; margin:.4rem auto 1.4rem;}
.progreso {text-align:center; color:#8b93a8; font-size:.8rem; letter-spacing:.2em; margin-bottom:.6rem;}
.instruccion {text-align:center; font-weight:500; margin:1.2rem 0 .6rem;}
.placeholder {height:360px; border-radius:20px; border:1px dashed #c9a43a66; display:flex;
              align-items:center; justify-content:center; color:#8b93a8; text-align:center;
              background:#0a1226; padding:1rem; font-size:.85rem;}

[data-testid="stImage"] img {border-radius:20px; box-shadow:0 10px 40px #00000099;}

/* Input numérico */
[data-testid="stNumberInput"] input {background:#0a1226; color:#fff; border:1px solid #c9a43a66;
    border-radius:10px; text-align:center; height:3rem;}
[data-testid="stNumberInput"] > div {background:transparent;}
[data-testid="stNumberInput"] button {background:#0a1226; color:#c9a43a; border:none;}

/* Botones dorados */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    width:100%; height:3rem; border:none; border-radius:10px; font-weight:700;
    letter-spacing:.18em; color:#1a1405; text-transform:uppercase;
    background:linear-gradient(180deg,#f3d77a,#c9a43a);
    box-shadow:0 4px 20px #c9a43a55;}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    filter:brightness(1.08); color:#1a1405; border:none;}
[data-testid="stForm"] {border:none; padding:0;}

/* Ranking */
.fila {display:flex; align-items:center; gap:16px; padding:14px 18px; margin-bottom:10px;
       background:#0a1226cc; border:1px solid #c9a43a33; border-radius:14px;}
.fila.top {border-color:#c9a43a; box-shadow:0 0 24px #c9a43a33;}
.puesto {font-family:'Barlow Condensed',sans-serif; font-size:2rem; font-weight:800; color:#c9a43a; width:46px;}
.equipo {flex:1; font-weight:700; font-size:1.05rem;}
.tabla-wrap {overflow-x:auto; margin-top:1.6rem; border:1px solid #c9a43a33; border-radius:14px; background:#0a1226cc;}
.tabla-wrap h4 {margin:0; padding:14px 18px 0; font-family:'Barlow Condensed',sans-serif; font-size:1.5rem; color:#f3d77a; letter-spacing:.05em;}
table.detalle {border-collapse:collapse; width:100%; font-size:.9rem; margin-top:.6rem;}
table.detalle th {color:#c9a43a; font-weight:700; text-align:center; padding:10px 12px; border-bottom:1px solid #c9a43a55; white-space:nowrap;}
table.detalle th small {display:block; color:#8b93a8; font-weight:400; letter-spacing:.08em; font-size:.65rem; margin-top:2px;}
table.detalle td {text-align:center; padding:10px 12px; border-bottom:1px solid #ffffff10; white-space:nowrap;}
table.detalle td:first-child, table.detalle th:first-child {text-align:left; font-weight:700; position:sticky; left:0; background:#0a1226;}
table.detalle td.cero {color:#5b6379;}
table.detalle td.total {color:#f3d77a; font-weight:700;}
.pts {font-family:'Barlow Condensed',sans-serif; font-size:1.6rem; font-weight:700; color:#f3d77a;}
.pts small {font-size:.7rem; color:#8b93a8; letter-spacing:.15em;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# ESTADO
# ---------------------------------------------------------------
if "paso" not in st.session_state:
    st.session_state.paso = -1
    st.session_state.pesos = {}


def titulo_html(texto):
    palabras = texto.split()
    if len(palabras) == 1:
        return f"<span>{palabras[0]}</span>"
    return " ".join(palabras[:-1]) + f" <span>{palabras[-1]}</span>"


def encabezado(sub, texto):
    st.markdown(f'<div class="eyebrow">{sub}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="titulo">{titulo_html(texto)}</div><div class="linea"></div>',
                unsafe_allow_html=True)


# ---------------------------------------------------------------
# PREGUNTAS (una copa por pantalla)
# ---------------------------------------------------------------
if st.session_state.paso == -1:
    st.markdown(
        '''<div class="portada">
            <div class="copa">🏆</div>
            <div class="eyebrow">FPC · DIMAYOR</div>
            <div class="titulo">¿Cuál es el orden de los <span>equipos más grandes</span> del FPC?</div>
            <div class="linea"></div>
            <div class="sub">Dale un valor del 1 al 10 a cada copa y descubre el ranking según tu criterio.</div>
        </div>''',
        unsafe_allow_html=True,
    )
    _, centro, _ = st.columns([1, 1.4, 1])
    with centro:
        if st.button("Comenzar", key="comenzar"):
            st.session_state.paso = 0
            st.rerun()

elif st.session_state.paso < len(TORNEOS):
    i = st.session_state.paso
    nombre, organizador, archivo, periodo = TORNEOS[i]

    st.markdown(f'<div class="progreso">{i + 1} / {len(TORNEOS)}</div>', unsafe_allow_html=True)
    encabezado(organizador, nombre)
    if periodo:
        st.markdown(f'<div class="periodo">{periodo}</div>', unsafe_allow_html=True)

    _, centro, _ = st.columns([1, 1.6, 1])
    with centro:
        ruta = buscar_imagen(archivo)
        if ruta:
            st.image(ruta, use_container_width=True)
        else:
            st.markdown(f'<div class="placeholder">Falta la imagen<br>{archivo}</div>',
                        unsafe_allow_html=True)

    st.markdown('<div class="instruccion">Selecciona un número del 1 al 10</div>', unsafe_allow_html=True)

    _, centro, _ = st.columns([1, 3, 1])
    with centro:
        with st.form(key=f"form_{i}", border=False):
            c1, c2 = st.columns([1, 1.4])
            valor = c1.number_input("Valor", min_value=1, max_value=10, value=None, step=1,
                                    placeholder="1–10", label_visibility="collapsed")
            confirmar = c2.form_submit_button("Confirmar")

        if confirmar:
            if valor is None:
                st.warning("Escribe un número del 1 al 10.")
            else:
                st.session_state.pesos[nombre] = int(valor)
                st.session_state.paso += 1
                st.rerun()

        if st.button("← Anterior", key=f"atras_{i}"):
            st.session_state.paso -= 1
            st.rerun()

# ---------------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------------
else:
    encabezado("FPC", "Ranking por Títulos")

    df = pd.DataFrame(DATOS, index=NOMBRES).T
    df["Puntos"] = sum(df[t] * p for t, p in st.session_state.pesos.items())
    df = df.sort_values("Puntos", ascending=False).reset_index(names="Equipo")

    for n, f in df.iterrows():
        clase = "fila top" if n < 3 else "fila"
        st.markdown(
            f'<div class="{clase}"><div class="puesto">{n + 1}</div>'
            f'<div class="equipo">{f["Equipo"]}</div>'
            f'<div class="pts">{int(f["Puntos"])} <small>PTS</small></div></div>',
            unsafe_allow_html=True,
        )

    # Tabla de detalle: Títulos (Puntos) por copa
    pesos = st.session_state.pesos
    encabezados = "".join(
        f"<th>{n}<small>TÍTULOS (PUNTOS)</small></th>" for n in NOMBRES
    )
    filas = ""
    for _, f in df.iterrows():
        celdas = ""
        for n in NOMBRES:
            t = int(f[n])
            clase = ' class="cero"' if t == 0 else ""
            celdas += f"<td{clase}>{t} ({t * pesos[n]})</td>"
        total_t = int(sum(f[n] for n in NOMBRES))
        filas += (
            f"<tr><td>{f['Equipo']}</td>{celdas}"
            f"<td class='total'>{total_t} ({int(f['Puntos'])})</td></tr>"
        )
    st.markdown(
        f'''<div class="tabla-wrap"><h4>Detalle por copa</h4>
        <table class="detalle"><thead><tr><th>Equipo</th>{encabezados}
        <th>Total<small>TÍTULOS (PUNTOS)</small></th></tr></thead>
        <tbody>{filas}</tbody></table></div>''',
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Volver a empezar"):
        st.session_state.paso = -1
        st.session_state.pesos = {}
        st.rerun()
