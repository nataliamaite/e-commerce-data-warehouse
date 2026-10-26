/*Analisar o faturamento por mês e ano, identificando tendências de vendas.*/

SELECT
    dt.ano,
    dt.mes,
    dt.nome_mes,
    SUM(f.preco) AS faturamento_produtos,
    SUM(f.valor_frete) AS total_frete,
    SUM(f.valor_total_item) AS faturamento_total,
    COUNT(DISTINCT f.order_id) AS quantidade_pedidos
FROM dw.fato_vendas f
INNER JOIN dw.dim_tempo dt
    ON f.sk_tempo = dt.sk_tempo
GROUP BY
    dt.ano,
    dt.mes,
    dt.nome_mes
ORDER BY
    dt.ano,
    dt.mes;
