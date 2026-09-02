import pandas as pd
import os

def carregar_dados_renda():
    print("Carregando dados de renda...")
    return pd.DataFrame({
        "cidade": ["São Vicente", "Santos", "Guarujá", "Cubatão", "Praia Grande"],
        "renda_media": [2800, 3500, 2600, 3200, 2400],
        "renda_chefe_familia": [3200, 4100, 2900, 3700, 2700]
    })

def carregar_dados_populacao():
    print("Carregando dados de população...")
    return pd.DataFrame({
        "cidade": ["São Vicente", "Santos", "Guarujá", "Cubatão", "Praia Grande"],
        "populacao": [370000, 430000, 320000, 130000, 310000],
        "densidade_por_km2": [6200, 5800, 2100, 1400, 1800]
    })

def carregar_dados_empresas():
    print("Carregando dados de empresas...")
    return pd.DataFrame({
        "cidade": ["São Vicente", "Santos", "Guarujá", "Cubatão", "Praia Grande"] * 3,
        "setor": ["Comércio", "Serviços", "Indústria"] * 5,
        "quantidade": [4200, 3800, 650, 5100, 4500, 820, 2800, 2400, 520, 1600, 1400, 380, 3400, 2900, 490]
    })

def salvar_csv(df, nome_arquivo):
    os.makedirs("dados", exist_ok=True)
    caminho = f"dados/{nome_arquivo}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Salvo: {caminho}")

def main():
    print("Iniciando extração de dados...\n")
    
    df_renda = carregar_dados_renda()
    df_pop = carregar_dados_populacao()
    df_emp = carregar_dados_empresas()
    
    salvar_csv(df_renda, "renda_por_cidade")
    salvar_csv(df_pop, "populacao_por_cidade")
    salvar_csv(df_emp, "empresas_por_setor")
    
    print("\nExtração concluída!")
    return df_renda, df_pop, df_emp

if __name__ == "__main__":
    main()