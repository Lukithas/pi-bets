import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile
import glob
import textwrap
import os
# Adicionamos configuração na URL para forçar o tema Light por padrão,
# garantindo que o tema não seja influenciado pelo SO do usuário.
st.set_page_config(page_title="Ludopatia & BETs | PI", layout="wide", page_icon="📊")

# Função para injetar JS e forçar o tema claro se o usuário não tocou no botão ainda
# Isso sobrepõe a configuração de sistema (SO) que estava escurecendo o fundo.
st.markdown("""
    <script>
        var elements = window.parent.document.querySelectorAll('.stApp');
        if (elements.length > 0) {
            elements[0].style.backgroundColor = '#f8fafc';
        }
    </script>
    """, unsafe_allow_html=True)


# =====================================================================
# 1.1 ESTADO DOS CONTROLES DE ACESSIBILIDADE (botões simples ligar/desligar)
# =====================================================================
if "modo_escuro" not in st.session_state:
    st.session_state.modo_escuro = False
if "alto_contraste" not in st.session_state:
    st.session_state.alto_contraste = False
if "nivel_fonte" not in st.session_state:
    st.session_state.nivel_fonte = 1  # 0=A- 1=A 2=A+ 3=A++

def alternar_modo_escuro():
    st.session_state.modo_escuro = not st.session_state.modo_escuro

def alternar_alto_contraste():
    st.session_state.alto_contraste = not st.session_state.alto_contraste

def aumentar_fonte():
    st.session_state.nivel_fonte = min(3, st.session_state.nivel_fonte + 1)

def diminuir_fonte():
    st.session_state.nivel_fonte = max(0, st.session_state.nivel_fonte - 1)

modo_escuro = st.session_state.modo_escuro
alto_contraste = st.session_state.alto_contraste
escala_fonte = {0: 0.875, 1: 1.0, 2: 1.15, 3: 1.3}[st.session_state.nivel_fonte]

plt.close('all')

# Se o usuário clicar, ativamos o escuro. Caso contrário, forçamos o branco (claro).
if modo_escuro:
    bg_surface = "#1e293b"
    text_main = "#f8fafc"
    text_muted = "#94a3b8"
    border_color = "#334155"
    bg_desc = "#1e293b"
    accent = "#a7197f"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": "#0f172a", "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="darkgrid", rc=rc_params)
    bg_app = "#0f172a" 
    bg_sidebar = "#1e293b"
else:
    bg_surface = "#ffffff"
    text_main = "#0f172a"
    text_muted = "#64748b"
    border_color = "#e2e8f0"
    bg_desc = "#f8fafc"
    accent = "#a7197f"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": "#ffffff", "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="whitegrid", rc=rc_params)
    bg_app = "#f8fafc" 
    bg_sidebar = "#ffffff" 

# Sobrepõe as cores se o Alto Contraste estiver ativo (independente do modo claro/escuro)
if alto_contraste:
    if modo_escuro:
        bg_app, bg_sidebar, bg_surface, bg_desc = "#000000", "#000000", "#000000", "#000000"
        text_main, text_muted = "#ffffff", "#ffffff"
        border_color = "#ffffff"
        accent = "#ffe600"
    else:
        bg_app, bg_sidebar, bg_surface, bg_desc = "#ffffff", "#ffffff", "#ffffff", "#ffffff"
        text_main, text_muted = "#000000", "#000000"
        border_color = "#000000"
        accent = "#7a0058"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": bg_app, "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="darkgrid" if modo_escuro else "whitegrid", rc=rc_params)

borda_box = "2px" if alto_contraste else "1px"

