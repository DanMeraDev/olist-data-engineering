import pandas as pd
from .utils import normalizar_ciudad, log_inicio, log_limpieza, log_resultado


def limpiar_sellers(df):
    log_inicio('Sellers')
    df_original = df.copy()
    df = df.copy()

    df['seller_city'] = df['seller_city'].apply(normalizar_ciudad)
    log_limpieza('Ciudades normalizadas (minusculas, sin diacriticos)')

    df['seller_state'] = df['seller_state'].str.upper().str.strip()
    log_limpieza('Estados normalizados a mayusculas')

    log_resultado(df_original, df, 'Sellers')
    return df