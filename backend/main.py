from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORS
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
import os

# Cấu hình logging
logging.basicConfig(filename="ai.log", level=logging.INFO)

app = FastAPI()

# Cho phép CORS để frontend kết nối
app.add_middleware(
    CORS,
    allow_origins=["*"],  # Railway sẽ cung cấp domain cho frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tải mô hình và tokenizer từ thư mục cục bộ
model_name = "./distilgpt2"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    raise HTTPException(status_code=500, detail="Model loading failed")

class Prompt(BaseModel):
    text: str

@app.post("/generate")
async def generate(prompt: Prompt):
    if any(keyword in prompt.text.lower() for keyword in ["system:", "admin:"]):
        raise HTTPException(status_code=400, detail="Invalid prompt")
    try:
        inputs = tokenizer(prompt.text, return_tensors="pt")
        outputs = model.generate(
            inputs["input_ids"],
            max_length=50,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"Prompt: {prompt.text}, Response: {response}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail="Generation failed")

# Health check cho Railway
@app.get("/health")
async def health():
    return {"status": "healthy"}
