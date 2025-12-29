from fastapi import FastAPI
from tokenizers import Tokenizer
import onnxruntime as ort
import numpy as np
from pydantic import BaseModel
from mangum import Mangum

SENTIMENT_MAP = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    prediction: str

class SentimentInference:
    def __init__(self):
        try:
            self.tokenizer = Tokenizer.from_file("model/tokenizer.json")
            self.embedding_session = ort.InferenceSession("model/sentence_transformer.onnx")
            self.classifier_session = ort.InferenceSession("model/classifier.onnx")
        except Exception as e:
            raise RuntimeError(f"Failed to access ONNX {e}. Please check the file paths.")

    def predict(self, cleaned_text: str) -> str:
        # tokenize input
        encoded = self.tokenizer.encode(cleaned_text)

        # prepare numpy arrays for ONNX
        input_ids = np.array([encoded.ids])
        attention_mask = np.array([encoded.attention_mask])

        # run embedding inference
        embedding_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask
        }
        embeddings = self.embedding_session.run(None, embedding_inputs)[0]

        # run classifier inference
        classifier_input_name = self.classifier_session.get_inputs()[0].name
        classifier_inputs = {classifier_input_name: embeddings.astype(np.float32)}
        prediction = self.classifier_session.run(None, classifier_inputs)[0]

        label = SENTIMENT_MAP.get(prediction[0], "unknown")
        return label


app = FastAPI()
engine = SentimentInference()

@app.get("/")
def welcome_root():
    return {"message": "Welcome to the ML API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    predicted_label = engine.predict(request.text)

    return PredictResponse(prediction=predicted_label)


handler = Mangum(app)
