import torch
from transformers import pipeline
classifier = pipeline('sentiment-analysis')
def review(s):
    sentiment=''
    t=(classifier(s))   
    for i in t:
        sentiment=i['label']
    return sentiment    

# print(review('Hi this product has a good ui'))    

def summary(data1):
    summarizer=pipeline('summarization')
    
    # summarizer(data1, min_length = 0.1 * len(text), max_length = 0.2 * len(text))
    # summarizer=pipeline('summarization',max_length=30000)
    if len(data1) > 1024:
        data1 = data1[:1024]

    summary_text = summarizer(data1,min_length=100, max_length=100)[0]['summary_text']
    return summary_text
# print(summary('Hi this product has a good ui and gujju is a shit person and a very bad boy and also a very disobedient boy.'))    
