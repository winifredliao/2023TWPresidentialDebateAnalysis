import pandas as pd
import re
import opencc

#清除\r\n
def remove_elements(text):
    cleaned_text = re.sub(r"[\r\n]", "", text)
    return cleaned_text

#移除表符
def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def data_cleaning(df):
    #有哪些人重複留言
    #authors=df["author"]
    #duplicate_df=df[authors.isin(authors[authors.duplicated()])].sort_values("author")
    #print(duplicate_df)

    #將重複留言者的留言合併，其餘欄位保留第一次留言的資料
    df['text'] = df.groupby('author')['text'].transform(lambda x: '。'.join(x))
    df=df.drop_duplicates('author').reset_index(drop=True)

    #依照點讚數排序
    df=df.sort_values(by='like_count', ascending=False)
    df.reset_index()

    #清除\r\n_2_執行
    df['text'] = df['text'].apply(remove_elements)

    #移除表符_執行
    df['text'] = df['text'].apply(remove_emojis)

    #清除空值
    df.fillna(value=pd.NA, inplace=True)
    df.dropna()

    cc = opencc.OpenCC('s2twp')

    for index, row in df.iterrows():
        text = row['text']
        df.iat[index, 3] = cc.convert(text)
    
    return df

df_names=['TVBS', '東森', '三立', '民視', '中視', '年代', '中天', '公視', '台視']
for name in df_names:
    df=pd.read_csv('C:/Users/blues/Desktop/Projects/2023TWPresidentialDebateAnalysis/All_CSV/raw_data/'+name+'.csv')
    cleaned_file=data_cleaning(df)
    cleaned_file.to_csv('C:/Users/blues/Desktop/Projects/2023TWPresidentialDebateAnalysis/All_CSV/clean_data/'+name+'.csv', index=False, encoding='utf_8_sig')