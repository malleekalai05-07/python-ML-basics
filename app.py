from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

app = FastAPI(title="AI generated and Human Written Misinformation")

model_path = "model_dir"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

label_map = {
    0: "Human_real",
    1: "Human_fake",
    2: "AI_real",
    3: "AI_fake"
}

class Newsinput(BaseModel):
    text: str

@app.get("/")
async def home():
    return {"message": "API is running successfully"}

@app.post("/predict")
async def predict(data: Newsinput):
    text = data.text


    if not text.strip():
        return {"error": "Text cannot be empty"}

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding='max_length',
        max_length=256
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()

    result = label_map[prediction]
    source, truth = result.split("_")

    return {
        "prediction": result,
        "source": source,
        "truth": truth
    }