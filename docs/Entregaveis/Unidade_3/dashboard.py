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
# 1. CONFIGURAÇÃO DA PÁGINA E CSS SIMPLIFICADO
# =====================================================================
st.set_page_config(page_title="Ludopatia & BETs | PI", layout="wide", page_icon="📊")

st.sidebar.image("https://institucional.uniceub.br/hubfs/BrandCenter/img/logo-ceub-versao-estendida.png", width='stretch')
st.sidebar.title("Configurações")

# Limpa memória
plt.close('all')

# Força o estilo dos gráficos para terem sempre fundo branco e letras escuras.
# Assim, no Modo Escuro, os gráficos destacam-se como cartões iluminados e totalmente legíveis!
sns.set_theme(style="whitegrid", rc={
    "figure.facecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
    "text.color": "#1e293b",
    "axes.labelcolor": "#1e293b",
    "xtick.color": "#1e293b",
    "ytick.color": "#1e293b"
})

# CSS focado apenas na estrutura dos Cards
st.markdown('''
<style>
    .grafico-desc { 
        padding: 16px 20px; 
        border-radius: 8px; 
        border-left: 4px solid #a7197f; 
        margin-top: 12px; 
        margin-bottom: 24px; 
        font-size: 0.9rem; 
        line-height: 1.6; 
        border: 1px solid #e2e8f0; 
        opacity: 0.9;
        text-align: justify;
    }
    .grafico-desc strong { color: #a7197f !important; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 8px;}
    .kpi-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .kpi-box { padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; border-left: 5px solid #3b1054; }
    .kpi-box.danger { border-left-color: #ef4444; }
    .kpi-value { font-size: 2rem; font-weight: 700; margin: 0.5rem 0; }
    .kpi-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; opacity: 0.7; }
</style>
''', unsafe_allow_html=True)

st.sidebar.markdown("---")
filtro_genero = st.sidebar.multiselect("Filtrar por Gênero:", ['Masculino', 'Feminino'], default=['Masculino', 'Feminino'])
idade_slider = st.sidebar.slider("Faixa Etária:", 18, 65, (18, 65))
st.sidebar.markdown("---")

# =====================================================================
# 3. EXTRAÇÃO DE DADOS 
# =====================================================================

@st.cache_data(show_spinner="Carregando dados estatísticos...")
def get_data_estatistica():
    df_macro = pd.DataFrame([["Loterias", 71.3], ["Apostas Online (BETs)", 32.1], ["Jogo do Bicho", 28.9]], columns=["Categoria", "Valor"])
    df_bcb = pd.DataFrame({'Ano': range(2018, 2025), 'Inadimplencia': [3.1, 2.9, 2.7, 2.2, 2.7, 3.2, 3.1]})
    
    caminho_sus = 'dados_sus.csv'
    try:
        if os.path.exists(caminho_sus):
            df_pacientes = pd.read_csv(caminho_sus)
            return df_macro, df_bcb, df_pacientes, True
    except Exception as e:
        pass

    np.random.seed(42)
    df_pacientes = pd.DataFrame({'Idade': np.random.normal(28, 8, 500).astype(int), 'Renda_Mensal': np.random.lognormal(7.5, 0.6, 500), 'Divida_Acumulada': np.random.lognormal(7.5, 0.6, 500) * 2, 'Genero': np.random.choice(['Masculino', 'Feminino'], 500)})
    return df_macro, df_bcb, df_pacientes, False

