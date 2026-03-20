import pandas as pd
from .utils import convertir_fechas, log_inicio, log_limpieza, log_resultado


def limpiar_orders(df):
    log_inicio('Orders')
    df_original = df.copy()
    df = df.copy()

    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    df = convertir_fechas(df, date_cols)
    log_limpieza('Fechas convertidas a datetime (dayfirst=True)')

    df['order_estimated_delivery_date'] = df['order_estimated_delivery_date'].dt.normalize()
    log_limpieza('order_estimated_delivery_date normalizado a solo fecha')

    df['order_status'] = df['order_status'].str.lower().str.strip()
    log_limpieza('order_status normalizado a minusculas')

    entregas = df.dropna(subset=['order_delivered_customer_date'])
    anomalias = entregas[
        entregas['order_delivered_customer_date'] < entregas['order_purchase_timestamp']
    ]
    log_limpieza(f'Verificacion temporal: {len(anomalias)} entregas antes de compra')

    log_resultado(df_original, df, 'Orders')
    return df