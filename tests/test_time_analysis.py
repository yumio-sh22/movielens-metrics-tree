def test_peak_hour_is_evening(db):
    peak_hour = db.execute("""
        SELECT hour FROM time_activity 
        GROUP BY hour ORDER BY COUNT(*) DESC LIMIT 1
    """).fetchone()[0]
    
    assert 17 <= peak_hour <= 23, f"Пик активности в {peak_hour}:00 (ожидался вечер 17-23)"

def test_quiet_hour_is_night(db):
    quiet_hour = db.execute("""
        SELECT hour FROM time_activity 
        GROUP BY hour ORDER BY COUNT(*) ASC LIMIT 1
    """).fetchone()[0]
    
    assert 0 <= quiet_hour <= 5, f"Минимум активности в {quiet_hour}:00 (ожидалась ночь 0-5)"