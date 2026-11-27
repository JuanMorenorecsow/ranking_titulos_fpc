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
    ("Liga Semestral",      "FPC · DIMAYOR", "liga_semestral.png", "Temporadas 2002 – presente"),
    ("Liga Anual",          "FPC · DIMAYOR", "liga_anual.png", "Temporadas 1948 – 2001"),
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
# Fuente: CampeonesColombianos_Serio.xlsx (Ligas separadas en Anual 1948–2001 y Semestral 2002–).
# ---------------------------------------------------------------
DATOS = {
    "Atlético Nacional":      [11, 7, 8, 4, 2, 0, 1],
    "Millonarios":            [3, 13, 3, 2, 0, 0, 0],
    "Independiente Santa Fe": [4, 6, 2, 5, 0, 1, 0],
    "Junior":                 [8, 4, 2, 2, 0, 0, 0],
    "América de Cali":        [4, 11, 0, 0, 0, 0, 0],
    "Deportivo Cali":         [3, 7, 1, 1, 0, 0, 0],
    "Independiente Medellín": [4, 2, 3, 0, 0, 0, 0],
    "Once Caldas":            [4, 1, 0, 0, 1, 0, 0],
    "Deportes Tolima":        [3, 0, 1, 1, 0, 0, 0],
    "La Equidad":             [1, 0, 1, 0, 0, 0, 0],
    "Boca Juniors de Cali":   [1, 0, 1, 0, 0, 0, 0],
    "Deportivo Pasto":        [1, 0, 0, 0, 0, 0, 0],
    "Deportes Quindío":       [0, 1, 0, 0, 0, 0, 0],
    "Cúcuta Deportivo":       [1, 0, 0, 0, 0, 0, 0],
    "Atlético Bucaramanga":   [1, 0, 0, 0, 0, 0, 0],
    "Unión Magdalena":        [0, 1, 0, 0, 0, 0, 0],
    "Boyacá Chicó":           [1, 0, 0, 0, 0, 0, 0],
    "Deportivo Pereira":      [1, 0, 0, 0, 0, 0, 0],
    "Atlético Huila":         [1, 0, 0, 0, 0, 0, 0],
    "Real Cartagena":         [1, 0, 0, 0, 0, 0, 0],
}


