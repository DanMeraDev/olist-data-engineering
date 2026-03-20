import pandas as pd
from .utils import log_inicio, log_limpieza, log_resultado


def limpiar_payments(df):
    log_inicio('Payments')
    df_original = df.copy()
    df = df.copy()

    antes = len(df)
    df = df[df['payment_type'] != 'not_defined']
    log_limpieza(f'Pagos not_defined eliminados: {antes - len(df):,}')

    mask = (df['payment_type'] == 'credit_card') & (df['payment_installments'] == 0)
    corregidos = mask.sum()
    df.loc[mask, 'payment_installments'] = 1
    log_limpieza(f'Credit cards con installments=0 corregidos a 1: {corregidos}')

    log_resultado(df_original, df, 'Payments')
    return df