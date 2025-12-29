from download_artifacts import download_artifacts
from export_classifier_to_onnx import export_classifier_to_onnx
from export_sentence_transformer_to_onnx import export_model_to_onnx
from settings import Settings
import argparse
import sys

def download():
    parser = argparse.ArgumentParser()

    parser.add_argument("--download", action="store_true", help="Download artifacts from S3")
    parser.add_argument("--export", action="store_true", help="Export to ONNX")
    parser.add_argument("--all", action="store_true", help="Run all steps")

    args = parser.parse_args()
    settings = Settings()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.all or args.download:
        download_artifacts(settings)

    if args.all or args.export:
        export_classifier_to_onnx(settings)
        export_model_to_onnx(settings)

if __name__ == '__main__':
    download()