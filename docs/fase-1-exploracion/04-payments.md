# Payments (Pagos)

**103,886 filas** | 5 columnas | Sin nulos | Sin duplicados

> Datos obtenidos del análisis en [`01_exploracion_diagnostico.ipynb`](../../notebooks/01_exploracion_diagnostico.ipynb).

---

## Estructura

| Columna | Tipo | Únicos |
|---------|------|--------|
| order_id | str (32 hex) | 99,440 |
| payment_sequential | int64 | 29 |
| payment_type | str | 5 |
| payment_installments | int64 | 24 |
| payment_value | float64 | 29,077 |

---

## Distribución de Tipos de Pago

```
credit_card: 76,795 (73.9%)
boleto:      19,784 (19.0%)
voucher:      5,775  (5.6%)
debit_card:   1,529  (1.5%)
not_defined:      3  (0.0%)
```

---

## Problemas Detectados

### 1. Pagos "not_defined"
3 registros con tipo `not_defined`, todos con valor $0.00 y pertenecientes a **órdenes canceladas**.

### 2. Pagos con valor cero
9 pagos con valor = 0: 6 vouchers + 3 not_defined.

### 3. Installments = 0 en tarjeta de crédito
2 registros de `credit_card` con 0 cuotas (debería ser mínimo 1).

---

## Observaciones

- Solo `credit_card` usa cuotas > 1 (boleto, voucher y debit siempre son 1)
- 3,039 órdenes (3.1%) usan múltiples métodos de pago
- Sin valores negativos en montos

---

## Decisiones Fase 2

- Eliminar los 3 registros `not_defined` (órdenes canceladas sin valor)
- Corregir los 2 installments = 0 a 1
