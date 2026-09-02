import pandas as pd

def ler_dados_brutos():
    df_renda = pd.read_csv("dados/renda_por_cidade.csv")
    df_pop = pd.read_csv("dados/populacao_por_cidade.csv")
    df_emp = pd.read_csv("dados/empresas_por_setor.csv")
    return df_renda, df_pop, df_emp

def limpar_e_padronizar(df_renda, df_pop, df_emp):
    for df in [df_renda, df_pop, df_emp]:
        if "cidade" in df.columns:
            df["cidade"] = df["cidade"].str.strip().str.title()
    
    df_renda["renda_media"] = df_renda["renda_media"].fillna(df_renda["renda_media"].median())
    df_pop["populacao"] = df_pop["populacao"].fillna(0).astype(int)
    df_emp["quantidade"] = df_emp["quantidade"].fillna(0).astype(int)
    
    return df_renda, df_pop, df_emp

def criar_indices(df_renda, df_pop):
    df_renda["faixa_renda"] = pd.cut(
        df_renda["renda_media"],
        bins=[0, 2500, 3500, float("inf")],
        labels=["Baixa", "Média", "Alta"]
    )
    
    df_pop["porte_cidade"] = pd.cut(
        df_pop["populacao"],
        bins=[0, 200000, 400000, float("inf")],
        labels=["Pequena", "Média", "Grande"]
    )
    
    return df_renda, df_pop

def cruzar_bases(df_renda, df_pop):
    df_consolidado = pd.merge(df_renda, df_pop, on="cidade", how="inner")
    return df_consolidado

def salvar_dados(df_renda, df_pop, df_emp, df_consolidado):
    df_renda.to_csv("dados/renda_processada.csv", index=False, encoding="utf-8-sig")
    df_pop.to_csv("dados/populacao_processada.csv", index=False, encoding="utf-8-sig")
    df_emp.to_csv("dados/empresas_processada.csv", index=False, encoding="utf-8-sig")
    df_consolidado.to_csv("dados/base_consolidada.csv", index=False, encoding="utf-8-sig")
    print("Todos os dados salvos!")

def main():
    print("Iniciando transformação...\n")
    
    df_renda, df_pop, df_emp = ler_dados_brutos()
    df_renda, df_pop, df_emp = limpar_e_padronizar(df_renda, df_pop, df_emp)
    df_renda, df_pop = criar_indices(df_renda, df_pop)
    df_consolidado = cruzar_bases(df_renda, df_pop)
    salvar_dados(df_renda, df_pop, df_emp, df_consolidado)
    
    print("\nTransformação concluída!")

if __name__ == "__main__":
    main()