# 📊 PI-BETS: Análise do Impacto Econômico das Apostas Online no Endividamento Familiar

> Projeto Integrador I — Ciência da Computação | **UniCEUB** (5º Semestre)

## 🎯 Sobre o Projeto

Investigação acadêmica focada no cruzamento de dados entre **apostas online** e **endividamento doméstico**. Este estudo busca validar a hipótese do vício mediado pela **tecnologia (IHC)** e pela **facilidade do Pix**, analisando a perda da estabilidade financeira e da renda básica familiar.

**Tema Central:** O Impacto Econômico das Plataformas de Apostas (Bets) no Endividamento Familiar

---

## 🔗 Links Rápidos

| Recurso | Link de Acesso |
| :--- | :--- |
| **Apresentação do Projeto** | [ihcbets.netlify.app](https://ihcbets.netlify.app/) |
| **Backlog do Projeto** | [backlogpibets.netlify.app](https://backlogpibets.netlify.app/) |
| **Dashboard Interativo** | [pi-bets-site-dashboard.streamlit.app](https://pi-bets-site-dashboard.streamlit.app/) |

---

## 📋 Propósito e Escopo

O foco deste semestre é a **"resolução de problemas complexos"** por meio de investigação profunda do cenário atual. Existe uma lacuna no entendimento sobre o impacto real da facilidade de acesso às apostas.

**Entrega Principal:** Um **Dashboard Interativo** embasado em "modelagem estatística e desenvolvimento de indicadores (KPIs)", que comprova a viabilidade e a necessidade de projetar uma solução tecnológica futura.

---

## 🎯 Funcionalidades do Dashboard

- **📈 Análise Macro** — Evolução da inadimplência cruzada com dados do Banco Central (SGS)
- **🏥 Perfil Epidemiológico** — Filtros dinâmicos simulando microdados do DataSUS (CID-10 F63.0)
- **🔍 Mineração de Dados (Batch)** — Processamento em lote de arquivos `.csv` do portal Consumidor.gov.br
- **🎨 Design IHC** — Interface adaptativa, modo escuro nativo e design comportamental

---

## 🔬 Abordagem Metodológica

Para identificar as necessidades reais dos usuários e o escopo do problema, aplicamos conceitos de **Lean Inception** e **métodos ágeis**:

- **Descoberta:** Levantar os gatilhos comportamentais (como a ilusão de renda extra) que incentivam o uso contínuo
- **Delimitação:** Isolar a correlação entre facilidade de pagamentos digitais e comprometimento do or��amento doméstico

---

## 🚨 Problemas Identificados

### Gamificação do Dinheiro

| Problema | Descrição |
|:---|:---|
| **Liquidez Imediata (O Fator Pix)** | Ausência de atrito nas transações instantâneas diminui o tempo de decisão racional |
| **Fuga da Realidade vs. Investimento** | Distorção cognitiva onde o usuário vê a plataforma como ferramenta de alavancagem financeira |
| **Privacidade e Segurança** | Desafio de estruturar pesquisas e tratar dados comportamentais e financeiros sensíveis |

---

## 🌱 Relevância Socioeconômica (ODS)

O projeto atende aos requisitos de **Atividades Curriculares de Extensão (ACE)** e alinha-se com:

- **ODS 1 (Erradicação da Pobreza):** Investigar como o volume de capital drenado pelas plataformas afeta o poder de compra
- **ODS 3 (Saúde e Bem-Estar):** Abordar o vício em apostas (ludopatia) potencializado pelo acesso mobile

---

## 📊 Coleta e Transformação de Dados

### Fontes de Dados

- **Banco Central do Brasil** - Volume de transações via Pix para CNPJs de apostas
- **Serasa/SP** - Índices de inadimplência
- **DataSUS** - Microdados epidemiológicos (CID-10 F63.0)
- **Consumidor.gov.br** - Dados públicos de reclamações
- **Ministério da Fazenda** - Diretrizes regulatórias do setor

---

## ⚙️ Pré-requisitos

- **Python 3.11** ou **3.12**
- **Git LFS** (para arquivos grandes)

> ⚠️ **Usuários de Windows:** Durante a instalação do Python, marque a opção **"Add Python to PATH"**

---

## 🚀 Como Instalar e Rodar Localmente

### 1. Clonar o Repositório

```bash
git clone https://github.com/Lukithas/pi-bets.git
cd pi-bets
```

### 2. Preparar as Bases de Dados

Certifique-se de que os seguintes arquivos estão na **mesma pasta** que `dashboard.py`:

| Arquivo | Descrição | Tamanho |
|:---|:---|:---|
| `bases_consumidor.zip` | Base bruta do Consumidor.gov.br | ~200 MB |
| `dados_apostas_consolidado.csv` | Pesquisa estruturada da equipe | - |
| `dados_consumidor_csvs/` | CSVs por mês (2024-2026) | ~1.5 GB |

### 3. Criar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install streamlit pandas numpy seaborn matplotlib requests
```

### 5. Executar o Dashboard

```bash
streamlit run dashboard.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

---

## 📁 Estrutura do Repositório

```
pi-bets/
├── README.md
├── requirements.txt
├── dashboard.py                          # Aplicação principal
├── .gitattributes                        # Configuração Git LFS
├── docs/
│   └── Entregáveis/
│       ├── Relatórios Técnicos/
│       ├── Unidade 1/
│       ├── Unidade 2/
│       └── Unidade_3/                   # Arquivos da entrega final
│           ├── README.md
│           ├── bases_consumidor.zip
│           ├── prototipo_dashboard.zip
│           ├── dados_apostas_consolidado.csv
│           ├── dados_consumidor_csvs/
│           └── dashboard.py
```

---

## 👨‍💻 Equipe de Desenvolvimento

| Nome |
|:---|
| **Caio Lima** |
| **Guilherme Augusto** |
| **Gustavo Albuquerque** |
| **Lucas Bretas** |
| **Mateus Onival** |

---

## 📚 Referencial Teórico

### Banco Central do Brasil
*Análise do perfil dos usuários do Pix em plataformas de apostas* — Este estudo evidencia o alto volume de recursos transferidos por pessoas físicas (incluindo beneficiários de programas sociais) para empresas de apostas esportivas.

---

## 📝 Licença

Este projeto é desenvolvido como parte do currículo do curso de Ciência da Computação - UniCEUB.

---

<p align="center">
  Desenvolvido com ❤️ para o Projeto Integrador I — UniCEUB<br/>
  <strong>5º Semestre - 2026</strong>
</p>
