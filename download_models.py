from transformers import DonutProcessor, VisionEncoderDecoderModel
import os

def download_model(model_path, model_name):
    """Download a Hugging Face model and tokenizer to the specified directory"""
    # Check if the directory already exists
    if not os.path.exists(model_path):
        # Create the directory
        os.makedirs(model_path)

    tokenizer = DonutProcessor.from_pretrained(model_name)
    model = VisionEncoderDecoderModel.from_pretrained(model_name)

    # Save the model and tokenizer to the specified directory
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

# For this demo, download the English-French and French-English models
download_model('models/invoice-and-receipts_donut_v1/', 'mychen76/invoice-and-receipts_donut_v1')