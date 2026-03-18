import sqlite3
import csv

# Establish connection to the database
conn = sqlite3.connect('database.db')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create table if it doesn't exist (database schema definition)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    customer_id INTEGER PRIMARY KEY,                        -- Unique identifier for each customer
    full_name TEXT NOT NULL,                                -- Customer full name (required)
    email TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),  -- Email must be unique, not null and LIKE
    phone TEXT CHECK (phone LIKE '+%'),                     -- Optional phone number
    city TEXT NOT NULL,                                     -- Customer city (required)
    segment TEXT CHECK (segment IN ('retail','wholesale','online_only','vip')), -- Values two option
    created_at TEXT NOT NULL,                               -- Creation date (required)
    is_active INTEGER CHECK (is_active IN (0, 1)),          -- Boolean True o False
    deleted_at TEXT                                         -- Soft delete timestamp (nullable)
);                            
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


    
        