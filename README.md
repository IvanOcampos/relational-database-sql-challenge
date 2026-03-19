# Relational Database SQL Challenge

A relational SQL database project focused on **data integrity, constraints, and structural queries**, built from raw CSV datasets.

---

## 🗂 Project Structure
```
relational-database-sql-challenge/
│
├─ transact-sql-challenge/
│ └─ data/
│ ├─ customers.csv
│ ├─ products.csv
│ ├─ orders.csv
│ ├─ order_items.csv
│ ├─ payments.csv
│ ├─ order_status_history.csv
│ └─ order_audit.csv
│
├─ database_setup.py # Main Python script: create tables + import CSV
├─ Commerce.db # Generated SQLite database
├─ import_log.log # Log of CSV import
├─ create_indexes.sql # SQL script to create indexes
├─ integrity_checks.sql # SQL validation queries
└─ structural_queries.sql # Sample queries for analysis
````
---

## ⚙ Technologies

- **Python 3.11** – Data import and logging
- **SQLite3** – Lightweight relational database
- **CSV** – Data input format
- **Logging** – Tracks errors during import

---

## 📝 Features

### 1. Database Schema

Tables with constraints and foreign keys:

- `Customers` – Client information
- `Products` – Product catalog
- `Orders` – Orders by customers
- `OrderItems` – Items in each order
- `Payments` – Payment details
- `OrderStatusHistory` – Status history per order
- `OrderAudit` – Audit trail of changes

Each table enforces:

- Type constraints (`CHECK`)
- Referential integrity (`FOREIGN KEY`)
- ISO datetime format (`YYYY-MM-DDTHH:MM:SS`)
- Soft delete (`DeletedAt` column)

### 2. CSV Import

- Reads CSV files from `transact-sql-challenge/data/`
- Inserts rows into the corresponding tables
- Converts empty strings to `NULL`
- Logs errors in `import_log.log`

### 3. Indexing

Indexes on critical columns improve query performance:

```sql
CREATE INDEX idx_orders_customer ON Orders(CustomerID);
CREATE INDEX idx_orderitems_order ON OrderItems(OrderID);
CREATE INDEX idx_orderitems_product ON OrderItems(ProductID);
CREATE INDEX idx_payments_order ON Payments(OrderID);
CREATE INDEX idx_orderstatushistory_order ON OrderStatusHistory(OrderID);
CREATE INDEX idx_orderaudit_order ON OrderAudit(OrderID);
```

### 4. Validation & Analysis Queries

- **Detect orders with non-existent customers**  
- **Detect products in `OrderItems` that do not exist**  
- **Find impossible order statuses**  
- **Retrieve paid orders with customer and product details**  

---

## 🚀 Usage

1. **Clone the repository:**

```bash
git clone https://github.com/IvanOcampos/relational-database-sql-challenge.git
```

2. **Run the database setup script:**

```bash
python database_setup.py
```

3. **Open `Commerce.db` with DB Browser for SQLite or any SQLite client to run queries.**

---

## 📌 Notes

- **Ensure foreign keys are enabled:**

```sql
PRAGMA foreign_keys = ON;
```

- **Import logs: Errors during CSV import are recorded in `import_log.log`**

- **Data files location: All CSV files are in `transact-sql-challenge/data/`**
