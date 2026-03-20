import pandas as pd
from .utils import normalizar_ciudad, log_inicio, log_limpieza, log_resultado


def limpiar_customers(df):
    log_inicio('Customers')
    df_original = df.copy()
    df = df.copy()

    df['customer_city'] = df['customer_city'].apply(normalizar_ciudad)
    log_limpieza('Ciudades normalizadas (minusculas, sin diacriticos)')

    df['customer_state'] = df['customer_state'].str.upper().str.strip()
    log_limpieza('Estados normalizados a mayusculas')

    log_resultado(df_original, df, 'Customers')
    return df