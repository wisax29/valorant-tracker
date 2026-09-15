"""
HenrikDev Valorant API Client (api.henrikdev.xyz)
The standard community API for Valorant match histories, player cards, and ranks.
"""
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.henrikdev.xyz"

MAP_SPLASHES = {
    "ascent": "https://media.valorant-api.com/maps/7eae254d-459c-6c7c-f3b1-1294027ab989/splash.png",
    "bind": "https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/splash.png",
    "haven": "https://media.valorant-api.com/maps/2bee0dc9-40a8-7df8-3786-409e6f939e69/splash.png",
    "lotus": "https://media.valorant-api.com/maps/2fe4ed3a-450a-948b-6d6b-e89a5bb8ffba/splash.png",
    "sunset": "https://media.valorant-api.com/maps/92584fbe-486a-b1b2-9faa-39b0f486b498/splash.png",
    "split": "https://media.valorant-api.com/maps/d960549e-485c-68e3-6170-71a2e8e04041/splash.png",
    "abyss": "https://media.valorant-api.com/maps/224b0a95-48b9-f703-1bd8-67aca101a61f/splash.png",
    "breeze": "https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/splash.png",
    "icebox": "https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/splash.png",
    "fracture": "https://media.valorant-api.com/maps/b52973d7-44fa-493b-34a3-a8c402123088/splash.png",
    "pearl": "https://media.valorant-api.com/maps/fd267035-4914-14b2-27cc-93888caa4504/splash.png"
}

class HenrikValorantAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or ""
        self.headers = {
            "User-Agent": "ValorantTrackerFlask/1.0"
        }
        if self.api_key:
            self.headers["Authorization"] = self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key
        if api_key:
            self.headers["Authorization"] = api_key
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]

    def _get(self, endpoint, params=None):
        url = f"{BASE_URL}{endpoint}"
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=8)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                try:
                    data = resp.json()
                    errors = data.get("errors", [])
                    if errors and errors[0].get("code") == 24:
                        return {
                            "status": 404,
                            "error_code": 24,
                            "error": "Compte non synchronisé : aucune partie récente n'a encore été indexée par l'API pour ce joueur. Lancez simplement une petite partie sur Valorant (un Deathmatch ou Swiftplay rapide suffit) pour activer la synchronisation de vos stats !"
                        }
                    elif errors and errors[0].get("message"):
                        return {"status": 404, "error": errors[0]["message"]}
                except Exception:
                    pass
                return {"status": 404, "error": "Joueur introuvable ou profil privé."}
            elif resp.status_code == 429:
                return {"status": 429, "error": "Trop de requêtes envoyées à l'API (Rate Limit atteint). Réessayez dans un instant."}
            elif resp.status_code == 401 or resp.status_code == 403:
                return {"status": resp.status_code, "error": "Clé API invalide ou non autorisée."}
            else:
                return {"status": resp.status_code, "error": f"Erreur API ({resp.status_code}): {resp.text}"}
        except requests.exceptions.Timeout:
            return {"status": 408, "error": "Le serveur de l'API met trop de temps à répondre (Timeout)."}
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur requête HenrikDev: {e}")
            return {"status": 500, "error": f"Erreur de connexion à l'API: {str(e)}"}

    def get_account(self, name, tag):
        """Fetches account info: puuid, account level, player card."""
        return self._get(f"/valorant/v1/account/{name}/{tag}")

    def get_mmr(self, region, name, tag):
        """Fetches current rank, RR, and highest peak rank."""
        return self._get(f"/valorant/v2/mmr/{region}/{name}/{tag}")

    def get_matches(self, region, name, tag, size=10, mode=None):
        """Fetches recent match history."""
        params = {"size": size}
        if mode:
            params["filter"] = mode
        return self._get(f"/valorant/v3/matches/{region}/{name}/{tag}", params=params)

    def get_match_detail(self, match_id):
        """Fetches full scoreboard for a single match."""
        return self._get(f"/valorant/v2/match/{match_id}")

    def format_player_data(self, account_resp, mmr_resp, region):
        """Combines account & MMR into a clean, uniform profile structure."""
        acc_data = account_resp.get("data", {}) if isinstance(account_resp, dict) else {}
        mmr_data = mmr_resp.get("data", {}) if isinstance(mmr_resp, dict) else {}
        
        current_data = mmr_data.get("current_data", {})
        highest_data = mmr_data.get("highest_rank", {})
        
        card_obj = acc_data.get("card", {})
        card_image = card_obj.get("large") or card_obj.get("wide") or card_obj.get("small") or "https://media.valorant-api.com/playercards/9fb348bc-41a0-91ad-8a3e-818035c4e561/largeart.png"

        current_rank_name = current_data.get("currenttierpatched", "Unranked")
        current_tier = current_data.get("currenttier", 0)
        current_rr = current_data.get("ranking_in_tier", 0)
        rank_images = current_data.get("images", {})
        rank_icon = rank_images.get("large") or rank_images.get("small") or "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/0/largeicon.png"

        peak_rank_name = highest_data.get("patched_tier", "Unranked")
        peak_season = highest_data.get("season", "N/A")

        return {
            "name": acc_data.get("name", ""),
            "tag": acc_data.get("tag", ""),
            "puuid": acc_data.get("puuid", ""),
            "region": region.upper(),
            "account_level": acc_data.get("account_level", 1),
            "card": card_image,
            "current_rank": {
                "tier": current_tier,
                "name": current_rank_name,
                "icon": rank_icon,
                "rr": current_rr,
                "last_change": f"{current_data.get('mmr_change_to_last_game', 0):+d}" if current_data.get('mmr_change_to_last_game') is not None else "+0"
            },
            "peak_rank": {
                "name": peak_rank_name,
                "season": peak_season
            }
        }

    def format_matches(self, matches_resp, current_name, current_tag):
        """Converts raw HenrikDev match list into standardized format."""
        raw_matches = matches_resp.get("data") or []
        if not isinstance(raw_matches, list):
            return []

        formatted = []
        c_name = current_name.lower().strip()
        c_tag = current_tag.lower().strip()
        
        for m in raw_matches:
            if not isinstance(m, dict) or m.get("is_available") is False:
                continue

            metadata = m.get("metadata") or {}
            players_obj = m.get("players") or {}
            players = players_obj.get("all_players") or []
            teams = m.get("teams") or {}

            if not players:
                continue
            
            # Find current player in match
            user_player = None
            for p in players:
                if not isinstance(p, dict):
                    continue
                p_name = (p.get("name") or "").lower().strip()
                p_tag = (p.get("tag") or "").lower().strip()
                if p_name == c_name and p_tag == c_tag:
                    user_player = p
                    break
            
            if not user_player:
                continue

            user_team_color = (user_player.get("team") or "Blue").lower()
            team_info = teams.get(user_team_color) or {}
            opp_team_color = "red" if user_team_color == "blue" else "blue"
            opp_info = teams.get(opp_team_color) or {}

            rounds_won = team_info.get("rounds_won", 0)
            rounds_lost = team_info.get("rounds_lost", 0)
            has_won = team_info.get("has_won", False)
            is_draw = rounds_won == rounds_lost and rounds_won > 0

            if not team_info and not opp_info:
                result = "Terminé"
                score_display = f"{(user_player.get('stats') or {}).get('kills', 0)} Kills"
            else:
                result = "Draw" if is_draw else ("Victory" if has_won else "Defeat")
                score_display = f"{rounds_won} - {rounds_lost}"
            
            # Stats calculation
            stats = user_player.get("stats") or {}
            kills = stats.get("kills", 0)
            deaths = stats.get("deaths", 0)
            assists = stats.get("assists", 0)
            score = stats.get("score", 0)
            damage = stats.get("damage_dealt", 0)
            
            rounds_played = max(1, metadata.get("rounds_played") or (rounds_won + rounds_lost) or 1)
            acs = score // rounds_played
            damage_per_round = damage // rounds_played

            shots = {
                "head": stats.get("headshots", 0),
                "body": stats.get("bodyshots", 0),
                "leg": stats.get("legshots", 0)
            }
            total_shots = sum(shots.values())
            hs_pct = round((shots["head"] / total_shots * 100), 1) if total_shots > 0 else 0.0

            agent_assets = (user_player.get("assets") or {}).get("agent") or {}
            agent_icon = agent_assets.get("small") or "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6c6-319589ce4e0e/displayicon.png"
            agent_bust = agent_assets.get("bust") or agent_assets.get("full") or agent_icon

            map_name = metadata.get("map") or "Inconnu"

            formatted.append({
                "match_id": metadata.get("matchid", ""),
                "mode": metadata.get("mode", "Competitive"),
                "map": {
                    "name": map_name,
                    "splash": MAP_SPLASHES.get(map_name.lower(), "https://media.valorant-api.com/maps/7eae254d-459c-6c7c-f3b1-1294027ab989/splash.png")
                },
                "agent": {
                    "name": user_player.get("character", "Agent"),
                    "icon": agent_icon,
                    "bust": agent_bust
                },
                "result": result,
                "score_display": score_display,
                "rounds_won": rounds_won,
                "rounds_lost": rounds_lost,
                "stats": {
                    "kills": kills,
                    "deaths": deaths,
                    "assists": assists,
                    "kd": round(kills / max(1, deaths), 2),
                    "acs": acs,
                    "headshot_pct": hs_pct,
                    "damage_per_round": damage_per_round
                },
                "timestamp": metadata.get("game_start", 0),
                "duration_minutes": max(1, (metadata.get("game_length") or 1800) // 60)
            })

        return formatted

    def format_match_detail(self, match_resp, current_name="", current_tag=""):
        """Formats the single match detail for the 10-player modal scoreboard."""
        match_data = match_resp.get("data") or {}
        metadata = match_data.get("metadata") or {}
        players_obj = match_data.get("players") or {}
        all_players = players_obj.get("all_players") or []
        teams = match_data.get("teams") or {}

        c_name = current_name.lower().strip()
        c_tag = current_tag.lower().strip()

        blue_players = []
        red_players = []

        rounds_played = max(1, metadata.get("rounds_played", 1))

        for p in all_players:
            stats = p.get("stats", {})
            shots = {
                "head": stats.get("headshots", 0),
                "body": stats.get("bodyshots", 0),
                "leg": stats.get("legshots", 0)
            }
            tot_shots = sum(shots.values())
            hs_pct = round((shots["head"] / tot_shots * 100), 1) if tot_shots > 0 else 0.0

            agent_assets = p.get("assets", {}).get("agent", {})
            k = stats.get("kills", 0)
            d = stats.get("deaths", 0)
            a = stats.get("assists", 0)
            score = stats.get("score", 0)

            player_obj = {
                "name": p.get("name", "Joueur"),
                "tag": p.get("tag", "VAL"),
                "is_current_player": (p.get("name", "").lower() == c_name and p.get("tag", "").lower() == c_tag),
                "agent": {
                    "name": p.get("character", "Agent"),
                    "icon": agent_assets.get("small") or "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6c6-319589ce4e0e/displayicon.png"
                },
                "rank": {
                    "name": p.get("currenttier_patched", "Unranked"),
                    "tier": p.get("currenttier", 0)
                },
                "kills": k,
                "deaths": d,
                "assists": a,
                "kd": round(k / max(1, d), 2),
                "score": score,
                "acs": score // rounds_played,
                "headshot_pct": hs_pct,
                "ping": p.get("ping", 25)
            }

            if (p.get("team") or "").lower() == "blue":
                blue_players.append(player_obj)
            else:
                red_players.append(player_obj)

        # Sort by ACS descending
        blue_players.sort(key=lambda x: x["acs"], reverse=True)
        red_players.sort(key=lambda x: x["acs"], reverse=True)

        return {
            "match_id": metadata.get("matchid"),
            "map": {
                "name": metadata.get("map", "Inconnu")
            },
            "mode": metadata.get("mode", "Competitive"),
            "score": {
                "blue": teams.get("blue", {}).get("rounds_won", 0),
                "red": teams.get("red", {}).get("rounds_won", 0)
            },
            "team_blue": blue_players,
            "team_red": red_players
        }