@st.cache_data(show_spinner="Processando base de dados...")
def get_dados_consumidor_local():
    pasta_extracao = 'dados_consumidor_csvs'
    caminho_zip = 'bases_consumidor.zip'
    if os.path.exists(caminho_zip):
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref: zip_ref.extractall(pasta_extracao)
            arquivos_csv = glob.glob(os.path.join(pasta_extracao, "*.csv"))
            lista_dfs = [pd.read_csv(f, sep=';', encoding='utf-8', low_memory=False) for f in arquivos_csv]
            df_total = pd.concat(lista_dfs, ignore_index=True)
            filtro = df_total['Nome Fantasia'].str.contains('BET|APOSTA|CASSINO|BLAZE', case=False, na=False)
            df_bets = df_total[filtro]
            top_problemas = df_bets['Problema'].value_counts().head(5).reset_index()
            top_problemas.columns = ['Problema', 'Quantidade']
            return top_problemas, True
        except: pass
    return pd.DataFrame({'Problema': ['Saque', 'Publicidade', 'Bloqueio', 'Cobrança', 'Bônus'], 'Quantidade': [1450, 980, 750, 620, 410]}), False

@st.cache_data(show_spinner="Carregando pesquisa da equipe...")
def get_dados_consolidados_csv():
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

df_macro, df_bcb, df_pacientes, sus_encontrado = get_data_estatistica()
df_problemas, zip_encontrado = get_dados_consumidor_local()
df_consolidado, csv_encontrado = get_dados_consolidados_csv()

st.sidebar.subheader("Status das Bases de Dados")
if sus_encontrado: st.sidebar.success("✅ dados_sus.csv carregado!")
else: st.sidebar.warning("⚠️ SUS (CSV) não encontrado. Usando dados simulados.")
if zip_encontrado: st.sidebar.success("✅ bases_consumidor.zip carregado!")
else: st.sidebar.warning("⚠️ ZIP não encontrado. Usando dados simulados.")
if csv_encontrado: st.sidebar.success("✅ dados_apostas.csv carregado!")
else: st.sidebar.warning("⚠️ CSV não encontrado. Usando dados simulados.")

if not df_pacientes.empty:
    df_pacientes = df_pacientes[(df_pacientes['Genero'].isin(filtro_genero)) & (df_pacientes['Idade'].between(idade_slider[0], idade_slider[1]))]

