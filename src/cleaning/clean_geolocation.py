import pandas as pd
from .utils import normalizar_ciudad, log_inicio, log_limpieza, log_resultado


def limpiar_geolocation(df):
    log_inicio('Geolocation')
    df_original = df.copy()
    df = df.copy()

    antes = len(df)
    df = df.drop_duplicates()
    log_limpieza(f'Duplicados eliminados: {antes - len(df):,}')

    df['geolocation_city'] = df['geolocation_city'].apply(normalizar_ciudad)
    log_limpieza('Ciudades normalizadas (encoding, diacriticos, comas)')

    df['geolocation_state'] = df['geolocation_state'].str.upper().str.strip()
    log_limpieza('Estados normalizados a mayusculas')

    lat_min, lat_max = -33.75, 5.27
    lng_min, lng_max = -73.99, -34.79
    antes = len(df)
    df = df[
        (df['geolocation_lat'] >= lat_min) &
        (df['geolocation_lat'] <= lat_max) &
        (df['geolocation_lng'] >= lng_min) &
        (df['geolocation_lng'] <= lng_max)
    ]
    log_limpieza(f'Coordenadas fuera de Brasil eliminadas: {antes - len(df):,}')

    df['geolocation_lat'] = df['geolocation_lat'].round(6)
    df['geolocation_lng'] = df['geolocation_lng'].round(6)
    log_limpieza('Coordenadas redondeadas a 6 decimales')
    
    antes = len(df)
    df = df.drop_duplicates()
    if antes - len(df) > 0:
        log_limpieza(f'Duplicados post-normalizacion eliminados: {antes - len(df):,}')
    log_resultado(df_original, df, 'Geolocation')
    return df