def test_cold_start_users(db):
    cold = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT userId FROM raw_ratings GROUP BY userId HAVING COUNT(*) < 5
        )
    """).fetchone()[0]
    total = db.execute("SELECT COUNT(DISTINCT userId) FROM raw_ratings").fetchone()[0]
    ratio = cold / total
    print(f"\nCold Start Ratio: {ratio:.2%} ({cold}/{total})")
    # В MovieLens 25M может быть мало холодных пользователей
    # Просто проверяем что ratio < 50%
    assert ratio < 0.50, f"Too many cold start users: {ratio:.2%}"
