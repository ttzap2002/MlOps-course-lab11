
class Settings:
    s3_bucket: str = "mlops-lab11-models-tzapart"
    region: str = "us-east-1"
    s3_model_dir: str = "model"
    sentence_transformer_dir: str = "model/sentence_transformer.model"
    onnx_tokenizer_path: str = "model/transformer_tokenizer"
    classifier_joblib_path: str = "model/classifier.joblib"
    onnx_classifier_path: str = "model/classifier.onnx"
    onnx_embedding_model_path: str = "model/sentence_transformer.onnx"
    embedding_dim: int = 384
