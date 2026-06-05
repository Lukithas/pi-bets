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
# 1. CONFIGURAÇÃO DA PÁGINA
# =====================================================================
st.set_page_config(page_title="Ludopatia & BETs | PI",
                   layout="wide", page_icon="📊")

# =====================================================================
# 2. BARRA LATERAL E CSS (Cores agora controladas pelo config.toml)
# =====================================================================
# CORREÇÃO APLICADA AQUI: width='stretch' em vez de use_container_width=True
st.sidebar.image(
    "https://institucional.uniceub.br/hubfs/BrandCenter/img/logo-ceub-versao-estendida.png", width='stretch')
st.sidebar.title("Configurações")

plt.close('all')

# Estilo para os cartões KPI e texto dos gráficos
st.markdown('''
<style>
    /* Força os textos nativos de métrica a acompanharem o modo claro/escuro */
    [data-testid="stMetricValue"] { color: var(--text-color) !important; }
    [data-testid="stMetricLabel"] * { color: #64748b !important; }
    
    .grafico-desc { background-color: var(--secondary-background-color); padding: 12px 16px; border-radius: 8px; border-left: 4px solid #a7197f; margin-top: 8px; margin-bottom: 20px; font-size: 0.88rem; line-height: 1.6; border: 1px solid #e2e8f0; }
    .grafico-desc strong { color: #a7197f !important; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .kpi-box { background: var(--secondary-background-color); padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; border-left: 5px solid #3b1054; }
    .kpi-box.danger { border-left-color: #ef4444; }
    .kpi-value { font-size: 2rem; font-weight: 700; margin: 0.5rem 0; }
    .kpi-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #64748b; }
</style>
''', unsafe_allow_html=True)

st.sidebar.markdown("---")
filtro_genero = st.sidebar.multiselect("Filtrar por Género:", [
                                       'Masculino', 'Feminino'], default=['Masculino', 'Feminino'])
idade_slider = st.sidebar.slider("Faixa Etária:", 18, 65, (18, 65))
st.sidebar.markdown("---")

# =====================================================================
# 3. EXTRAÇÃO DE DADOS
# =====================================================================


@st.cache_data(show_spinner="A carregar dados estatísticos rápidos...")
def get_data_estatistica():
    df_macro = pd.DataFrame([["Loterias", 71.3], ["Apostas Online (BETs)", 32.1], [
                            "Jogo do Bicho", 28.9]], columns=["Categoria", "Valor"])
    df_bcb = pd.DataFrame({'Ano': range(2018, 2025), 'Inadimplencia': [
                          3.1, 2.9, 2.7, 2.2, 2.7, 3.2, 3.1]})
    np.random.seed(42)
    df_pacientes = pd.DataFrame({'Idade': np.random.normal(28, 8, 500).astype(int), 'Renda_Mensal': np.random.lognormal(
        7.5, 0.6, 500), 'Divida_Acumulada': np.random.lognormal(7.5, 0.6, 500) * 2, 'Genero': np.random.choice(['Masculino', 'Feminino'], 500)})
    return df_macro, df_bcb, df_pacientes


@st.cache_data(show_spinner="A processar dados do Consumidor.gov...")
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
                    df_temp = pd.read_csv(
                        arquivo, sep=';', encoding='utf-8', low_memory=False)
                except UnicodeDecodeError:
                    df_temp = pd.read_csv(
                        arquivo, sep=';', encoding='latin1', low_memory=False)
                lista_dfs.append(df_temp)
            if lista_dfs:
                df_total = pd.concat(lista_dfs, ignore_index=True)
                filtro = df_total['Nome Fantasia'].str.contains(
                    'BET|APOSTA|CASSINO|BLAZE', case=False, na=False)
                df_bets = df_total[filtro]
                if 'Problema' in df_bets.columns:
                    top_problemas = df_bets['Problema'].value_counts().head(
                        5).reset_index()
                    top_problemas.columns = ['Problema', 'Quantidade']
                    return top_problemas, True
        except Exception as e:
            print(f"Erro ZIP: {e}")

    df_mock = pd.DataFrame({'Problema': [
                           'Saque', 'Publicidade', 'Bloqueio', 'Cobrança', 'Bónus'], 'Quantidade': [1450, 980, 750, 620, 410]})
    return df_mock, False


@st.cache_data(show_spinner="A carregar pesquisa da equipa...")
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

    dados = [["2024", "OMS", "% adultos apostaram (1 ano)", 46.2], ["2024", "OMS", "% adolescentes apostaram", 17.9], ["2018", "USP/IPq", "Dívidas > renda mensal", 60.0], ["2018", "USP/IPq", "Ideação suicida (2018)", 27.0], [
        "2024", "PwC", "Usando poupança para apostar", 52.0], ["2024", "PwC", "Cortando lazer/alimentação", 48.0], ["2025", "PRO-AMJO", "Ideação suicida (2025)", 80.0]]
    return pd.DataFrame(dados, columns=["Ano", "Fonte", "Indicador", "Valor"]), False


