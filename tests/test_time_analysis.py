def test_peak_hour_evening(db):
    peak = db.execute("SELECT hour FROM time_activity GROUP BY hour ORDER BY COUNT(*) DESC LIMIT 1").fetchone()[0]
    assert 17 <= peak <= 23, f"Peak hour is {peak}, expected evening (17-23)"

def test_quiet_hour_night(db):
    quiet = db.execute("SELECT hour FROM time_activity GROUP BY hour ORDER BY COUNT(*) ASC LIMIT 1").fetchone()[0]
    assert 0 <= quiet <= 5, f"Quiet hour is {quiet}, expected night (0-5)"
