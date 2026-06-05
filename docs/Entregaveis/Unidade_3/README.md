# 📊 Painel Analítico: Ludopatia & BETs

> Projeto Integrador I — Ciência da Computação | **UniCEUB**

Este repositório contém a aplicação web desenvolvida para o **Projeto Integrador I** do curso de Ciência da Computação da UniCEUB. O dashboard realiza extração, transformação e carregamento **(ETL)** de dados públicos e privados para analisar o impacto socioeconômico das plataformas de apostas online (BETs) no Brasil.

---

## 🎯 Funcionalidades

- **Análise Macro** — Evolução da inadimplência cruzada com dados do Banco Central (SGS).
- **Perfil Epidemiológico** — Filtros dinâmicos simulando microdados do DataSUS (CID-10 F63.0).
- **Mineração de Dados (Batch)** — Processamento em lote de arquivos `.csv` do portal Consumidor.gov.br.
- **Design IHC** — Interface adaptativa, modo escuro nativo e design comportamental.

---

## ⚙️ Pré-requisitos

- **Python 3.11** ou **3.12**

> ⚠️ **Usuários de Windows:** Durante a instalação do Python, certifique-se de marcar a opção **"Add Python to PATH"**.

---

## 🚀 Como instalar e rodar localmente

### 1. Clonar o repositório

Baixe este repositório para o seu computador e abra a pasta no **VS Code**.

### 2. Preparar as Bases de Dados

Certifique-se de que os seguintes arquivos estão na **mesma pasta** que o script `dashboard.py`:

| Arquivo | Descrição |
|---|---|
| `bases_consumidor.zip` | Base bruta do Consumidor.gov.br |
| `dados_apostas_consolidado.csv` | Pesquisa estruturada da equipe |

### 3. Instalar as dependências

Abra o terminal do VS Code (`Ctrl + '`) e execute:

```bash
pip install streamlit pandas numpy seaborn matplotlib requests
```

### 4. Iniciar a aplicação

```bash
python -m streamlit run dashboard.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 👨‍💻 Equipe de Desenvolvimento

| Nome |
|---|
| Caio Lima |
| Guilherme Augusto |
| Gustavo Albuquerque |
| Lucas Bretas |
| Mateus Onival |

---

<p align="center">
  Desenvolvido com ❤️ para o Projeto Integrador I — UniCEUB
</p>
