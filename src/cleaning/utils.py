import unicodedata
import pandas as pd


def remover_diacriticos(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto)
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_ciudad(ciudad):
    """
    Normaliza nombres de ciudades:
    1. Minúsculas
    2. Remueve diacríticos
    3. Remueve espacios extra
    4. Corrige encoding corrupto (£ → a)
    5. Si tiene comas (formato 'ciudad, estado, pais'), extrae solo la ciudad
    6. Si tiene guion (formato 'ciudad - estado'), extrae solo la ciudad
    7. Si tiene paréntesis, los remueve
    """
    if pd.isna(ciudad):
        return ciudad
    ciudad = str(ciudad).strip().lower()
    # Corregir encoding corrupto
    ciudad = ciudad.replace('£', 'a')
    # Extraer solo ciudad si tiene formato 'ciudad, estado, pais'
    if ',' in ciudad:
        ciudad = ciudad.split(',')[0].strip()
    # Extraer solo ciudad si tiene formato 'ciudad - estado/distrito'
    if ' - ' in ciudad:
        ciudad = ciudad.split(' - ')[0].strip()
    # Remover paréntesis y su contenido
    import re
    ciudad = re.sub(r'\s*\(.*?\)', '', ciudad).strip()
    # Remover diacríticos
    ciudad = remover_diacriticos(ciudad)
    # Remover espacios múltiples
    ciudad = ' '.join(ciudad.split())
    return ciudad


def convertir_fechas(df, columnas, dayfirst=True):
    df = df.copy()
    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=dayfirst, errors='coerce')
    return df


def log_limpieza(mensaje):
    print(f'   {mensaje}')


def log_inicio(nombre):
    print(f'\n{"=" * 50}')
    print(f'  Limpiando: {nombre}')
    print(f'{"=" * 50}')


def log_resultado(df_original, df_limpio, nombre):
    filas_orig = len(df_original)
    filas_limp = len(df_limpio)
    eliminadas = filas_orig - filas_limp
    print(f'\n   Resultado {nombre}:')
    print(f'   Filas originales: {filas_orig:,}')
    print(f'   Filas finales:    {filas_limp:,}')
    if eliminadas > 0:
        print(f'   Filas eliminadas: {eliminadas:,} ({eliminadas/filas_orig*100:.2f}%)')
    print(f'   Limpieza completada')