import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY=os.getenv("API_KEY")

CHANNEL_HANDLE="MrBeast"

def getChannelId():
    try: 
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response=requests.get(url)
        response.raise_for_status()

        data=response.json()
        # print(json.dumps(data,indent=4))

        playlist_id=data["items"][0]
        channel_id=playlist_id["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(channel_id)

        return channel_id
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__=="__main__":
    getChannelId()