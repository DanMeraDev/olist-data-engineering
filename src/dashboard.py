import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon="O",
    layout="wide"
)

DB_URL = "postgresql://olist:olist123@localhost:5433/olist"

BRL_TO_USD = 3.50


@st.cache_resource
def get_engine():
    return create_engine(DB_URL)


@st.cache_data(ttl=600)
def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="st-"], .stMarkdown, .stMetric, .stCaption {
    font-family: 'Inter', sans-serif !important;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600;
}
[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}
[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

col_title, col_divisa = st.columns([4, 1])
with col_title:
    st.title("Olist Brazilian E-Commerce — Dashboard")
with col_divisa:
    divisa = st.selectbox("Divisa", ["BRL (R$)", "USD (US$)"])

es_usd = divisa.startswith("USD")
simbolo = "US$" if es_usd else "R$"
factor = 1 / BRL_TO_USD if es_usd else 1.0

st.markdown("**Dataset:** ~100k ordenes reales (Sep 2016 - Oct 2018) · Marketplace brasileno · Tasa de conversion: R\\$3.50 = US\\$1")
st.divider()

kpis = run_query("""
    SELECT
        COUNT(DISTINCT o.order_id) AS total_ordenes,
        COUNT(DISTINCT c.customer_unique_id) AS total_clientes,
        ROUND(SUM(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS revenue_total,
        ROUND(AVG(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS ticket_promedio
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
""")

revenue = float(kpis['revenue_total'].iloc[0]) * factor
ticket = float(kpis['ticket_promedio'].iloc[0]) * factor

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ordenes", f"{kpis['total_ordenes'].iloc[0]:,}")
col2.metric("Clientes Unicos", f"{kpis['total_clientes'].iloc[0]:,}")
col3.metric("Revenue Total", f"{simbolo} {revenue:,.2f}")
col4.metric("Ticket Promedio", f"{simbolo} {ticket:,.2f}")

st.divider()

st.header("Q1: Volumen de transacciones por mes")
st.markdown("Hay estacionalidad en las ventas?")

q1_data = run_query("""
    SELECT
        DATE_TRUNC('month', purchase_timestamp)::DATE AS mes,
        COUNT(*) AS total_ordenes,
        ROUND(SUM(oi.total_revenue)::numeric, 2) AS revenue
    FROM orders o
    JOIN (
        SELECT order_id, SUM(price + COALESCE(freight_value, 0)) AS total_revenue
        FROM order_items
        GROUP BY order_id
    ) oi ON o.order_id = oi.order_id
    GROUP BY DATE_TRUNC('month', purchase_timestamp)::DATE
    ORDER BY mes
""")

q1_data['mes'] = pd.to_datetime(q1_data['mes'])
q1_data = q1_data[(q1_data['mes'] >= '2016-10-01') & (q1_data['mes'] <= '2018-08-01')]

col_q1a, col_q1b = st.columns(2)

with col_q1a:
    fig_q1_ordenes = px.bar(
        q1_data, x='mes', y='total_ordenes',
        title='Ordenes por Mes',
        labels={'mes': 'Mes', 'total_ordenes': 'Cantidad de Ordenes'},
        color_discrete_sequence=['#636EFA']
    )
    fig_q1_ordenes.update_layout(xaxis_tickformat='%b %Y')
    st.plotly_chart(fig_q1_ordenes, use_container_width=True)

with col_q1b:
    q1_plot = q1_data.copy()
    q1_plot['revenue_conv'] = q1_plot['revenue'] * factor
    fig_q1_revenue = px.line(
        q1_plot, x='mes', y='revenue_conv',
        title=f'Revenue por Mes ({simbolo})',
        labels={'mes': 'Mes', 'revenue_conv': f'Revenue ({simbolo})'},
        color_discrete_sequence=['#00CC96'],
        markers=True
    )
    fig_q1_revenue.update_layout(xaxis_tickformat='%b %Y')
    st.plotly_chart(fig_q1_revenue, use_container_width=True)

st.info("**Hallazgo:** Noviembre 2017 muestra un pico significativo (Black Friday Brasil). "
        "El crecimiento es sostenido hasta mediados de 2018, donde se estabiliza.")

st.divider()

st.header("Q2: Top 10 categorias con mayor valor generado")

q2_data = run_query("""
    SELECT
        p.category_name_english AS categoria,
        COUNT(DISTINCT oi.order_id) AS total_ordenes,
        ROUND(SUM(oi.price)::numeric, 2) AS revenue_productos,
        ROUND(SUM(oi.price + COALESCE(oi.freight_value, 0))::numeric, 2) AS revenue_total
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category_name_english
    ORDER BY revenue_total DESC
    LIMIT 10
""")

col_q2a, col_q2b = st.columns(2)

with col_q2a:
    q2_plot = q2_data.copy()
    q2_plot['revenue_conv'] = q2_plot['revenue_total'] * factor
    fig_q2_revenue = px.bar(
        q2_plot.sort_values('revenue_conv'),
        x='revenue_conv', y='categoria',
        orientation='h',
        title=f'Top 10 Categorias por Revenue Total ({simbolo})',
        labels={'revenue_conv': f'Revenue Total ({simbolo})', 'categoria': ''},
        color_discrete_sequence=['#EF553B']
    )
    st.plotly_chart(fig_q2_revenue, use_container_width=True)

with col_q2b:
    fig_q2_ordenes = px.bar(
        q2_data.sort_values('total_ordenes'),
        x='total_ordenes', y='categoria',
        orientation='h',
        title='Top 10 Categorias por Cantidad de Ordenes',
        labels={'total_ordenes': 'Ordenes', 'categoria': ''},
        color_discrete_sequence=['#AB63FA']
    )
    st.plotly_chart(fig_q2_ordenes, use_container_width=True)

st.info("**Hallazgo:** health_beauty lidera en revenue (R\\$1.44M / ~US\\$411k), "
        "pero bed_bath_table tiene mas ordenes (9,417). "
        "Esto indica que health_beauty vende productos de mayor valor unitario.")

st.divider()

st.header("Q3: Tiempo promedio entre eventos clave del flujo")
st.markdown("Cuanto tarda cada etapa del proceso de entrega?")

q3_data = run_query("""
    SELECT
        ROUND(AVG(EXTRACT(EPOCH FROM (approved_at - purchase_timestamp)) / 3600)::numeric, 1) AS horas_aprobacion,
        ROUND(AVG(EXTRACT(DAY FROM (delivered_carrier_date - purchase_timestamp)))::numeric, 1) AS dias_a_carrier,
        ROUND(AVG(EXTRACT(DAY FROM (delivered_customer_date - delivered_carrier_date)))::numeric, 1) AS dias_en_transito,
        ROUND(AVG(EXTRACT(DAY FROM (delivered_customer_date - purchase_timestamp)))::numeric, 1) AS dias_total_entrega
    FROM orders
    WHERE delivered_customer_date IS NOT NULL
      AND approved_at IS NOT NULL
      AND delivered_carrier_date IS NOT NULL
""")

col_q3a, col_q3b, col_q3c, col_q3d = st.columns(4)
col_q3a.metric("Aprobacion", f"{q3_data['horas_aprobacion'].iloc[0]}h")
col_q3b.metric("Compra -> Carrier", f"{q3_data['dias_a_carrier'].iloc[0]} dias")
col_q3c.metric("En Transito", f"{q3_data['dias_en_transito'].iloc[0]} dias")
col_q3d.metric("Total Entrega", f"{q3_data['dias_total_entrega'].iloc[0]} dias")

q3_dist = run_query("""
    SELECT
        EXTRACT(DAY FROM (delivered_customer_date - purchase_timestamp))::INTEGER AS dias_entrega
    FROM orders
    WHERE delivered_customer_date IS NOT NULL
      AND EXTRACT(DAY FROM (delivered_customer_date - purchase_timestamp)) BETWEEN 0 AND 60
""")

fig_q3 = px.histogram(
    q3_dist, x='dias_entrega', nbins=60,
    title='Distribucion de Tiempo de Entrega (dias)',
    labels={'dias_entrega': 'Dias hasta Entrega', 'count': 'Cantidad de Ordenes'},
    color_discrete_sequence=['#19D3F3']
)
fig_q3.add_vline(x=q3_data['dias_total_entrega'].iloc[0], line_dash="dash", line_color="red",
                  annotation_text=f"Promedio: {q3_data['dias_total_entrega'].iloc[0]} dias")
st.plotly_chart(fig_q3, use_container_width=True)

q3_estados = run_query("""
    SELECT
        c.state AS estado,
        ROUND(AVG(EXTRACT(DAY FROM (o.delivered_customer_date - o.purchase_timestamp)))::numeric, 1) AS dias_promedio,
        COUNT(*) AS total_ordenes
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.delivered_customer_date IS NOT NULL
    GROUP BY c.state
    HAVING COUNT(*) > 100
    ORDER BY dias_promedio DESC
""")

fig_q3_estado = px.bar(
    q3_estados, x='estado', y='dias_promedio',
    title='Tiempo Promedio de Entrega por Estado (solo estados con >100 ordenes)',
    labels={'estado': 'Estado', 'dias_promedio': 'Dias Promedio'},
    color='dias_promedio',
    color_continuous_scale='RdYlGn_r'
)
st.plotly_chart(fig_q3_estado, use_container_width=True)

st.info("**Hallazgo:** El cuello de botella esta en el transito, no en la aprobacion ni en el despacho. "
        "Los estados del norte/nordeste de Brasil tienen tiempos de entrega significativamente mayores.")

st.divider()

st.header("Q4: Incidencias y resultados negativos")

q4_data = run_query("""
    SELECT
        COUNT(*) AS total_ordenes,
        COUNT(*) FILTER (WHERE status = 'canceled') AS canceladas,
        COUNT(*) FILTER (WHERE status = 'unavailable') AS unavailable,
        ROUND(COUNT(*) FILTER (WHERE status = 'canceled')::numeric / COUNT(*) * 100, 2) AS pct_canceladas,
        ROUND(COUNT(*) FILTER (WHERE status = 'unavailable')::numeric / COUNT(*) * 100, 2) AS pct_unavailable
    FROM orders
""")

q4_reviews = run_query("""
    SELECT
        review_score,
        COUNT(*) AS cantidad,
        ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS porcentaje
    FROM order_reviews
    GROUP BY review_score
    ORDER BY review_score
""")

q4_entregas = run_query("""
    SELECT
        COUNT(*) AS total_delivered,
        COUNT(*) FILTER (WHERE delivered_customer_date > estimated_delivery_date) AS entrega_tardia,
        ROUND(COUNT(*) FILTER (WHERE delivered_customer_date > estimated_delivery_date)::numeric / COUNT(*) * 100, 2) AS pct_tardia
    FROM orders
    WHERE delivered_customer_date IS NOT NULL
      AND estimated_delivery_date IS NOT NULL
""")

col_q4a, col_q4b, col_q4c = st.columns(3)
col_q4a.metric("Cancelaciones", f"{q4_data['pct_canceladas'].iloc[0]}%",
               delta=f"{q4_data['canceladas'].iloc[0]} ordenes", delta_color="inverse")
col_q4b.metric("Reviews Negativas (1-2)",
               f"{q4_reviews[q4_reviews['review_score'] <= 2]['porcentaje'].sum():.1f}%")
col_q4c.metric("Entregas Tardias",
               f"{q4_entregas['pct_tardia'].iloc[0]}%",
               delta=f"{q4_entregas['entrega_tardia'].iloc[0]:,} ordenes", delta_color="inverse")

col_q4d, col_q4e = st.columns(2)

with col_q4d:
    colors = ['#EF553B', '#FFA15A', '#FECB52', '#00CC96', '#00B5F7']
    fig_q4_reviews = px.bar(
        q4_reviews, x='review_score', y='cantidad',
        title='Distribucion de Review Scores',
        labels={'review_score': 'Score', 'cantidad': 'Cantidad'},
        color='review_score',
        color_discrete_sequence=colors
    )
    st.plotly_chart(fig_q4_reviews, use_container_width=True)

with col_q4e:
    q4_status = run_query("""
        SELECT status, COUNT(*) AS cantidad
        FROM orders
        GROUP BY status
        ORDER BY cantidad DESC
    """)
    fig_q4_status = px.pie(
        q4_status, values='cantidad', names='status',
        title='Distribucion de Status de Ordenes',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_q4_status, use_container_width=True)

st.info("**Hallazgo:** Las cancelaciones son bajas (0.63%), pero las reviews negativas (14.7%) "
        "y las entregas tardias revelan un problema de satisfaccion mayor. "
        "La insatisfaccion real es ~10x mayor que la tasa de cancelacion.")

st.divider()

st.header("Q5: Distribucion geografica de sellers y customers")
st.markdown("Existen estados que solo consumen pero no venden? Hay oportunidades de expansion?")

q5_data = run_query("""
    SELECT
        COALESCE(c.state, s.state) AS estado,
        COALESCE(c.total_customers, 0) AS customers,
        COALESCE(s.total_sellers, 0) AS sellers,
        COALESCE(c.total_customers, 0)::FLOAT / NULLIF(COALESCE(s.total_sellers, 0), 0) AS ratio_customer_seller
    FROM (SELECT state, COUNT(*) AS total_customers FROM customers GROUP BY state) c
    FULL OUTER JOIN (SELECT state, COUNT(*) AS total_sellers FROM sellers GROUP BY state) s
    ON c.state = s.state
    ORDER BY customers DESC
""")

col_q5a, col_q5b = st.columns(2)

with col_q5a:
    fig_q5_comp = go.Figure()
    fig_q5_comp.add_trace(go.Bar(
        name='Customers', x=q5_data['estado'], y=q5_data['customers'],
        marker_color='#636EFA'
    ))
    fig_q5_comp.add_trace(go.Bar(
        name='Sellers', x=q5_data['estado'], y=q5_data['sellers'],
        marker_color='#EF553B'
    ))
    fig_q5_comp.update_layout(
        title='Customers vs Sellers por Estado',
        barmode='group',
        xaxis_title='Estado', yaxis_title='Cantidad'
    )
    st.plotly_chart(fig_q5_comp, use_container_width=True)

with col_q5b:
    q5_pagos = run_query("""
        SELECT
            c.state AS estado,
            op.payment_type,
            COUNT(*) AS cantidad
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_payments op ON o.order_id = op.order_id
        WHERE c.state IN ('SP', 'RJ', 'MG', 'RS', 'PR')
        GROUP BY c.state, op.payment_type
        ORDER BY c.state, cantidad DESC
    """)
    fig_q5_pagos = px.bar(
        q5_pagos, x='estado', y='cantidad', color='payment_type',
        title='Metodos de Pago por Estado (Top 5 estados)',
        labels={'estado': 'Estado', 'cantidad': 'Cantidad', 'payment_type': 'Tipo de Pago'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_q5_pagos, use_container_width=True)

sin_sellers = q5_data[q5_data['sellers'] == 0]
if len(sin_sellers) > 0:
    estados_sin = ', '.join(sin_sellers['estado'].tolist())
    st.warning(f"Estados sin ningun seller: **{estados_sin}** — "
               f"Representan {sin_sellers['customers'].sum():,} clientes que compran desde otros estados.")

st.info("**Hallazgo:** Sao Paulo concentra el 60% de los sellers pero solo el 42% de los customers. "
        "Hay una oportunidad de expansion: estados como BA, PE, CE tienen muchos clientes pero casi ningun seller, "
        "lo que aumenta costos de flete y tiempos de entrega.")

st.divider()

st.caption("Dashboard creado por Daniel Mera como parte de la Prueba Técnica — Data Engineer Intern · Invers AI")
st.caption("Datos: Olist Brazilian E-Commerce (Kaggle) · ~100k ordenes · 2016-2018")
