import sqlite3
import csv
import logging

# Configure logger
logging.basicConfig(
    filename = 'import_log.log',    # File where logs will be saved
    level = logging.INFO,           # Minimum level to record
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------------------------------------
# Generic Funtion to Import CSV data into any table
# -------------------------------------------------
def import_csv_to_table(csv_path, table_name, cursor):
    """
    Read a CSV file and inserts its row into a specified table
    
    Parameters:
        csv_path (str): Path to the CSV file
        table_name (str): Name of the database table to insert data info
        cursor (sqlite3.cursor): Cursor object to excute SQL commands
    """
    
    # Log results
    success = 0
    errors = 0    
    with open(f"transact-sql-challenge/data/{csv_path}", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) # Skip header row
    
        # Prepare a parameterized SQL statement with as many placeholders as columns
        placeholders = ', '.join(['?'] * len(header))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        # Iterate over each row in the csv
        for row in reader:
            # Convert empty strings to None (NULL in SQLite)
            row = [None if value == '' else value for value in row]
            try:
                # Execute insert for the current row
                cursor.execute(sql, row)
                success +=1
                
            except Exception as e:
                errors += 1
                logging.error(f'Table: {table_name} | Row: {row} | Error: {e}')
    print(f"{table_name} → OK: {success}, FAIL: {errors}")
    logging.info(f"Finished {table_name} → Success: {success}, Errors: {errors}")
                
# Establish connection to the database
conn = sqlite3.connect('Commerce.db')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Enable foreign key contraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Create table if it doesn't exist
# --- CUSTOMERS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    CustomerID INTEGER PRIMARY KEY,                        -- Unique identifier for each customer
    FullName TEXT NOT NULL,                                -- Customer full name (required)
    Email TEXT NOT NULL UNIQUE CHECK (Email LIKE '%@%.%'),  -- Email must be unique, not null and LIKE
    Phone TEXT CHECK (Phone LIKE '+%'),                     -- Optional phone number
    City TEXT NOT NULL,                                     -- Customer city (required)
    Segment TEXT CHECK (Segment IN ('retail','wholesale','online_only','vip')), -- Values two option
    CreatedAt TEXT NOT NULL CHECK (CreatedAt LIKE '____-__-__T__:__:__'),          -- Creation date (required)
    IsActive INTEGER CHECK (IsActive IN (0, 1)),          -- Boolean True o False
    DeletedAt TEXT CHECK (DeletedAt IS NULL OR DeletedAt LIKE '____-__-__T__:__:__')    -- Soft delete timestamp (nullable)
);                            
""")

# --- PRODUCTS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
    ProductID INTEGER PRIMARY KEY,
    SKU TEXT NOT NULL UNIQUE CHECK (SKU LIKE 'SKU-%'),
    ProductName TEXT NOT NULL,
    Category TEXT CHECK (Category IN ('fashion','office','beauty','electronics','books','home','toys','automotive','sports','grocery')),
    Brand TEXT NOT NULL CHECK (Brand GLOB '[A-Z]*'),
    UnitPrice REAL NOT NULL CHECK (UnitPrice > 0),
    UnitCost REAL NOT NULL CHECK (UnitCost <= UnitPrice),
    CreatedAt TEXT NOT NULL CHECK (CreatedAt LIKE '____-__-__T__:__:__'),
    IsActive INTEGER NOT NULL CHECK (IsActive IN (0,1)),
    DeletedAt TEXT CHECK (DeletedAt IS NULL OR DeletedAt LIKE '____-__-__T__:__:__')
);                
""")

# --- ORDERS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders(
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    OrderDatetime TEXT NOT NULL CHECK (OrderDatetime LIKE '____-__-__T__:__:__'),
    Channel TEXT NOT NULL CHECK (Channel IN ('mobile','phone','store','web')),
    Currency TEXT NOT NULL CHECK (length(Currency) = 3),
    CurrentStatus TEXT NOT NULL CHECK (CurrentStatus IN ('created','paid','shipped','packed','delivered','cancelled','refunded')),
    IsActive INTEGER NOT NULL CHECK (IsActive IN (0,1)),
    DeletedAt TEXT CHECK (DeletedAt IS NULL OR DeletedAt LIKE '____-__-__T__:__:__'),
    OrderTotal REAL NOT NULL CHECK (OrderTotal >= 0),
    
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
""")

# --- ORDERS ITEMS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderItems(
    OrderItemID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice REAL NOT NULL CHECK (UnitPrice > 0),
    DiscountRate REAL NOT NULL CHECK (DiscountRate >= 0 AND DiscountRate <= 1),
    LineTotal REAL NOT NULL CHECK (LineTotal >= 0),
    -- UNIQUE (OrderID, ProductID),
    
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);               
""")

# --- PAYMENTS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments(
    PaymentID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    PaymentDatetime TEXT NOT NULL CHECK (PaymentDatetime LIKE '____-__-__T__:__:__'),
    Method TEXT NOT NULL CHECK (Method IN ('transfer','card','wallet','cash')),
    PaymentStatus TEXT NOT NULL CHECK (PaymentStatus IN ('rejected','approved','pending','refunded')),
    Amount REAL NOT NULL CHECK (Amount >= 0),
    Currency TEXT NOT NULL CHECK (length(Currency) = 3),
    
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderStatusHistory(
    StatusHistoryID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    Status TEXT NOT NULL CHECK (Status IN ('created','paid','packed','shipped','delivered','cancelled','refunded')),
    ChangedAt TEXT NOT NULL CHECK (ChangedAt LIKE '____-__-__T__:__:__'),
    ChangedBy TEXT NOT NULL CHECK (ChangedBy IN ('system','user','ops','warehouse','payment_gateway')),
    Reason TEXT,
    
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderAudit(
    AuditID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    FieldName TEXT NOT NULL,
    OldValue TEXT CHECK (OldValue LIKE '______'),
    NewValue TEXT CHECK (NewValue LIKE '______'),
    ChangedAt TEXT NOT NULL CHECK (ChangedAt LIKE '____-__-__T__:__:__'),
    ChangedBy TEXT NOT NULL CHECK (ChangedBy IN ('system','user','ops','support')),
    
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
""")

# List for each table
file_csv = ['customers.csv', 'products.csv', 'orders.csv','order_items.csv','payments.csv','order_status_history.csv','order_audit.csv']
table_sql = ['Customers', 'Products', 'Orders', 'OrderItems', 'Payments', 'OrderStatusHistory', 'OrderAudit']

# Call the funtion for each table
for i in range(len(file_csv)):
    import_csv_to_table(file_csv[i], table_sql[i], cursor)

# Save changes to the database
conn.commit()

# Close the database connection
conn.close()


    
        