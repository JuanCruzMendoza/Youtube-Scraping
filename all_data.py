import pandas as pd
from yt_stats import YTstats
from tqdm import tqdm
import numpy as np
from search_api import youtube_search_keyword
import datetime
from PIL import Image
from io import BytesIO
import requests
import sys

# For characters that cannot be encoded in titles
sys.stdin.reconfigure(encoding='utf-8')

# Variables
# API_KEY = 'AIzaSyCarGpEfvHg-9zsYEMpbZ754o1OvsuBvok'
# MAX_RESULTS = 5

# Function to download and convert an image to a NumPy array
def url_to_numpy(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_array = np.array(img)
            return img_array
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def create_df(API_KEY, MAX_RESULTS):
    results = youtube_search_keyword("", max_results=MAX_RESULTS)

    results = np.array(results)
    df = pd.DataFrame()
    df["title"] = results[:,2]
    df["video_id"] = results[:,3]
    df["channel_id"] = results[:,4]
    df["image_url"] = results[:, 0]
    df["date"] = results[:,1]

    # With YTstats extract views, viewCount (all views from channel), subscriberCount, videoCount
    Views =[]
    viewCount = []
    suscriberCount = []
    videoCount = []


    for x,y in tqdm(zip(df["video_id"],df["channel_id"])):
        channel_id = y
        video_id = x
        part = 'statistics'
        yt = YTstats(API_KEY, channel_id)
        video_stats = yt._get_single_video_data(video_id,part)
        Views.append(int(video_stats['viewCount']))

    df["views"] = Views
    

    # Apply the function to each row in the DataFrame and create a new column
    df['image_array'] = df['image_url'].apply(url_to_numpy) 

    return df

# df = create_df(API_KEY, MAX_RESULTS)

# date = str(datetime.datetime.now())[:10]
# print(df["views"])
# print(df["Image"])
# df.to_csv(f"{date}")