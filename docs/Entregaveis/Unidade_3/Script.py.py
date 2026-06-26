import pandas as pd
import zipfile
import glob
import os

def processar_dados_consumidor(caminho_zip, pasta_extracao='dados_consumidor_csvs'):
    """
    Script de ETL (Extração, Transformação e Carga) para processar 
    as bases brutas do Consumidor.gov.br e filtrar dados do setor de BETs.
    """
    print(f"--- Iniciando Processamento: {caminho_zip} ---")
    
    # 1. Extração
    if not os.path.exists(caminho_zip):
        print("Erro: Arquivo ZIP não encontrado.")
        return None

    if not os.path.exists(pasta_extracao):
        os.makedirs(pasta_extracao)
        
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        print(f"Extraindo arquivos para {pasta_extracao}...")
        zip_ref.extractall(pasta_extracao)

    # 2. Transformação (Carga e Filtro)
    arquivos_csv = glob.glob(os.path.join(pasta_extracao, "*.csv"))
    lista_dfs = []
    
    print(f"Encontrados {len(arquivos_csv)} arquivos CSV. Processando...")
    
    for arquivo in arquivos_csv:
        try:
            # Tenta ler com UTF-8, se falhar tenta Latin1 (comum em arquivos do governo)
            try:
                df_temp = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
            except UnicodeDecodeError:
                df_temp = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False)
            
            lista_dfs.append(df_temp)
            print(f"  [OK] {os.path.basename(arquivo)}")
        except Exception as e:
            print(f"  [ERRO] {os.path.basename(arquivo)}: {e}")

    if not lista_dfs:
        print("Nenhum dado carregado.")
        return None

    df_total = pd.concat(lista_dfs, ignore_index=True)
    print(f"Total de registros processados: {len(df_total)}")

    # 3. Filtro Específico (BETs e Cassinos)
    palavras_chave = 'BET|APOSTA|CASSINO|BLAZE'
    filtro = df_total['Nome Fantasia'].str.contains(palavras_chave, case=False, na=False)
    df_bets = df_total[filtro]
    
    print(f"Registros filtrados (Setor de Apostas): {len(df_bets)}")

    # 4. Geração de Insights para o Dashboard
    if 'Problema' in df_bets.columns:
        top_problemas = df_bets['Problema'].value_counts().head(10).reset_index()
        top_problemas.columns = ['Problema', 'Quantidade']
        
        # Salva o resultado processado para uso no Dashboard
        output_file = 'top_problemas_bets.csv'
        top_problemas.to_csv(output_file, index=False, encoding='utf-8')
        print(f"--- Processamento Concluído! Resultado salvo em: {output_file} ---")
        return top_problemas

if __name__ == "__main__":
    # Exemplo de uso local
    processar_dados_consumidor('bases_consumidor.zip')
