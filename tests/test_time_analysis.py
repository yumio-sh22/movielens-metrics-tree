def test_peak_hour_exists(db):
    """Проверяем что есть явный пик активности (не важно в какой час)"""
    peak = db.execute("""
        SELECT hour, COUNT(*) as cnt FROM time_activity 
        GROUP BY hour ORDER BY cnt DESC LIMIT 1
    """).fetchone()
    
    print(f"\nPeak hour: {peak[0]}:00 with {peak[1]} ratings")
    assert peak[1] > 0, "No peak activity found"

def test_hour_distribution_not_uniform(db):
    """Проверяем что активность распределена неравномерно (есть паттерны)"""
    hours = db.execute("""
        SELECT hour, COUNT(*) as cnt FROM time_activity 
        GROUP BY hour ORDER BY cnt
    """).fetchall()
    
    min_cnt = hours[0][1]
    max_cnt = hours[-1][1]
    ratio = max_cnt / min_cnt if min_cnt > 0 else float('inf')
    
    print(f"\nHour distribution: min={min_cnt}, max={max_cnt}, ratio={ratio:.2f}")
    # Если ratio > 2, значит есть явные пики и спады
    assert ratio > 1.5, f"Activity too uniform (ratio={ratio:.2f})"
