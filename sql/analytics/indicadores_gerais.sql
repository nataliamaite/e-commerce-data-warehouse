/*indicadores que podem ser usados nos cartoes de um dashboard*/
SELECT
    COUNT(DISTINCT order_id) AS total_pedidos,
    COUNT(*) AS total_itens_vendidos,
    COUNT(DISTINCT sk_cliente) AS total_clientes,
    COUNT(DISTINCT sk_produto) AS total_produtos,
    COUNT(DISTINCT sk_vendedor) AS total_vendedores,
    SUM(preco) AS faturamento_produtos,
    SUM(valor_frete) AS total_frete,
    SUM(valor_total_item) AS faturamento_total,
    ROUND(AVG(valor_total_item), 2) AS ticket_medio_por_item
FROM dw.fato_vendas;
