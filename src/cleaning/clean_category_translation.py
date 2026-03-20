import pandas as pd
from .utils import log_inicio, log_limpieza, log_resultado


def limpiar_category_translation(df):
    log_inicio('Category Translation')
    df_original = df.copy()
    df = df.copy()

    correcciones = {
        'fashio_female_clothing': 'fashion_female_clothing',
        'costruction_tools_garden': 'construction_tools_garden',
        'costruction_tools_tools': 'construction_tools_tools',
        'home_confort': 'home_comfort'
    }
    for mal, bien in correcciones.items():
        df.loc[df['product_category_name_english'] == mal, 'product_category_name_english'] = bien
        log_limpieza(f'Typo corregido: "{mal}" -> "{bien}"')

    nuevas = pd.DataFrame([
        {'product_category_name': 'pc_gamer', 'product_category_name_english': 'pc_gamer'},
        {'product_category_name': 'portateis_cozinha_e_preparadores_de_alimentos',
         'product_category_name_english': 'portable_kitchen_and_food_preparers'}
    ])
    df = pd.concat([df, nuevas], ignore_index=True)
    log_limpieza('2 categorias faltantes agregadas')

    log_resultado(df_original, df, 'Category Translation')
    return df