"""
Mock & Demo data for Valorant Tracker.
Provides realistic sample profiles, stats, and match histories when API keys are not provided
or when demo mode is enabled.
"""
import random
import time

RANKS = [
    {"tier": 27, "name": "Radiant", "color": "#FFFFA5", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/27/largeicon.png"},
    {"tier": 26, "name": "Immortal 3", "color": "#BE1A58", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/26/largeicon.png"},
    {"tier": 25, "name": "Immortal 2", "color": "#BE1A58", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/25/largeicon.png"},
    {"tier": 24, "name": "Immortal 1", "color": "#BE1A58", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/24/largeicon.png"},
    {"tier": 23, "name": "Ascendant 3", "color": "#339B78", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/23/largeicon.png"},
    {"tier": 22, "name": "Ascendant 2", "color": "#339B78", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/22/largeicon.png"},
    {"tier": 20, "name": "Diamond 3", "color": "#765CEB", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/20/largeicon.png"},
    {"tier": 17, "name": "Platinum 3", "color": "#4EBAC4", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/17/largeicon.png"},
    {"tier": 14, "name": "Gold 3", "color": "#E5B942", "icon": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/14/largeicon.png"},
]

MAPS = [
    {
        "name": "Ascent",
        "splash": "https://media.valorant-api.com/maps/7eae254d-459c-6c7c-f3b1-1294027ab989/splash.png",
        "icon": "https://media.valorant-api.com/maps/7eae254d-459c-6c7c-f3b1-1294027ab989/displayicon.png"
    },
    {
        "name": "Bind",
        "splash": "https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/splash.png",
        "icon": "https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/displayicon.png"
    },
    {
        "name": "Haven",
        "splash": "https://media.valorant-api.com/maps/2bee0dc9-40a8-7df8-3786-409e6f939e69/splash.png",
        "icon": "https://media.valorant-api.com/maps/2bee0dc9-40a8-7df8-3786-409e6f939e69/displayicon.png"
    },
    {
        "name": "Lotus",
        "splash": "https://media.valorant-api.com/maps/2fe4ed3a-450a-948b-6d6b-e89a5bb8ffba/splash.png",
        "icon": "https://media.valorant-api.com/maps/2fe4ed3a-450a-948b-6d6b-e89a5bb8ffba/displayicon.png"
    },
    {
        "name": "Sunset",
        "splash": "https://media.valorant-api.com/maps/92584fbe-486a-b1b2-9faa-39b0f486b498/splash.png",
        "icon": "https://media.valorant-api.com/maps/92584fbe-486a-b1b2-9faa-39b0f486b498/displayicon.png"
    },
    {
        "name": "Split",
        "splash": "https://media.valorant-api.com/maps/d960549e-485c-68e3-6170-71a2e8e04041/splash.png",
        "icon": "https://media.valorant-api.com/maps/d960549e-485c-68e3-6170-71a2e8e04041/displayicon.png"
    },
    {
        "name": "Abyss",
        "splash": "https://media.valorant-api.com/maps/224b0a95-48b9-f703-1bd8-67aca101a61f/splash.png",
        "icon": "https://media.valorant-api.com/maps/224b0a95-48b9-f703-1bd8-67aca101a61f/displayicon.png"
    }
]

AGENTS = [
    {
        "name": "Jett",
        "role": "Duelist",
        "icon": "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6c6-319589ce4e0e/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6c6-319589ce4e0e/bustportrait.png"
    },
    {
        "name": "Reyna",
        "role": "Duelist",
        "icon": "https://media.valorant-api.com/agents/a3bfb85b-4241-247b-60da-05ac5ff4b61f/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/a3bfb85b-4241-247b-60da-05ac5ff4b61f/bustportrait.png"
    },
    {
        "name": "Omen",
        "role": "Controller",
        "icon": "https://media.valorant-api.com/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/8e253930-4c05-31dd-1b6c-968525494517/bustportrait.png"
    },
    {
        "name": "Sova",
        "role": "Initiator",
        "icon": "https://media.valorant-api.com/agents/320746e4-45c4-Marker-0d81-80bb6e288e28/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/ded3520f-4264-bfed-162d-b080e2abccf9/bustportrait.png"
    },
    {
        "name": "Clove",
        "role": "Controller",
        "icon": "https://media.valorant-api.com/agents/1dbf2edd-4729-0984-3115-ffbced4463b1/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/1dbf2edd-4729-0984-3115-ffbced4463b1/bustportrait.png"
    },
    {
        "name": "Cypher",
        "role": "Sentinel",
        "icon": "https://media.valorant-api.com/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/bustportrait.png"
    },
    {
        "name": "Iso",
        "role": "Duelist",
        "icon": "https://media.valorant-api.com/agents/0e38b510-41a8-5780-5e8f-568b2a4f2d6c/displayicon.png",
        "bust": "https://media.valorant-api.com/agents/0e38b510-41a8-5780-5e8f-568b2a4f2d6c/bustportrait.png"
    }
]

BOT_PLAYERS = [
    {"name": "Chronos", "tag": "FR1"},
    {"name": "Shadow", "tag": "VAL"},
    {"name": "Valkyrie", "tag": "EUW"},
    {"name": "Aethelgard", "tag": "PRO"},
    {"name": "ViperMain", "tag": "TOX"},
    {"name": "NoAimJustLuck", "tag": "LUCK"},
    {"name": "HeadshotOnly", "tag": "TAP"},
    {"name": "Zenith", "tag": "777"},
    {"name": "PhantomKing", "tag": "ONE"}
]

PLAYER_CARDS = [
    "https://media.valorant-api.com/playercards/9fb348bc-41a0-91ad-8a3e-818035c4e561/largeart.png",
    "https://media.valorant-api.com/playercards/3f82084c-4235-9f5b-6f8c-c89b7bbfdb73/largeart.png",
    "https://media.valorant-api.com/playercards/13755b00-47b2-03d3-7d52-6ab5cc1c062c/largeart.png"
]

def get_demo_player(name="TenZ", tag="SEN", region="na"):
    """Generates a realistic player profile for demo mode."""
    # Seed by name to get consistent demo stats for the same player
    seed_val = sum(ord(c) for c in (name + tag))
    rng = random.Random(seed_val)
    
    rank_idx = rng.choice([0, 1, 2, 3, 4, 5])  # High tier for demo
    rank = RANKS[rank_idx]
    peak_rank = RANKS[max(0, rank_idx - 1)]
    
    account_level = rng.randint(110, 480)
    card = rng.choice(PLAYER_CARDS)
    
    # Calculate lifetime stats
    total_matches = rng.randint(45, 120)
    winrate = round(rng.uniform(52.0, 68.5), 1)
    kd_ratio = round(rng.uniform(1.15, 1.62), 2)
    headshot_pct = round(rng.uniform(24.0, 36.5), 1)
    avg_damage = rng.randint(145, 185)
    avg_combat_score = rng.randint(220, 290)
    
    return {
        "status": 200,
        "is_demo": True,
        "data": {
            "name": name,
            "tag": tag,
            "region": region.upper(),
            "account_level": account_level,
            "card": card,
            "current_rank": {
                "tier": rank["tier"],
                "name": rank["name"],
                "color": rank["color"],
                "icon": rank["icon"],
                "rr": rng.randint(25, 95),
                "last_change": f"+{rng.randint(14, 28)}"
            },
            "peak_rank": {
                "tier": peak_rank["tier"],
                "name": peak_rank["name"],
                "icon": peak_rank["icon"],
                "season": "E8:A3"
            },
            "stats": {
                "matches": total_matches,
                "winrate": winrate,
                "kd": kd_ratio,
                "headshot_pct": headshot_pct,
                "avg_combat_score": avg_combat_score,
                "avg_damage": avg_damage
            }
        }
    }


def get_demo_matches(name="TenZ", tag="SEN", region="na", count=8):
    """Generates a list of realistic match histories for demo mode."""
    seed_val = sum(ord(c) for c in (name + tag))
    rng = random.Random(seed_val)
    
    matches = []
    base_time = int(time.time())
    
    for i in range(count):
        match_id = f"demo-match-{seed_val}-{i}"
        game_map = rng.choice(MAPS)
        agent = rng.choice(AGENTS)
        mode = "Competitive" if rng.random() > 0.25 else "Unrated"
        
        is_win = rng.random() > 0.40
        rounds_won = 13 if is_win else rng.randint(7, 11)
        rounds_lost = rng.randint(4, 11) if is_win else 13
        
        kills = rng.randint(16, 31)
        deaths = rng.randint(10, 19)
        assists = rng.randint(3, 11)
        
        kd = round(kills / max(1, deaths), 2)
        score = rng.randint(4000, 7500)
        acs = score // (rounds_won + rounds_lost)
        hs_pct = round(rng.uniform(22.0, 42.0), 1)
        damage_round = rng.randint(130, 210)
        
        # Time ago: spaced out over the last few days
        time_ago_sec = (i * 10800) + rng.randint(1800, 7200)
        match_timestamp = base_time - time_ago_sec
        
        matches.append({
            "match_id": match_id,
            "mode": mode,
            "map": {
                "name": game_map["name"],
                "splash": game_map["splash"],
                "icon": game_map["icon"]
            },
            "agent": {
                "name": agent["name"],
                "role": agent["role"],
                "icon": agent["icon"],
                "bust": agent["bust"]
            },
            "result": "Victory" if is_win else "Defeat",
            "score_display": f"{rounds_won} - {rounds_lost}",
            "rounds_won": rounds_won,
            "rounds_lost": rounds_lost,
            "stats": {
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "kd": kd,
                "acs": acs,
                "headshot_pct": hs_pct,
                "damage_per_round": damage_round
            },
            "timestamp": match_timestamp,
            "duration_minutes": rng.randint(28, 44)
        })
        
    return {
        "status": 200,
        "is_demo": True,
        "data": matches
    }


def get_demo_match_detail(match_id, player_name="TenZ", player_tag="SEN"):
    """Generates detailed scoreboard for a match with 10 players (5 Blue vs 5 Red)."""
    rng = random.Random(sum(ord(c) for c in match_id))
    game_map = rng.choice(MAPS)
    
    rounds_blue = 13 if rng.random() > 0.45 else rng.randint(8, 11)
    rounds_red = rng.randint(7, 11) if rounds_blue == 13 else 13
    
    # Team Blue (includes user)
    team_blue = []
    user_agent = rng.choice(AGENTS)
    user_rank = RANKS[rng.randint(0, 4)]
    
    user_kills = rng.randint(18, 30)
    user_deaths = rng.randint(11, 18)
    user_assists = rng.randint(4, 10)
    
    team_blue.append({
        "name": player_name,
        "tag": player_tag,
        "is_current_player": True,
        "agent": user_agent,
        "rank": user_rank,
        "kills": user_kills,
        "deaths": user_deaths,
        "assists": user_assists,
        "kd": round(user_kills / max(1, user_deaths), 2),
        "score": rng.randint(5200, 7100),
        "acs": rng.randint(220, 310),
        "headshot_pct": round(rng.uniform(22, 38), 1),
        "ping": rng.randint(14, 32)
    })
    
    # Fill remaining 4 Blue teammates
    remaining_agents_blue = [a for a in AGENTS if a["name"] != user_agent["name"]]
    rng.shuffle(remaining_agents_blue)
    
    for i in range(4):
        bot = BOT_PLAYERS[i]
        ag = remaining_agents_blue[i]
        rk = RANKS[rng.randint(0, 5)]
        k = rng.randint(9, 22)
        d = rng.randint(10, 19)
        a = rng.randint(3, 14)
        team_blue.append({
            "name": bot["name"],
            "tag": bot["tag"],
            "is_current_player": False,
            "agent": ag,
            "rank": rk,
            "kills": k,
            "deaths": d,
            "assists": a,
            "kd": round(k / max(1, d), 2),
            "score": rng.randint(3200, 5800),
            "acs": rng.randint(150, 240),
            "headshot_pct": round(rng.uniform(18, 32), 1),
            "ping": rng.randint(18, 48)
        })
    
    # Sort team blue by ACS
    team_blue.sort(key=lambda p: p["acs"], reverse=True)
    
    # Team Red (opponents)
    team_red = []
    shuffled_agents_red = list(AGENTS)
    rng.shuffle(shuffled_agents_red)
    
    for i in range(5):
        bot = BOT_PLAYERS[min(i + 4, len(BOT_PLAYERS) - 1)]
        ag = shuffled_agents_red[i]
        rk = RANKS[rng.randint(0, 5)]
        k = rng.randint(10, 26)
        d = rng.randint(11, 21)
        a = rng.randint(2, 11)
        team_red.append({
            "name": f"{bot['name']}_Opp",
            "tag": bot["tag"],
            "is_current_player": False,
            "agent": ag,
            "rank": rk,
            "kills": k,
            "deaths": d,
            "assists": a,
            "kd": round(k / max(1, d), 2),
            "score": rng.randint(3400, 6200),
            "acs": rng.randint(160, 265),
            "headshot_pct": round(rng.uniform(19, 35), 1),
            "ping": rng.randint(15, 45)
        })
    
    # Sort team red by ACS
    team_red.sort(key=lambda p: p["acs"], reverse=True)
    
    return {
        "status": 200,
        "is_demo": True,
        "data": {
            "match_id": match_id,
            "map": game_map,
            "mode": "Competitive",
            "score": {
                "blue": rounds_blue,
                "red": rounds_red
            },
            "team_blue": team_blue,
            "team_red": team_red
        }
    }
