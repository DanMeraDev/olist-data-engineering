import pandas as pd
from .utils import log_inicio, log_limpieza, log_resultado


def limpiar_products(df):
    log_inicio('Products')
    df_original = df.copy()
    df = df.copy()

    df = df.rename(columns={
        'product_name_lenght': 'product_name_length',
        'product_description_lenght': 'product_description_length'
    })
    log_limpieza('Typo corregido: "lenght" -> "length" en nombres de columnas')

    sin_cat = df['product_category_name'].isna().sum()
    df['product_category_name'] = df['product_category_name'].fillna('sin_categoria')
    log_limpieza(f'{sin_cat} productos sin categoria etiquetados como "sin_categoria"')

    peso_cero = (df['product_weight_g'] == 0).sum()
    df.loc[df['product_weight_g'] == 0, 'product_weight_g'] = pd.NA
    log_limpieza(f'{peso_cero} productos con peso=0g convertidos a NaN')

    log_resultado(df_original, df, 'Products')
    return df