"""
Verification test script for Valorant Tracker
"""
from app import app
import json

def test_all():
    client = app.test_client()

    print("--- 1. Testing GET / (Homepage) ---")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "VALOTRACKER" in res.get_data(as_text=True)
    print("[OK] Homepage loads successfully with HTML content.")

    print("\n--- 2. Testing GET /api/status ---")
    res = client.get("/api/status")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"
    print(f"[OK] Status endpoint: {data}")

    print("\n--- 3. Testing GET /api/player/eu/TenZ/SEN (Demo/Mock) ---")
    res = client.get("/api/player/eu/TenZ/SEN?demo=true")
    assert res.status_code == 200
    pdata = res.get_json()
    assert pdata["status"] == 200
    player = pdata["data"]
    assert player["name"] == "TenZ"
    assert "current_rank" in player
    print(f"[OK] Player: {player['name']}#{player['tag']} | Rank: {player['current_rank']['name']} ({player['current_rank']['rr']} RR)")

    print("\n--- 4. Testing GET /api/matches/eu/TenZ/SEN (Demo/Mock) ---")
    res = client.get("/api/matches/eu/TenZ/SEN?demo=true")
    assert res.status_code == 200
    mdata = res.get_json()
    matches = mdata["data"]
    assert len(matches) > 0
    first_match = matches[0]
    print(f"[OK] Matches count: {len(matches)} | First match: {first_match['map']['name']} ({first_match['result']} {first_match['score_display']}) with Agent {first_match['agent']['name']}")

    print("\n--- 5. Testing GET /api/match/<match_id> (Scoreboard details) ---")
    res = client.get(f"/api/match/{first_match['match_id']}?name=TenZ&tag=SEN")
    assert res.status_code == 200
    sdata = res.get_json()
    assert len(sdata["data"]["team_blue"]) == 5
    assert len(sdata["data"]["team_red"]) == 5
    print(f"[OK] Match detail 10 players scoreboard: Team Blue ({len(sdata['data']['team_blue'])}) vs Team Red ({len(sdata['data']['team_red'])})")

    print("\n === ALL TESTS PASSED SUCCESSFULLY! === ")

if __name__ == "__main__":
    test_all()
