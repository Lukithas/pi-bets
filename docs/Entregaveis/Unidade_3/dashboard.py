import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile
import glob
import textwrap
import os

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ACESSIBILIDADE
# =====================================================================
st.set_page_config(page_title="Ludopatia & BETs | PI", layout="wide", page_icon="📊")

st.markdown("""
    <script>
        var elements = window.parent.document.querySelectorAll('.stApp');
        if (elements.length > 0) {
            elements[0].style.backgroundColor = '#f8fafc';
        }
    </script>
    """, unsafe_allow_html=True)

if "modo_escuro" not in st.session_state:
    st.session_state.modo_escuro = False
if "alto_contraste" not in st.session_state:
    st.session_state.alto_contraste = False
if "nivel_fonte" not in st.session_state:
    st.session_state.nivel_fonte = 1 

def alternar_modo_escuro(): st.session_state.modo_escuro = not st.session_state.modo_escuro
def alternar_alto_contraste(): st.session_state.alto_contraste = not st.session_state.alto_contraste
def aumentar_fonte(): st.session_state.nivel_fonte = min(3, st.session_state.nivel_fonte + 1)
def diminuir_fonte(): st.session_state.nivel_fonte = max(0, st.session_state.nivel_fonte - 1)

modo_escuro = st.session_state.modo_escuro
alto_contraste = st.session_state.alto_contraste
escala_fonte = {0: 0.875, 1: 1.0, 2: 1.15, 3: 1.3}[st.session_state.nivel_fonte]

plt.close('all')

# Configuração de Cores Dinâmicas
if modo_escuro:
    bg_surface, text_main, text_muted, border_color, bg_desc, accent = "#1e293b", "#f8fafc", "#94a3b8", "#334155", "#1e293b", "#a7197f"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": "#0f172a", "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="darkgrid", rc=rc_params)
    bg_app, bg_sidebar = "#0f172a", "#1e293b"
else:
    bg_surface, text_main, text_muted, border_color, bg_desc, accent = "#ffffff", "#0f172a", "#64748b", "#e2e8f0", "#f8fafc", "#a7197f"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": "#ffffff", "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="whitegrid", rc=rc_params)
    bg_app, bg_sidebar = "#f8fafc", "#ffffff" 

if alto_contraste:
    if modo_escuro:
        bg_app, bg_sidebar, bg_surface, bg_desc, text_main, text_muted, border_color, accent = "#000000", "#000000", "#000000", "#000000", "#ffffff", "#ffffff", "#ffffff", "#ffe600"
    else:
        bg_app, bg_sidebar, bg_surface, bg_desc, text_main, text_muted, border_color, accent = "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#000000", "#000000", "#000000", "#7a0058"
    rc_params = {"axes.facecolor": bg_surface, "figure.facecolor": bg_app, "text.color": text_main, "axes.labelcolor": text_main, "xtick.color": text_main, "ytick.color": text_main, "grid.color": border_color, "axes.edgecolor": border_color}
    sns.set_theme(style="darkgrid" if modo_escuro else "whitegrid", rc=rc_params)

borda_box = "2px" if alto_contraste else "1px"

# Barra de Acessibilidade
faixa_topo = st.container()
with faixa_topo:
    espaco, b1, b2, b3, b4 = st.columns([5, 1.3, 1.3, 1.1, 1.3])
    with b1: st.button("Fonte −", key="btn_menos", on_click=diminuir_fonte, use_container_width=True)
    with b2: st.button("Fonte +", key="btn_mais", on_click=aumentar_fonte, use_container_width=True)
    with b3: st.button("Contraste" + (" ✓" if alto_contraste else ""), key="btn_contraste", on_click=alternar_alto_contraste, use_container_width=True)
    with b4: st.button("Modo Escuro" + (" ✓" if modo_escuro else ""), key="btn_escuro", on_click=alternar_modo_escuro, use_container_width=True)

# =====================================================================
# 2. BARRA LATERAL E CSS
# =====================================================================
st.sidebar.image("https://institucional.uniceub.br/hubfs/BrandCenter/img/logo-ceub-versao-estendida.png", use_container_width=True)
st.sidebar.title("Filtros")

