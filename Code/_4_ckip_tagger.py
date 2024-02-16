import pandas as pd
import tensorflow as tf
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

ws = WS("./data")
pos = POS("./data")
ner = NER("./data")

df=pd.read_csv('C:/Users/blues/Desktop/Projects/2024TWPresidentialDebateAnalysis/All_CSV/senti_dataset.csv')

text_column = str('text')
sentences = df[text_column].tolist()

# 使用 CKIPtagger 進行斷詞
word_segments = ws(sentences, sentence_segmentation=True, 
                    segment_delimiter_set={'?', '？', '!', '！', '。', ',', '，', ';', ':', '、'})

# 將斷詞結果添加到 DataFrame
df['word_segments'] = word_segments

# 使用 CKIPtagger 進行詞性標注
pos_results = pos(sentences)

# 使用 CKIPtagger 進行實體辨識
ner_results={}
ner_lists = ner(sentences, pos_results)
for entity in ner_lists:
    for elements in entity:
        ner_results[elements[2]]=elements[3]

# 將詞性標注和實體辨識結果添加到 DataFrame
df['pos_results'] = pos_results
df['ner_results'] = ner_results

df.to_csv('C:/Users/blues/Desktop/Projects/2024TWPresidentialDebateAnalysis/All_CSV/final_dataset.csv', index=False, encoding='utf_8_sig')