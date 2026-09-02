import pandas as pd
import numpy as np
from datetime import datetime

def ler_dados_brutos():
    print("Carregando dados brutos...")
    
    try:
        df_renda = pd.read_csv("dados/renda_por_cidade.csv", sep=";", encoding="utf-8-sig")
        df_pop = pd.read_csv("dados/populacao_por_cidade.csv", sep=";", encoding="utf-8-sig")
        df_emp = pd.read_csv("dados/empresas_por_setor.csv", sep=";", encoding="utf-8-sig")
        df_emprego = pd.read_csv("dados/emprego_formal.csv", sep=";", encoding="utf-8-sig")
        
        print(f"Renda: {len(df_renda)} registros")
        print(f"Populacao: {len(df_pop)} registros")
        print(f"Empresas: {len(df_emp)} registros")
        print(f"Emprego: {len(df_emprego)} registros")
        
        return df_renda, df_pop, df_emp, df_emprego
    
    except FileNotFoundError as e:
        print(f"Arquivo nao encontrado: {e}")
        print("Execute primeiro o script 'extracao_dados.py'")
        raise SystemExit(1)

def padronizar_textos(df, coluna="cidade"):
    print(f"\nPadronizando nomes em '{coluna}'...")
    
    df[coluna] = df[coluna].str.strip()
    df[coluna] = df[coluna].str.title()
    
    substituicoes = {
        "Sao Vicente": "Sao Vicente",
        "Sao Paulo": "Sao Paulo",
        "Santos Sp": "Santos"
    }
    df[coluna] = df[coluna].replace(substituicoes)
    
    print(f"Padronizacao concluida — {df[coluna].nunique()} valores unicos")
    return df

def tratar_valores_nulos(df, nome_base):
    print(f"\nTratando valores nulos em {nome_base}...")
    
    for coluna in df.columns:
        qtd_nulos = df[coluna].isnull().sum()
        if qtd_nulos > 0:
            if pd.api.types.is_numeric_dtype(df[coluna]):
                mediana = df[coluna].median()
                df[coluna] = df[coluna].fillna(mediana)
                print(f"  '{coluna}': {qtd_nulos} nulos -> preenchidos com mediana ({mediana:.0f})")
            else:
                df[coluna] = df[coluna].fillna("Nao informado")
                print(f"  '{coluna}': {qtd_nulos} nulos -> preenchidos com 'Nao informado'")
        else:
            print(f"  '{coluna}': sem valores nulos")
    
    return df

def remover_duplicatas(df, nome_base):
    qtd_duplicatas = df.duplicated().sum()
    if qtd_duplicatas > 0:
        df = df.drop_duplicates(keep="first")
        print(f"\nRemovidas {qtd_duplicatas} linhas duplicadas em {nome_base}")
    else:
        print(f"\nNenhuma duplicata encontrada em {nome_base}")
    return df

def corrigir_tipos(df, nome_base):
    print(f"\nVerificando tipos de dados em {nome_base}...")
    
    colunas_numericas = df.select_dtypes(include=["object"]).columns
    for coluna in colunas_numericas:
        if any(palavra in coluna.lower() for palavra in ["quantidade", "populacao", "renda", "emprego", "area"]):
            try:
                df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
                print(f"  '{coluna}' convertida para numerico")
            except:
                pass
    
    return df

def criar_indices_e_classificacoes(df_renda, df_pop, df_emprego):
    print("\nCriando indices e classificacoes...")
    
    df_renda["faixa_renda"] = pd.cut(
        df_renda["renda_media"],
        bins=[0, 2000, 3000, 4000, float("inf")],
        labels=["Baixa", "Media-Baixa", "Media-Alta", "Alta"]
    )
    
    df_pop["porte_cidade"] = pd.cut(
        df_pop["populacao_2023"],
        bins=[0, 50000, 150000, 300000, float("inf")],
        labels=["Pequena", "Media-Pequena", "Media-Grande", "Grande"]
    )
    
    df_pop["crescimento_demografico"] = pd.cut(
        df_pop["taxa_crescimento_percent"],
        bins=[-10, 0, 1.5, 3, float("inf")],
        labels=["Declinio", "Estavel", "Crescimento Moderado", "Crescimento Acelerado"]
    )
    
    df_emprego["nivel_emprego_formal"] = pd.cut(
        df_emprego["taxa_emprego_formal_percent"],
        bins=[0, 40, 55, 70, 100],
        labels=["Baixo", "Medio", "Alto", "Muito Alto"]
    )
    
    print("Classificacoes criadas com sucesso")
    return df_renda, df_pop, df_emprego

