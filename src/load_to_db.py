import os
import pandas as pd
from sqlalchemy import create_engine, text

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(project_root, 'data', 'clean')
SQL_PATH = os.path.join(project_root, 'sql', 'schema.sql')

DB_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://olist:olist123@localhost:5433/olist')


def crear_schema(engine):
    with open(SQL_PATH, 'r') as f:
        schema_sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()
    print('   Schema creado (tablas e indices)')


def cargar_geolocation(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_geolocation_clean.csv'))

    df_agg = df.groupby('geolocation_zip_code_prefix').agg(
        lat=('geolocation_lat', 'median'),
        lng=('geolocation_lng', 'median'),
        city=('geolocation_city', lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]),
        state=('geolocation_state', lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
    ).reset_index()

    df_agg = df_agg.rename(columns={'geolocation_zip_code_prefix': 'zip_code_prefix'})
    df_agg['lat'] = df_agg['lat'].round(6)
    df_agg['lng'] = df_agg['lng'].round(6)

    df_agg.to_sql('geolocation', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   geolocation: {len(df_agg):,} zip codes (agregada de {len(df):,} filas)')
    return df_agg


def cargar_customers(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_customers_clean.csv'))
    df = df.rename(columns={
        'customer_zip_code_prefix': 'zip_code_prefix',
        'customer_city': 'city',
        'customer_state': 'state'
    })
    df.to_sql('customers', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   customers: {len(df):,} filas')


def cargar_sellers(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_sellers_clean.csv'))
    df = df.rename(columns={
        'seller_zip_code_prefix': 'zip_code_prefix',
        'seller_city': 'city',
        'seller_state': 'state'
    })
    df.to_sql('sellers', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   sellers: {len(df):,} filas')


def cargar_products(engine):
    df_products = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_products_clean.csv'))
    df_translation = pd.read_csv(os.path.join(CLEAN_PATH, 'product_category_name_translation_clean.csv'))

    df = df_products.merge(df_translation, on='product_category_name', how='left')

    df = df.rename(columns={
        'product_category_name': 'category_name',
        'product_category_name_english': 'category_name_english',
        'product_name_length': 'name_length',
        'product_description_length': 'description_length',
        'product_photos_qty': 'photos_qty',
        'product_weight_g': 'weight_g',
        'product_length_cm': 'length_cm',
        'product_height_cm': 'height_cm',
        'product_width_cm': 'width_cm'
    })

    df.to_sql('products', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   products: {len(df):,} filas (con traduccion incluida)')


def cargar_orders(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_orders_clean.csv'))
    df = df.rename(columns={
        'order_status': 'status',
        'order_purchase_timestamp': 'purchase_timestamp',
        'order_approved_at': 'approved_at',
        'order_delivered_carrier_date': 'delivered_carrier_date',
        'order_delivered_customer_date': 'delivered_customer_date',
        'order_estimated_delivery_date': 'estimated_delivery_date'
    })

    for col in ['purchase_timestamp', 'approved_at', 'delivered_carrier_date', 'delivered_customer_date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df['estimated_delivery_date'] = pd.to_datetime(df['estimated_delivery_date'], errors='coerce').dt.date

    df.to_sql('orders', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   orders: {len(df):,} filas')


def cargar_order_items(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_order_items_clean.csv'))
    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
    df.to_sql('order_items', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   order_items: {len(df):,} filas')


def cargar_payments(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_order_payments_clean.csv'))
    df.to_sql('order_payments', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   order_payments: {len(df):,} filas')


def cargar_reviews(engine):
    df = pd.read_csv(os.path.join(CLEAN_PATH, 'olist_order_reviews_clean.csv'))
    df = df.rename(columns={
        'review_comment_title': 'comment_title',
        'review_comment_message': 'comment_message',
        'review_creation_date': 'creation_date',
        'review_answer_timestamp': 'answer_timestamp'
    })

    df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce').dt.date
    df['answer_timestamp'] = pd.to_datetime(df['answer_timestamp'], errors='coerce')

    df.to_sql('order_reviews', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    print(f'   order_reviews: {len(df):,} filas')


def main():
    print('=' * 50)
    print('  FASE 3 -- Carga de datos a PostgreSQL')
    print('=' * 50)

    engine = create_engine(DB_URL)

    print('\nCreando schema...')
    crear_schema(engine)

    print('\nCargando datos...')
    cargar_geolocation(engine)
    cargar_customers(engine)
    cargar_sellers(engine)
    cargar_products(engine)
    cargar_orders(engine)
    cargar_order_items(engine)
    cargar_payments(engine)
    cargar_reviews(engine)

    print('\nVerificacion...')
    with engine.connect() as conn:
        for table in ['geolocation', 'customers', 'sellers', 'products',
                      'orders', 'order_items', 'order_payments', 'order_reviews']:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
            count = result.scalar()
            print(f'   {table}: {count:,} registros')

    print(f'\n{"=" * 50}')
    print('  FASE 3 COMPLETADA')
    print(f'{"=" * 50}')


if __name__ == '__main__':
    main()
