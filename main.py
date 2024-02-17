import time
from io import BytesIO

import requests


class Player:
    def __init__(self, minecraft_id: str, minecraft_name: str):
        self.minecraft_id = minecraft_id
        self.minecraft_name = minecraft_name




def get_player_from_code(code: str) -> Player:
    res = requests.post(
        url="https://login.live.com/oauth20_token.srf",
        data={
            "client_id": "00000000402b5328",
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL"
        }
    )

    if res.status_code != 200:
        raise ValueError(f"Wrong code: {code}")

    access_token = res.json()["access_token"]

    res = requests.post(
        url="https://user.auth.xboxlive.com/user/authenticate",
        json={
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        }
    )

    if res.status_code != 200:
        raise ValueError(f"Wrong code: {code}")

    xbl_token = res.json()["Token"]
    uhs = res.json()["DisplayClaims"]["xui"][0]["uhs"]

    res = requests.post(
        url="https://xsts.auth.xboxlive.com/xsts/authorize",
        json={
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [xbl_token]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        }
    )

    if res.status_code != 200:
        raise ValueError(f"Wrong code: {code}")

    xsts_token = res.json()["Token"]

    res = requests.post(
        url="https://api.minecraftservices.com/authentication/login_with_xbox",
        json={
            "identityToken": f"XBL3.0 x={uhs};{xsts_token}"
        }
    )

    if res.status_code != 200:
        raise ValueError(f"Wrong code: {code}")

    global minecraft_access_token
    minecraft_access_token = "eyJraWQiOiJhYzg0YSIsImFsZyI6IkhTMjU2In0.eyJ4dWlkIjoiMjUzNTQ1NzAyMDUxMTM4NCIsImFnZyI6IkFkdWx0Iiwic3ViIjoiZjE1ZWFhYTEtZTcxOC00YTBjLTk3ZWYtZjMxNmVhNzA1OTI4IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsidHdvZmFjdG9yYXV0aCIsIm1zYW1pZ3JhdGlvbl9zdGFnZTQiLCJvcmRlcnNfMjAyMiIsIm11bHRpcGxheWVyIl0sInByb2ZpbGVzIjp7Im1jIjoiZTUzYWM3MDItMDE5Yy00NTEyLWI2NjAtNTE2YzgxMTVhNzQyIn0sInBsYXRmb3JtIjoiVU5LTk9XTiIsIm5iZiI6MTcwODE5ODExOSwiZXhwIjoxNzA4Mjg0NTE5LCJpYXQiOjE3MDgxOTgxMTl9.nH3_07x3qHCnukcPmfAn5m0oIzSqVWCphl8MnZdtkkA"

    res = requests.get(
        url="https://api.minecraftservices.com/minecraft/profile",
        headers={
            "Authorization": f"Bearer {minecraft_access_token}"
        }
    )
    #print(minecraft_access_token)

    if res.status_code != 200:
        raise ValueError(f"Wrong code: {code}")

    minecraft_id = res.json()["id"]
    minecraft_name = res.json()["name"]

    return Player(minecraft_id, minecraft_name)


def main():
    print("Open this link in your browser:")
    print(
        "https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code"
        "&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&"
        "redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf"
    )

    minecraft_id = 1
    if minecraft_id != "0":
        name = "Q7J"
        while minecraft_id != 0:
            time.sleep(5)
            minecraft_access_token = "eyJraWQiOiJhYzg0YSIsImFsZyI6IkhTMjU2In0.eyJ4dWlkIjoiMjUzNTQ1NzAyMDUxMTM4NCIsImFnZyI6IkFkdWx0Iiwic3ViIjoiZjE1ZWFhYTEtZTcxOC00YTBjLTk3ZWYtZjMxNmVhNzA1OTI4IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsidHdvZmFjdG9yYXV0aCIsIm1zYW1pZ3JhdGlvbl9zdGFnZTQiLCJvcmRlcnNfMjAyMiIsIm11bHRpcGxheWVyIl0sInByb2ZpbGVzIjp7Im1jIjoiZTUzYWM3MDItMDE5Yy00NTEyLWI2NjAtNTE2YzgxMTVhNzQyIn0sInBsYXRmb3JtIjoiVU5LTk9XTiIsIm5iZiI6MTcwODE5ODExOSwiZXhwIjoxNzA4Mjg0NTE5LCJpYXQiOjE3MDgxOTgxMTl9.nH3_07x3qHCnukcPmfAn5m0oIzSqVWCphl8MnZdtkkA"
            res1 = requests.put(
                url=f"https://api.minecraftservices.com/minecraft/profile/name/{name}",
                headers={
                    "Authorization": f"Bearer {minecraft_access_token}"
                }
            )
            print(res1.json())


if __name__ == '__main__':
    main()
