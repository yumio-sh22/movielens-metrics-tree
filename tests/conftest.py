import pytest
import duckdb
from pathlib import Path

@pytest.fixture(scope="session")
def db():
    con = duckdb.connect()
    DATA_DIR = Path(r'C:\Users\Мартинсон Диана\metric tree\data\raw\ml-25m')
    
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data not found: {DATA_DIR}")
        
    con.execute(f"CREATE TABLE raw_ratings AS SELECT * FROM read_csv_auto('{DATA_DIR}/ratings.csv')")
    con.execute(f"CREATE TABLE raw_movies AS SELECT * FROM read_csv_auto('{DATA_DIR}/movies.csv')")
    
    con.execute("""
        CREATE TABLE time_activity AS
        SELECT 
            userId,
            to_timestamp(timestamp) as event_time,
            DATE_PART('hour', to_timestamp(timestamp)) as hour
        FROM raw_ratings
    """)
    
    yield con
    con.close()
