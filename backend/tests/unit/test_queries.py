from app.queries import build_filters


def test_no_filters_returns_only_active_jobs():
    where, params = build_filters(None, None, None)
    assert where == "active"
    assert params == {}


def test_filters_are_combined_with_and():
    where, params = build_filters("google", "Software", "Remote")
    assert where.count(" AND ") == 3
    assert params == {"search": "%google%", "category": "Software", "location": "%Remote%"}


def test_user_input_never_becomes_part_of_the_sql_text():
    attack = "'; DROP TABLE jobs; --"
    where, params = build_filters(attack, attack, attack)
    assert "DROP" not in where
    assert params["category"] == attack
