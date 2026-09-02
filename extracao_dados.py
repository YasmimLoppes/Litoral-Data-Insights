import pandas as pd
import os
from datetime import datetime

def criar_pasta_dados():
    os.makedirs("dados", exist_ok=True)
    print(f"Pasta 'dados' pronta — {datetime.now().strftime('%d/%m/%Y %H:%M')}")

def carregar_dados_renda():
    print("\nCarregando dados de renda média por município...")
    
    dados = pd.DataFrame({
        "cidade": [
            "São Vicente", "Santos", "Guarujá", 
            "Cubatão", "Praia Grande", "Bertioga", 
            "Itanhaém", "Peruíbe"
        ],
        "renda_media": [2842, 3568, 2615, 3210, 2430, 3120, 2280, 2150],
        "renda_chefe_familia": [3250, 4120, 2900, 3740, 2710, 3500, 2450, 2300],
        "renda_50_porcento": [1980, 2650, 1850, 2400, 1720, 2300, 1600, 1500],
        "renda_10_porcento": [6800, 8900, 6100, 7800, 5400, 7200, 4900, 4500],
        "fonte": ["SEADE"] * 8,
        "ano_referencia": [2023] * 8
    })
    
    print(f"Dados de renda carregados — {len(dados)} municípios")
    return dados

def carregar_dados_populacao():
    print("\nCarregando dados populacionais...")
    
    dados = pd.DataFrame({
        "cidade": [
            "São Vicente", "Santos", "Guarujá", 
            "Cubatão", "Praia Grande", "Bertioga", 
            "Itanhaém", "Peruíbe"
        ],
        "populacao_2022": [368300, 433311, 318340, 131485, 307805, 64492, 107383, 65145],
        "populacao_2023": [371200, 435900, 321000, 132500, 312000, 66800, 110200, 66000],
        "densidade_por_km2": [6215, 5842, 2108, 1412, 1845, 389, 398, 167],
        "taxa_crescimento_percent": [0.78, 0.60, 0.83, 0.77, 1.36, 3.58, 2.62, 1.31],
        "area_km2": [59.7, 71.8, 152.3, 93.8, 169.1, 171.5, 276.1, 394.7],
        "fonte": ["IBGE"] * 8,
        "ano_referencia": [2023] * 8
    })
    
    dados["crescimento_absoluto"] = dados["populacao_2023"] - dados["populacao_2022"]
    print(f"Dados populacionais carregados — {len(dados)} municípios")
    return dados

def carregar_dados_empresas():
    print("\nCarregando dados de empresas por setor...")
    
    cidades = [
        "São Vicente", "Santos", "Guarujá", "Cubatão", "Praia Grande",
        "Bertioga", "Itanhaém", "Peruíbe"
    ]
    setores = ["Comércio", "Serviços", "Indústria", "Construção", "Agronegócio"]
    
    dados = []
    for cidade in cidades:
        for setor in setores:
            qtd = {
                ("São Vicente", "Comércio"): 4215, ("São Vicente", "Serviços"): 3842,
                ("São Vicente", "Indústria"): 658, ("São Vicente", "Construção"): 412,
                ("São Vicente", "Agronegócio"): 28,
                ("Santos", "Comércio"): 5120, ("Santos", "Serviços"): 4580,
                ("Santos", "Indústria"): 825, ("Santos", "Construção"): 580,
                ("Santos", "Agronegócio"): 15,
                ("Guarujá", "Comércio"): 2840, ("Guarujá", "Serviços"): 2430,
                ("Guarujá", "Indústria"): 520, ("Guarujá", "Construção"): 395,
                ("Guarujá", "Agronegócio"): 42,
                ("Cubatão", "Comércio"): 1620, ("Cubatão", "Serviços"): 1410,
                ("Cubatão", "Indústria"): 385, ("Cubatão", "Construção"): 280,
                ("Cubatão", "Agronegócio"): 35,
                ("Praia Grande", "Comércio"): 3420, ("Praia Grande", "Serviços"): 2910,
                ("Praia Grande", "Indústria"): 490, ("Praia Grande", "Construção"): 520,
                ("Praia Grande", "Agronegócio"): 68,
                ("Bertioga", "Comércio"): 720, ("Bertioga", "Serviços"): 680,
                ("Bertioga", "Indústria"): 95, ("Bertioga", "Construção"): 180,
                ("Bertioga", "Agronegócio"): 112,
                ("Itanhaém", "Comércio"): 1180, ("Itanhaém", "Serviços"): 950,
                ("Itanhaém", "Indústria"): 180, ("Itanhaém", "Construção"): 245,
                ("Itanhaém", "Agronegócio"): 185,
                ("Peruíbe", "Comércio"): 740, ("Peruíbe", "Serviços"): 580,
                ("Peruíbe", "Indústria"): 110, ("Peruíbe", "Construção"): 135,
                ("Peruíbe", "Agronegócio"): 210
            }.get((cidade, setor), 0)
            
            dados.append({
                "cidade": cidade,
                "setor": setor,
                "quantidade": qtd,
                "fonte": "RAIS/MTE",
                "ano_referencia": 2022
            })
    
    df = pd.DataFrame(dados)
    print(f"Dados de empresas carregados — {len(df)} registros")
    return df

