import requests
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"
maxResults=50

def getplaylistId():#or playlist id
    try: 
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response=requests.get(url)
        response.raise_for_status()

        data=response.json()
        # print(json.dumps(data,indent=4))

        playlist_id=data["items"][0]
        playlist_id=playlist_id["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(playlist_id)

        return playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e

def getVideoIds(playlist_id):

    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    video_ids=[]
    PageToken=None

    try:
        while True:

            if PageToken:
                base_url+=f"&pageToken={PageToken}"
            response=requests.get(base_url)
            response.raise_for_status()
            data=response.json()

            for items in data.get("items",[]):
                video_id=items["contentDetails"]["videoId"]

                video_ids.append(video_id)

            PageToken=data['nextPageToken']

            if not PageToken:
                break

            return video_ids
    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_lst):
    extracted_data=[]

    def get_batch_video(video_id_lst,batchSize):
        for video_id in (0,len(video_id_lst),batchSize):
            yield video_id_lst[video_id : video_id + batchSize]

    try:
        for batch_ids in (get_batch_video(video_lst,maxResults)):
            str_batch_ids=','.join(batch_ids)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={str_batch_ids}&key={API_KEY}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None),
                }

                extracted_data.append(video_data)
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e
def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__=="__main__":
    playlist_id=getplaylistId()
    video_lst=getVideoIds(playlist_id)
    video_data=extract_video_data(video_lst)
    save_to_json(video_data)

# Get the playlist items from the link https://developers.google.com/youtube/v3/docs/playlistItems/list