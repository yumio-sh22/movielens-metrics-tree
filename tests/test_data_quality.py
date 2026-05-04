def test_rating_range(db):
    invalid = db.execute("SELECT COUNT(*) FROM raw_ratings WHERE rating < 0.5 OR rating > 5.0").fetchone()[0]
    assert invalid == 0, f"Found {invalid} invalid ratings"

def test_no_null_ids(db):
    nulls = db.execute("SELECT COUNT(*) FROM raw_ratings WHERE userId IS NULL OR movieId IS NULL").fetchone()[0]
    assert nulls == 0

def test_no_duplicates(db):
    dups = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT userId, movieId, timestamp FROM raw_ratings 
            GROUP BY userId, movieId, timestamp HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    assert dups == 0, f"Found {dups} duplicates"