# =====================================================================
# 1.2 BARRA DE ACESSIBILIDADE (canto superior direito, botões simples)
# =====================================================================
faixa_topo = st.container()
with faixa_topo:
    espaco, b1, b2, b3, b4 = st.columns([5, 1.3, 1.3, 1.1, 1.3])
    with b1:
        st.button("Fonte −", key="btn_menos", on_click=diminuir_fonte, use_container_width=True)
    with b2:
        st.button("Fonte +", key="btn_mais", on_click=aumentar_fonte, use_container_width=True)
    with b3:
        st.button("Contraste" + (" ✓" if alto_contraste else ""), key="btn_contraste", on_click=alternar_alto_contraste, use_container_width=True)
    with b4:
        st.button("Modo Escuro" + (" ✓" if modo_escuro else ""), key="btn_escuro", on_click=alternar_modo_escuro, use_container_width=True)

# =====================================================================
# 2. BARRA LATERAL — SOMENTE FILTROS DE DADOS
# =====================================================================
st.sidebar.image("https://institucional.uniceub.br/hubfs/BrandCenter/img/logo-ceub-versao-estendida.png", use_container_width=True)
st.sidebar.title("Filtros")

# Injeção de CSS Dinâmico FORÇANDO as cores sobre a configuração do Streamlit/SO
st.markdown(f'''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html {{ font-size: {escala_fonte * 100}%; }}

    /* FORÇA a cor de fundo do aplicativo inteiro e da barra lateral */
    [data-testid="stAppViewContainer"] {{ background-color: {bg_app} !important; }}
    [data-testid="stSidebar"] {{ background-color: {bg_sidebar} !important; border-right: {borda_box} solid {border_color} !important; }}
    [data-testid="stHeader"] {{ background-color: {bg_app} !important; }}

    /* FORÇA as cores dos textos para ignorar o SO, mas PRESERVA os ícones nativos (Material Symbols) */
    html, body, p, h1, h2, h3, h4, h5, h6, label, span {{
        color: {text_main} !important;
    }}
    html, body, p, h1, h2, h3, h4, h5, h6, label,
    span:not([class*="material"]):not([data-testid*="Icon"]) {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stIconMaterial"], span[class*="material-symbols"] {{
        font-family: 'Material Symbols Rounded' !important;
    }}
    .stMarkdown, .stMetricLabel, .stMetricValue {{
        color: {text_main} !important;
    }}

    /* Título principal com leve destaque tipográfico */
    .titulo-principal {{ font-weight: 800 !important; letter-spacing: -0.02em; margin-bottom: 0.2rem !important; }}
    .subtitulo-principal {{ font-weight: 400 !important; opacity: 0.85; }}

    /* Cartões de gráfico com sombra suave e leve elevação no hover */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 14px !important;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        box-shadow: 0 6px 18px rgba(0,0,0,0.10);
        transform: translateY(-2px);
    }}

    /* Box da Descrição do Gráfico */
    .grafico-desc {{ background-color: {bg_desc}; padding: 12px 16px; border-radius: 10px; border-left: 4px solid {accent}; margin-top: 10px; margin-bottom: 4px; font-size: 0.88em; color: {text_main} !important; line-height: 1.65; border-top: {borda_box} solid {border_color}; border-right: {borda_box} solid {border_color}; border-bottom: {borda_box} solid {border_color}; }}
    .grafico-desc strong {{ color: {accent} !important; font-size: 0.82em; text-transform: uppercase; letter-spacing: 0.06em; }}

    /* Caixas de KPI com hierarquia visual mais clara */
    .kpi-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
    .kpi-box {{ background: {bg_surface}; padding: 1.5rem; border-radius: 14px; border: {borda_box} solid {border_color}; text-align: center; border-left: 5px solid #3b1054; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: transform 0.2s ease; }}
    .kpi-box:hover {{ transform: translateY(-3px); }}
    .kpi-box.danger {{ border-left-color: #ef4444; }}
    .kpi-value {{ font-size: 2.1em; font-weight: 800; color: {text_main} !important; margin: 0.4rem 0; letter-spacing: -0.02em; }}
    .kpi-label {{ font-size: 0.78em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; color: {text_muted} !important; }}

    /* Abas com aparência mais limpa */
    [data-baseweb="tab-list"] {{ gap: 4px; }}
    [data-baseweb="tab"] {{ font-weight: 600 !important; }}

    /* Foco visível em elementos interativos (acessibilidade de teclado) */
    button:focus-visible, [role="tab"]:focus-visible, a:focus-visible {{
        outline: 3px solid {accent} !important;
        outline-offset: 2px !important;
    }}

    /* Barra de acessibilidade no topo — botões mais amigáveis: cor suave, arredondados, com hover */
    button[data-testid="stBaseButton-secondary"] {{
        font-size: 0.85em !important;
        font-weight: 700 !important;
        padding: 0.45rem 0.6rem !important;
        border-radius: 999px !important;
        border: {("3px solid " + border_color) if alto_contraste else "none"} !important;
        background-color: {bg_surface if alto_contraste else ("#33415540" if modo_escuro else "#a7197f14")} !important;
        color: {accent} !important;
        white-space: nowrap !important;
        transition: background-color 0.15s ease, transform 0.15s ease !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        background-color: {accent} !important;
        color: {bg_app if alto_contraste else "#ffffff"} !important;
        transform: translateY(-1px);
    }}
</style>
''', unsafe_allow_html=True)

