from io import BytesIO
from PIL import Image
from flask import Flask, request
from transformers import DonutProcessor, VisionEncoderDecoderModel

def get_model(model_path):
    """Load a Hugging Face model and tokenizer from the specified directory"""
    tokenizer = DonutProcessor.from_pretrained(model_path)
    model = VisionEncoderDecoderModel.from_pretrained(model_path)
    return model, tokenizer

# Load the models and tokenizers for each supported language
model, tokenizer = get_model('models/invoice-and-receipts_donut_v1/')


app = Flask(__name__)

@app.route('/read-invoice/', methods=['POST'])
def read_invoice():
    if "invoice" in request.files:
        invoice_image = request.files["invoice"]
        if invoice_image:
            image_bytes = Image.open(invoice_image).convert("RGB")
            pixel_values = tokenizer(images=image_bytes, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values)
            generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return generated_text
        else:
            return "Invalid file"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)