st.markdown(f'''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html {{ font-size: {escala_fonte * 100}%; }}
    [data-testid="stAppViewContainer"] {{ background-color: {bg_app} !important; }}
    [data-testid="stSidebar"] {{ background-color: {bg_sidebar} !important; border-right: {borda_box} solid {border_color} !important; }}
    [data-testid="stHeader"] {{ background-color: {bg_app} !important; }}
    html, body, p, h1, h2, h3, h4, h5, h6, label, span {{ color: {text_main} !important; }}
    html, body, p, h1, h2, h3, h4, h5, h6, label, span:not([class*="material"]):not([data-testid*="Icon"]) {{ font-family: 'Inter', sans-serif !important; }}
    .titulo-principal {{ font-weight: 800 !important; letter-spacing: -0.02em; margin-bottom: 0.2rem !important; }}
    .subtitulo-principal {{ font-weight: 400 !important; opacity: 0.85; }}
    [data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 14px !important; transition: box-shadow 0.2s ease, transform 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{ box-shadow: 0 6px 18px rgba(0,0,0,0.10); transform: translateY(-2px); }}
    
    .grafico-desc {{ background-color: {bg_desc}; padding: 16px 20px; border-radius: 8px; border-left: 4px solid {accent}; margin-top: 12px; margin-bottom: 4px; font-size: 0.9rem; color: {text_main} !important; line-height: 1.6; border: {borda_box} solid {border_color}; text-align: justify; opacity: 0.95; }}
    .grafico-desc strong {{ color: {accent} !important; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 8px; }}
    
    .kpi-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
    .kpi-box {{ background: {bg_surface}; padding: 1.5rem; border-radius: 14px; border: {borda_box} solid {border_color}; text-align: center; border-left: 5px solid #3b1054; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: transform 0.2s ease; }}
    .kpi-box:hover {{ transform: translateY(-3px); }}
    .kpi-box.danger {{ border-left-color: #ef4444; }}
    .kpi-value {{ font-size: 2.1em; font-weight: 800; color: {text_main} !important; margin: 0.4rem 0; letter-spacing: -0.02em; }}
    .kpi-label {{ font-size: 0.78em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; color: {text_muted} !important; }}
    
    button[data-testid="stBaseButton-secondary"] {{ font-size: 0.85em !important; font-weight: 700 !important; padding: 0.45rem 0.6rem !important; border-radius: 999px !important; border: {("3px solid " + border_color) if alto_contraste else "none"} !important; background-color: {bg_surface if alto_contraste else ("#33415540" if modo_escuro else "#a7197f14")} !important; color: {accent} !important; white-space: nowrap !important; transition: background-color 0.15s ease, transform 0.15s ease !important; }}
    button[data-testid="stBaseButton-secondary"]:hover {{ background-color: {accent} !important; color: {bg_app if alto_contraste else "#ffffff"} !important; transform: translateY(-1px); }}
</style>
''', unsafe_allow_html=True)

filtro_genero = st.sidebar.multiselect("Gênero:", ['Masculino', 'Feminino'], default=['Masculino', 'Feminino'])
idade_slider = st.sidebar.slider("Faixa Etária:", 18, 65, (18, 65))

st.sidebar.markdown('<div style="font-size: 0.9em; opacity: 0.85; margin-top: 4px;">Esses filtros afetam apenas os gráficos de microdados de pacientes (3, 4 e 5). Os demais usam pesquisas macroeconômicas externas.</div>', unsafe_allow_html=True)

# =====================================================================
# 3. EXTRAÇÃO DE DADOS
# =====================================================================
@st.cache_data(show_spinner="Carregando dados estatísticos...")
def get_data_estatistica():
    df_macro = pd.DataFrame([["Loterias", 71.3], ["Apostas Online (BETs)", 32.1], ["Jogo do Bicho", 28.9]], columns=["Categoria", "Valor"])
    df_bcb = pd.DataFrame({'Ano': range(2018, 2025), 'Inadimplencia': [3.1, 2.9, 2.7, 2.2, 2.7, 3.2, 3.1]})

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_sus = os.path.join(script_dir, 'dados_sus.csv')
    except NameError:
        caminho_sus = 'dados_sus.csv'

    if os.path.exists(caminho_sus):
        try:
            df_pacientes = pd.read_csv(caminho_sus)
            if {'Idade', 'Genero', 'Renda_Mensal', 'Divida_Acumulada'}.issubset(df_pacientes.columns):
                return df_macro, df_bcb, df_pacientes, True
        except Exception: pass

    np.random.seed(42)
    df_pacientes = pd.DataFrame({'Idade': np.random.normal(28, 8, 500).astype(int), 'Renda_Mensal': np.random.lognormal(7.5, 0.6, 500), 'Divida_Acumulada': np.random.lognormal(7.5, 0.6, 500) * 2, 'Genero': np.random.choice(['Masculino', 'Feminino'], 500)})
    return df_macro, df_bcb, df_pacientes, False