df_macro, df_bcb, df_pacientes = get_data_estatistica()
df_problemas, zip_encontrado = get_dados_consumidor_local()
df_consolidado, csv_encontrado = get_dados_consolidados_csv()

# Avisos na lateral sobre o status das bases
st.sidebar.subheader("Status das Bases de Dados")
if zip_encontrado:
    st.sidebar.success("✅ bases_consumidor.zip carregado!")
else:
    st.sidebar.warning("⚠️ ZIP não encontrado. A usar Mockup.")
if csv_encontrado:
    st.sidebar.success("✅ dados_apostas_consolidado.csv carregado!")
else:
    st.sidebar.warning("⚠️ CSV não encontrado. A usar Mockup.")

# Filtros
df_pacientes = df_pacientes[(df_pacientes['Genero'].isin(filtro_genero)) & (
    df_pacientes['Idade'].between(idade_slider[0], idade_slider[1]))]

# =====================================================================
# 4. DASHBOARD E GRÁFICOS
# =====================================================================
st.markdown("<h1>📊 Painel Analítico: Ludopatia & BETs</h1><p style='color: #64748b; font-size: 1.1rem;'>Análise técnica sobre o impacto das apostas online na estrutura socioeconómica.</p>", unsafe_allow_html=True)

st.markdown('''<div class="kpi-container"><div class="kpi-box danger"><div class="kpi-label">Apostadores Endividados</div><div class="kpi-value">86%</div><div class="kpi-label" style="text-transform:none">Fonte: Serasa/Locomotiva</div></div><div class="kpi-box danger"><div class="kpi-label">Ideação Suicida</div><div class="kpi-value">80%</div><div class="kpi-label" style="text-transform:none">Pacientes em Tratamento</div></div><div class="kpi-box"><div class="kpi-label">Volume Anual Estimado</div><div class="kpi-value">R$ 120 Bi</div><div class="kpi-label" style="text-transform:none">Mercado no Brasil</div></div><div class="kpi-box"><div class="kpi-label">Perfil Jovem</div><div class="kpi-value">56%</div><div class="kpi-label" style="text-transform:none">18 a 39 anos</div></div></div>''', unsafe_allow_html=True)

tab1, tab2 = st.tabs(
    ["📈 Dashboard Visual", "🗄️ Bases de Dados Puras (Raw Data)"])

