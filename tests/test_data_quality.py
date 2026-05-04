import pytest

def test_rating_range(db):
    invalid_count = db.execute("""
        SELECT COUNT(*) FROM raw_ratings 
        WHERE rating < 0.5 OR rating > 5.0
    """).fetchone()[0]
    assert invalid_count == 0, f"Найдено {invalid_count} оценок за пределами диапазона"

def test_no_null_ids(db):
    null_count = db.execute("""
        SELECT COUNT(*) FROM raw_ratings 
        WHERE userId IS NULL OR movieId IS NULL
    """).fetchone()[0]
    assert null_count == 0

def test_no_exact_duplicates(db):
    dup_count = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT userId, movieId, timestamp, COUNT(*) as cnt
            FROM raw_ratings 
            GROUP BY userId, movieId, timestamp 
            HAVING cnt > 1
        )
    """).fetchone()[0]
    assert dup_count == 0, f"Найдено {dup_count} дублирующихся записей"