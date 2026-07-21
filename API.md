# Masa Internal API

FastAPI application for customer, contract, aggregate, invoice, FX rate, and financial KPI management.

**Base URL:** `http://localhost:8000` (default when running `uvicorn main:app --reload`)

**Interactive docs:** `/docs` (Swagger UI) · `/redoc` (ReDoc)

---

## Table of Contents

- [General](#general)
- [Root](#root)
- [Customers](#customers)
  - [Customers](#customers-1)
  - [Contracts](#contracts)
  - [Aggregates](#aggregates)
  - [Equipments](#equipments)
- [Treasury](#treasury)
  - [Financial KPIs](#financial-kpis)
  - [Invoices](#invoices)
  - [FX Rates](#fx-rates)

---

## General

### Conventions

| Topic | Detail |
|-------|--------|
| **Dates** | ISO 8601 date strings: `YYYY-MM-DD` |
| **Decimals** | Monetary and rate values are `Decimal`; JSON responses may serialize them as strings |
| **List responses** | Supabase-backed endpoints return a JSON **array** of row objects, even for single-record lookups |
| **PATCH** | Only fields included in the request body are updated (`exclude_unset`) |
| **Errors** | Failures return standard FastAPI error bodies, e.g. `{"detail": "..."}` with HTTP 4xx/5xx |

### Common response shape

Most CRUD endpoints return an array of database rows. Each row includes an auto-generated `id` plus the table columns.

**Example (single customer lookup):**

```json
[
  {
    "id": 1,
    "name": "Acme Mining",
    "legal_name": "PT Acme Mining Indonesia",
    "npwp": "01.234.567.8-901.000",
    "address": "Jakarta, Indonesia",
    "customer_type": "mining",
    "site_name": "Site Alpha",
    "site_legal_name": "PT Acme Site Alpha",
    "site_address": "Kalimantan",
    "resource": "coal",
    "pic_id": 2
  }
]
```

An empty result set returns `[]`.

---

## Root

### `GET /`

Health-style root endpoint.

**Response**

```json
{
  "Hello": "World"
}
```

**Example**

```bash
curl http://localhost:8000/
```

---

### `GET /items/{item_id}`

Sample endpoint (FastAPI boilerplate).

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `item_id` | `int` | Item identifier |

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `q` | `string` | No | Optional query string |

**Response**

```json
{
  "item_id": 42,
  "q": "search term"
}
```

**Example**

```bash
curl "http://localhost:8000/items/42?q=search+term"
```

---

## Customers

**Prefix:** `/customers`

---

### Customers

#### `GET /customers/customers`

List all customers.

**Response:** Array of customer objects.

**Example**

```bash
curl http://localhost:8000/customers/customers
```

```json
[
  {
    "id": 1,
    "name": "Acme Mining",
    "legal_name": "PT Acme Mining Indonesia",
    "npwp": "01.234.567.8-901.000",
    "address": "Jakarta, Indonesia",
    "customer_type": "mining",
    "site_name": "Site Alpha",
    "site_legal_name": "PT Acme Site Alpha",
    "site_address": "Kalimantan",
    "resource": "coal",
    "pic_id": 2
  }
]
```

---

#### `GET /customers/customers/{customer_id}`

Get a customer by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `customer_id` | `int` | Customer ID |

**Response:** Array with zero or one customer object.

**Example**

```bash
curl http://localhost:8000/customers/customers/1
```

---

#### `POST /customers/add_customer`

Create a customer.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No | Display name |
| `legal_name` | `string` | No | Legal entity name |
| `npwp` | `string` | No | Tax ID (NPWP) |
| `address` | `string` | No | Address |
| `customer_type` | `string` | No | Customer type |
| `site_name` | `string` | No | Site display name |
| `site_legal_name` | `string` | No | Site legal name |
| `site_address` | `string` | No | Site address |
| `resource` | `string` | No | Resource type |
| `pic_id` | `int` | No | Person-in-charge ID |

**Response:** Array containing the created row(s).

**Example**

```bash
curl -X POST http://localhost:8000/customers/add_customer \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Mining",
    "legal_name": "PT Acme Mining Indonesia",
    "npwp": "01.234.567.8-901.000",
    "address": "Jakarta, Indonesia",
    "customer_type": "mining",
    "site_name": "Site Alpha",
    "site_legal_name": "PT Acme Site Alpha",
    "site_address": "Kalimantan",
    "resource": "coal",
    "pic_id": 2
  }'
```

---

#### `PATCH /customers/update_customer/{customer_id}`

Update a customer. Only fields present in the body are updated.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `customer_id` | `int` | Customer ID |

**Request body:** Same fields as `POST /customers/add_customer` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/customers/update_customer/1 \
  -H "Content-Type: application/json" \
  -d '{"site_name": "Site Beta"}'
```

---

#### `DELETE /customers/delete_customer/{customer_id}`

Delete a customer by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `customer_id` | `int` | Customer ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_customer/1
```

---

#### `DELETE /customers/delete_customers`

Delete all customers.

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_customers
```

---

### Contracts

#### `GET /customers/contracts`

List all contracts.

**Response:** Array of contract objects.

**Example**

```bash
curl http://localhost:8000/customers/contracts
```

```json
[
  {
    "id": 1,
    "customer_id": 1,
    "contract_number": "CTR-2024-001",
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    "currency": "USD",
    "price_dt": "5000.00",
    "price_exca": "8000.00",
    "price_lv": "3000.00",
    "price_dozer": "4000.00",
    "price_grader": "3500.00",
    "price_water_truck": "2500.00",
    "price_fuel_truck": "2800.00",
    "price_manhauler": "6000.00"
  }
]
```

---

#### `GET /customers/contracts/{contract_id}`

Get a contract by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `contract_id` | `int` | Contract ID |

**Response:** Array with zero or one contract object.

**Example**

```bash
curl http://localhost:8000/customers/contracts/1
```

---

#### `POST /customers/add_contract`

Create a contract.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer_id` | `int` | No | Linked customer ID |
| `contract_number` | `string` | No | Contract reference number |
| `start_date` | `date` | No | Contract start date |
| `end_date` | `date` | No | Contract end date |
| `currency` | `string` | No | `"USD"` or `"IDR"` |
| `price_dt` | `decimal` | No | Unit price — dump truck |
| `price_exca` | `decimal` | No | Unit price — excavator |
| `price_lv` | `decimal` | No | Unit price — light vehicle |
| `price_dozer` | `decimal` | No | Unit price — dozer |
| `price_grader` | `decimal` | No | Unit price — grader |
| `price_water_truck` | `decimal` | No | Unit price — water truck |
| `price_fuel_truck` | `decimal` | No | Unit price — fuel truck |
| `price_manhauler` | `decimal` | No | Unit price — manhauler |

**Response:** Array containing the created row(s).

**Example**

```bash
curl -X POST http://localhost:8000/customers/add_contract \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "contract_number": "CTR-2024-001",
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    "currency": "USD",
    "price_dt": 5000,
    "price_exca": 8000,
    "price_lv": 3000,
    "price_dozer": 4000,
    "price_grader": 3500,
    "price_water_truck": 2500,
    "price_fuel_truck": 2800,
    "price_manhauler": 6000
  }'
```

---

#### `PATCH /customers/update_contract/{contract_id}`

Update a contract. Only fields present in the body are updated.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `contract_id` | `int` | Contract ID |

**Request body:** Same fields as `POST /customers/add_contract` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/customers/update_contract/1 \
  -H "Content-Type: application/json" \
  -d '{"end_date": "2026-12-31"}'
```

---

#### `DELETE /customers/delete_contract/{contract_id}`

Delete a contract by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `contract_id` | `int` | Contract ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_contract/1
```

---

#### `DELETE /customers/delete_contracts`

Delete all contracts.

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_contracts
```

---

### Aggregates

Vehicle fleet counts per customer, used for invoice and MRR/ARR calculations.

#### `GET /customers/aggregates`

List all aggregates.

**Response:** Array of aggregate objects.

**Example**

```bash
curl http://localhost:8000/customers/aggregates
```

```json
[
  {
    "id": 1,
    "customer_id": 1,
    "updated_at": "2024-06-01",
    "dt": 10,
    "exca": 5,
    "lv": 8,
    "dozer": 3,
    "grader": 2,
    "water_truck": 4,
    "fuel_truck": 3,
    "manhauler": 6
  }
]
```

---

#### `GET /customers/aggregates/{aggregate_id}`

Get an aggregate by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `aggregate_id` | `int` | Aggregate ID |

**Response:** Array with zero or one aggregate object.

**Example**

```bash
curl http://localhost:8000/customers/aggregates/1
```

---

#### `POST /customers/add_aggregate`

Create an aggregate record.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer_id` | `int` | No | Linked customer ID |
| `updated_at` | `date` | No | Effective date of this fleet snapshot |
| `dt` | `int` | No | Dump truck count |
| `exca` | `int` | No | Excavator count |
| `lv` | `int` | No | Light vehicle count |
| `dozer` | `int` | No | Dozer count |
| `grader` | `int` | No | Grader count |
| `water_truck` | `int` | No | Water truck count |
| `fuel_truck` | `int` | No | Fuel truck count |
| `manhauler` | `int` | No | Manhauler count |

**Response:** Array containing the created row(s).

**Example**

```bash
curl -X POST http://localhost:8000/customers/add_aggregate \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "updated_at": "2024-06-01",
    "dt": 10,
    "exca": 5,
    "lv": 8,
    "dozer": 3,
    "grader": 2,
    "water_truck": 4,
    "fuel_truck": 3,
    "manhauler": 6
  }'
```

---

#### `PATCH /customers/update_aggregate/{aggregate_id}`

Update an aggregate. Only fields present in the body are updated.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `aggregate_id` | `int` | Aggregate ID |

**Request body:** Same fields as `POST /customers/add_aggregate` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/customers/update_aggregate/1 \
  -H "Content-Type: application/json" \
  -d '{"dt": 12, "exca": 6}'
```

---

#### `DELETE /customers/delete_aggregate/{aggregate_id}`

Delete an aggregate by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `aggregate_id` | `int` | Aggregate ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_aggregate/1
```

---

#### `DELETE /customers/delete_aggregates`

Delete all aggregates.

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_aggregates
```

---

### Equipments

Vehicle equipment counts per customer.

#### `GET /customers/equipments`

List all equipments.

**Response:** Array of equipment objects.

**Example**

```bash
curl http://localhost:8000/customers/equipments
```

```json
[
  {
    "id": 1,
    "customer_id": 1,
    "updated_at": "2024-06-01",
    "dt": 10,
    "exca": 5,
    "lv": 8,
    "dozer": 3,
    "grader": 2,
    "water_truck": 4,
    "fuel_truck": 3,
    "manhauler": 6
  }
]
```

---

#### `GET /customers/equipments/{equipment_id}`

Get an equipment record by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `equipment_id` | `int` | Equipment ID |

**Response:** Array with zero or one equipment object.

**Example**

```bash
curl http://localhost:8000/customers/equipments/1
```

---

#### `POST /customers/add_equipment`

Create an equipment record.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customer_id` | `int` | No | Linked customer ID |
| `updated_at` | `date` | No | Effective date of this fleet snapshot |
| `dt` | `int` | No | Dump truck count |
| `exca` | `int` | No | Excavator count |
| `lv` | `int` | No | Light vehicle count |
| `dozer` | `int` | No | Dozer count |
| `grader` | `int` | No | Grader count |
| `water_truck` | `int` | No | Water truck count |
| `fuel_truck` | `int` | No | Fuel truck count |
| `manhauler` | `int` | No | Manhauler count |

**Response:** Array containing the created row(s).

**Example**

```bash
curl -X POST http://localhost:8000/customers/add_equipment \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "updated_at": "2024-06-01",
    "dt": 10,
    "exca": 5,
    "lv": 8,
    "dozer": 3,
    "grader": 2,
    "water_truck": 4,
    "fuel_truck": 3,
    "manhauler": 6
  }'
```

---

#### `PATCH /customers/update_equipment/{equipment_id}`

Update an equipment record. Only fields present in the body are updated.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `equipment_id` | `int` | Equipment ID |

**Request body:** Same fields as `POST /customers/add_equipment` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/customers/update_equipment/1 \
  -H "Content-Type: application/json" \
  -d '{"dt": 12, "exca": 6}'
```

---

#### `DELETE /customers/delete_equipment/{equipment_id}`

Delete an equipment record by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `equipment_id` | `int` | Equipment ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_equipment/1
```

---

#### `DELETE /customers/delete_equipments`

Delete all equipments.

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/customers/delete_equipments
```

---

## Treasury

**Prefix:** `/treasury`

---

### Financial KPIs

MRR (Monthly Recurring Revenue) and ARR (Annual Recurring Revenue) are computed from contracts, aggregates, and FX rates. Amounts are derived by multiplying each vehicle count by its contract price for each month in the contract period.

#### `GET /treasury/financial_kpis`

> **Not implemented.** Returns `null` (no response body logic).

---

#### `GET /treasury/mrr_arr_monthly`

Aggregated MRR and ARR totals across all customers, broken down by calendar month.

**Response:** Array of monthly summary objects.

| Field | Type | Description |
|-------|------|-------------|
| `year` | `int` | Calendar year |
| `month` | `int` | Calendar month (1–12) |
| `mrr_idr_original` | `decimal` | MRR from IDR-denominated contracts |
| `mrr_usd_original` | `decimal` | MRR from USD-denominated contracts |
| `mrr_total_idr` | `decimal` | Total MRR in IDR |
| `mrr_total_usd` | `decimal` | Total MRR in USD |
| `mrr_usd_percentage` | `decimal` | USD share of total MRR (%) |
| `arr_idr_original` | `decimal` | ARR from IDR contracts |
| `arr_usd_original` | `decimal` | ARR from USD contracts |
| `arr_total_idr` | `decimal` | Total ARR in IDR |
| `arr_total_usd` | `decimal` | Total ARR in USD |
| `arr_usd_percentage` | `decimal` | USD share of total ARR (%) |
| `percentage_change` | `decimal` | MRR total IDR change vs. previous month (%) |

**Example**

```bash
curl http://localhost:8000/treasury/mrr_arr_monthly
```

```json
[
  {
    "year": 2024,
    "month": 6,
    "mrr_idr_original": "150000000.00",
    "mrr_usd_original": "50000.00",
    "mrr_total_idr": "1025000000.00",
    "mrr_total_usd": "58571.43",
    "mrr_usd_percentage": "85.37",
    "arr_idr_original": "1800000000.00",
    "arr_usd_original": "600000.00",
    "arr_total_idr": "12300000000.00",
    "arr_total_usd": "702857.16",
    "arr_usd_percentage": "85.37",
    "percentage_change": "3.25"
  }
]
```

---

#### `GET /treasury/mrr_arr_current`

Same metrics as `mrr_arr_monthly`, but only for the current calendar month.

**Response:** Single summary object (not wrapped in an array).

**Example**

```bash
curl http://localhost:8000/treasury/mrr_arr_current
```

```json
{
  "year": 2026,
  "month": 7,
  "mrr_idr_original": "150000000.00",
  "mrr_usd_original": "50000.00",
  "mrr_total_idr": "1025000000.00",
  "mrr_total_usd": "58571.43",
  "mrr_usd_percentage": "85.37",
  "arr_idr_original": "1800000000.00",
  "arr_usd_original": "600000.00",
  "arr_total_idr": "12300000000.00",
  "arr_total_usd": "702857.16",
  "arr_usd_percentage": "85.37",
  "percentage_change": "1.50"
}
```

---

#### `GET /treasury/average_mrr_arr_per_customer_current`

Average MRR and ARR per customer for the current calendar month. Totals include all USD and IDR amounts (with FX conversion), divided by the number of customers with an active contract in that month.

**Response:** Single summary object.

| Field | Type | Description |
|-------|------|-------------|
| `year` | `int` | Calendar year |
| `month` | `int` | Calendar month (1–12) |
| `active_customers` | `int` | Customers with an active contract in this month |
| `mrr_per_customer_idr` | `decimal` | Total MRR in IDR ÷ `active_customers` |
| `mrr_per_customer_usd` | `decimal` | Total MRR in USD ÷ `active_customers` |
| `arr_per_customer_idr` | `decimal` | Total ARR in IDR ÷ `active_customers` |
| `arr_per_customer_usd` | `decimal` | Total ARR in USD ÷ `active_customers` |
| `percentage_change` | `decimal` | Change in average MRR per customer (IDR) vs. previous month (%) |

**Example**

```bash
curl http://localhost:8000/treasury/average_mrr_arr_per_customer_current
```

```json
{
  "year": 2026,
  "month": 7,
  "active_customers": 2,
  "mrr_per_customer_idr": "59625000",
  "mrr_per_customer_usd": "3407.14",
  "arr_per_customer_idr": "715500000",
  "arr_per_customer_usd": "40885.71",
  "percentage_change": "0"
}
```

---

#### `GET /treasury/average_mrr_arr_per_unit_current`

Average MRR and ARR per unit for the current calendar month. Totals include all USD and IDR amounts (with FX conversion), divided by the total number of active units across all customers with active contracts.

A **unit** is one vehicle counted in aggregates: `dt`, `exca`, `lv`, `manhauler`, `dozer`, `grader`, `fuel_truck`, or `water_truck`.

**Response:** Single summary object.

| Field | Type | Description |
|-------|------|-------------|
| `year` | `int` | Calendar year |
| `month` | `int` | Calendar month (1–12) |
| `active_units` | `int` | Total active units across all customers in this month |
| `mrr_per_unit_idr` | `decimal` | Total MRR in IDR ÷ `active_units` |
| `mrr_per_unit_usd` | `decimal` | Total MRR in USD ÷ `active_units` |
| `arr_per_unit_idr` | `decimal` | Total ARR in IDR ÷ `active_units` |
| `arr_per_unit_usd` | `decimal` | Total ARR in USD ÷ `active_units` |
| `percentage_change` | `decimal` | Change in average MRR per unit (IDR) vs. previous month (%) |

**Example**

```bash
curl http://localhost:8000/treasury/average_mrr_arr_per_unit_current
```

```json
{
  "year": 2026,
  "month": 7,
  "active_units": 225,
  "mrr_per_unit_idr": "530000",
  "mrr_per_unit_usd": "30.29",
  "arr_per_unit_idr": "6360000",
  "arr_per_unit_usd": "363.43",
  "percentage_change": "0"
}
```

---

#### `GET /treasury/mrr_by_customer`

MRR breakdown for a single customer.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `customer_id` | `int` | Yes | Customer ID |

**Response:** MRR object.

| Field | Type | Description |
|-------|------|-------------|
| `customer_id` | `int` | Customer ID |
| `name` | `string` | Customer name |
| `legal_name` | `string` | Legal name |
| `site_name` | `string` | Site name |
| `site_legal_name` | `string` | Site legal name |
| `currency` | `string` | Contract currency |
| `monthly` | `array` | Per-month breakdown |
| `total_usd` | `decimal` | Sum of monthly USD amounts |
| `total_idr` | `decimal` | Sum of monthly IDR amounts |

Each item in `monthly`:

| Field | Type | Description |
|-------|------|-------------|
| `month` | `date` | Month (ISO date, first of month logic) |
| `currency` | `string` | Contract currency |
| `amount_usd` | `decimal` | MRR in USD for that month |
| `amount_idr` | `decimal` | MRR in IDR for that month |

**Errors:** `404` if customer, contract, or aggregates are missing. `400` if contract dates are missing.

**Example**

```bash
curl "http://localhost:8000/treasury/mrr_by_customer?customer_id=1"
```

```json
{
  "customer_id": 1,
  "name": "Acme Mining",
  "legal_name": "PT Acme Mining Indonesia",
  "site_name": "Site Alpha",
  "site_legal_name": "PT Acme Site Alpha",
  "currency": "USD",
  "monthly": [
    {
      "month": "2024-02-01",
      "currency": "USD",
      "amount_usd": "85000.00",
      "amount_idr": "1487500000.00"
    }
  ],
  "total_usd": "1020000.00",
  "total_idr": "17850000000.00"
}
```

---

#### `GET /treasury/mrr_all_customers`

MRR breakdown for every customer that has sufficient contract and aggregate data. Customers missing required data are skipped.

**Response:** Array of MRR objects (same shape as `mrr_by_customer`).

**Example**

```bash
curl http://localhost:8000/treasury/mrr_all_customers
```

---

#### `GET /treasury/mrr_by_customer_entity`

MRR for all sites sharing the same customer `legal_name`.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legal_name` | `string` | Yes | Customer legal entity name |

**Response:** Array of MRR objects.

**Errors:** `404` if no customers match the legal name.

**Example**

```bash
curl "http://localhost:8000/treasury/mrr_by_customer_entity?legal_name=PT%20Acme%20Mining%20Indonesia"
```

---

#### `GET /treasury/mrr_by_site`

MRR for all customers at a given site.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `site_legal_name` | `string` | Yes | Site legal name |

**Response:** Array of MRR objects.

**Errors:** `404` if no customers match the site legal name.

**Example**

```bash
curl "http://localhost:8000/treasury/mrr_by_site?site_legal_name=PT%20Acme%20Site%20Alpha"
```

---

#### `GET /treasury/arr_by_customer`

ARR for a single customer. Same shape as `mrr_by_customer`, but monthly amounts and totals are multiplied by 12.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `customer_id` | `int` | Yes | Customer ID |

**Response:** ARR object (MRR shape with amounts × 12).

**Example**

```bash
curl "http://localhost:8000/treasury/arr_by_customer?customer_id=1"
```

---

#### `GET /treasury/arr_all_customers`

ARR for all customers. Array of ARR objects.

**Example**

```bash
curl http://localhost:8000/treasury/arr_all_customers
```

---

#### `GET /treasury/arr_by_customer_entity`

ARR for all sites under a customer legal entity.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legal_name` | `string` | Yes | Customer legal entity name |

**Response:** Array of ARR objects.

**Example**

```bash
curl "http://localhost:8000/treasury/arr_by_customer_entity?legal_name=PT%20Acme%20Mining%20Indonesia"
```

---

#### `GET /treasury/arr_by_site`

ARR for all customers at a given site.

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `site_legal_name` | `string` | Yes | Site legal name |

**Response:** Array of ARR objects.

**Example**

```bash
curl "http://localhost:8000/treasury/arr_by_site?site_legal_name=PT%20Acme%20Site%20Alpha"
```

---

### Invoices

Creating, updating, or deleting invoices also synchronizes linked **RECEIVABLES** (unpaid) and **REVENUES** (paid) ledger entries.

#### `GET /treasury/invoices`

List all invoices.

**Response:** Array of invoice objects.

**Example**

```bash
curl http://localhost:8000/treasury/invoices
```

```json
[
  {
    "id": 1,
    "contract_id": 1,
    "invoice_number": "24/01/06/0001",
    "invoicing_date": "2024-06-01",
    "due_date": "2024-06-15",
    "is_paid": false,
    "payment_date": null,
    "currency": "USD",
    "fx_rate": "17500.00",
    "pretax_usd": "85000.00",
    "vat_usd": "9350.00",
    "total_usd": "94350.00",
    "pretax_idr": "1487500000.00",
    "vat_idr": "163625000.00",
    "total_idr": "1651125000.00"
  }
]
```

---

#### `GET /treasury/invoices/{invoice_id}`

Get an invoice by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `invoice_id` | `int` | Invoice ID |

**Response:** Array with zero or one invoice object.

**Example**

```bash
curl http://localhost:8000/treasury/invoices/1
```

---

#### `POST /treasury/add_invoice`

Manually create an invoice. Also creates a receivable ledger entry.

**Request body** (`application/json`)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `contract_id` | `int` | No | — | Linked contract ID |
| `invoice_number` | `string` | No | — | Invoice reference |
| `invoicing_date` | `date` | No | — | Invoice issue date |
| `due_date` | `date` | No | — | Payment due date |
| `is_paid` | `bool` | No | `false` | Whether invoice is paid |
| `payment_date` | `date` | No | — | Date of payment |
| `currency` | `string` | No | — | `"USD"` or `"IDR"` |
| `fx_rate` | `decimal` | No | — | FX rate used |
| `pretax_usd` | `decimal` | No | — | Pretax amount in USD |
| `vat_usd` | `decimal` | No | — | VAT in USD (11%) |
| `total_usd` | `decimal` | No | — | Total in USD |
| `pretax_idr` | `decimal` | No | — | Pretax amount in IDR |
| `vat_idr` | `decimal` | No | — | VAT in IDR |
| `total_idr` | `decimal` | No | — | Total in IDR |

**Response:** Array containing the created invoice row(s).

**Example**

```bash
curl -X POST http://localhost:8000/treasury/add_invoice \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": 1,
    "invoice_number": "24/01/06/0001",
    "invoicing_date": "2024-06-01",
    "due_date": "2024-06-15",
    "is_paid": false,
    "currency": "USD",
    "fx_rate": 17500,
    "pretax_usd": 85000,
    "vat_usd": 9350,
    "total_usd": 94350,
    "pretax_idr": 1487500000,
    "vat_idr": 163625000,
    "total_idr": 1651125000
  }'
```

---

#### `POST /treasury/generate_invoice`

Auto-generate an invoice from a contract and the customer's latest aggregate on or before the invoicing date. Computes pretax from vehicle counts × contract prices, applies 11% VAT, and creates the invoice plus receivable entry.

**Query parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `contract_id` | `int` | Yes | — | Contract to invoice |
| `fx_rate` | `decimal` | No | — | FX rate for cross-currency conversion |
| `invoicing_date` | `date` | No | Today | Invoice issue date |

**Invoice number format:** `{YY}/{DD}/{MM}/{####}` (sequential per calendar year).

**Due date:** `invoicing_date + 14 days`.

**Response:** Array containing the created invoice row(s) (same shape as `add_invoice`).

**Errors:**
- `404` — Contract not found
- `404` — No aggregate found for the customer on or before the invoicing date

**Example**

```bash
curl -X POST "http://localhost:8000/treasury/generate_invoice?contract_id=1&fx_rate=17500&invoicing_date=2024-06-01"
```

---

#### `PATCH /treasury/update_invoice/{invoice_id}`

Update an invoice. Only fields present in the body are updated. Toggles between receivable and revenue ledgers when `is_paid` changes.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `invoice_id` | `int` | Invoice ID |

**Request body:** Same fields as `POST /treasury/add_invoice` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/treasury/update_invoice/1 \
  -H "Content-Type: application/json" \
  -d '{"due_date": "2024-06-30"}'
```

---

#### `PATCH /treasury/mark_invoice_paid/{invoice_id}`

Mark an invoice as paid. Sets `is_paid` to `true`, records the payment date, moves the ledger entry from receivables to revenues.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `invoice_id` | `int` | Invoice ID |

**Query parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `payment_date` | `date` | No | Today | Date payment was received |

**Response:** Array containing the updated invoice row(s).

**Example**

```bash
curl -X PATCH "http://localhost:8000/treasury/mark_invoice_paid/1?payment_date=2024-06-10"
```

```json
[
  {
    "id": 1,
    "contract_id": 1,
    "invoice_number": "24/01/06/0001",
    "invoicing_date": "2024-06-01",
    "due_date": "2024-06-15",
    "is_paid": true,
    "payment_date": "2024-06-10",
    "currency": "USD",
    "fx_rate": "17500.00",
    "pretax_usd": "85000.00",
    "vat_usd": "9350.00",
    "total_usd": "94350.00",
    "pretax_idr": "1487500000.00",
    "vat_idr": "163625000.00",
    "total_idr": "1651125000.00"
  }
]
```

---

#### `DELETE /treasury/delete_invoice/{invoice_id}`

Delete an invoice and its linked receivable or revenue entry.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `invoice_id` | `int` | Invoice ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/treasury/delete_invoice/1
```

---

#### `DELETE /treasury/delete_invoices`

Delete all invoices, receivables, and revenues.

**Response:** Array of deleted invoice row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/treasury/delete_invoices
```

---

### FX Rates

#### `GET /treasury/fxrates`

List all FX rates.

**Response:** Array of FX rate objects.

**Example**

```bash
curl http://localhost:8000/treasury/fxrates
```

```json
[
  {
    "id": 1,
    "fx_date": "2024-06-01",
    "rate": "17500.00"
  }
]
```

---

#### `GET /treasury/fxrates/{fxrate_id}`

Get an FX rate by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `fxrate_id` | `int` | FX rate ID |

**Response:** Array with zero or one FX rate object.

**Example**

```bash
curl http://localhost:8000/treasury/fxrates/1
```

---

#### `POST /treasury/add_fxrate`

Create an FX rate.

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fx_date` | `date` | No | Effective date |
| `rate` | `decimal` | No | USD/IDR rate (IDR per 1 USD) |

**Response:** Array containing the created row(s).

**Example**

```bash
curl -X POST http://localhost:8000/treasury/add_fxrate \
  -H "Content-Type: application/json" \
  -d '{"fx_date": "2024-06-01", "rate": 17500}'
```

---

#### `PATCH /treasury/update_fxrate/{fxrate_id}`

Update an FX rate. Only fields present in the body are updated.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `fxrate_id` | `int` | FX rate ID |

**Request body:** Same fields as `POST /treasury/add_fxrate` (all optional).

**Response:** Array containing the updated row(s).

**Example**

```bash
curl -X PATCH http://localhost:8000/treasury/update_fxrate/1 \
  -H "Content-Type: application/json" \
  -d '{"rate": 17600}'
```

---

#### `DELETE /treasury/delete_fxrate/{fxrate_id}`

Delete an FX rate by ID.

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `fxrate_id` | `int` | FX rate ID |

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/treasury/delete_fxrate/1
```

---

#### `DELETE /treasury/delete_fxrates`

Delete all FX rates.

**Response:** Array of deleted row(s).

**Example**

```bash
curl -X DELETE http://localhost:8000/treasury/delete_fxrates
```
