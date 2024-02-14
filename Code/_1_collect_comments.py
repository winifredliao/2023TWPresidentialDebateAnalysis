import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "" #來自Google cloud console的Youtube API

Video_ID=['nlketOzpI_E', 'Z8ZI53Cyk6Y', '8wOkaUWlLbM', '7S383KYEs18', 'cuZf0lr4F14',
         'BriQbgbqFYM', 'Pj61e_JSUCk', '2bIRjTiAHms', 'FpF-bEcMCYE']
df_names=['TVBS', '東森', '三立', '民視', '中視', '年代', '中天', '公視', '台視']

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

for i in range(8):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=Video_ID[i],
        maxResults=10000
    )

    comments = []

    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['likeCount'],
            comment['textOriginal'],
        ])

    while (1 == 1):
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            break
        nextPageToken = response['nextPageToken']
        nextRequest = youtube.commentThreads().list(part="snippet", videoId=Video_ID[i], maxResults=10000, pageToken=nextPageToken)
        response = nextRequest.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textOriginal'],
            ])

    df = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text'])
    df.to_csv(df_names[i]+'.csv', index=False, encoding='utf_8_sig')