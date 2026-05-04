def test_cold_start_ratio(db):
    cold_users = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT userId FROM raw_ratings GROUP BY userId HAVING COUNT(*) < 5
        )
    """).fetchone()[0]
    
    total_users = db.execute("SELECT COUNT(DISTINCT userId) FROM raw_ratings").fetchone()[0]
    ratio = cold_users / total_users
    
    print(f"\nCold Start Ratio: {ratio:.2%}")
    assert 0.05 < ratio < 0.60, f"Доля холодных пользователей {ratio:.2%} вне ожидаемых рамок"

def test_data_sparsity(db):
    users = db.execute("SELECT COUNT(DISTINCT userId) FROM raw_ratings").fetchone()[0]
    items = db.execute("SELECT COUNT(DISTINCT movieId) FROM raw_ratings").fetchone()[0]
    interactions = db.execute("SELECT COUNT(*) FROM raw_ratings").fetchone()[0]
    
    sparsity = 1 - (interactions / (users * items))
    print(f"\nMatrix Sparsity: {sparsity:.4f} ({sparsity:.2%})")
    assert sparsity > 0.95, f"Матрица слишком плотная ({sparsity:.2%})"