filtro_genero = st.sidebar.multiselect("Gênero:", ['Masculino', 'Feminino'], default=['Masculino', 'Feminino'])

st.sidebar.markdown("**Faixa Etária:**")
col_idade_min, col_idade_max = st.sidebar.columns(2)
with col_idade_min:
    idade_min = st.number_input("Idade mínima", min_value=18, max_value=65, value=18, step=1, key="idade_min")
with col_idade_max:
    idade_max = st.number_input("Idade máxima", min_value=18, max_value=65, value=65, step=1, key="idade_max")
idade_slider = (min(idade_min, idade_max), max(idade_min, idade_max))

st.sidebar.markdown(
    '<div style="font-size: 1.05em; line-height: 1.5; opacity: 0.85; margin-top: 4px;">'
    'Esses filtros afetam apenas os gráficos 3, 4 e 5 (baseados em microdados simulados de pacientes). '
    'Os demais gráficos usam dados de pesquisas externas (Serasa, PwC, USP, Consumidor.gov) e não são '
    'segmentáveis por gênero/idade.</div>',
    unsafe_allow_html=True
)

# =====================================================================
# 3. EXTRAÇÃO DE DADOS INTELIGENTE
# =====================================================================
@st.cache_data(show_spinner="Carregando dados estatísticos...")
def get_data_estatistica():
    df_macro = pd.DataFrame([["Loterias", 71.3], ["Apostas Online (BETs)", 32.1], ["Jogo do Bicho", 28.9]], columns=["Categoria", "Valor"])
    df_bcb = pd.DataFrame({'Ano': range(2018, 2025), 'Inadimplencia': [3.1, 2.9, 2.7, 2.2, 2.7, 3.2, 3.1]})
    np.random.seed(42)
    df_pacientes = pd.DataFrame({'Idade': np.random.normal(28, 8, 500).astype(int), 'Renda_Mensal': np.random.lognormal(7.5, 0.6, 500), 'Divida_Acumulada': np.random.lognormal(7.5, 0.6, 500) * 2, 'Genero': np.random.choice(['Masculino', 'Feminino'], 500)})
    return df_macro, df_bcb, df_pacientes

st.sidebar.markdown("---")
st.sidebar.subheader("Status das Bases de Dados")