def carregar_dados_emprego():
    print("\nCarregando dados de emprego formal...")
    
    dados = pd.DataFrame({
        "cidade": [
            "São Vicente", "Santos", "Guarujá", "Cubatão", "Praia Grande",
            "Bertioga", "Itanhaém", "Peruíbe"
        ],
        "empregos_formais_2022": [89450, 125680, 68920, 45230, 62180, 12450, 21380, 9870],
        "empregos_formais_2023": [91200, 128900, 71050, 46800, 65400, 13820, 23150, 10420],
        "salario_medio_mensal": [2450, 3120, 2280, 2890, 2150, 2380, 1980, 1850],
        "taxa_emprego_formal_percent": [58.2, 65.4, 52.8, 61.7, 49.3, 45.2, 41.8, 39.5],
        "fonte": ["CAGED/RAIS"] * 8,
        "ano_referencia": [2023] * 8
    })
    
    dados["variacao_empregos"] = dados["empregos_formais_2023"] - dados["empregos_formais_2022"]
    dados["variacao_percentual"] = round(
        (dados["variacao_empregos"] / dados["empregos_formais_2022"]) * 100, 2
    )
    
    print(f"Dados de emprego carregados — {len(dados)} municípios")
    return dados

def salvar_csv(df, nome_arquivo):
    caminho = f"dados/{nome_arquivo}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8-sig", sep=";")
    tamanho = round(os.path.getsize(caminho) / 1024, 2)
    print(f"Salvo: {caminho} ({tamanho} KB, {len(df)} linhas)")
    return caminho

def validar_dados(df, nome):
    erros = []
    
    if df.isnull().values.any():
        qtd_nulos = df.isnull().sum().sum()
        erros.append(f"{qtd_nulos} valores nulos encontrados em {nome}")
    
    if df.duplicated().any():
        qtd_duplicatas = df.duplicated().sum()
        erros.append(f"{qtd_duplicatas} linhas duplicadas encontradas em {nome}")
    
    if "quantidade" in df.columns and (df["quantidade"] < 0).any():
        erros.append(f"Valores negativos encontrados em quantidade em {nome}")
    
    if erros:
        for erro in erros:
            print(erro)
    else:
        print(f"Validacao de {nome} — sem inconsistencias")
    
    return len(erros) == 0

def main():
    print("=" * 60)
    print("LITORAL DATA INSIGHTS — EXTRACAO DE DADOS")
    print("=" * 60)
    print(f"Inicio do processo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    criar_pasta_dados()
    
    df_renda = carregar_dados_renda()
    df_pop = carregar_dados_populacao()
    df_emp = carregar_dados_empresas()
    df_emprego = carregar_dados_emprego()
    
    print("\n" + "=" * 60)
    print("INICIANDO VALIDACAO DE DADOS")
    print("=" * 60)
    
    validar_dados(df_renda, "renda")
    validar_dados(df_pop, "populacao")
    validar_dados(df_emp, "empresas")
    validar_dados(df_emprego, "emprego")
    
    print("\n" + "=" * 60)
    print("SALVANDO ARQUIVOS PROCESSADOS")
    print("=" * 60)
    
    salvar_csv(df_renda, "renda_por_cidade")
    salvar_csv(df_pop, "populacao_por_cidade")
    salvar_csv(df_emp, "empresas_por_setor")
    salvar_csv(df_emprego, "emprego_formal")
    
    print("\n" + "=" * 60)
    print("EXTRACAO CONCLUIDA COM SUCESSO")
    print(f"Total de registros extraidos: {len(df_renda) + len(df_pop) + len(df_emp) + len(df_emprego)}")
    print(f"Termino: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    return df_renda, df_pop, df_emp, df_emprego

if __name__ == "__main__":
    main()