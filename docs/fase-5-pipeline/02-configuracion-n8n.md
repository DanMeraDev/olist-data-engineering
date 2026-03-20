# Configuracion de n8n

> Datos extraidos de [`docker-compose.yml`](../../docker-compose.yml) y [`n8n/olist_workflow.json`](../../n8n/olist_workflow.json).

---

## Docker Compose

n8n corre en Docker junto a PostgreSQL, conectados en la misma red Docker.

| Parametro | PostgreSQL | n8n |
|-----------|-----------|-----|
| Imagen | `postgres:16-alpine` | `n8nio/n8n` |
| Contenedor | `olist_postgres` | `olist_n8n` |
| Puerto host | 5433 | 5678 |
| Puerto contenedor | 5432 | 5678 |
| Volumen | `pgdata` | `n8n_data` |

n8n usa PostgreSQL como su propia base de datos interna (no SQLite), almacenando sus datos en una base separada llamada `n8n` dentro del mismo servidor PostgreSQL.

| Parametro n8n | Valor |
|---------------|-------|
| DB_TYPE | `postgresdb` |
| DB_POSTGRESDB_HOST | `postgres` |
| DB_POSTGRESDB_PORT | `5432` |
| DB_POSTGRESDB_DATABASE | `n8n` |
| DB_POSTGRESDB_USER | `olist` |
| DB_POSTGRESDB_PASSWORD | `olist123` |

n8n depende de PostgreSQL con `condition: service_healthy`, asi que no arranca hasta que PostgreSQL pase su healthcheck (`pg_isready`).

### Volumenes montados en n8n

| Volumen | Destino en contenedor | Proposito |
|---------|----------------------|-----------|
| `n8n_data` | `/home/node/.n8n` | Datos persistentes de n8n |
| `./src` | `/home/node/scripts` | Scripts de Python accesibles desde n8n |
| `./data` | `/home/node/data` | Datos accesibles desde n8n |

### Levantar los servicios

```bash
docker compose up -d
```

Verificar que ambos contenedores estan corriendo:

```bash
docker ps --filter name=olist
```

Acceder a n8n: `http://localhost:5678`

---

## Importar el Workflow

1. Abrir n8n en `http://localhost:5678`
2. Crear una cuenta local (primera vez)
3. Ir a **Workflows** > **Add workflow** > menu (tres puntos) > **Import from file**
4. Seleccionar `n8n/olist_workflow.json`
5. Guardar el workflow

---

## Configurar Credenciales de PostgreSQL

Desde n8n, ir a **Settings** > **Credentials** > **Add credential** > **Postgres**.

| Campo | Valor |
|-------|-------|
| Host | `postgres` |
| Port | `5432` |
| Database | `olist` |
| User | `olist` |
| Password | `olist123` |

**Importante:** El host debe ser `postgres` (nombre del servicio en Docker Compose), NO `localhost`. El puerto debe ser `5432` (puerto interno del contenedor), NO `5433` (puerto mapeado al host). Esto es porque dentro de la red de Docker los contenedores se comunican entre si usando el nombre del servicio como hostname y el puerto interno del contenedor, no el puerto expuesto al host.

Despues de crear la credencial, abrir cada nodo de PostgreSQL en el workflow y asignar esta credencial:
- Test DB Connection
- Query KPIs
- Query Top Categorias
- Query Metricas

---

## Configurar Credenciales de Telegram

### 1. Crear el bot

1. Abrir [`@BotFather`](https://telegram.me/BotFather) en Telegram
2. Enviar `/newbot`
3. Elegir un nombre para el bot (ej: "Olist Pipeline Bot")
4. Elegir un username (ej: `olist_pipeline_bot`)
5. BotFather responde con el **token** del bot — guardarlo

### 2. Obtener el chat_id

1. Enviar cualquier mensaje al bot recien creado en Telegram (mensaje aparte del mensjae /start)
2. Abrir en el navegador:

```
https://api.telegram.org/botTU_TOKEN/getUpdates
```

3. En el JSON de respuesta, buscar `"chat":{"id":NUMERO}` — ese numero es el `chat_id`

### 3. Configurar en n8n

Ir a **Settings** > **Credentials** > **Add credential** > **Telegram**.

| Campo | Valor |
|-------|-------|
| Access Token | El token de BotFather |

Abrir el nodo **Enviar a Telegram** en el workflow y configurar:
- Asignar la credencial de Telegram
- En el campo `chatId`, poner el `chat_id` obtenido en el paso anterior

---

## Nota sobre Telegram Trigger

El nodo **Telegram Trigger** de n8n NO funciona en localhost porque requiere un webhook HTTPS publico al que Telegram pueda enviar las actualizaciones. En un entorno local sin HTTPS, esto no es posible.

Por eso el workflow usa un **Webhook propio** de n8n como trigger (que funciona en localhost) y el nodo **Telegram** solo para enviar mensajes (que no requiere HTTPS, ya que es una llamada saliente a la API de Telegram).

---

## Nodos del Workflow

El workflow `"Olist Pipeline + Reporte Telegram"` tiene 8 nodos que se ejecutan en secuencia:

| # | Nodo | Tipo | Funcion |
|---|------|------|---------|
| 1 | Webhook Trigger | `webhook` | Recibe POST en `/webhook/olist-pipeline` |
| 2 | Test DB Connection | `postgres` | Verifica conexion con `SELECT COUNT(*) FROM orders` |
| 3 | Query KPIs | `postgres` | Total ordenes, clientes, revenue, ticket promedio |
| 4 | Query Top Categorias | `postgres` | Top 5 categorias por revenue |
| 5 | Query Metricas | `postgres` | Dias entrega, cancelaciones, reviews negativas, entregas tardias |
| 6 | Formatear Mensaje | `code` | JavaScript que construye el mensaje Markdown |
| 7 | Enviar a Telegram | `telegram` | Envia el mensaje con parse_mode Markdown |
| 8 | Responder Webhook | `respondToWebhook` | Responde `{"status": "ok"}` al pipeline |

Los queries (nodos 3, 4, 5) se disparan en paralelo desde el nodo 2. El nodo 6 (Formatear Mensaje) espera a que los 3 queries terminen, ya que necesita los resultados de todos para armar el mensaje completo.

El webhook esta configurado con `responseMode: "responseNode"`, lo que significa que la respuesta HTTP al pipeline la controla el nodo Responder Webhook al final del flujo, no el nodo Webhook Trigger.

---

## Activar el Workflow

Despues de configurar credenciales, el workflow debe estar **activo** para que el webhook funcione:

1. Abrir el workflow en n8n
2. Toggle de **Active** en la esquina superior derecha
3. Verificar que el webhook esta escuchando ejecutando:

```bash
curl -X POST http://localhost:5678/webhook/olist-pipeline -H "Content-Type: application/json" -d '{"trigger": "test"}'
```

Respuesta esperada: `{"status": "ok", "mensaje": "Reporte enviado a Telegram"}`
