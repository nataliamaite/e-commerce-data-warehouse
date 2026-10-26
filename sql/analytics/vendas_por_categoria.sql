/*Identificar as categorias de produtos que geram mais receita.*/

SELECT
    COALESCE(dp.categoria_ingles, dp.categoria, 'Sem categoria')
        AS categoria,
    COUNT(*) AS quantidade_itens_vendidos,
    COUNT(DISTINCT f.order_id) AS quantidade_pedidos,
    SUM(f.preco) AS faturamento_produtos,
    SUM(f.valor_frete) AS total_frete,
    SUM(f.valor_total_item) AS faturamento_total
FROM dw.fato_vendas f
INNER JOIN dw.dim_produto dp
    ON f.sk_produto = dp.sk_produto
GROUP BY
    COALESCE(dp.categoria_ingles, dp.categoria, 'Sem categoria')
ORDER BY
    faturamento_total DESC;