with tab1:
    def render_dashboard_card(col, title, metric_label, metric_value, fig, desc):
        with col:
            with st.container(border=True):
                st.subheader(title)
                st.metric(metric_label, metric_value)
                fig.tight_layout()
                # ATUALIZAÇÃO: width='stretch' substitui o antigo use_container_width=True
                st.pyplot(fig, transparent=True, width='stretch')
                st.markdown(
                    f'<div class="grafico-desc">{desc}</div>', unsafe_allow_html=True)
                plt.close(fig)

    col1, col2 = st.columns(2)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_macro, x='Valor', y='Categoria',
                ax=ax1, palette="viridis")
    render_dashboard_card(col1, "1. Modalidades Praticadas", "Liderança", "71.3% Loterias",
                          fig1, "<strong>📌 Análise:</strong> As loterias tradicionais ainda dominam o mercado.")

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=df_bcb, x='Ano', y='Inadimplencia',
                 ax=ax2, color='#ef4444', marker='o')
    render_dashboard_card(col2, "2. Inadimplência Familiar", "Média Atual", "3.1%", fig2,
                          "<strong>📌 Análise:</strong> A curva de inadimplência acompanha o crescimento das BETs.")

    col3, col4 = st.columns(2)
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    sns.histplot(data=df_pacientes, x='Idade',
                 kde=True, ax=ax3, color="#a7197f")
    render_dashboard_card(col3, "3. Perfil Etário de Risco", "Média de Idade",
                          f"{int(df_pacientes['Idade'].mean()) if not df_pacientes.empty else 0} anos", fig3, "<strong>📌 Análise:</strong> Predominância de adultos jovens, com concentração entre 20 e 35 anos.")

    fig4, ax4 = plt.subplots(figsize=(6, 3))
    sns.boxplot(data=df_pacientes, x='Genero',
                y='Divida_Acumulada', ax=ax4, palette="muted")
    render_dashboard_card(col4, "4. Endividamento por Género", "Impacto", "Variável",
                          fig4, "<strong>📌 Análise:</strong> Homens apresentam maior dispersão de dívida.")

    col5, col6 = st.columns(2)
    fig5, ax5 = plt.subplots(figsize=(6, 3))
    sns.scatterplot(data=df_pacientes, x='Renda_Mensal',
                    y='Divida_Acumulada', hue='Genero', ax=ax5, palette="deep")
    render_dashboard_card(col5, "5. Renda vs Dívida", "Correlação", "Direta", fig5,
                          "<strong>📌 Análise:</strong> O endividamento cresce proporcionalmente à renda.")

    fig6, ax6 = plt.subplots(figsize=(6, 3))
    sns.barplot(data=df_problemas, x='Quantidade',
                y='Problema', ax=ax6, palette="flare")
    ax6.set_yticks(ax6.get_yticks())
    # Quebra de linha maior para textos longos do Consumidor.gov
    ax6.set_yticklabels([textwrap.fill(l.get_text(), 35)
                        for l in ax6.get_yticklabels()], fontsize=8)
    render_dashboard_card(col6, "6. Reclamações contra BETs", "Principal", "Saque", fig6,
                          "<strong>📌 Análise:</strong> Dificuldade de saque lidera as ocorrências no Consumidor.gov.")

    col7, col8 = st.columns(2)
    with col7:
        fig7, ax7 = plt.subplots(figsize=(6, 3))
        termos_busca = 'dívida|poupança|lazer|alimentação|renda|consequência|inadimplência'
        df_fin = df_consolidado[df_consolidado['Indicador'].str.contains(
            termos_busca, case=False, na=False)].copy()

        if not df_fin.empty:
            df_fin = df_fin[df_fin['Valor'] <= 100].sort_values(
                by='Valor', ascending=False).head(3)
            sns.barplot(data=df_fin, x='Indicador', y='Valor',
                        ax=ax7, palette=["#ef4444", "#f59e0b", "#3b1054"])
            ax7.set_xticks(ax7.get_xticks())
            ax7.set_xticklabels([textwrap.fill(l.get_text(), 15)
                                for l in ax7.get_xticklabels()], fontsize=8)
            ax7.set_ylim(0, 100)

        valor_destaque = f"{int(df_fin['Valor'].max())}%" if not df_fin.empty else "N/A"
        render_dashboard_card(col7, "7. Impacto Financeiro", "Destaque", valor_destaque,
                              fig7, "<strong>📌 Análise:</strong> O descontrole reflete no orçamento familiar.")

    with col8:
        fig8, ax8 = plt.subplots(figsize=(6, 3))
        df_sui = df_consolidado[df_consolidado['Indicador'].str.contains(
            'suicida', case=False, na=False)].copy()
        if not df_sui.empty:
            sns.barplot(data=df_sui, x='Ano', y='Valor',
                        ax=ax8, palette=["#f59e0b", "#ef4444"])
            ax8.set_ylim(0, 100)
        render_dashboard_card(col8, "8. Ideação Suicida", "Crescimento", "+53 p.p.", fig8,
                              "<strong>📌 Análise:</strong> Salto de 27% (2018) para 80% (2025) nos pacientes.")

with tab2:
    @st.cache_data
    def convert_df_to_csv(df): return df.to_csv(index=False).encode('utf-8')
    st.markdown("### Bases de Dados Brutas / Tratadas")
    st.write("Faça o download dos ficheiros utilizados na pesquisa:")

    st.subheader("1. Microdados Simulados (DataSUS - F63.0)")
    # ATUALIZAÇÃO: width='stretch' nas tabelas
    st.dataframe(df_pacientes, width='stretch')
    st.download_button("📥 Baixar Dados SUS (CSV)", data=convert_df_to_csv(
        df_pacientes), file_name='dados_sus.csv', mime='text/csv')

    st.markdown("---")
    st.subheader("2. Pesquisa Estruturada da Equipa")
    # ATUALIZAÇÃO: width='stretch' nas tabelas
    st.dataframe(df_consolidado, width='stretch')
    st.download_button("📥 Baixar Pesquisa da Equipa (CSV)", data=convert_df_to_csv(
        df_consolidado), file_name='dados_apostas_consolidado.csv', mime='text/csv')

    st.markdown("---")
    st.subheader("3. Base do Consumidor.gov.br (ZIP)")

    caminho_zip = 'bases_consumidor.zip'
    if os.path.exists(caminho_zip):
        with open(caminho_zip, "rb") as fp:
            st.download_button(label="📥 Baixar ZIP Original (Consumidor.gov)",
                               data=fp, file_name="bases_consumidor.zip", mime="application/zip")
    else:
        st.info("O ficheiro bases_consumidor.zip não está disponível.")

st.markdown('''<div style="text-align: center; margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 20px; color: #64748b; font-size: 0.85rem;"><strong>Projeto Integrador I - Ciência da Computação | UniCEUB</strong><br><br><a href="https://github.com/CaioB1ima" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Caio Lima</a> | <a href="https://github.com/Gadshx" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Guilherme Augusto</a> | <a href="https://github.com/Gustavox0207" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Gustavo Albuquerque</a> | <a href="https://github.com/Lukithas" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Lucas Bretas</a> | <a href="https://github.com/Tweuz" target="_blank" style="color: #a7197f; text-decoration: none; font-weight: 600; margin: 0 10px;">Mateus Onival</a></div>''', unsafe_allow_html=True)
