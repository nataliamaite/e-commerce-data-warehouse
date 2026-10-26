
-- Dimensão de clientes
INSERT INTO dw.dim_cliente (
    customer_id,
    customer_unique_id,
    cidade,
    estado,
    cep
)
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    customer_zip_code_prefix
FROM staging.customers
WHERE customer_id IS NOT NULL
ON CONFLICT (customer_id) DO NOTHING;


-- Dimensão de produtos
INSERT INTO dw.dim_produto (
    product_id,
    categoria,
    categoria_ingles,
    peso_g,
    comprimento_cm,
    altura_cm,
    largura_cm
)
SELECT
    p.product_id,
    p.product_category_name,
    ct.product_category_name_english,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM staging.products p
LEFT JOIN staging.category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE p.product_id IS NOT NULL
ON CONFLICT (product_id) DO NOTHING;


-- Dimensão de vendedores
INSERT INTO dw.dim_vendedor (
    seller_id,
    cidade,
    estado,
    cep
)
SELECT
    seller_id,
    seller_city,
    seller_state,
    seller_zip_code_prefix
FROM staging.sellers
WHERE seller_id IS NOT NULL
ON CONFLICT (seller_id) DO NOTHING;


-- Dimensão de tempo
WITH limites AS (
    SELECT
        MIN(order_purchase_timestamp::date) AS data_inicial,
        MAX(order_purchase_timestamp::date) AS data_final
    FROM staging.orders
    WHERE order_purchase_timestamp IS NOT NULL
),
calendario AS (
    SELECT
        generate_series(
            data_inicial,
            data_final,
            INTERVAL '1 day'
        )::date AS data
    FROM limites
    WHERE data_inicial IS NOT NULL
      AND data_final IS NOT NULL
)
INSERT INTO dw.dim_tempo (
    sk_tempo,
    data_completa,
    dia,
    mes,
    nome_mes,
    trimestre,
    ano,
    dia_semana,
    nome_dia_semana
)
SELECT
    TO_CHAR(data, 'YYYYMMDD')::INTEGER,
    data,
    EXTRACT(DAY FROM data)::INTEGER,
    EXTRACT(MONTH FROM data)::INTEGER,
    CASE EXTRACT(MONTH FROM data)::INTEGER
        WHEN 1 THEN 'Janeiro'
        WHEN 2 THEN 'Fevereiro'
        WHEN 3 THEN 'Março'
        WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Maio'
        WHEN 6 THEN 'Junho'
        WHEN 7 THEN 'Julho'
        WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Setembro'
        WHEN 10 THEN 'Outubro'
        WHEN 11 THEN 'Novembro'
        WHEN 12 THEN 'Dezembro'
    END,
    EXTRACT(QUARTER FROM data)::INTEGER,
    EXTRACT(YEAR FROM data)::INTEGER,
    EXTRACT(ISODOW FROM data)::INTEGER,
    CASE EXTRACT(ISODOW FROM data)::INTEGER
        WHEN 1 THEN 'Segunda-feira'
        WHEN 2 THEN 'Terça-feira'
        WHEN 3 THEN 'Quarta-feira'
        WHEN 4 THEN 'Quinta-feira'
        WHEN 5 THEN 'Sexta-feira'
        WHEN 6 THEN 'Sábado'
        WHEN 7 THEN 'Domingo'
    END
FROM calendario
ON CONFLICT (sk_tempo) DO NOTHING;
