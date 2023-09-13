from googleapiclient.discovery import build

import sys
import datetime

sys.stdin.reconfigure(encoding='utf-8')
# sys.stdout.reconfigure(encoding='utf-8')

# Arguments that need to passed to the build function
DEVELOPER_KEY = "AIzaSyCarGpEfvHg-9zsYEMpbZ754o1OvsuBvok"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating Youtube Resource Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                        developerKey = DEVELOPER_KEY)

# Create date
date_3months = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)).isoformat()
date_6months = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=180)).isoformat()

def youtube_search_keyword(query, max_results):

    # calling the search.list method to
    # retrieve youtube search results
    search_keyword = youtube_object.search().list(q = query, part = "id, snippet",
                                               maxResults = max_results, type="video", order="viewCount",

                                               # Location of Buenos Aires
                                               location=(34.6037, 58.3816),locationRadius=1000km, 

                                               # Span of 3-6 months ago
                                               publishedAfter=date_6months, publishedBefore=date_3months).execute()

    # extracting the results from search response
    results = search_keyword.get("items", [])

    # empty list to store video,
    # channel, playlist metadata
    videos = []
    playlists = []
    channels = []

    # extracting required info from each result object
    for result in results:
        # video result object
        if result['id']['kind'] == "youtube#video":
            videos.append([
                result['snippet']['thumbnails']['default']['url'], # image
                result["snippet"]["publishedAt"], # date
                (result["snippet"]["title"].encode(encoding="utf-8",errors="ignore")).decode(errors="ignore"), # title
                result["id"]["videoId"],
                result["snippet"]["channelId"]])
            
        # # playlist result object
        # elif result['id']['kind'] == "youtube#playlist":
        #     playlists.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
        #                          result["id"]["playlistId"],
        #                          result['snippet']['description'],
        #                          result['snippet']['thumbnails']['default']['url']))

        # # channel result object
        # elif result['id']['kind'] == "youtube#channel":
        #     channels.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
        #                            result["id"]["channelId"],
        #                            result['snippet']['description'],
        #                            result['snippet']['thumbnails']['default']['url']))

    # print("Videos:\n", "\n".join(videos), "\n")
    # print("Channels:\n", "\n".join(channels), "\n")
    # print("Playlists:\n", "\n".join(playlists), "\n")
    # print(results)

    return videos

youtube_search_keyword('', max_results = 10)
