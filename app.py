
from flask import Flask, request
import requests
import xml_converter
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/web-hook', methods=['POST'])
def home():
    if request.method == 'POST':
        dict_messages = request.json['data']
        if dict_messages != []:
            message = dict_messages
            msg_from = message['from'].split()
            msg_text = message['body'].split()
            print("sender phone number : " + msg_from[0])
            print("message : " + msg_text[0])
            return 'vaibhav'
        

@app.route('/read-invoice/', methods=['POST'])
def read_invoice():
    csv_headers = ["Date", "Time", "Store Name", "Total", "Item Name", "Value", "Quantity", "File Name", "Processed At"]
    csv_file_name = "data.csv"
    if "invoice" in request.files:
        invoice_image = request.files["invoice"]
        if not check_csv_for_values(csv_file_name, "File Name", invoice_image.filename):
            API_URL = "https://api-inference.huggingface.co/models/selvakumarcts/sk_invoice_receipts"
            headers = {"Authorization": "Bearer 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"}
            response = requests.post(API_URL, headers=headers, data=invoice_image)
            receipt_response =  str(response.json()[0]['generated_text']) + "</s_receipt>"
            receipt = xml_converter.parse_xml(receipt_response)
            receipt.file_name = invoice_image.filename
            receipt.processed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values = [[
                receipt.date,
                receipt.time,
                receipt.store_name,
                receipt.subtotal,
                item.item_name,
                item.item_value,
                item.item_quantity,
                receipt.file_name,
                receipt.processed_at
            ] for item in receipt.line_items]
            write_to_csv(csv_file_name, values, csv_headers)
            return xml_converter.convert_to_json(receipt)
        else:
            return 'Data already present'


def write_to_csv(csv_file_path, data, headers):
    try:
        # Check if the file exists
        file_exists = False
        with open(csv_file_path, 'r', newline='') as existing_file:
            csv_reader = csv.reader(existing_file)
            file_exists = any(row for row in csv_reader)

        # Write data to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                csv_header = []
                csv_header.append(headers)
                writer.writerows(csv_header)
            writer.writerows(data)
            print(f"Data has been appended to {csv_file_path}")
        

    except Exception as e:
        print(f"Error: {e}")


def check_csv_for_values(csv_file_path, column_name, target_values):
    try:
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row[column_name])
                # Check if the column_name is in the row and if its value is in the target_values
                if column_name in row and row[column_name] in target_values:
                    return True

    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print(f"Error: {e}")

    return False

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)