import os
import sys
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.cleaning.clean_customers import limpiar_customers
from src.cleaning.clean_geolocation import limpiar_geolocation
from src.cleaning.clean_order_items import limpiar_order_items
from src.cleaning.clean_payments import limpiar_payments
from src.cleaning.clean_reviews import limpiar_reviews
from src.cleaning.clean_orders import limpiar_orders
from src.cleaning.clean_products import limpiar_products
from src.cleaning.clean_sellers import limpiar_sellers
from src.cleaning.clean_category_translation import limpiar_category_translation


def main():
    RAW_PATH = os.path.join(project_root, 'data', 'raw')
    CLEAN_PATH = os.path.join(project_root, 'data', 'clean')
    os.makedirs(CLEAN_PATH, exist_ok=True)

    print('=' * 50)
    print('  FASE 2 — Limpieza y Transformacion')
    print('  Dataset: Olist Brazilian E-Commerce')
    print('=' * 50)
    print(f'\nLeyendo datos de: {RAW_PATH}')
    print(f'Guardando datos en: {CLEAN_PATH}')

    print('\nCargando datasets raw...')
    df_customers = pd.read_csv(os.path.join(RAW_PATH, 'olist_customers_dataset.csv'))
    df_geolocation = pd.read_csv(os.path.join(RAW_PATH, 'olist_geolocation_dataset.csv'))
    df_order_items = pd.read_csv(os.path.join(RAW_PATH, 'olist_order_items_dataset.csv'))
    df_payments = pd.read_csv(os.path.join(RAW_PATH, 'olist_order_payments_dataset.csv'))
    df_reviews = pd.read_csv(os.path.join(RAW_PATH, 'olist_order_reviews_dataset.csv'), on_bad_lines='warn')
    df_orders = pd.read_csv(os.path.join(RAW_PATH, 'olist_orders_dataset.csv'))
    df_products = pd.read_csv(os.path.join(RAW_PATH, 'olist_products_dataset.csv'))
    df_sellers = pd.read_csv(os.path.join(RAW_PATH, 'olist_sellers_dataset.csv'))
    df_category_translation = pd.read_csv(os.path.join(RAW_PATH, 'product_category_name_translation.csv'))
    print('Todos los datasets cargados')

    df_customers_clean = limpiar_customers(df_customers)
    df_geolocation_clean = limpiar_geolocation(df_geolocation)
    df_order_items_clean = limpiar_order_items(df_order_items)
    df_payments_clean = limpiar_payments(df_payments)
    df_reviews_clean = limpiar_reviews(df_reviews)
    df_orders_clean = limpiar_orders(df_orders)
    df_products_clean = limpiar_products(df_products)
    df_sellers_clean = limpiar_sellers(df_sellers)
    df_category_clean = limpiar_category_translation(df_category_translation)

    print(f'\n{"=" * 50}')
    print('  Guardando datasets limpios...')
    print(f'{"=" * 50}')

    datasets_limpios = {
        'olist_customers_clean.csv': df_customers_clean,
        'olist_geolocation_clean.csv': df_geolocation_clean,
        'olist_order_items_clean.csv': df_order_items_clean,
        'olist_order_payments_clean.csv': df_payments_clean,
        'olist_order_reviews_clean.csv': df_reviews_clean,
        'olist_orders_clean.csv': df_orders_clean,
        'olist_products_clean.csv': df_products_clean,
        'olist_sellers_clean.csv': df_sellers_clean,
        'product_category_name_translation_clean.csv': df_category_clean
    }

    date_format = '%Y-%m-%d %H:%M'
    date_only_format = '%Y-%m-%d'

    for nombre, df in datasets_limpios.items():
        ruta = os.path.join(CLEAN_PATH, nombre)
        # Formatear columnas datetime antes de guardar
        df_export = df.copy()
        for col in df_export.columns:
            if pd.api.types.is_datetime64_any_dtype(df_export[col]):
                # Detectar si es solo fecha (hora siempre 00:00) o fecha+hora
                tiene_hora = (df_export[col].dropna().dt.hour != 0).any()
                if tiene_hora:
                    df_export[col] = df_export[col].dt.strftime(date_format)
                else:
                    df_export[col] = df_export[col].dt.strftime(date_only_format)
                # Limpiar los NaT que strftime convierte a 'NaT'
                df_export[col] = df_export[col].replace('NaT', '')
        df_export.to_csv(ruta, index=False)
        print(f'     {nombre} ({len(df):,} filas)')

    print(f'\n{"=" * 50}')
    print('  FASE 2 COMPLETADA')
    print(f'{"=" * 50}')
    print(f'\n  {len(datasets_limpios)} datasets limpiados y guardados en {CLEAN_PATH}')


if __name__ == '__main__':
    main()