def tabla_datos():
    """Arma la tabla de títulos. Cada equipo necesita exactamente un número por copa de TORNEOS."""
    malas = {e: len(v) for e, v in DATOS.items() if len(v) != len(NOMBRES)}
    if malas:
        st.error(
            f"Cada equipo debe tener {len(NOMBRES)} números (uno por copa, en este orden: "
            f"{', '.join(NOMBRES)}). Revisa estos equipos en DATOS: "
            + ", ".join(f"{e} ({n} números)" for e, n in malas.items())
        )
        st.stop()
    return pd.DataFrame.from_dict(DATOS, orient="index", columns=NOMBRES)

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
.ejemplos {text-align:center; color:#8b93a8; font-size:.8rem; margin:-.2rem 0 .8rem;}
.ejemplos b {color:#f3d77a;}
.ejemplos div {line-height:1.6;}
.ej-titulo {display:block; color:#c9a43a; letter-spacing:.25em; text-transform:uppercase; font-size:.7rem; margin-bottom:.2rem;}
.ej-rango {margin-top:.3rem; font-size:.72rem; color:#6f7790;}
.caja-base {height:3rem; display:flex; align-items:center; justify-content:center; border:1px solid #c9a43a66;
            border-radius:10px; background:#0a1226; color:#f3d77a; font-weight:700;}
/* botones de la fila del formulario: siempre en una sola fila */
[data-testid="stForm"] [data-testid="stHorizontalBlock"] {flex-direction:row !important; flex-wrap:nowrap !important; gap:.6rem;}
[data-testid="stForm"] [data-testid="stColumn"] {min-width:0 !important; flex:1 1 0 !important; width:auto !important;}
[data-testid="stForm"] [data-testid="stColumn"]:first-child button {
    background:transparent; color:#f3d77a; border:1px solid #c9a43a99; box-shadow:none;}
[data-testid="stForm"] button {letter-spacing:.1em; font-size:.8rem; padding:0 .4rem;}
[data-testid="stTextInput"] input {background:#0a1226; color:#fff; border:1px solid #c9a43a66;
    border-radius:10px; text-align:center; height:3rem;}
.stButton, [data-testid="stFormSubmitButton"] {width:100% !important;}
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
.tabla-wrap {overflow-x:auto; margin-top:.5rem; border:1px solid #c9a43a33; border-radius:14px; background:#0a1226cc;}
.tabla-wrap h4 {margin:0; padding:14px 18px 0; font-family:'Barlow Condensed',sans-serif; font-size:1.5rem; color:#f3d77a; letter-spacing:.05em;}
table.detalle {border-collapse:collapse; width:100%; font-size:.9rem; margin-top:.6rem;}
table.detalle th {color:#c9a43a; font-weight:700; text-align:center; padding:10px 12px; border-bottom:1px solid #c9a43a55; white-space:nowrap;}
table.detalle th small {display:block; color:#8b93a8; font-weight:400; letter-spacing:.08em; font-size:.65rem; margin-top:2px;}
table.detalle td {text-align:center; padding:10px 12px; border-bottom:1px solid #ffffff10; white-space:nowrap;}
table.detalle td:first-child, table.detalle th:first-child {text-align:left; font-weight:700; position:sticky; left:0; background:#0a1226;}
table.detalle td.cero {color:#5b6379;}
table.detalle td.total {color:#f3d77a; font-weight:800; font-size:1.15rem; font-family:'Barlow Condensed',sans-serif;}
table.detalle .pos {display:inline-block; width:2rem; color:#c9a43a; font-family:'Barlow Condensed',sans-serif; font-size:1.3rem; font-weight:800;}
table.detalle tr.top td {background:#c9a43a12;}
table.detalle tr.top td:first-child {box-shadow: inset 3px 0 0 #c9a43a;}
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


def fmt(x):
    """Número con coma decimal y sin ceros sobrantes: 2.5 -> '2,5', 3.0 -> '3'."""
    x = round(float(x), 2)
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def leer_numero(texto):
    """Acepta '0,5' o '0.5'. Devuelve None si no es un número válido."""
    try:
        return round(float(texto.strip().replace(",", ".")), 2)
    except ValueError:
        return None


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
            <div class="sub">Toma la Liga Semestral como base, dinos cuántas Ligas Semestrales vale cada copa y descubre el ranking según tu criterio.</div>
        </div>''',
        unsafe_allow_html=True,
    )
    _, centro, _ = st.columns([1, 1, 1])
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

    es_base = (nombre == "Liga Semestral")
    previo = st.session_state.pesos.get(nombre)

    if es_base:
        st.markdown(
            '<div class="instruccion">La Liga Semestral es la base del ranking: <b>1 título = 1 punto</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="instruccion">¿Cuántas Ligas Semestrales vale la <b>{nombre}</b>?</div>'
            '<div class="ejemplos"><span class="ej-titulo">Ejemplos</span>'
            '<div><b>0,5</b> = media Liga Semestral</div>'
            '<div><b>1</b> = igual a una Liga Semestral</div>'
            '<div><b>3</b> = tres Ligas Semestrales</div>'
            '<div class="ej-rango">Rango permitido: de 0,1 a 10</div></div>',
            unsafe_allow_html=True,
        )

    _, centro, _ = st.columns([1, 1.6, 1])
    with centro:
        ruta = buscar_imagen(archivo)
        if ruta:
            st.image(ruta, use_container_width=True)
        else:
            st.markdown(f'<div class="placeholder">Falta la imagen<br>{archivo}</div>',
                        unsafe_allow_html=True)

    _, centro, _ = st.columns([1, 4, 1])
    with centro:
        with st.form(key=f"form_{i}", border=False):
            c_ant, c_val, c_ok = st.columns([1, 1, 1])
            anterior = c_ant.form_submit_button("← Anterior")
            if es_base:
                c_val.markdown('<div class="caja-base">1</div>', unsafe_allow_html=True)
                texto = "1"
            else:
                texto = c_val.text_input("Puntuación", value=fmt(previo) if previo else "",
                                         placeholder="0,1 – 10", label_visibility="collapsed", key=f"txt_{i}")
            confirmar = c_ok.form_submit_button("Confirmar")

        if anterior:
            st.session_state.paso -= 1
            st.rerun()
        if confirmar:
            valor = leer_numero(texto)
            if valor is None or not (0.1 <= valor <= 10):
                st.warning("Escribe un número entre 0,1 y 10 (puedes usar coma, por ejemplo 0,5).")
            else:
                st.session_state.pesos[nombre] = valor
                st.session_state.paso += 1
                st.rerun()

# ---------------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------------
else:
    st.markdown("<style>.block-container {max-width: 1100px;}</style>", unsafe_allow_html=True)
    encabezado("FPC", "Ranking por Títulos")

    pesos = st.session_state.pesos
    df = tabla_datos()
    df["Puntos"] = sum(df[t] * p for t, p in pesos.items())
    df = df.sort_values("Puntos", ascending=False).reset_index(names="Equipo")

    # Una sola lista: Equipo | Puntos | Títulos (Puntos) por cada copa
    encabezados = "".join(
        f"<th>{n}<small>TÍTULOS (PUNTOS)</small></th>" for n in NOMBRES
    )
    filas = ""
    for n, f in df.iterrows():
        clase_fila = ' class="top"' if n < 3 else ""
        celdas = ""
        for c in NOMBRES:
            t = int(f[c])
            clase = ' class="cero"' if t == 0 else ""
            celdas += f"<td{clase}>{t} ({fmt(t * pesos[c])})</td>"
        filas += (
            f"<tr{clase_fila}><td><span class='pos'>{n + 1}</span>{f['Equipo']}</td>"
            f"<td class='total'>{fmt(f['Puntos'])}</td>{celdas}</tr>"
        )
    st.markdown(
        f'''<div class="tabla-wrap">
        <table class="detalle"><thead><tr><th>Equipo</th>
        <th>Puntos<small>TOTAL</small></th>{encabezados}</tr></thead>
        <tbody>{filas}</tbody></table></div>''',
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Volver a empezar"):
        st.session_state.paso = -1
        st.session_state.pesos = {}
        st.rerun()
