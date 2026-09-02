-- Litoral Data Insights: Consultas de Análise
-- Dados econômicos da Baixada Santista

-- 1. Visão geral por cidade
SELECT 
    cidade,
    renda_media,
    faixa_renda,
    populacao,
    porte_cidade
FROM base_consolidada
ORDER BY renda_media DESC;

-- 2. Total de empresas por cidade e setor
SELECT 
    cidade,
    setor,
    SUM(quantidade) AS total_empresas
FROM empresas_processada
GROUP BY cidade, setor
ORDER BY cidade, total_empresas DESC;

-- 3. Cidades com renda acima da média
SELECT 
    cidade,
    renda_media,
    populacao
FROM base_consolidada
WHERE faixa_renda = 'Alta'
ORDER BY renda_media DESC;

-- 4. Relação empresas / habitantes
SELECT 
    e.cidade,
    p.populacao,
    SUM(e.quantidade) AS total_empresas,
    ROUND(SUM(e.quantidade) * 1000.0 / p.populacao, 2) 
        AS empresas_por_mil_habitantes
FROM empresas_processada e
JOIN populacao_processada p ON e.cidade = p.cidade
GROUP BY e.cidade, p.populacao
ORDER BY empresas_por_mil_habitantes DESC;