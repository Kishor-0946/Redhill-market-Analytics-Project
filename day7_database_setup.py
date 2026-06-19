import os
import sqlite3
import duckdb

# Define the physical paths for our database files
SQLITE_DB_PATH = "redhill_market_sqlite.db"
DUCKDB_DB_PATH = "redhill_market_duckdb.db"

def setup_sqlite_engine():
    print("\n--- Initializing SQLite3 Engine (Row-Oriented OLTP) ---")
    
    # Establish a connection handshake and create the file if it doesn't exist
    # Using 'with' acts as a context manager to handle sessions safely
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        # A cursor is like a pointer/workspace that lets us execute SQL commands
        cursor = conn.cursor()
        
        # Write DDL (Data Definition Language) to create a structured table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regional_market_data (
                transaction_id INTEGER PRIMARY KEY,
                location VARCHAR(100) NOT NULL,
                product_category VARCHAR(100),
                rating FLOAT,
                revenue REAL
            );
        """)
        print("[SQLite] Table 'regional_market_data' structurally verified.")
        
        # Insert a mock single-row transaction to test the database state
        cursor.execute("""
            INSERT OR IGNORE INTO regional_market_data (transaction_id, location, product_category, rating, revenue)
            VALUES (101, 'Bangalore', 'Electronics', 4.8, 25000.00);
        """)
        
        # Explicitly commit changes to save them permanently to the disk file
        conn.commit()
        print("[SQLite] Mock data transaction committed successfully.")

        # Read back verification check
        cursor.execute("SELECT * FROM regional_market_data;")
        row = cursor.fetchone()
        print(f"[SQLite] Read Verification Snapshot: {row}")


def setup_duckdb_engine():
    print("\n--- Initializing DuckDB Engine (Column-Oriented OLAP) ---")
    
    # Establish connection handshake to a persistent file database
    conn = duckdb.connect(DUCKDB_DB_PATH)
    
    # Create the structured schema table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS regional_market_data (
            transaction_id INTEGER PRIMARY KEY,
            location VARCHAR(100) NOT NULL,
            product_category VARCHAR(100),
            rating DOUBLE,
            revenue DOUBLE
        );
    """)
    print("[DuckDB] Table 'regional_market_data' structurally verified.")
    
    # Insert a mock transaction record
    # DuckDB's standard syntax handles internal checking, let's inject row 102
    # We use a try/except or conditional tracking because DuckDB handles PK constraints cleanly
    try:
        conn.execute("""
            INSERT INTO regional_market_data (transaction_id, location, product_category, rating, revenue)
            VALUES (102, 'Mumbai', 'Apparel', 4.5, 12500.50);
        """)
        print("[DuckDB] Mock data transaction injected successfully.")
    except Exception as e:
        # Handles duplicate run protection seamlessly if script runs twice
        print("[DuckDB] Row already exists or constraint handled.")

    # Read back verification check
    result = conn.execute("SELECT * FROM regional_market_data;").fetchone()
    print(f"[DuckDB] Read Verification Snapshot: {result}")
    
    # Close connection wrapper safely
    conn.close()
    print("[DuckDB] Engine connection securely closed.")


if __name__ == "__main__":
    # Run the setup routines for both database paradigms
    setup_sqlite_engine()
    setup_duckdb_engine()
    
    print("\n=======================================================")
    print("Verification Summary:")
    print(f"SQLite file generated: {os.path.exists(SQLITE_DB_PATH)} ({SQLITE_DB_PATH})")
    print(f"DuckDB file generated: {os.path.exists(DUCKDB_DB_PATH)} ({DUCKDB_DB_PATH})")
    print("=======================================================")