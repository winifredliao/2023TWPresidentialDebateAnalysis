GOOGLE_APPLICATION_CREDENTIALS="" #API json file

import pandas as pd
from google.cloud import language_v1
import time

batch_size = 500
client = language_v1.LanguageServiceClient()

def senti(df):
    missings=[]
    for group_name, group_df in df.groupby(df.index // batch_size):
        senti_score = []
        senti_magnitude = []

        for index, row in group_df.iterrows():
            text = row['text']
            try:
                document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
                sentiment = client.analyze_sentiment(document=document).document_sentiment

                score = f"{sentiment.score}"
                senti_score.append(score)

                magni = f"{sentiment.magnitude}"
                senti_magnitude.append(magni)

            except:
                missings.append(index)
                senti_score.append('0')
                senti_magnitude.append('0')
                
        time.sleep(10)

        df.loc[group_df.index, 'Sentiment_Score'] = senti_score
        df.loc[group_df.index, 'Sentiment_Magnitude'] = senti_magnitude

    for i in missings:
        df.drop([i])
    
    return(df)

df_re=pd.read_csv('C:/Users/blues/Desktop/Projects/2024TWPresidentialDebateAnalysis/All_CSV/clean_data/台視.csv')
df_names=['TVBS', '東森', '三立', '民視', '中視', '年代', '中天', '公視']
df_all=df_re
for name in df_names:
    df=pd.read_csv('C:/Users/blues/Desktop/Projects/2024TWPresidentialDebateAnalysis/All_CSV/clean_data/'+name+'.csv')
    df_all=pd.concat([df_all, df]).reset_index(drop=True)

senti_data=senti(df_all)
senti_data.to_csv('C:/Users/blues/Desktop/Projects/2024TWPresidentialDebateAnalysis/All_CSV/senti_dataset.csv', index=False, encoding='utf_8_sig')