import duckdb
import os

DB_PATH = "redhill_market_duckdb.db"

def build_robust_analytical_engine():
    print("--- Initializing Day 8 Production Analytical Engine (DuckDB) ---")
    
    # Establish local file connection handshake
    conn = duckdb.connect(DB_PATH)
    
    # Drop older draft tracking structures to refresh state definitions cleanly
    conn.execute("DROP TABLE IF EXISTS regional_market_data;")
    
    # Write a multi-variable strict schema mapping explicitly applying constraints
    conn.execute("""
        CREATE TABLE regional_market_data (
            transaction_id INTEGER PRIMARY KEY,
            location VARCHAR(100) NOT NULL,
            product_category VARCHAR(100) NOT NULL,
            rating DOUBLE CHECK (rating >= 0.0 AND rating <= 5.0),
            revenue DOUBLE CHECK (revenue >= 0.0)
        );
    """)
    print("[Success] Robust schema matrix built with strict relational constraints.")

    # Test Ingestion 1: Valid transactional record pipeline write
    try:
        conn.execute("""
            INSERT INTO regional_market_data (transaction_id, location, product_category, rating, revenue)
            VALUES (201, 'Chennai', 'Electronics', 4.2, 85000.00);
        """)
        print("[Injected] Record 201 written safely.")
    except Exception as e:
        print(f"[Failed] Record 201 blocked: {e}")

    # Test Ingestion 2: CONSTRAINT VIOLATION CHECK (Duplicate Primary Key)
    try:
        conn.execute("""
            INSERT INTO regional_market_data (transaction_id, location, product_category, rating, revenue)
            VALUES (201, 'Delhi', 'Apparel', 3.9, 1400.00);
        """)
    except Exception as e:
        print(f"[Constraint Blocked Successfully] Duplicate Key Protection caught: {e}")

    # Test Ingestion 3: CONSTRAINT VIOLATION CHECK (Out-of-bound Mathematical Rating)
    try:
        conn.execute("""
            INSERT INTO regional_market_data (transaction_id, location, product_category, rating, revenue)
            VALUES (202, 'Kolkata', 'Home Decor', 6.5, 5000.00);
        """)
    except Exception as e:
        print(f"[Constraint Blocked Successfully] Rating Upper Bound Domain Validation caught: {e}")

    # Verify and inspect committed row parameters
    print("\n--- Final Active Database State View ---")
    df_snapshot = conn.execute("SELECT * FROM regional_market_data;").fetchdf()
    print(df_snapshot)
    
    conn.close()

if __name__ == "__main__":
    build_robust_analytical_engine()
    