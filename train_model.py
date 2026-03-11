import torch
from transformers import DistilBertTokenizerFast,DistilBertForSequenceClassification,Trainer,TrainingArguments
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

true=pd.read_csv("True.csv")
fake=pd.read_csv("Fake.csv")
ai_real=pd.read_csv("AI_realistic.csv")
ai_fake=pd.read_csv("AI_fake.csv")
ai_human=pd.read_csv("AI_vs_Human.csv")
ai_gen=pd.read_csv("AI Gen.csv")
ai_det=pd.read_csv("AI_det.csv")
aiVShuman=pd.read_csv("AIvsHuman.csv")

true['label']=0
fake['label']=1
ai_real['label']=2
ai_fake['label']=3

ai_human['label'] = ai_human['author_type'].apply(
    lambda x: 2 if str(x).lower()=='ai' else 0
)

ai_gen['label'] = ai_gen['generated'].apply(
    lambda x: 2 if x==1 else 0
)

ai_det['label'] = ai_det['source_model'].apply(
    lambda x: 0 if str(x).lower()=='human' else 2
)

aiVShuman['label'] = aiVShuman['label'].apply(
    lambda x: 2 if str(x).lower()=='ai' else 0
)

true = true.rename(columns={'title':'text','content':'text'})
data = pd.concat(
    [true, fake, ai_real, ai_fake, ai_human, ai_gen, ai_det, aiVShuman],
    ignore_index=True
)

data = data[['text','label']]
data = data.dropna()
data = data.drop_duplicates()
print("Unique labels:", data['label'].unique())

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

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_labels),
    y=train_labels
)
class_weights = torch.tensor(class_weights, dtype=torch.float)

tokenizer=DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
train_encodings=tokenizer(
    list(train_texts),
    truncation=True,
    padding='max_length',
    max_length=256
    )
test_encodings=tokenizer(
    list(test_texts),
    truncation=True,
    padding='max_length',
    max_length=256
)
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
train_dataset = NewsDataset(train_encodings, list(train_labels))
test_dataset = NewsDataset(test_encodings, list(test_labels))

model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=4)

class WeightedTrainer(Trainer):

    def __init__(self, class_weights=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):

        labels = inputs.get("labels")
        outputs = model(**inputs)

        logits = outputs.get("logits")

        loss_fct = torch.nn.CrossEntropyLoss(
            weight=self.class_weights.to(logits.device)
        )

        loss = loss_fct(logits, labels)

        return (loss, outputs) if return_outputs else loss
    
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    
    predictions = torch.argmax(torch.tensor(logits), dim=1).numpy()
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average='weighted'
    )
    
    acc = accuracy_score(labels, predictions)
    
    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall,
    }

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir='./logs',
    learning_rate=2e-5,
    load_best_model_at_end=True,
    warmup_steps=500,
    weight_decay=0.01
)
trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    class_weights=class_weights
)
trainer.train()
metrics = trainer.evaluate()
print("\nEvaluation Results:")
print(metrics)

model.save_pretrained("model_dir")
tokenizer.save_pretrained("model_dir")

print("Training samples:",len(train_texts))
print("Testing samples:",len(test_texts))
print("Examble train texts:",train_texts.iloc[0])
print("Example train label:", train_labels.iloc[0])

print("DistilBert Model and tokenizer saved to 'model_dir'")