@st.cache_data(show_spinner="Processando 200MB de dados do Consumidor.gov...")
def get_dados_consumidor_local():
    pasta_extracao = 'dados_consumidor_csvs'
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_zip = os.path.join(script_dir, 'bases_consumidor.zip')
    except NameError:
        caminho_zip = 'bases_consumidor.zip'
        
    if os.path.exists(caminho_zip):
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(pasta_extracao)
            arquivos_csv = glob.glob(os.path.join(pasta_extracao, "*.csv"))
            lista_dfs = []
            for arquivo in arquivos_csv:
                try:
                    df_temp = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
                except UnicodeDecodeError:
                    df_temp = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False)
                lista_dfs.append(df_temp)
            if lista_dfs:
                df_total = pd.concat(lista_dfs, ignore_index=True)
                filtro = df_total['Nome Fantasia'].str.contains('BET|APOSTA|CASSINO|BLAZE', case=False, na=False)
                df_bets = df_total[filtro]
                if 'Problema' in df_bets.columns:
                    top_problemas = df_bets['Problema'].value_counts().head(5).reset_index()
                    top_problemas.columns = ['Problema', 'Quantidade']
                    return top_problemas, True
        except Exception as e:
            pass
            
    df_mock = pd.DataFrame({'Problema': ['Saque', 'Publicidade', 'Bloqueio', 'Cobrança', 'Bônus'], 'Quantidade': [1450, 980, 750, 620, 410]})
    return df_mock, False

@st.cache_data(show_spinner="Carregando pesquisa da equipe...")
def get_dados_consolidados_csv():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_csv = os.path.join(script_dir, 'dados_apostas_consolidado.csv')
    except NameError:
        caminho_csv = 'dados_apostas_consolidado.csv'
        
    if os.path.exists(caminho_csv):
        try:
            df = pd.read_csv(caminho_csv)
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
            return df, True
        except:
            pass
    
    dados = [["2024", "OMS", "% adultos apostaram (1 ano)", 46.2], ["2024", "OMS", "% adolescentes apostaram", 17.9], ["2018", "USP/IPq", "Dívidas > renda mensal", 60.0], ["2018", "USP/IPq", "Ideação suicida (2018)", 27.0], ["2024", "PwC", "Usando poupança para apostar", 52.0], ["2024", "PwC", "Cortando lazer/alimentação", 48.0], ["2025", "PRO-AMJO", "Ideação suicida (2025)", 80.0]]
    return pd.DataFrame(dados, columns=["Ano", "Fonte", "Indicador", "Valor"]), False

df_macro, df_bcb, df_pacientes = get_data_estatistica()
df_problemas, zip_encontrado = get_dados_consumidor_local()
df_consolidado, csv_encontrado = get_dados_consolidados_csv()

if zip_encontrado: st.sidebar.success("✅ bases_consumidor.zip carregado!")
else: st.sidebar.warning("⚠️ ZIP não encontrado. Usando Mockup.")

if csv_encontrado: st.sidebar.success("✅ dados_apostas_consolidado.csv carregado!")
else: st.sidebar.warning("⚠️ CSV não encontrado. Usando Mockup.")

df_pacientes = df_pacientes[(df_pacientes['Genero'].isin(filtro_genero)) & (df_pacientes['Idade'].between(idade_slider[0], idade_slider[1]))]

# =====================================================================
# 4. DASHBOARD E GRÁFICOS
# =====================================================================
st.markdown(f"<h1 class='titulo-principal' style='color: {text_main}; font-size: 2.55em;'>Painel Analítico: Ludopatia & BETs</h1><p class='subtitulo-principal' style='color: {text_muted}; font-size: 1.15em;'>Análise técnica sobre o impacto das apostas online na estrutura socioeconômica.</p>", unsafe_allow_html=True)