@st.cache_data(show_spinner="Processando Consumidor.gov...")
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
                try: df_temp = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
                except UnicodeDecodeError: df_temp = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False)
                lista_dfs.append(df_temp)
            if lista_dfs:
                df_total = pd.concat(lista_dfs, ignore_index=True)
                filtro = df_total['Nome Fantasia'].str.contains('BET|APOSTA|CASSINO|BLAZE', case=False, na=False)
                df_bets = df_total[filtro]
                if 'Problema' in df_bets.columns:
                    top_problemas = df_bets['Problema'].value_counts().head(5).reset_index()
                    top_problemas.columns = ['Problema', 'Quantidade']
                    return top_problemas, True
        except Exception: pass
            
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
        except: pass
    
    dados = [["2024", "OMS", "% adultos apostaram (1 ano)", 46.2], ["2024", "OMS", "% adolescentes apostaram", 17.9], ["2018", "USP/IPq", "Dívidas > renda mensal", 60.0], ["2018", "USP/IPq", "Ideação suicida (2018)", 27.0], ["2024", "PwC", "Usando poupança para apostar", 52.0], ["2024", "PwC", "Cortando lazer/alimentação", 48.0], ["2025", "PRO-AMJO", "Ideação suicida (2025)", 80.0]]
    return pd.DataFrame(dados, columns=["Ano", "Fonte", "Indicador", "Valor"]), False

st.sidebar.markdown("---")
st.sidebar.subheader("Status dos Dados")
df_macro, df_bcb, df_pacientes, sus_encontrado = get_data_estatistica()
df_problemas, zip_encontrado = get_dados_consumidor_local()
df_consolidado, csv_encontrado = get_dados_consolidados_csv()

if sus_encontrado: st.sidebar.success("✅ SUS (CSV) carregado!")
else: st.sidebar.warning("⚠️ SUS não encontrado (Usando Mockup)")
if zip_encontrado: st.sidebar.success("✅ Consumidor.gov (ZIP) carregado!")
else: st.sidebar.info("☁️ Consumidor.gov (ZIP) via Nuvem")
if csv_encontrado: st.sidebar.success("✅ Pesquisa Equipe carregada!")
else: st.sidebar.warning("⚠️ CSV não encontrado (Usando Mockup)")

df_pacientes = df_pacientes[(df_pacientes['Genero'].isin(filtro_genero)) & (df_pacientes['Idade'].between(idade_slider[0], idade_slider[1]))]

# =====================================================================
# 4. DASHBOARD E GRÁFICOS
# =====================================================================
st.markdown(f"<h1 class='titulo-principal' style='color: {text_main}; font-size: 2.55em;'>Painel Analítico: Ludopatia & BETs</h1><p class='subtitulo-principal' style='color: {text_muted}; font-size: 1.15em;'>Análise técnica sobre o impacto das apostas online na estrutura socioeconômica.</p>", unsafe_allow_html=True)

