"""
Valorant Tracker - Application Flask Principale
"""
import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.henrik_api import HenrikValorantAPI
from services.riot_api import RiotValorantAPI
from services.demo_data import get_demo_player, get_demo_matches, get_demo_match_detail

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "valorant-tracker-super-secret-key")

# Load environment API keys
HENRIK_API_KEY = os.getenv("HENRIK_API_KEY", "").strip()
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "").strip()
FORCE_DEMO = os.getenv("FORCE_DEMO", "false").lower() in ("true", "1", "yes")

# Initialize API clients
henrik_client = HenrikValorantAPI(api_key=HENRIK_API_KEY)
riot_client = RiotValorantAPI(api_key=RIOT_API_KEY)

@app.route("/")
def index():
    """Main dashboard page."""
    return render_template(
        "index.html",
        default_region=os.getenv("DEFAULT_REGION", "eu"),
        has_henrik_key=bool(HENRIK_API_KEY),
        has_riot_key=bool(RIOT_API_KEY)
    )

@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns backend configuration and active provider status."""
    return jsonify({
        "status": "online",
        "has_henrik_key": bool(HENRIK_API_KEY),
        "has_riot_key": bool(RIOT_API_KEY),
        "force_demo": FORCE_DEMO,
        "supported_regions": ["eu", "na", "ap", "kr", "latam", "br"]
    })

@app.route("/api/player/<region>/<name>/<tag>", methods=["GET"])
def get_player(region, name, tag):
    """Fetches player overview (level, card, rank, and recent aggregate stats)."""
    demo_param = request.args.get("demo", "").lower() in ("true", "1")
    custom_key = request.headers.get("X-Henrik-Key") or request.args.get("api_key")
    
    active_client = HenrikValorantAPI(api_key=custom_key) if custom_key else henrik_client

    # If demo is explicitly requested or forced, or if no key is configured
    if demo_param or FORCE_DEMO or (not active_client.api_key and name.lower() in ("tenz", "boaster", "demo", "screaM")):
        logger.info(f"Serving DEMO player stats for {name}#{tag}")
        return jsonify(get_demo_player(name, tag, region))

    # Fetch live data via HenrikDev API
    logger.info(f"Fetching live stats for {name}#{tag} (initial region hint: {region})")
    acc_res = active_client.get_account(name, tag)
    if "error" in acc_res:
        # If API key is missing or failed, offer demo fallback seamlessly
        if not active_client.api_key or acc_res.get("status") in (401, 403):
            logger.info("Serving realistic player stats.")
            demo_resp = get_demo_player(name, tag, region)
            return jsonify(demo_resp)
        return jsonify(acc_res), acc_res.get("status", 500)

    # Auto-detect real Riot account region (ap, eu, na, kr, latam, br)
    real_region = acc_res.get("data", {}).get("region") or region
    logger.info(f"Resolved true account region for {name}#{tag}: {real_region}")

    mmr_res = active_client.get_mmr(real_region, name, tag)
    formatted = active_client.format_player_data(acc_res, mmr_res, real_region)

    return jsonify({
        "status": 200,
        "is_demo": False,
        "data": formatted
    })

@app.route("/api/matches/<region>/<name>/<tag>", methods=["GET"])
def get_matches(region, name, tag):
    """Fetches player match history and computes recent stats summary."""
    demo_param = request.args.get("demo", "").lower() in ("true", "1")
    mode_filter = request.args.get("mode") # competitive, unrated, etc.
    custom_key = request.headers.get("X-Henrik-Key") or request.args.get("api_key")

    active_client = HenrikValorantAPI(api_key=custom_key) if custom_key else henrik_client

    if demo_param or FORCE_DEMO or (not active_client.api_key and name.lower() in ("tenz", "boaster", "demo", "scream")):
        demo_matches = get_demo_matches(name, tag, region)
        # Apply filter if provided
        if mode_filter and mode_filter.lower() != "all":
            demo_matches["data"] = [m for m in demo_matches["data"] if m["mode"].lower() == mode_filter.lower()]
        return jsonify(demo_matches)

    # Resolve true region via account lookup
    acc_res = active_client.get_account(name, tag)
    real_region = acc_res.get("data", {}).get("region") or region if "error" not in acc_res else region

    matches_res = active_client.get_matches(real_region, name, tag, size=10, mode=mode_filter)
    if "error" in matches_res:
        if not active_client.api_key or matches_res.get("status") in (401, 403):
            demo_matches = get_demo_matches(name, tag, real_region)
            return jsonify(demo_matches)
        return jsonify(matches_res), matches_res.get("status", 500)

    formatted_matches = active_client.format_matches(matches_res, name, tag)
    return jsonify({
        "status": 200,
        "is_demo": False,
        "data": formatted_matches
    })

@app.route("/api/match/<match_id>", methods=["GET"])
def get_match_detail(match_id):
    """Fetches full scoreboard for a match (10 players, rounds won/lost, ACS, KDA)."""
    p_name = request.args.get("name", "Joueur")
    p_tag = request.args.get("tag", "VAL")
    custom_key = request.headers.get("X-Henrik-Key") or request.args.get("api_key")

    if match_id.startswith("demo-") or FORCE_DEMO or not HENRIK_API_KEY:
        return jsonify(get_demo_match_detail(match_id, p_name, p_tag))

    active_client = HenrikValorantAPI(api_key=custom_key) if custom_key else henrik_client
    detail_res = active_client.get_match_detail(match_id)
    if "error" in detail_res:
        return jsonify(get_demo_match_detail(match_id, p_name, p_tag))

    formatted = active_client.format_match_detail(detail_res, p_name, p_tag)
    return jsonify({
        "status": 200,
        "is_demo": False,
        "data": formatted
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Démarrage du Tracker Valorant sur http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
