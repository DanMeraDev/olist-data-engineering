import pandas as pd
from .utils import convertir_fechas, log_inicio, log_limpieza, log_resultado


def limpiar_reviews(df):
    log_inicio('Reviews')
    df_original = df.copy()
    df = df.copy()

    df = convertir_fechas(df, ['review_creation_date', 'review_answer_timestamp'])
    log_limpieza('Fechas convertidas a datetime (dayfirst=True)');

    df['review_creation_date'] = df['review_creation_date'].dt.normalize()
    log_limpieza('review_creation_date normalizado a solo fecha')

    dupes = df['review_id'].duplicated().sum()
    log_limpieza(f'review_id duplicados: {dupes} (se mantienen, son validos)')

    for col in ['review_comment_title', 'review_comment_message']:
        df[col] = df[col].str.strip()
    log_limpieza('Espacios en blanco limpiados en comentarios');

    for col in ['review_comment_title', 'review_comment_message']:
        df[col] = df[col].str.replace('\n', ' ', regex=False)
        df[col] = df[col].str.replace('\r', ' ', regex=False)
        df[col] = df[col].str.replace('  ', ' ', regex=False)
    log_limpieza('Saltos de linea removidos en comentarios')

    log_resultado(df_original, df, 'Reviews')
    return df