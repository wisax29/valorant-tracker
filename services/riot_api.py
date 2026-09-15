"""
Official Riot Games API Client.
Handles:
- Riot Account V1 (Riot ID -> PUUID, gameName, tagLine)
- VAL-STATUS-V1 (Server health)
- VAL-CONTENT-V1 (Game content, maps, localized strings)
- VAL-MATCH-V1 (Matchlists and match details, when production key is enabled)
"""
import requests
import logging

logger = logging.getLogger(__name__)

# Account-v1 regional routes
ACCOUNT_REGIONS = {
    "eu": "europe.api.riotgames.com",
    "na": "americas.api.riotgames.com",
    "latam": "americas.api.riotgames.com",
    "br": "americas.api.riotgames.com",
    "kr": "asia.api.riotgames.com",
    "ap": "asia.api.riotgames.com"
}

# Val-specific platform routes
VAL_PLATFORMS = {
    "eu": "eu.api.riotgames.com",
    "na": "na.api.riotgames.com",
    "latam": "latam.api.riotgames.com",
    "br": "br.api.riotgames.com",
    "kr": "kr.api.riotgames.com",
    "ap": "ap.api.riotgames.com"
}

class RiotValorantAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or ""
        self.headers = {
            "User-Agent": "ValorantTrackerFlask/1.0"
        }
        if self.api_key:
            self.headers["X-Riot-Token"] = self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key
        if api_key:
            self.headers["X-Riot-Token"] = api_key
        elif "X-Riot-Token" in self.headers:
            del self.headers["X-Riot-Token"]

    def _get(self, host, endpoint, params=None):
        if not self.api_key:
            return {"status": 401, "error": "Aucune clé API Riot Games renseignée (RGAPI-...)."}
        url = f"https://{host}{endpoint}"
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=8)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                return {"status": 404, "error": "Joueur ou ressource Riot introuvable."}
            elif resp.status_code == 403:
                return {
                    "status": 403, 
                    "error": "Accès refusé par Riot. Note : Les clés de développement Riot normales ne donnent pas accès à l'historique des matchs Valorant sans approbation Production."
                }
            elif resp.status_code == 429:
                return {"status": 429, "error": "Rate limit Riot Games dépassé."}
            else:
                return {"status": resp.status_code, "error": f"Erreur Riot API ({resp.status_code}): {resp.text}"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur Riot API: {e}")
            return {"status": 500, "error": f"Erreur de connexion Riot: {str(e)}"}

    def get_account_by_riot_id(self, game_name, tag_line, region="eu"):
        """Resolves Riot ID (Pseudo#TAG) to PUUID via Riot Account V1."""
        host = ACCOUNT_REGIONS.get(region.lower(), "europe.api.riotgames.com")
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self._get(host, endpoint)

    def get_val_status(self, region="eu"):
        """Checks platform status for Valorant."""
        host = VAL_PLATFORMS.get(region.lower(), "eu.api.riotgames.com")
        endpoint = "/val/status/v1/platform-data"
        return self._get(host, endpoint)

    def get_matchlist(self, puuid, region="eu"):
        """Fetches match history by PUUID (requires approved key)."""
        host = VAL_PLATFORMS.get(region.lower(), "eu.api.riotgames.com")
        endpoint = f"/val/match/v1/matchlists/by-puuid/{puuid}"
        return self._get(host, endpoint)

    def get_match(self, match_id, region="eu"):
        """Fetches match details by matchId (requires approved key)."""
        host = VAL_PLATFORMS.get(region.lower(), "eu.api.riotgames.com")
        endpoint = f"/val/match/v1/matches/{match_id}"
        return self._get(host, endpoint)
