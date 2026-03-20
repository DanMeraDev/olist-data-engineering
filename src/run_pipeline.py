"""
Fase 5 — Pipeline End-to-End
Ejecuta el flujo completo: Limpieza → Carga a DB → Reporte a Telegram → Dashboard

Uso:
    python src/run_pipeline.py
"""

import subprocess
import sys
import os
import requests
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/olist-pipeline')
DASHBOARD_URL = 'http://localhost:8501'


def run_step(name, command):
    print(f'\n{"=" * 50}')
    print(f'  {name}')
    print(f'{"=" * 50}')
    result = subprocess.run(
        command,
        cwd=project_root,
        capture_output=False,
        text=True
    )
    if result.returncode != 0:
        print(f'\n   Error en: {name}')
        sys.exit(1)
    return result


def trigger_n8n_report():
    print(f'\n{"=" * 50}')
    print(f'  Paso 3: Enviando reporte a Telegram (via n8n)')
    print(f'{"=" * 50}')
    try:
        response = requests.post(N8N_WEBHOOK_URL, json={'trigger': 'pipeline'}, timeout=30)
        if response.status_code == 200:
            print(f'   Reporte enviado a Telegram')
        else:
            print(f'   n8n respondio con status {response.status_code}')
            print(f'   Respuesta: {response.text}')
    except requests.exceptions.ConnectionError:
        print(f'   No se pudo conectar a n8n en {N8N_WEBHOOK_URL}')
        print(f'   Verifica que n8n esté corriendo (docker compose up -d)')
    except Exception as e:
        print(f'   Error: {e}')


def launch_dashboard():
    print(f'\n{"=" * 50}')
    print(f'  Paso 4: Lanzando Dashboard')
    print(f'{"=" * 50}')
    dashboard_path = os.path.join(project_root, 'src', 'dashboard.py')
    process = subprocess.Popen(
        [sys.executable, '-m', 'streamlit', 'run', dashboard_path, '--server.headless', 'true'],
        cwd=project_root
    )
    time.sleep(3)
    print(f'   Dashboard corriendo en: {DASHBOARD_URL}')
    return process


def main():
    print('=' * 50)
    print('  PIPELINE END-TO-END — Olist E-Commerce')
    print('=' * 50)
    print(f'\n  Flujo: Limpieza → Carga DB → Reporte Telegram → Dashboard')

    run_step(
        'Paso 1: Limpieza y Transformación',
        [sys.executable, os.path.join(project_root, 'src', 'run_cleaning.py')]
    )

    run_step(
        'Paso 2: Carga a PostgreSQL',
        [sys.executable, os.path.join(project_root, 'src', 'load_to_db.py')]
    )

    trigger_n8n_report()

    dashboard_process = launch_dashboard()

    print(f'\n{"=" * 50}')
    print(f'  PIPELINE COMPLETADO')
    print(f'{"=" * 50}')
    print(f'\n  Paso 1: Datos limpios en data/clean/')
    print(f'  Paso 2: Datos cargados en PostgreSQL')
    print(f'  Paso 3: Reporte enviado a Telegram')
    print(f'  Paso 4: Dashboard en {DASHBOARD_URL}')
    print(f'\n  Presiona Ctrl+C para detener el dashboard')

    try:
        dashboard_process.wait()
    except KeyboardInterrupt:
        dashboard_process.terminate()
        print(f'\n   Dashboard detenido')


if __name__ == '__main__':
    main()