# =====================================================================
# 4. DASHBOARD E GRÁFICOS
# =====================================================================
st.markdown("<h1>📊 Painel Analítico: Ludopatia & BETs</h1><p style='color: #64748b; font-size: 1.1rem;'>Análise técnica sobre o impacto das apostas online na estrutura socioeconômica.</p>", unsafe_allow_html=True)
st.markdown('''<div class="kpi-container"><div class="kpi-box danger"><div class="kpi-label">Apostadores Endividados</div><div class="kpi-value">86%</div><div class="kpi-label" style="text-transform:none">Fonte: Serasa/Locomotiva</div></div><div class="kpi-box danger"><div class="kpi-label">Ideação Suicida</div><div class="kpi-value">80%</div><div class="kpi-label" style="text-transform:none">Pacientes em Tratamento</div></div><div class="kpi-box"><div class="kpi-label">Volume Anual Estimado</div><div class="kpi-value">R$ 120 Bi</div><div class="kpi-label" style="text-transform:none">Mercado no Brasil</div></div><div class="kpi-box"><div class="kpi-label">Perfil Jovem</div><div class="kpi-value">56%</div><div class="kpi-label" style="text-transform:none">18 a 39 anos</div></div></div>''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Dashboard Visual", "🗄️ Bases de Dados Puras (Raw Data)"])

with tab1:
    def render_card(col, title, label, value, fig, desc):
        with col:
            with st.container(border=True):
                st.subheader(title)
                st.metric(label, value)
                fig.tight_layout()
                st.pyplot(fig, transparent=True, width='stretch')
                st.markdown(f'<div class="grafico-desc">{desc}</div>', unsafe_allow_html=True)
                plt.close(fig)

    col1, col2 = st.columns(2)
    
    # Gráfico 1
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_macro, x='Valor', y='Categoria', ax=ax1, palette="viridis")
    desc_1 = "<strong>Análise de Participação no Mercado:</strong> Embora as loterias tradicionais operadas pelo Estado ainda representem a maior parcela (71,3%), a rápida ascensão das Apostas Online (32,1%) demonstra como a histórica normalização cultural do jogo de azar no Brasil serviu como porta de entrada para plataformas digitais mais agressivas e acessíveis via smartphone."
    render_card(col1, "1. Modalidades Praticadas", "Liderança", "71.3%", fig1, desc_1)

    # Gráfico 2
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=df_bcb, x='Ano', y='Inadimplencia', ax=ax2, color='#ef4444', marker='o')
    desc_2 = "<strong>Análise Macroeconômica:</strong> O gráfico evidencia a correlação temporal entre a popularização das BETs (após a legalização em 2018 e o boom na pandemia) e a taxa média de inadimplência das famílias. A falsa promessa de renda extra alimenta o ciclo perigoso de 'chasing losses' (perseguição de perdas), resultando no comprometimento crônico do orçamento."
    render_card(col2, "2. Inadimplência Familiar", "Média Atual", "3.1%", fig2, desc_2)

    col3, col4 = st.columns(2)
    if not df_pacientes.empty:
        # Gráfico 3
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        sns.histplot(data=df_pacientes, x='Idade', kde=True, ax=ax3, color="#a7197f")
        desc_3 = "<strong>Análise Epidemiológica:</strong> A distribuição etária dos pacientes do SUS com diagnóstico de ludopatia (F63.0) revela uma forte prevalência entre adultos jovens (20 a 35 anos). Este grupo é o alvo principal do design comportamental das plataformas e do marketing de influenciadores, acelerando o desenvolvimento do transtorno mental."
        render_card(col3, "3. Perfil Etário de Risco", "Média", f"{int(df_pacientes['Idade'].mean())} anos", fig3, desc_3)

        # Gráfico 4
        fig4, ax4 = plt.subplots(figsize=(6, 3))
        sns.boxplot(data=df_pacientes, x='Genero', y='Divida_Acumulada', ax=ax4, palette="muted")
        desc_4 = "<strong>Análise de Endividamento por Gênero:</strong> O boxplot ilustra a disparidade na dispersão de dívidas. O público masculino apresenta maiores picos extremos de dívida acumulada, refletindo um comportamento de aposta de alto risco. Contudo, a desestruturação familiar gerada pelo vício impacta severamente e silenciosamente ambos os gêneros."
        render_card(col4, "4. Endividamento por Gênero", "Impacto", "Transversal", fig4, desc_4)

    col5, col6 = st.columns(2)
    if not df_pacientes.empty and 'Renda_Mensal' in df_pacientes.columns:
        # Gráfico 5
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        sns.scatterplot(data=df_pacientes, x='Renda_Mensal', y='Divida_Acumulada', hue='Genero', ax=ax5, palette="deep")
        desc_5 = "<strong>Análise de Vulnerabilidade:</strong> O gráfico de dispersão desmistifica a ideia de que a ludopatia afeta apenas as classes de baixa renda. Observa-se uma forte correlação positiva: quanto maior a renda, maior a dívida absoluta. O limite de crédito atua como um amplificador do vício estrutural."
        render_card(col5, "5. Renda vs Dívida Adquirida", "Correlação", "Direta", fig5, desc_5)

    # Gráfico 6
    fig6, ax6 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_problemas, x='Quantidade', y='Problema', ax=ax6, palette="flare")
    ax6.set_yticks(ax6.get_yticks())
    ax6.set_yticklabels([textwrap.fill(l.get_text(), 35) for l in ax6.get_yticklabels()], fontsize=8)
    desc_6 = "<strong>Análise de Experiência do Usuário (UX):</strong> A volumetria de queixas no Consumidor.gov.br destaca a 'Dificuldade de Saque' como problema central. Isso expõe a eficácia dos chamados 'dark patterns' de retenção: a plataforma dificulta o resgate para incentivar que o saldo seja apostado novamente até a perda total."
    render_card(col6, "6. Reclamações contra BETs", "Top", "Saque", fig6, desc_6)

    col7, col8 = st.columns(2)
    with col7:
        # Gráfico 7
        fig7, ax7 = plt.subplots(figsize=(6, 3))
        df_fin = df_consolidado[df_consolidado['Indicador'].str.contains('dívida|poupança|lazer|alimentação|renda|consequência|inadimplência', case=False, na=False)].copy()
        if not df_fin.empty:
            df_fin = df_fin[df_fin['Valor'] <= 100].sort_values(by='Valor', ascending=False).head(3)
            sns.barplot(data=df_fin, x='Indicador', y='Valor', ax=ax7, palette=["#ef4444", "#f59e0b", "#3b1054"])
            ax7.set_xticks(ax7.get_xticks())
            ax7.set_xticklabels([textwrap.fill(l.get_text(), 15) for l in ax7.get_xticklabels()], fontsize=8)
            ax7.set_ylim(0, 100)
        desc_7 = "<strong>Análise de Consequência Financeira:</strong> A pesquisa revela a face mais dura do vício: a dilapidação do patrimônio essencial. Ludopatas recorrem sistematicamente ao esvaziamento de poupanças (52%) e ao corte drástico de itens básicos da família como alimentação e lazer (48%) para financiar o transtorno."
        render_card(col7, "7. Drenagem do Orçamento", "Alerta", "Crítico", fig7, desc_7)

    with col8:
        # Gráfico 8
        fig8, ax8 = plt.subplots(figsize=(6, 3))
        df_sui = df_consolidado[df_consolidado['Indicador'].str.contains('suicida', case=False, na=False)].copy()
        if not df_sui.empty:
            sns.barplot(data=df_sui, x='Ano', y='Valor', ax=ax8, palette=["#f59e0b", "#ef4444"])
            ax8.set_ylim(0, 100)
        desc_8 = "<strong>Análise de Saúde Pública:</strong> Trata-se do indicador epidemiológico mais alarmante deste estudo. O expressivo salto de 27% (em 2018) para quase 80% (em 2025) na taxa de ideação suicida entre pacientes clínicos reflete o quão devastador é o colapso financeiro absoluto gerado pelas apostas."
        render_card(col8, "8. Risco Suicida Clínico", "Crescimento", "Exponencial", fig8, desc_8)

with tab2:
    @st.cache_data
    def convert_csv(df): return df.to_csv(index=False).encode('utf-8')
    
    st.markdown("### Bases de Dados Brutas / Tratadas")
    st.write("Faça o download dos arquivos utilizados na pesquisa:")
    
    st.subheader("1. Microdados Simulados (DataSUS - F63.0)")
    st.dataframe(df_pacientes, width='stretch')
    st.download_button("📥 Baixar Dados SUS (CSV)", data=convert_csv(df_pacientes), file_name='dados_sus.csv', mime='text/csv')
    
    st.markdown("---")
    st.subheader("2. Pesquisa Estruturada da Equipe")
    st.dataframe(df_consolidado, width='stretch')
    st.download_button("📥 Baixar Pesquisa da Equipe (CSV)", data=convert_csv(df_consolidado), file_name='dados_apostas_consolidado.csv', mime='text/csv')
    
    st.markdown("---")
    st.subheader("3. Base do Consumidor.gov.br (ZIP)")
    caminho_zip = 'bases_consumidor.zip'
    if os.path.exists(caminho_zip):
        with open(caminho_zip, "rb") as fp:
            st.download_button(label="📥 Baixar ZIP Original (Consumidor.gov)", data=fp, file_name="bases_consumidor.zip", mime="application/zip")
    else:
        st.info("O arquivo bases_consumidor.zip não está disponível.")

st.markdown('''<div style="text-align: center; margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 20px; color: #64748b; font-size: 0.85rem;"><strong>Projeto Integrador I - Ciência da Computação | UniCEUB</strong><br><br><a href="https://github.com/CaioB1ima" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Caio Lima</a> | <a href="https://github.com/Gadshx" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Guilherme Augusto</a> | <a href="https://github.com/Gustavox0207" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Gustavo Albuquerque</a> | <a href="https://github.com/Lukithas" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Lucas Bretas</a> | <a href="https://github.com/Tweuz" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Mateus Onival</a></div>''', unsafe_allow_html=True)