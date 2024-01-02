import os
import googleapiclient.discovery
from google.oauth2 import service_account
from datetime import datetime, timedelta
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
api_key = ""  # Replace with your own API key
today = datetime.today().date()
five_months_ago = today - timedelta(days=5 * 30)
# Create a YouTube Data API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
def get_channel_creation_date(channel_id):
    response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()
    print()
    if 'items' in response:
        channel = response['items'][0]
        snippet = channel['snippet']
        published_at = snippet['publishedAt']
        subs = response['items'][0]['statistics']['subscriberCount']
        return published_at,subs
    else:
        return None

def find_newest_channels(max_results):
    newest_channels = []

    next_page_token = None
    while len(newest_channels) < max_results:
        response = youtube.search().list(
            part='snippet',
            maxResults=min(50, max_results - len(newest_channels)),
            q='',
            type='channel',
            order='viewCount ',
            pageToken=next_page_token
        ).execute()
        print(min(50, max_results - len(newest_channels)))
        if 'items' in response:
            for item in response['items']:
                channel_id = item['id']['channelId']
                channel_title = item['snippet']['title']
                creation_date,subs = get_channel_creation_date(channel_id)
        try:
                # Try parsing with format '%Y-%m-%dT%H:%M:%S.%fZ'
                channel_creation_date = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        except ValueError:
            try:
                # Try parsing with format '%Y-%m-%dT%H:%M:%SZ'
                channel_creation_date = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%SZ").date()
            except ValueError:
                # Handle other datetime formats as needed
                continue
        if (
            int(subs) >= 1000000
            #and niche in channel_response["items"][0]["snippet"]["title"]
        ):
            newest_channels.append((channel_title,subs,channel_id, creation_date))
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

    return newest_channels

channels = find_newest_channels(max_results=5)
for channel_title,subs,channel_id, creation_date in channels:
    print(f"Channel Title: {channel_title}")
    print(f"Subs: {subs}")
