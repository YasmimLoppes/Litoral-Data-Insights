-- ==============================================================
-- LITORAL DATA INSIGHTS — CONSULTAS DE ANALISE
-- Base de Dados Economicos da Baixada Santista
-- Fontes: IBGE, SEADE, RAIS/MTE, CAGED
-- Periodo de Referencia: 2022-2023
-- ==============================================================

-- ==============================================================
-- 1. VISAO GERAL — Panorama economico por municipio
-- ==============================================================
SELECT 
    cidade,
    renda_media,
    faixa_renda,
    renda_chefe_familia,
    populacao_2023,
    porte_cidade,
    taxa_crescimento_percent,
    crescimento_demografico,
    taxa_emprego_formal_percent,
    nivel_emprego_formal
FROM base_consolidada
ORDER BY renda_media DESC;

-- ==============================================================
-- 2. RENDA — Classificacao e comparacao entre municipios
-- ==============================================================
SELECT 
    cidade,
    renda_media,
    faixa_renda,
    renda_chefe_familia,
    renda_10_porcento AS renda_top_10,
    renda_50_porcento AS renda_mediana,
    ROUND((renda_media / renda_50_porcento), 2) AS indice_concentracao_renda
FROM base_consolidada
ORDER BY renda_media DESC;

-- ==============================================================
-- 3. POPULACAO — Crescimento e densidade demografica
-- ==============================================================
SELECT 
    cidade,
    populacao_2022,
    populacao_2023,
    crescimento_absoluto,
    taxa_crescimento_percent,
    crescimento_demografico,
    densidade_por_km2,
    area_km2,
    porte_cidade
FROM base_consolidada
ORDER BY taxa_crescimento_percent DESC;

-- ==============================================================
-- 4. EMPRESAS — Distribuicao por setor e municipio
-- ==============================================================
SELECT 
    e.cidade,
    e.setor,
    e.quantidade,
    p.populacao_2023,
    ROUND((e.quantidade * 1000.0 / p.populacao_2023), 2) AS empresas_por_mil_habitantes,
    ROUND((e.quantidade * 100.0 / SUM(e.quantidade) OVER (PARTITION BY e.cidade)), 2) AS percentual_do_setor_no_municipio
FROM empresas_processada e
JOIN populacao_processada p ON e.cidade = p.cidade
ORDER BY e.cidade, e.quantidade DESC;

-- ==============================================================
-- 5. EMPRESAS — Total geral por municipio
-- ==============================================================
SELECT 
    cidade,
    SUM(quantidade) AS total_empresas,
    MAX(CASE WHEN setor = 'Comercio' THEN quantidade END) AS comercio,
    MAX(CASE WHEN setor = 'Servicos' THEN quantidade END) AS servicos,
    MAX(CASE WHEN setor = 'Industria' THEN quantidade END) AS industria,
    MAX(CASE WHEN setor = 'Construcao' THEN quantidade END) AS construcao,
    MAX(CASE WHEN setor = 'Agronegocio' THEN quantidade END) AS agronegocio
FROM empresas_processada
GROUP BY cidade
ORDER BY total_empresas DESC;

-- ==============================================================
-- 6. EMPREGO — Formalidade e variacao
-- ==============================================================
SELECT 
    cidade,
    empregos_formais_2022,
    empregos_formais_2023,
    variacao_empregos,
    variacao_percentual,
    salario_medio_mensal,
    taxa_emprego_formal_percent,
    nivel_emprego_formal
FROM base_consolidada
ORDER BY variacao_percentual DESC;

-- ==============================================================
-- 7. INDICADORES COMPOSTOS — Potencial de mercado
-- ==============================================================
SELECT 
    cidade,
    renda_media,
    populacao_2023,
    total_empresas,
    empresas_por_mil_habitantes,
    renda_per_capita_ajustada,
    potencial_consumo,
    CASE 
        WHEN faixa_renda = 'Alta' AND empresas_por_mil_habitantes < 10 THEN 'ALTA OPORTUNIDADE'
        WHEN faixa_renda IN ('Media-Alta', 'Media-Baixa') AND empresas_por_mil_habitantes < 15 THEN 'OPORTUNIDADE MODERADA'
        ELSE 'MERCADO SATURADO OU BAIXO POTENCIAL'
    END AS avaliacao_oportunidade
FROM base_consolidada
ORDER BY potencial_consumo DESC;

-- ==============================================================
-- 8. OPORTUNIDADES — Municipios com maior potencial
-- ==============================================================
SELECT 
    cidade,
    faixa_renda,
    porte_cidade,
    renda_media,
    populacao_2023,
    empresas_por_mil_habitantes,
    potencial_consumo,
    avaliacao_oportunidade
FROM (
    SELECT 
        *,
        RANK() OVER (ORDER BY potencial_consumo DESC, empresas_por_mil_habitantes ASC) AS rank_oportunidade
    FROM base_consolidada
) sub
WHERE avaliacao_oportunidade LIKE '%OPORTUNIDADE%'
ORDER BY rank_oportunidade;

-- ==============================================================
-- 9. ANALISE SETORIAL — Setor com maior participacao por cidade
-- ==============================================================
WITH ranking_setores AS (
    SELECT 
        e.cidade,
        e.setor,
        e.quantidade,
        RANK() OVER (PARTITION BY e.cidade ORDER BY e.quantidade DESC) AS rank_setor
    FROM empresas_processada e
)
SELECT 
    cidade,
    setor AS setor_dominante,
    quantidade AS quantidade_empresas,
    ROUND((quantidade * 100.0 / SUM(quantidade) OVER (PARTITION BY cidade)), 2) AS participacao_percentual
FROM ranking_setores
WHERE rank_setor = 1
ORDER BY quantidade DESC;

-- ==============================================================
-- 10. RESUMO FINAL — Panorama completo da regiao
-- ==============================================================
SELECT 
    COUNT(DISTINCT cidade) AS total_municipios,
    SUM(populacao_2023) AS populacao_total_regiao,
    ROUND(AVG(renda_media), 2) AS renda_media_regional,
    SUM(total_empresas) AS total_empresas_regiao,
    ROUND(AVG(taxa_emprego_formal_percent), 2) AS taxa_emprego_formal_media,
    ROUND(AVG(empresas_por_mil_habitantes), 2) AS media_empresas_por_mil_habitantes
FROM base_consolidada;

-- ==============================================================
-- FIM DAS CONSULTAS
-- ==============================================================