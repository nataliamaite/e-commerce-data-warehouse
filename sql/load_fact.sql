
INSERT INTO dw.fato_vendas (
    order_id,
    order_item_id,
    sk_cliente,
    sk_produto,
    sk_vendedor,
    sk_tempo,
    preco,
    valor_frete,
    valor_total_item
)
SELECT
    oi.order_id,
    oi.order_item_id,
    dc.sk_cliente,
    dp.sk_produto,
    dv.sk_vendedor,
    dt.sk_tempo,
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value
FROM staging.order_items oi
INNER JOIN staging.orders o
    ON oi.order_id = o.order_id
INNER JOIN dw.dim_cliente dc
    ON o.customer_id = dc.customer_id
INNER JOIN dw.dim_produto dp
    ON oi.product_id = dp.product_id
INNER JOIN dw.dim_vendedor dv
    ON oi.seller_id = dv.seller_id
INNER JOIN dw.dim_tempo dt
    ON o.order_purchase_timestamp::date = dt.data_completa
WHERE oi.order_id IS NOT NULL
  AND oi.order_item_id IS NOT NULL
  AND oi.price IS NOT NULL
  AND oi.freight_value IS NOT NULL
ON CONFLICT (order_id, order_item_id) DO NOTHING;
