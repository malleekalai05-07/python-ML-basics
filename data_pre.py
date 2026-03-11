import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import torch

true=pd.read_csv("True.csv")
fake=pd.read_csv("Fake.csv")
ai_real=pd.read_csv("AI_realistic.csv")
ai_fake=pd.read_csv("AI_fake.csv")
ai_human=pd.read_csv("AI_vs_Human.csv")
ai_gen=pd.read_csv("AI Gen.csv")
ai_det=pd.read_csv("AI_det.csv")
aiVShuman=pd.read_csv("AIvsHuman.csv")

print("true:",len(true))
print("fake:",len(fake))
print("ai_real:",len(ai_real))
print("ai_fake:",len(ai_fake))
print("ai_human:",len(ai_human))
print("ai_gen:",len(ai_gen))
print("ai_det:",len(ai_det))
print("aiVShuman:",len(aiVShuman))

true['label']=0
fake['label']=1
ai_real['label']=2
ai_fake['label']=3

print(ai_human.columns)
print(ai_gen.columns)
print(ai_det.columns)
print(aiVShuman.columns)

ai_human['label'] = ai_human['author_type'].apply(lambda x: 1 if x=='AI' else 0)
ai_gen['label'] = ai_gen['generated'].apply(lambda x: 'AI' if x==1 else 'Human')
print(ai_gen['generated'].unique())
ai_det['label'] = ai_det['source_model'].apply(lambda x:0 if x=='Human' else 1)

data=pd.concat([true,fake,ai_fake,ai_real,ai_human,ai_gen,ai_det,aiVShuman],ignore_index=True)
data=data.drop_duplicates()
data = data.dropna(subset=['label'])

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(data['label']),
    y=data['label']
)

class_weights = torch.tensor(class_weights, dtype=torch.float)

print("combined datasets shape:",data.shape)
print(data.head())

data['text']=data['text'].astype(str).str.lower().str.strip()

train_texts,test_texts,train_labels,test_labels= train_test_split(
    data['text'],
    data['label'],
    test_size=0.2,
    random_state=42,
    stratify=data['label']
)
print("Training samples:",len(train_texts))
print("Testing samples:",len(test_texts))
print("Examble train texts:",train_texts.iloc[0])
print("Example train label:", train_labels.iloc[0])
