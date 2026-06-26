#  PI-BETS: Análise do Impacto Econômico das Apostas Online no Endividamento Familiar

> Projeto Integrador I — Ciência da Computação | **UniCEUB** (5º Semestre)

##  Sobre o Projeto

Investigação acadêmica focada no cruzamento de dados entre **apostas online** e **endividamento doméstico**. Este estudo busca validar a hipótese do vício mediado pela **tecnologia (IHC)** e pela **facilidade do Pix**, analisando a perda da estabilidade financeira e da renda básica familiar.

**Tema Central:** O Impacto Econômico das Plataformas de Apostas (Bets) no Endividamento Familiar

---

## 🔗 Links Rápidos

### Acesso ao Projeto

| Recurso | Link de Acesso |
| :--- | :--- |
| **Apresentação do Projeto** | [ihcbets.netlify.app](https://ihcbets.netlify.app/) |
| **Backlog do Projeto** | [backlogpibets.netlify.app](https://backlogpibets.netlify.app/) |
| **Dashboard Interativo** | [dashboard](https://pi-bets-site-dashboard.streamlit.app/) |
| **Demo do projeto** | [drive](https://drive.google.com/drive/folders/1QlBr48-jLnKbVU0bVwNZok616hX0oSwk?usp=sharing) |

### Documentação e Relatórios

| Documento | O que contém | Link |
| :--- | :--- | :--- |
| 📂 **Fontes dos Dados** | Todas as fontes e referências usadas na pesquisa | [fontesdados.netlify.app](https://fontesdados.netlify.app/) |
| 📄 **1º Relatório Técnico** | Primeira entrega de análise técnica do projeto | [primeirorelatorio.netlify.app](https://primeirorelatorio.netlify.app/) |
| 📄 **2º Relatório Técnico** | Segunda entrega de análise técnica do projeto | [segundorelatorio.netlify.app](https://segundorelatorio.netlify.app/) |
| 📘 **Documentos do Projeto** | Documentos produzidos ao longo do semestre | [projectdocumentss.netlify.app](https://projectdocumentss.netlify.app/) |

---

## Propósito e Escopo

O foco deste semestre é a **"resolução de problemas complexos"** por meio de investigação profunda do cenário atual. Existe uma lacuna no entendimento sobre o impacto real da facilidade de acesso às apostas.

**Entrega Principal:** Um **Dashboard Interativo** embasado em "modelagem estatística e desenvolvimento de indicadores (KPIs)", que comprova a viabilidade e a necessidade de projetar uma solução tecnológica futura.

---

##  Funcionalidades do Dashboard

- **Análise Macro** — Evolução da inadimplência cruzada com dados do Banco Central (SGS)
- **Perfil Epidemiológico** — Microdados de pacientes (DataSUS, CID-10 F63.0), com fallback simulado quando o dado real não está disponível
- **Mineração de Dados (Batch)** — Processamento em lote de arquivos `.csv` do portal Consumidor.gov.br
- **Design IHC** — Interface adaptativa, modo escuro, alto contraste e ajuste de fonte

---

##  Abordagem Metodológica

Para identificar as necessidades reais dos usuários e o escopo do problema, aplicamos conceitos de **Lean Inception** e **métodos ágeis**:

- **Descoberta:** Levantar os gatilhos comportamentais (como a ilusão de renda extra) que incentivam o uso contínuo
- **Delimitação:** Isolar a correlação entre facilidade de pagamentos digitais e comprometimento do orçamento doméstico

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

## Coleta e Transformação de Dados

### Fontes de Dados

- **Banco Central do Brasil** — Volume de transações via Pix para CNPJs de apostas
- **Serasa/SPC** — Índices de inadimplência
- **DataSUS** — Microdados epidemiológicos (CID-10 F63.0)
- **Consumidor.gov.br** — Dados públicos de reclamações
- **Ministério da Fazenda** — Diretrizes regulatórias do setor

---

##  Pré-requisitos

- **Python 3.11** ou **3.12**
- **Git LFS** (para os arquivos grandes do repositório)

>  **Usuários de Windows:** durante a instalação do Python, marque a opção **"Add Python to PATH"**.

---

##  Como Instalar e Rodar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Lukithas/pi-bets.git
cd pi-bets
```

### 2. Ir até a pasta do dashboard

A versão mais atual do dashboard está em `docs/Entregaveis/Unidade_3/`:

```bash
cd docs/Entregaveis/Unidade_3
```

### 3. Preparar as bases de dados

Confirme que estão nessa mesma pasta:

| Arquivo | Descrição |
|:---|:---|
| `bases_consumidor.zip` | Base bruta do Consumidor.gov.br (~200 MB) |
| `dados_apostas_consolidado.csv` | Pesquisa estruturada da equipe |
| `dados_sus.csv` | Microdados de pacientes (DataSUS) |

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar o dashboard

```bash
python -m streamlit run dashboard.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 📁 Estrutura do Repositório

```
pi-bets/
├── data/                               # Bases de dados e referências
│   ├── base_consumidorgov_2024_01.csv
│   ├── base_consumidorgov_2025_07.csv
│   ├── base_consumidorgov_2026_02.csv
│   ├── dados_apostas_consolidados.csv
│   └── Fontes.md
├── docs/                               # Documentação e Entregáveis
│   ├── Entregaveis/
│   │   ├── Relatórios Técnicos/        # Relatórios de análise técnica
│   │   ├── Unidade 1/                  # Documentação inicial
│   │   ├── Unidade 2/                  # Modelagem e KPIs
│   │   ├── Unidade 3/                  # Dashboard Interativo (Streamlit)
│   │   │   ├── dados_consumidor_csvs/  # Bases específicas do dashboard
│   │   │   ├── config.toml             # Configurações do Streamlit
│   │   │   ├── dashboard.py            # Código principal do painel
│   │   │   └── requirements.txt        # Dependências do Python
│   │   ├── Unidade 4/                  # Documento Mestre
│   │   │   └── pi_bets_documento_mestre.pdf
│   │   ├── Unidade 5/                  # Entrega Final e Conformidade
│   │   │   ├── Documentação_Final.pdf
│   │   │   ├── Relatório de Conformidade (LGPD).pdf
│   │   │   └── ACE - Avaliação Comunidade.pdf
│   │   ├── TERMO DE ABERTURA DO PROJETO.docx
│   │   └── VISÃO GERAL DO PROJETO.docx
│   └── .gitkeep
├── sites/                              # Páginas de apresentação (Netlify)
│   ├── Documentação.html
│   └── Fontes.html
├── .gitattributes
├── README.md                           # Documentação principal
└── Sprintfinal.md                      # Backlog e controle de sprints

```

---

##  Equipe de Desenvolvimento

| Nome | GitHub |
|:---|:---|
| **Caio Lima** | [@CaioB1ima](https://github.com/CaioB1ima) |
| **Guilherme Augusto** | [@Gadshx](https://github.com/Gadshx) |
| **Gustavo Albuquerque** | [@Gustavox0207](https://github.com/Gustavox0207) |
| **Lucas Bretas** | [@Lukithas](https://github.com/Lukithas) |
| **Mateus Onival** | [@Tweuz](https://github.com/Tweuz) |

---

##  Referencial Teórico

### Banco Central do Brasil
*Análise do perfil dos usuários do Pix em plataformas de apostas* — este estudo evidencia o alto volume de recursos transferidos por pessoas físicas (incluindo beneficiários de programas sociais) para empresas de apostas esportivas.

---

##  Licença

Este projeto é desenvolvido como parte do currículo do curso de Ciência da Computação - UniCEUB.

---

<p align="center">
  Desenvolvido com para o Projeto Integrador I — UniCEUB<br/>
  <strong>5º Semestre - 2026</strong>
</p>
