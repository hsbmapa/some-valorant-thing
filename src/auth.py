import asyncio
import riot_auth
import requests
import time
from InquirerPy import inquirer

def get_agents():
    agents = {}
    res = requests.get("https://valorant-api.com/v1/agents").json()
    for agent in res['data']:
        agents[agent["displayName"]] = agent["uuid"]
    return agents

def get_maps():
    maps = {}
    res = requests.get("https://valorant-api.com/v1/maps").json()
    for map in res['data']:
        maps[map['displayName']] = map['uuid']
    return maps

class ValorantClient:
    def __init__(self) -> None:
        self.agents = get_agents()

        self.session = requests.session()

        self.id_token = None
        self.access_token = None
        self.entitlements_token = None
        self.user_id = None
        self.region = None
        self.auth()
        self.session.headers.update({
            "Authorization": "Bearer " + self.access_token
        })
        self.set_region()
        self.base_url = f"https://glz-{self.region}-1.{self.region}.a.pvp.net"

        
    def auth(self):
        username = inquirer.text(message="Enter your username: ").execute()
        password = inquirer.secret(message="Enter your password: ").execute()
        try:
            CREDS = username, password

            auth = riot_auth.RiotAuth()
            asyncio.run(auth.authorize(*CREDS))
            asyncio.run(auth.reauthorize())
        except Exception as e:
            print(e)
            time.sleep(10)
            exit(1)
            
        self.id_token = auth.id_token
        self.access_token = auth.access_token
        self.entitlements_token = auth.entitlements_token
        self.user_id = auth.user_id
        
    def get_ingame_name(self):
        url = "https://auth.riotgames.com/userinfo"
        res = self.session.post(url, headers=self.session.headers, json={})
        data = res.json()
        name = data['acct']['game_name']+'#'+data['acct']['tag_line']
        return name
        
        
    def set_region(self):
        url = "https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant"
        payload = {"id_token": self.id_token}
        res = self.session.put(url, json=payload)
        self.region = res.json()['affinities']['live']
        return self.region

    def get_session_status(self):
        url = f"{self.base_url}/session/v1/sessions/{self.user_id}"
        res = self.session.get(url, headers={"X-Riot-Entitlements-JWT": self.entitlements_token})
        while res.status_code == 404:
            print("Session not found, waiting...")
            time.sleep(10)
            res = self.session.get(url, headers={"X-Riot-Entitlements-JWT": self.entitlements_token})
        session_status = res.json()['loopState']
        return session_status

    def get_pregame_id(self):
        url = f"{self.base_url}/pregame/v1/players/{self.user_id}"
        res = self.session.get(url, headers={"X-Riot-Entitlements-JWT": self.entitlements_token})
        if res.status_code == 200:
            match_id = res.json()['MatchID']
            return match_id
        else:
            print("Error getting match id - not in pregame?")
        return None


    def lock_agent(self, agent_name: str):
        while self.get_session_status() != "PREGAME":
            print("Not in pregame, waiting...")
            time.sleep(5)

        pregame_id = self.get_pregame_id()
        url = f"{self.base_url}/pregame/v1/matches/{pregame_id}/lock/{self.agents[agent_name]}"
        res = self.session.post(url, headers={"X-Riot-Entitlements-JWT": self.entitlements_token})

if __name__ == "__main__":
    agents = get_agents()
    maps = get_maps()
    # client = ValorantClient()
    
