import pandas as pd
from .utils import convertir_fechas, log_inicio, log_limpieza, log_resultado


def limpiar_order_items(df):
    log_inicio('Order Items')
    df_original = df.copy()
    df = df.copy()

    df['freight_value'] = pd.to_numeric(df['freight_value'], errors='coerce')
    nulos_freight = df['freight_value'].isna().sum()
    log_limpieza(f'freight_value convertido a numerico ({nulos_freight} no convertibles -> NaN)')

    df = convertir_fechas(df, ['shipping_limit_date'])
    log_limpieza('shipping_limit_date convertido a datetime')

    fechas_2020 = df['shipping_limit_date'].dt.year == 2020
    if fechas_2020.sum() > 0:
        log_limpieza(f'{fechas_2020.sum()} registros con shipping_limit_date en 2020 (se mantienen)')

    log_resultado(df_original, df, 'Order Items')
    return df