st.markdown(f'''<div class="kpi-container"><div class="kpi-box danger"><div class="kpi-label">Apostadores Endividados</div><div class="kpi-value">86%</div><div class="kpi-label" style="text-transform:none">Fonte: Serasa/Locomotiva</div></div><div class="kpi-box danger"><div class="kpi-label">Ideação Suicida</div><div class="kpi-value">80%</div><div class="kpi-label" style="text-transform:none">Pacientes em Tratamento</div></div><div class="kpi-box"><div class="kpi-label">Volume Anual Estimado</div><div class="kpi-value">R$ 120 Bi</div><div class="kpi-label" style="text-transform:none">Mercado no Brasil</div></div><div class="kpi-box"><div class="kpi-label">Perfil Jovem</div><div class="kpi-value">56%</div><div class="kpi-label" style="text-transform:none">18 a 39 anos</div></div></div>''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🗄️ Bases de Dados Puras (Raw Data)"])

with tab1:
    def render_dashboard_card(col, title, metric_label, metric_value, fig, desc):
        with col:
            with st.container(border=True):
                st.subheader(title)
                st.metric(metric_label, metric_value)
                st.pyplot(fig, transparent=True) 
                st.markdown(f'<div class="grafico-desc">{desc}</div>', unsafe_allow_html=True)
                plt.close(fig) 

    col1, col2 = st.columns(2)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_macro, x='Valor', y='Categoria', ax=ax1, palette="viridis")
    render_dashboard_card(col1, "1. Modalidades Praticadas", "Liderança", "71.3% Loterias", fig1, "<strong>📌 Análise:</strong> As loterias tradicionais ainda dominam o mercado.")

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=df_bcb, x='Ano', y='Inadimplencia', ax=ax2, color='#ef4444', marker='o')
    render_dashboard_card(col2, "2. Inadimplência Familiar", "Média Atual", "3.1%", fig2, "<strong>📌 Análise:</strong> A curva de inadimplência acompanha o crescimento das BETs.")

    col3, col4 = st.columns(2)
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    sns.histplot(data=df_pacientes, x='Idade', kde=True, ax=ax3, color="#a7197f")
    render_dashboard_card(col3, "3. Perfil Etário de Risco", "Média de Idade", f"{int(df_pacientes['Idade'].mean()) if not df_pacientes.empty else 0} anos", fig3, "<strong>📌 Análise:</strong> Predominância de adultos jovens, com concentração entre 20 e 35 anos.")

    fig4, ax4 = plt.subplots(figsize=(6, 3))
    sns.boxplot(data=df_pacientes, x='Genero', y='Divida_Acumulada', ax=ax4, palette="muted")
    render_dashboard_card(col4, "4. Endividamento por Gênero", "Impacto", "Variável", fig4, "<strong>📌 Análise:</strong> Homens apresentam maior dispersão de dívida.")

    col5, col6 = st.columns(2)
    fig5, ax5 = plt.subplots(figsize=(6, 3))
    sns.scatterplot(data=df_pacientes, x='Renda_Mensal', y='Divida_Acumulada', hue='Genero', ax=ax5, palette="deep")
    render_dashboard_card(col5, "5. Renda vs Dívida", "Correlação", "Direta", fig5, "📌 <strong>ANÁLISE:</strong> Endividamento cresce proporcionalmente à renda.")

    fig6, ax6 = plt.subplots(figsize=(6, 3.5))
    sns.barplot(data=df_problemas, x='Quantidade', y='Problema', ax=ax6, palette="flare")
    ax6.set_yticks(ax6.get_yticks())
    # Aumentamos o limite para 35 caracteres para evitar esmagamento vertical
    ax6.set_yticklabels([textwrap.fill(l.get_text(), 35) for l in ax6.get_yticklabels()], fontsize=8)
    fig6.tight_layout() # Força o Matplotlib a ajustar as margens para não cortar o texto
    render_dashboard_card(col6, "6. Reclamações contra BETs", "Principal", "Saque", fig6, "📌 <strong>ANÁLISE:</strong> Dificuldade de saque lidera as ocorrências no Consumidor.gov.")

    col7, col8 = st.columns(2)
    with col7:
        fig7, ax7 = plt.subplots(figsize=(6, 3))
        termos_busca = 'dívida|poupança|lazer|alimentação|renda|consequência|inadimplência'
        df_fin = df_consolidado[df_consolidado['Indicador'].str.contains(termos_busca, case=False, na=False)].copy()
        
        if not df_fin.empty:
            df_fin = df_fin[df_fin['Valor'] <= 100].sort_values(by='Valor', ascending=False).head(3)
            sns.barplot(data=df_fin, x='Indicador', y='Valor', ax=ax7, palette=["#ef4444", "#f59e0b", "#3b1054"])
            ax7.set_xticks(ax7.get_xticks())
            ax7.set_xticklabels([textwrap.fill(l.get_text(), 15) for l in ax7.get_xticklabels()], fontsize=8)
            ax7.set_ylim(0, 100)
            
        valor_destaque = f"{int(df_fin['Valor'].max())}%" if not df_fin.empty else "N/A"
        render_dashboard_card(col7, "7. Impacto Financeiro", "Destaque", valor_destaque, fig7, "<strong>📌 Análise:</strong> O descontrole reflete no orçamento familiar.")

    with col8:
        fig8, ax8 = plt.subplots(figsize=(6, 3))
        df_sui = df_consolidado[df_consolidado['Indicador'].str.contains('suicida', case=False, na=False)].copy()
        if not df_sui.empty:
            sns.barplot(data=df_sui, x='Ano', y='Valor', ax=ax8, palette=["#f59e0b", "#ef4444"])
            ax8.set_ylim(0, 100)
        render_dashboard_card(col8, "8. Ideação Suicida", "Crescimento", "+53 p.p.", fig8, "<strong>📌 Análise:</strong> Salto de 27% (2018) para 80% (2025) nos pacientes.")

with tab2:
    @st.cache_data
    def convert_df_to_csv(df): return df.to_csv(index=False).encode('utf-8')
    
    st.markdown("### Bases de Dados Brutas / Tratadas")
    st.write("Faça o download dos arquivos utilizados na pesquisa:")
    
    st.subheader("1. Microdados Simulados (DataSUS - F63.0)")
    st.dataframe(df_pacientes, use_container_width=True)
    st.download_button("📥 Baixar Dados SUS (CSV)", data=convert_df_to_csv(df_pacientes), file_name='dados_sus.csv', mime='text/csv')
    
    st.markdown("---")
    st.subheader("2. Pesquisa Estruturada da Equipe")
    st.dataframe(df_consolidado, use_container_width=True)
    st.download_button("📥 Baixar Pesquisa da Equipe (CSV)", data=convert_df_to_csv(df_consolidado), file_name='dados_apostas_consolidado.csv', mime='text/csv')
    
    st.markdown("---")
    st.subheader("3. Base do Consumidor.gov.br (ZIP)")
    st.write("Faça o download da base bruta original compactada com os arquivos CSV (200MB).")
    
    caminho_zip = 'bases_consumidor.zip'
    if os.path.exists(caminho_zip):
        with open(caminho_zip, "rb") as fp:
            st.download_button(label="📥 Baixar ZIP Original (Consumidor.gov)", data=fp, file_name="bases_consumidor.zip", mime="application/zip")
    else:
        st.error(f"Arquivo '{caminho_zip}' não foi encontrado na pasta do sistema para download.")

st.markdown(f'''<div style="text-align: center; margin-top: 56px; border-top: {borda_box} solid {border_color}; padding-top: 30px; padding-bottom: 14px; color: {text_muted}; font-size: 1.05em;"><strong style="font-size: 1.25em; letter-spacing: 0.02em;">Projeto Integrador I · Ciência da Computação · UniCEUB</strong><br><br><a href="https://github.com/CaioB1ima" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Caio Lima</a> | <a href="https://github.com/Gadshx" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Guilherme Augusto</a> | <a href="https://github.com/Gustavox0207" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Gustavo Albuquerque</a> | <a href="https://github.com/Lukithas" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Lucas Bretas</a> | <a href="https://github.com/Tweuz" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Mateus Onival</a></div>''', unsafe_allow_html=True)
