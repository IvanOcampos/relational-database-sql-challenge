import sqlite3
import csv

# Establish connection to the database
conn = sqlite3.connect('Tra.db')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Activar llaves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# Create table if it doesn't exist (database schema definition)
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
    FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID),
    OrderDatatime TEXT NOT NULL CHECK (OrderDatatime LIKE '____-__-__T__:__:__'),
    Channel TEXT NOT NULL CHECK (Channel IN ('mobile','phone','store','web')),
    Currency TEXT NOT NULL CHECK (length(Currency) = 3),
    CurrentStatus TEXT NOT NULL CHECK (CurrentStatus IN ('created','paid','shipped','packed','delivered','cancelled')),
    IsActive INTEGER NOT NULL CHECK (IsActive IN (0,1)),
    DeletedAt TEXT CHECK (DeletedAt IS NULL OR DeletedAt LIKE '____-__-__T__:__:__'),
    OrderTotal REAL NOT NULL CHECK (OrderTotal >= 0)
);
""")

# --- ORDERS ITEMS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderItems(
    OrderItemID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    Quantity INTEGER NOT NULL CHECK (Quantity > 0),
    UnitPrice REAL NOT NULL CHECK (UnitPrice > 0),
    DiscountRate REAL NOT NULL CHECK (DiscountRate >= 0 AND DiscountRate <= 1),
    LineTotal REAL NOT NULL CHECK (LineTotal >= 0)
    UNIQUE (OrderID, ProductID)
)               
""")

# --- PAYMENTS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments(
    PaymentID INTEGER PRIMARY KEY,
    OrderID INTEGER NOT NULL,
    
)               
""")

#Open CSV file for reading
with open("transact-sql-challenge/data/customers.csv", newline="", encoding="utf-8") as csv_customers:
    reader = csv.reader(csv_customers)
    
    next(reader) # Skip header row
    
    # Iterate over each row in the CSV
    for row in reader:
        try:
            # Insert row into the database using parameterized query
            cursor.execute("""
                INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)               
            """, row)
        
        except Exception as e:
            # Print error if insertion fails (integrity constrains, etc.)
            print(f"Error in row: {row}")
            print(f"Motivo {e}")

# Save changes to the database
conn.commit()

# Close the database connection
conn.close()


    
        