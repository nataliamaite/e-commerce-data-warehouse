/*Comparar vendedores por faturamento e quantidade de itens vendidos.*/

SELECT
    dv.seller_id,
    dv.cidade,
    dv.estado,
    COUNT(*) AS quantidade_itens_vendidos,
    COUNT(DISTINCT f.order_id) AS quantidade_pedidos,
    SUM(f.preco) AS faturamento_produtos,
    SUM(f.valor_frete) AS total_frete,
    SUM(f.valor_total_item) AS faturamento_total
FROM dw.fato_vendas f
INNER JOIN dw.dim_vendedor dv
    ON f.sk_vendedor = dv.sk_vendedor
GROUP BY
    dv.seller_id,
    dv.cidade,
    dv.estado
ORDER BY
    faturamento_total DESC;