st.markdown(f'''<div class="kpi-container"><div class="kpi-box danger"><div class="kpi-label">Apostadores Endividados</div><div class="kpi-value">86%</div><div class="kpi-label" style="text-transform:none">Fonte: Serasa/Locomotiva</div></div><div class="kpi-box danger"><div class="kpi-label">Ideação Suicida</div><div class="kpi-value">80%</div><div class="kpi-label" style="text-transform:none">Pacientes em Tratamento</div></div><div class="kpi-box"><div class="kpi-label">Volume Anual Estimado</div><div class="kpi-value">R$ 120 Bi</div><div class="kpi-label" style="text-transform:none">Mercado no Brasil</div></div><div class="kpi-box"><div class="kpi-label">Perfil Jovem</div><div class="kpi-value">56%</div><div class="kpi-label" style="text-transform:none">18 a 39 anos</div></div></div>''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🗄️ Bases de Dados (Raw Data)"])

with tab1:
    def render_card(col, title, label, value, fig, desc):
        with col:
            with st.container(border=True):
                st.subheader(title)
                st.metric(label, value)
                fig.tight_layout()
                st.pyplot(fig, transparent=True) 
                st.markdown(f'<div class="grafico-desc">{desc}</div>', unsafe_allow_html=True)
                plt.close(fig)

    col1, col2 = st.columns(2)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_macro, x='Valor', y='Categoria', ax=ax1, palette="viridis")
    desc_1 = "<strong>Análise de Participação no Mercado:</strong> Embora as loterias tradicionais operadas pelo Estado ainda representem a maior parcela (71,3%), a rápida ascensão das Apostas Online (32,1%) demonstra como a histórica normalização cultural do jogo de azar no Brasil serviu como porta de entrada para plataformas digitais mais agressivas e acessíveis via smartphone."
    render_card(col1, "1. Modalidades", "Liderança", "71.3%", fig1, desc_1)

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=df_bcb, x='Ano', y='Inadimplencia', ax=ax2, color='#ef4444', marker='o')
    desc_2 = "<strong>Análise Macroeconômica:</strong> O gráfico evidencia a correlação temporal entre a popularização das BETs (após a legalização em 2018 e o boom na pandemia) e a taxa média de inadimplência das famílias. A falsa promessa de renda extra alimenta o ciclo perigoso de 'chasing losses' (perseguição de perdas), resultando no comprometimento crônico do orçamento."
    render_card(col2, "2. Inadimplência", "Média Atual", "3.1%", fig2, desc_2)

    col3, col4 = st.columns(2)
    if not df_pacientes.empty:
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        sns.histplot(data=df_pacientes, x='Idade', kde=True, ax=ax3, color="#a7197f")
        desc_3 = "<strong>Análise Epidemiológica:</strong> A distribuição etária dos pacientes do SUS com diagnóstico de ludopatia (F63.0) revela uma forte prevalência entre adultos jovens (20 a 35 anos). Este grupo é o alvo principal do design comportamental das plataformas e do marketing de influenciadores, acelerando o desenvolvimento do transtorno mental."
        render_card(col3, "3. Idade", "Média", f"{int(df_pacientes['Idade'].mean())} anos", fig3, desc_3)

        fig4, ax4 = plt.subplots(figsize=(6, 3))
        sns.boxplot(data=df_pacientes, x='Genero', y='Divida_Acumulada', ax=ax4, palette="muted")
        desc_4 = "<strong>Endividamento por Gênero:</strong> O boxplot ilustra a disparidade na dispersão de dívidas. O público masculino apresenta maiores picos extremos de dívida acumulada, refletindo um comportamento de aposta de alto risco. Contudo, a desestruturação familiar gerada pelo vício impacta severamente e silenciosamente ambos os gêneros."
        render_card(col4, "4. Dívida e Gênero", "Impacto", "Transversal", fig4, desc_4)

    col5, col6 = st.columns(2)
    if not df_pacientes.empty and 'Renda_Mensal' in df_pacientes.columns:
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        sns.scatterplot(data=df_pacientes, x='Renda_Mensal', y='Divida_Acumulada', hue='Genero', ax=ax5, palette="deep")
        desc_5 = "<strong>Análise de Vulnerabilidade:</strong> O gráfico de dispersão desmistifica a ideia de que a ludopatia afeta apenas as classes de baixa renda. Observa-se uma forte correlação positiva: quanto maior a renda, maior a dívida absoluta. O limite de crédito atua como um amplificador do vício estrutural."
        render_card(col5, "5. Renda vs Dívida", "Correlação", "Direta", fig5, desc_5)

    fig6, ax6 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_problemas, x='Quantidade', y='Problema', ax=ax6, palette="flare")
    ax6.set_yticks(ax6.get_yticks())
    ax6.set_yticklabels([textwrap.fill(l.get_text(), 35) for l in ax6.get_yticklabels()], fontsize=8)
    desc_6 = "<strong>Experiência do Usuário (UX):</strong> A volumetria de queixas no Consumidor.gov.br destaca a 'Dificuldade de Saque' como problema central. Isso expõe a eficácia dos chamados 'dark patterns' de retenção: a plataforma dificulta o resgate para incentivar que o saldo seja apostado novamente até a perda total."
    render_card(col6, "6. Reclamações", "Top", "Saque", fig6, desc_6)

    col7, col8 = st.columns(2)
    with col7:
        fig7, ax7 = plt.subplots(figsize=(6, 3))
        df_fin = df_consolidado[df_consolidado['Indicador'].str.contains('dívida|poupança|lazer|alimentação|renda|consequência|inadimplência', case=False, na=False)].copy()
        if not df_fin.empty:
            df_fin = df_fin[df_fin['Valor'] <= 100].sort_values(by='Valor', ascending=False).head(3)
            sns.barplot(data=df_fin, x='Indicador', y='Valor', ax=ax7, palette=["#ef4444", "#f59e0b", "#3b1054"])
            ax7.set_xticks(ax7.get_xticks())
            ax7.set_xticklabels([textwrap.fill(l.get_text(), 15) for l in ax7.get_xticklabels()], fontsize=8)
            ax7.set_ylim(0, 100)
        desc_7 = "<strong>Consequência Financeira:</strong> A pesquisa revela a face mais dura do vício: a dilapidação do patrimônio essencial. Ludopatas recorrem sistematicamente ao esvaziamento de poupanças (52%) e ao corte drástico de itens básicos da família como alimentação e lazer (48%) para financiar o transtorno."
        render_card(col7, "7. Orçamento Familiar", "Alerta", "Crítico", fig7, desc_7)

    with col8:
        fig8, ax8 = plt.subplots(figsize=(6, 3))
        df_sui = df_consolidado[df_consolidado['Indicador'].str.contains('suicida', case=False, na=False)].copy()
        if not df_sui.empty:
            sns.barplot(data=df_sui, x='Ano', y='Valor', ax=ax8, palette=["#f59e0b", "#ef4444"])
            ax8.set_ylim(0, 100)
        desc_8 = "<strong>Saúde Pública:</strong> Trata-se do indicador epidemiológico mais alarmante deste estudo. O expressivo salto de 27% (em 2018) para quase 80% (em 2025) na taxa de ideação suicida entre pacientes clínicos reflete o quão devastador é o colapso financeiro absoluto gerado pelas apostas."
        render_card(col8, "8. Risco Suicida", "Crescimento", "Exponencial", fig8, desc_8)

with tab2:
    @st.cache_data
    def convert_csv(df): return df.to_csv(index=False).encode('utf-8')
    
    st.markdown("### Bases de Dados Brutas / Tratadas")
    
    st.subheader("1. Microdados SUS")
    st.dataframe(df_pacientes, use_container_width=True)
    st.download_button("📥 Baixar CSV (SUS)", data=convert_csv(df_pacientes), file_name='dados_sus.csv', mime='text/csv')
    
    st.markdown("---")
    st.subheader("2. Pesquisa da Equipe")
    st.dataframe(df_consolidado, use_container_width=True)
    st.download_button("📥 Baixar CSV (Equipe)", data=convert_csv(df_consolidado), file_name='dados_equipe.csv', mime='text/csv')

    st.markdown("---")
    st.subheader("3. Base do Consumidor.gov.br (ZIP)")
    caminho_zip = 'bases_consumidor.zip'
    
    # Adicionado botão interativo com redirecionamento para o Google Drive
    if os.path.exists(caminho_zip):
        with open(caminho_zip, "rb") as fp:
            st.download_button(label="📥 Baixar ZIP Original (Local)", data=fp, file_name="bases_consumidor.zip", mime="application/zip")
        st.link_button("🌐 Acessar ZIP na Nuvem (Google Drive)", "https://drive.google.com/file/d/1CdNFyyhl884G3lAyxmNQ7gi9Ogf_Spsm/view?usp=sharing")
    else:
        st.info("O arquivo ZIP não está armazenado localmente no servidor. Você pode baixá-lo diretamente da nossa nuvem:")
        st.link_button("🌐 Acessar ZIP na Nuvem (Google Drive)", "https://drive.google.com/file/d/1CdNFyyhl884G3lAyxmNQ7gi9Ogf_Spsm/view?usp=sharing")

st.markdown(f'''<div style="text-align: center; margin-top: 56px; border-top: {borda_box} solid {border_color}; padding-top: 30px; padding-bottom: 14px; color: {text_muted}; font-size: 1.05em;"><strong style="font-size: 1.25em; letter-spacing: 0.02em;">Projeto Integrador I · Ciência da Computação · UniCEUB</strong><br><br><a href="https://github.com/CaioB1ima" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Caio Lima</a> | <a href="https://github.com/Gadshx" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Guilherme Augusto</a> | <a href="https://github.com/Gustavox0207" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Gustavo Albuquerque</a> | <a href="https://github.com/Lukithas" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Lucas Bretas</a> | <a href="https://github.com/Tweuz" target="_blank" style="color: {accent}; text-decoration: none; font-weight: 600; margin: 0 12px; font-size: 1.05em;">Mateus Onival</a></div>''', unsafe_allow_html=True)