def calcular_indicadores_economicos(df_consolidado, df_emp):
    print("\nCalculando indicadores economicos...")
    
    df_total_empresas = df_emp.groupby("cidade")["quantidade"].sum().reset_index()
    df_total_empresas.rename(columns={"quantidade": "total_empresas"}, inplace=True)
    
    df_consolidado = pd.merge(df_consolidado, df_total_empresas, on="cidade", how="left")
    
    df_consolidado["empresas_por_mil_habitantes"] = round(
        (df_consolidado["total_empresas"] / df_consolidado["populacao_2023"]) * 1000, 2
    )
    
    df_consolidado["renda_per_capita_ajustada"] = round(
        df_consolidado["renda_media"] / df_consolidado["empresas_por_mil_habitantes"], 2
    )
    
    df_consolidado["potencial_consumo"] = round(
        df_consolidado["renda_media"] * df_consolidado["populacao_2023"] / 1000000, 2
    )
    
    print("Indicadores economicos calculados")
    return df_consolidado

def cruzar_todas_bases(df_renda, df_pop, df_emprego):
    print("\nCruzando todas as bases de dados...")
    
    df_consolidado = pd.merge(df_renda, df_pop, on="cidade", how="inner")
    df_consolidado = pd.merge(df_consolidado, df_emprego, on="cidade", how="inner")
    
    print(f"Base consolidada criada: {len(df_consolidado)} municipios, {len(df_consolidado.columns)} colunas")
    return df_consolidado

def salvar_dados_processados(df_renda, df_pop, df_emp, df_emprego, df_consolidado):
    print("\nSalvando dados processados...")
    
    arquivos = [
        ("renda_processada", df_renda),
        ("populacao_processada", df_pop),
        ("empresas_processada", df_emp),
        ("emprego_processada", df_emprego),
        ("base_consolidada", df_consolidado)
    ]
    
    for nome, df in arquivos:
        caminho = f"dados/{nome}.csv"
        df.to_csv(caminho, index=False, encoding="utf-8-sig", sep=";")
        print(f"Salvo: {caminho} — {len(df)} linhas")

def gerar_resumo_qualidade(df_renda, df_pop, df_emp, df_emprego, df_consolidado):
    print("\n" + "=" * 60)
    print("RELATORIO DE QUALIDADE DOS DADOS")
    print("=" * 60)
    
    total_registros = len(df_renda) + len(df_pop) + len(df_emp) + len(df_emprego)
    total_colunas = len(df_renda.columns) + len(df_pop.columns) + len(df_emp.columns) + len(df_emprego.columns)
    
    print(f"Data do processamento: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de registros processados: {total_registros}")
    print(f"Total de colunas: {total_colunas}")
    print(f"Municipios na base consolidada: {len(df_consolidado)}")
    print(f"Periodo de referencia: 2022-2023")
    print(f"Fontes: IBGE, SEADE, RAIS/MTE, CAGED")
    print("=" * 60)

def main():
    print("=" * 60)
    print("LITORAL DATA INSIGHTS — TRANSFORMACAO DE DADOS")
    print("=" * 60)
    print(f"Inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    df_renda, df_pop, df_emp, df_emprego = ler_dados_brutos()
    
    df_renda = padronizar_textos(df_renda)
    df_pop = padronizar_textos(df_pop)
    df_emp = padronizar_textos(df_emp)
    df_emprego = padronizar_textos(df_emprego)
    
    df_renda = tratar_valores_nulos(df_renda, "renda")
    df_pop = tratar_valores_nulos(df_pop, "populacao")
    df_emp = tratar_valores_nulos(df_emp, "empresas")
    df_emprego = tratar_valores_nulos(df_emprego, "emprego")
    
    df_renda = remover_duplicatas(df_renda, "renda")
    df_pop = remover_duplicatas(df_pop, "populacao")
    df_emp = remover_duplicatas(df_emp, "empresas")
    df_emprego = remover_duplicatas(df_emprego, "emprego")
    
    df_renda = corrigir_tipos(df_renda, "renda")
    df_pop = corrigir_tipos(df_pop, "populacao")
    df_emp = corrigir_tipos(df_emp, "empresas")
    df_emprego = corrigir_tipos(df_emprego, "emprego")
    
    df_renda, df_pop, df_emprego = criar_indices_e_classificacoes(df_renda, df_pop, df_emprego)
    
    df_consolidado = cruzar_todas_bases(df_renda, df_pop, df_emprego)
    df_consolidado = calcular_indicadores_economicos(df_consolidado, df_emp)
    
    salvar_dados_processados(df_renda, df_pop, df_emp, df_emprego, df_consolidado)
    gerar_resumo_qualidade(df_renda, df_pop, df_emp, df_emprego, df_consolidado)
    
    print("\nTRANSFORMACAO CONCLUIDA COM SUCESSO")
    print(f"Termino: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    return df_renda, df_pop, df_emp, df_emprego, df_consolidado

if __name__ == "__main__":
    main()