import streamlit as st
import pandas as pd
import numpy as np
import ast
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Guía Aplicabilidad PMA-PSM",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d3b26 0%, #145c38 60%, #1a7a4a 100%);
  }
  [data-testid="stSidebar"] * { color: #e8f5ee !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stRadio label { color: #b8dfc8 !important; font-weight: 500; }

  /* ── SELECTBOX sidebar: fondo verde, texto blanco fijo ── */
  [data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {
    background-color: #1a5c38 !important;
  }
  [data-testid="stSidebar"] div[data-baseweb="select"] span,
  [data-testid="stSidebar"] div[data-baseweb="select"] div,
  [data-testid="stSidebar"] div[data-baseweb="select"] input,
  [data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"],
  [data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"] {
    color: #ffffff !important;
  }
  [data-testid="stSidebar"] [data-baseweb="popover"] *,
  [data-testid="stSidebar"] [data-baseweb="menu"] li,
  [data-testid="stSidebar"] [data-baseweb="option"] {
    background-color: #0d3b26 !important;
    color: #ffffff !important;
  }
  [data-testid="stSidebar"] [data-baseweb="option"]:hover,
  [data-testid="stSidebar"] [aria-selected="true"] {
    background-color: #1a7a4a !important;
    color: #ffffff !important;
  }

  /* Top header bar */
  .header-bar {
    background: linear-gradient(90deg, #0d3b26, #1a7a4a);
    padding: 18px 28px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .header-bar h1 { color: white; margin: 0; font-size: 1.6rem; font-weight: 700; }
  .header-bar p  { color: #b8dfc8; margin: 0; font-size: 0.85rem; }

  /* Metric cards */
  .metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .metric-card .number { font-size: 2.2rem; font-weight: 700; color: #0d3b26; }
  .metric-card .label  { font-size: 0.78rem; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: .05em; }

  /* Result card */
  .result-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #1a7a4a;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .result-card.no-aplica { border-left-color: #94a3b8; }
  .result-card .familia-tag {
    display: inline-block;
    background: #e8f5ee;
    color: #0d3b26;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: .04em;
  }
  .result-card h4 { margin: 4px 0 8px; font-size: 0.92rem; color: #1e293b; line-height: 1.4; }
  .badge-si {
    background: #dcfce7; color: #15803d;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600;
  }
  .badge-no {
    background: #f1f5f9; color: #64748b;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600;
  }
  .ficha-chip {
    display: inline-block;
    background: #f0fdf4;
    border: 1px solid #86efac;
    color: #166534;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    margin: 2px 3px 2px 0;
  }

  /* Search box style */
  .stTextInput input {
    border-radius: 8px !important;
    border: 2px solid #1a7a4a !important;
    font-size: 1rem !important;
    padding: 10px 14px !important;
  }

  /* Section headers */
  .section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0d3b26;
    border-bottom: 2px solid #e8f5ee;
    padding-bottom: 6px;
    margin: 20px 0 14px;
  }

  /* Hide streamlit default footer/menu */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    odl = pd.read_csv("data_odl_clean.csv")
    obc = pd.read_csv("data_obc_clean.csv")
    meta = pd.read_csv("fichas_meta.csv")

    for df in [odl, obc]:
        df['FICHAS_APLICAN'] = df['FICHAS_APLICAN'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
        )
    return odl, obc, meta

@st.cache_data
def load_uploaded(file_bytes, sheet_name, is_odl=True):
    """Parse an uploaded xlsm file dynamically."""
    import io
    df_raw = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet_name, header=None, engine='openpyxl')
    fichas = [str(x).strip() for x in df_raw.iloc[8, 4:].tolist()]
    data = df_raw.iloc[11:].copy()
    data.columns = ['FAMILIA', 'OBJETO_ALCANCE', 'SI', 'NO'] + fichas
    data = data.reset_index(drop=True)
    data['FAMILIA'] = data['FAMILIA'].replace('nan', np.nan)
    data['FAMILIA'] = data['FAMILIA'].apply(lambda x: str(x).replace('|','').strip() if pd.notna(x) else np.nan)
    data['FAMILIA'] = data['FAMILIA'].ffill()
    data = data[data['OBJETO_ALCANCE'].notna() & (data['OBJETO_ALCANCE'].astype(str).str.strip() != 'nan')]
    data['APLICA_PMA_PSM'] = data['SI'].apply(lambda x: True if str(x).strip().upper() == 'SI' else False)
    for col in fichas:
        data[col] = data[col].apply(lambda x: True if str(x).strip().upper() == 'X' else False)
    data = data.drop(columns=['SI', 'NO'])
    def get_fichas_list(row):
        return [f for f in fichas if row.get(f, False)]
    data['FICHAS_APLICAN'] = data.apply(get_fichas_list, axis=1)
    data['NUM_FICHAS'] = data['FICHAS_APLICAN'].apply(len)
    return data

try:
    odl_df, obc_df, meta_df = load_data()
    data_loaded = True
except Exception:
    data_loaded = False
    odl_df, obc_df, meta_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌿 PMA-PSM")
    st.markdown("**HSE-G-008 · Versión 6**")
    st.markdown("---")

    nav = st.radio(
        "Módulo",
        ["🔎 Buscador", "📊 Dashboard", "📁 Cargar archivo", "📑 Ficha de proyecto"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    oleoducto = st.selectbox("🛢️ Oleoducto", ["ODL (Llanos Orientales)", "OBC (Bicentenario)"])
    active_df = odl_df if "ODL" in oleoducto else obc_df

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem; color:#86efac; line-height:1.6'>"
        "📌 Contacto ambiental:<br>"
        "<b>sonia.frayle@odl.com.co</b><br>"
        "<b>derly.neira@odl.com.co</b>"
        "</div>",
        unsafe_allow_html=True
    )

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <div>
    <h1>🌿 Guía de Aplicabilidad PMA-PSM</h1>
    <p>Oleoducto de los Llanos Orientales · Bicentenario · HSE-G-008 · Versión 6</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — BUSCADOR
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🔎 Buscador":
    st.markdown("### 🔎 Buscador de Aplicabilidad")
    st.caption("Escribe palabras clave del objeto/alcance del contrato para encontrar sus fichas PMA-PSM aplicables.")

    col_s, col_f, col_a = st.columns([4, 2, 2])
    with col_s:
        query = st.text_input("Buscar contrato o actividad…", placeholder="Ej: mantenimiento tanques, ductos, capacitación fauna…")
    with col_f:
        familias = ["Todas"] + sorted(active_df['FAMILIA'].dropna().unique().tolist()) if not active_df.empty else ["Todas"]
        familia_filter = st.selectbox("Familia / PCC", familias)
    with col_a:
        aplica_filter = st.selectbox("Aplica PMA-PSM", ["Todas", "SÍ aplica", "NO aplica"])

    if not active_df.empty:
        results = active_df.copy()

        if query:
            mask = results['OBJETO_ALCANCE'].str.contains(query, case=False, na=False)
            results = results[mask]

        if familia_filter != "Todas":
            results = results[results['FAMILIA'] == familia_filter]

        if aplica_filter == "SÍ aplica":
            results = results[results['APLICA_PMA_PSM'] == True]
        elif aplica_filter == "NO aplica":
            results = results[results['APLICA_PMA_PSM'] == False]

        # Summary
        c1, c2, c3, c4 = st.columns(4)
        total_aplica = results['APLICA_PMA_PSM'].sum()
        with c1:
            st.markdown(f'<div class="metric-card"><div class="number">{len(results)}</div><div class="label">Resultados</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="number" style="color:#15803d">{int(total_aplica)}</div><div class="label">Aplican PMA-PSM</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="number" style="color:#94a3b8">{len(results)-int(total_aplica)}</div><div class="label">No aplican</div></div>', unsafe_allow_html=True)
        with c4:
            avg_fichas = results[results['APLICA_PMA_PSM']==True]['NUM_FICHAS'].mean() if total_aplica > 0 else 0
            st.markdown(f'<div class="metric-card"><div class="number">{avg_fichas:.1f}</div><div class="label">Fichas promedio</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        if len(results) == 0:
            st.info("🔍 Sin resultados. Intenta con otras palabras clave.")
        else:
            for _, row in results.head(60).iterrows():
                aplica = row['APLICA_PMA_PSM']
                card_class = "result-card" if aplica else "result-card no-aplica"
                badge = '<span class="badge-si">✅ SÍ APLICA</span>' if aplica else '<span class="badge-no">— No aplica</span>'
                fichas_html = ""
                if aplica and row['FICHAS_APLICAN']:
                    fichas_html = "".join([f'<span class="ficha-chip">{f}</span>' for f in row['FICHAS_APLICAN']])

                st.markdown(f"""
                <div class="{card_class}">
                  <span class="familia-tag">{row['FAMILIA']}</span>
                  <h4>{row['OBJETO_ALCANCE']}</h4>
                  {badge}
                  {"&nbsp;&nbsp;<span style='color:#64748b; font-size:0.75rem'>"+str(int(row['NUM_FICHAS']))+" fichas</span>" if aplica and row['NUM_FICHAS']>0 else ""}
                  {"<br><div style='margin-top:8px'>"+fichas_html+"</div>" if fichas_html else ""}
                </div>
                """, unsafe_allow_html=True)

            if len(results) > 60:
                st.caption(f"_Mostrando 60 de {len(results)} resultados. Refina la búsqueda para ver más._")

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📊 Dashboard":
    st.markdown("### 📊 Panel de Control")

    if active_df.empty:
        st.warning("No hay datos cargados.")
    else:
        df = active_df.copy()
        label = "ODL" if "ODL" in oleoducto else "OBC"

        # KPIs
        total = len(df)
        aplica = df['APLICA_PMA_PSM'].sum()
        no_aplica = total - aplica
        pct = (aplica / total * 100) if total > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="metric-card"><div class="number">{total}</div><div class="label">Contratos / Actividades</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="metric-card"><div class="number" style="color:#15803d">{int(aplica)}</div><div class="label">Aplican PMA-PSM</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="metric-card"><div class="number" style="color:#94a3b8">{int(no_aplica)}</div><div class="label">No aplican</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="metric-card"><div class="number">{pct:.1f}%</div><div class="label">Tasa de aplicabilidad</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        col_a, col_b = st.columns(2)

        # Chart 1: Aplicabilidad por familia
        with col_a:
            st.markdown('<div class="section-title">Aplicabilidad por Familia</div>', unsafe_allow_html=True)
            fam_stats = df.groupby('FAMILIA').agg(
                Total=('APLICA_PMA_PSM', 'count'),
                Aplica=('APLICA_PMA_PSM', 'sum')
            ).reset_index()
            fam_stats['No aplica'] = fam_stats['Total'] - fam_stats['Aplica']
            fam_stats = fam_stats.sort_values('Total', ascending=True).tail(12)

            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                y=fam_stats['FAMILIA'], x=fam_stats['Aplica'],
                name='Aplica', orientation='h',
                marker_color='#1a7a4a'
            ))
            fig1.add_trace(go.Bar(
                y=fam_stats['FAMILIA'], x=fam_stats['No aplica'],
                name='No aplica', orientation='h',
                marker_color='#cbd5e1'
            ))
            fig1.update_layout(
                barmode='stack', height=380,
                margin=dict(l=0, r=20, t=20, b=20),
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                plot_bgcolor='white', paper_bgcolor='white',
                xaxis=dict(gridcolor='#f1f5f9'),
            )
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Top fichas más frecuentes
        with col_b:
            st.markdown('<div class="section-title">Fichas PMA-PSM más requeridas</div>', unsafe_allow_html=True)
            df_aplica = df[df['APLICA_PMA_PSM'] == True]
            ficha_counts = {}
            for fichas_list in df_aplica['FICHAS_APLICAN']:
                for f in fichas_list:
                    ficha_counts[f] = ficha_counts.get(f, 0) + 1

            if ficha_counts:
                fc_df = pd.DataFrame({'Ficha': list(ficha_counts.keys()), 'Frecuencia': list(ficha_counts.values())})
                fc_df = fc_df.sort_values('Frecuencia', ascending=False).head(15)
                fig2 = px.bar(
                    fc_df, x='Ficha', y='Frecuencia',
                    color='Frecuencia', color_continuous_scale='Greens',
                )
                fig2.update_layout(
                    height=380, margin=dict(l=0, r=0, t=20, b=60),
                    plot_bgcolor='white', paper_bgcolor='white',
                    coloraxis_showscale=False,
                    xaxis=dict(tickangle=-45)
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Chart 3: Distribución de número de fichas
        st.markdown('<div class="section-title">Distribución de fichas por actividad (con aplicabilidad)</div>', unsafe_allow_html=True)
        df_num = df_aplica['NUM_FICHAS'].value_counts().reset_index()
        df_num.columns = ['Num Fichas', 'Contratos']
        df_num = df_num.sort_values('Num Fichas')

        fig3 = px.bar(
            df_num, x='Num Fichas', y='Contratos',
            labels={'Num Fichas': 'Número de fichas requeridas', 'Contratos': 'Cantidad de contratos'},
            color_discrete_sequence=['#1a7a4a']
        )
        fig3.update_layout(
            height=280, margin=dict(l=0, r=0, t=20, b=20),
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(dtick=1, gridcolor='#f1f5f9'),
        )
        st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — CARGAR ARCHIVO
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📁 Cargar archivo":
    st.markdown("### 📁 Cargar nueva versión del Excel")
    st.info("Sube un archivo `.xlsm` con la misma estructura que **GUIA_APLICABILIDAD_PMAPSM.xlsm** para actualizar los datos.")

    uploaded = st.file_uploader("Selecciona el archivo", type=["xlsm", "xlsx"])

    if uploaded:
        file_bytes = uploaded.read()
        import openpyxl
        wb = openpyxl.load_workbook(BytesIO(file_bytes), read_only=True)
        sheets = wb.sheetnames

        st.success(f"✅ Archivo cargado: **{uploaded.name}** ({len(sheets)} hojas)")
        st.write("**Hojas detectadas:**", sheets[:10], "…" if len(sheets) > 10 else "")

        col1, col2 = st.columns(2)
        with col1:
            sheet_odl = st.selectbox("Hoja ODL", [s for s in sheets if 'ODL' in s.upper() or 'LÍNEA' in s.upper() or 'LINEA' in s.upper()] or sheets)
        with col2:
            sheet_obc = st.selectbox("Hoja OBC/BIC", [s for s in sheets if 'OBC' in s.upper() or 'BIC' in s.upper()] or sheets)

        if st.button("🔄 Procesar y actualizar datos", type="primary"):
            with st.spinner("Procesando…"):
                try:
                    new_odl = load_uploaded(file_bytes, sheet_odl, is_odl=True)
                    new_obc = load_uploaded(file_bytes, sheet_obc, is_odl=False)
                    new_odl.to_csv("data_odl_clean.csv", index=False)
                    new_obc.to_csv("data_obc_clean.csv", index=False)
                    st.cache_data.clear()
                    st.success(f"✅ Datos actualizados: {len(new_odl)} registros ODL · {len(new_obc)} registros OBC")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al procesar: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4 — FICHA DE PROYECTO
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📑 Ficha de proyecto":
    st.markdown("### 📑 Ficha de Proyecto – Reporte de Aplicabilidad")
    st.caption("Selecciona una actividad para generar su ficha de aplicabilidad PMA-PSM completa.")

    if active_df.empty:
        st.warning("No hay datos cargados.")
    else:
        df = active_df.copy()
        label = "ODL" if "ODL" in oleoducto else "OBC"

        col_f, col_o = st.columns([2, 4])
        with col_f:
            familia_sel = st.selectbox("Familia", sorted(df['FAMILIA'].dropna().unique().tolist()))
        with col_o:
            objetos = df[df['FAMILIA'] == familia_sel]['OBJETO_ALCANCE'].tolist()
            objeto_sel = st.selectbox("Objeto / Alcance", objetos)

        row = df[(df['FAMILIA'] == familia_sel) & (df['OBJETO_ALCANCE'] == objeto_sel)].iloc[0]
        aplica = row['APLICA_PMA_PSM']
        fichas = row['FICHAS_APLICAN'] if aplica else []

        st.markdown("---")

        # Header card
        status_color = "#dcfce7" if aplica else "#f1f5f9"
        status_text = "✅ APLICA PMA-PSM" if aplica else "— NO APLICA PMA-PSM"
        status_fg = "#15803d" if aplica else "#64748b"

        st.markdown(f"""
        <div style="background:{status_color}; border-radius:12px; padding:20px 24px; margin-bottom:20px;">
          <div style="font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:.06em;">Resultado de Aplicabilidad</div>
          <div style="font-size:1.5rem; font-weight:700; color:{status_fg}; margin:6px 0 4px">{status_text}</div>
          <div style="font-size:0.85rem; color:#334155;"><b>Oleoducto:</b> {label} &nbsp;|&nbsp; <b>Familia:</b> {familia_sel}</div>
        </div>
        """, unsafe_allow_html=True)

        # Object description
        st.markdown(f"**Objeto / Alcance:**")
        st.markdown(f"> {objeto_sel}")

        if aplica and fichas:
            st.markdown('<div class="section-title">📋 Fichas PMA-PSM Aplicables</div>', unsafe_allow_html=True)

            # Group fichas by plan type
            pma_fichas = [f for f in fichas if any(f.startswith(p) for p in ['PMOOR','AS','ARH','ARA','ACA','BS','BPCH','BRAI','BH','BCEVF','BC','GS','PGSO','PSMA'])]
            psm_fichas = [f for f in fichas if any(f.startswith(p) for p in ['ASM','PM','BSM','SSM'])]

            col_pma, col_psm = st.columns(2)
            with col_pma:
                st.markdown("**🗂️ Plan de Manejo Ambiental (PMA)**")
                if pma_fichas:
                    for f in pma_fichas:
                        desc_row = meta_df[meta_df['FICHA'] == f] if not meta_df.empty else pd.DataFrame()
                        desc = desc_row.iloc[0]['DESCRIPCION'] if not desc_row.empty and pd.notna(desc_row.iloc[0]['DESCRIPCION']) else ""
                        st.markdown(f"""
                        <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                          <b style="color:#166534">{f}</b>
                          {"<br><span style='font-size:0.8rem; color:#374151'>"+desc+"</span>" if desc and desc != 'nan' else ""}
                        </div>""", unsafe_allow_html=True)
                else:
                    st.caption("—")

            with col_psm:
                st.markdown("**📈 Plan de Seguimiento y Monitoreo (PSM)**")
                if psm_fichas:
                    for f in psm_fichas:
                        desc_row = meta_df[meta_df['FICHA'] == f] if not meta_df.empty else pd.DataFrame()
                        desc = desc_row.iloc[0]['DESCRIPCION'] if not desc_row.empty and pd.notna(desc_row.iloc[0]['DESCRIPCION']) else ""
                        st.markdown(f"""
                        <div style="background:#eff6ff; border:1px solid #93c5fd; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                          <b style="color:#1e40af">{f}</b>
                          {"<br><span style='font-size:0.8rem; color:#374151'>"+desc+"</span>" if desc and desc != 'nan' else ""}
                        </div>""", unsafe_allow_html=True)
                else:
                    st.caption("—")

            # Export button
            st.markdown("---")
            st.markdown("**📥 Exportar reporte**")

            report_lines = [
                f"REPORTE DE APLICABILIDAD PMA-PSM",
                f"HSE-G-008 · Versión 6",
                f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}",
                f"",
                f"Oleoducto: {label}",
                f"Familia: {familia_sel}",
                f"Objeto/Alcance: {objeto_sel}",
                f"",
                f"RESULTADO: {'APLICA PMA-PSM' if aplica else 'NO APLICA PMA-PSM'}",
                f"Número de fichas: {len(fichas)}",
                f"",
                f"FICHAS PMA APLICABLES:",
                *[f"  - {f}" for f in pma_fichas],
                f"",
                f"FICHAS PSM APLICABLES:",
                *[f"  - {f}" for f in psm_fichas],
                f"",
                f"NOTAS:",
                f"  1. Las fichas sociales deben ser acordadas con RS empresarial.",
                f"  2. Verificar los alcances ya que algunos tienen observación de aplicabilidad.",
            ]
            report_txt = "\n".join(report_lines)

            st.download_button(
                label="⬇️ Descargar reporte (.txt)",
                data=report_txt.encode('utf-8'),
                file_name=f"Aplicabilidad_{label}_{familia_sel[:20].replace(' ','_')}.txt",
                mime="text/plain"
            )

        elif not aplica:
            st.info("Esta actividad **no requiere** medidas de manejo PMA-PSM.")

        # Notes section
        st.markdown("---")
        st.markdown("**⚠️ Notas importantes**")
        st.markdown("""
- Las fichas sociales deben ser acordadas con **RS empresarial**.
- Verificar los alcances ya que algunos tienen observación de aplicabilidad.
- Al diligenciar las fichas del PMA-PSM del formato 1a, no eliminar filas ni columnas.
- Para GDB no alterar columnas — ingresar dato a dato, sin copiar/pegar.
        """)
