from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as pd
import pandas as pd
import matplotlib.pyplot as plt
import wx


DEVELOPER_KEY = "AIzaSyA4IDPVIMXqYIZEDBxmkUppCzg1UkWaBTY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

            search_response = youtube.search().list(
            q=q,
            type="video",
            pageToken=token,
            order = order,
            part="id,snippet", # Part signifies the different types of data you want 
            maxResults=50,
            location=location,
            locationRadius=location_radius).execute()

            title = []
            channelId = []
            channelTitle = []
            categoryId = []
            videoId = []
            viewCount = []
            likeCount = []
            dislikeCount = []
            commentCount = []
            favoriteCount = []
            category = []
            tags = []
            videos = []
            
            for search_result in search_response.get("items", []):
                    	if search_result["id"]["kind"] == "youtube#video":

                            title.append(search_result['snippet']['title']) 

                            videoId.append(search_result['id']['videoId'])

                            response = youtube.videos().list(part='statistics, snippet',id=search_result['id']['videoId']).execute()

                            channelId.append(response['items'][0]['snippet']['channelId'])
                            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
                            categoryId.append(response['items'][0]['snippet']['categoryId'])
                            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
                            viewCount.append(response['items'][0]['statistics']['viewCount'])
                            likeCount.append(response['items'][0]['statistics']['likeCount'])
                            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
                            

         
                            if 'commentCount' in response['items'][0]['statistics'].keys():
                            
                                commentCount.append(response['items'][0]['statistics']['commentCount'])
                            else:
                                   commentCount.append([])
	          
                            if 'tags' in response['items'][0]['snippet'].keys():
                                        tags.append(response['items'][0]['snippet']['tags'])
                            else:
                                         tags.append([])
                                        

                            youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle':
                            channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,
                                                                       'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount}

            return youtube_dict

                                                                                                                                                                                                                                                                

                                                                                                                                                                                                                                                                                                                                                                                                

                                                                
app=wx.App()
tld=wx.TextEntryDialog(None,"Data","Enter the Channel Name: ")
if tld.ShowModal()==wx.ID_OK:
        print("App Started")
else:
        print("App Crashed!!!")
        
test = youtube_search(tld.GetValue())
print(test.keys())

df = pd.DataFrame(data=test)
print(df.head())

df1 = df[['title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']]
df1.columns = ['Title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']
print(df1.head())


import numpy as np
numeric_dtype = ['viewCount','commentCount','likeCount','dislikeCount','favoriteCount']
for i in numeric_dtype:
         df1[i] = df[i].astype(int)

tld=wx.TextEntryDialog(None,"Data","Enter the Channel ID Now: ")
if tld.ShowModal()==wx.ID_OK:
        print("App Started")
else:
        print("App Crashed!!!")

ImagineDragons = df1[df1['channelTitle']==tld.GetValue()]
print(ImagineDragons.head())



ImagineDragons = ImagineDragons.sort_values(ascending=False,by='viewCount')
plt.bar(range(ImagineDragons.shape[0]),ImagineDragons['viewCount'])
plt.xticks(range(ImagineDragons.shape[0]),ImagineDragons['Title'],rotation=90)
plt.ylabel('viewCount in 100 millions')

plt.show()
app.MainLoop()


