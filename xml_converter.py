import json
import xml.etree.ElementTree as ET

class ReceiptEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Receipt, SLineItem)):
            return obj.__dict__
        return super().default(obj)

class Receipt:
    def __init__(self):
        self.store_name = ""
        self.store_addr = ""
        self.telephone = ""
        self.date = ""
        self.time = ""
        self.subtotal = ""
        self.tax = ""
        self.total = ""
        self.ignore = ""
        self.tips = ""
        self.line_items = []

class SLineItem:
    def __init__(self):
        self.item_name = ""
        self.item_value = ""
        self.item_quantity = ""

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    
    receipt = Receipt()
    receipt.store_name = root.findtext("s_store_name")
    receipt.store_addr = root.findtext("s_store_addr")
    receipt.telephone = root.findtext("s_telephone")
    receipt.date = root.findtext("s_date")
    receipt.time = root.findtext("s_time")
    receipt.subtotal = root.findtext("s_subtotal")
    receipt.tax = root.findtext("s_tax")
    receipt.total = root.findtext("s_total")
    receipt.ignore = root.findtext("s_ignore")
    receipt.tips = root.findtext("s_tips")

    line_items = root.find("s_line_items")
    if line_items is not None:
        for line in line_items:
            tag = line.tag
            tag = tag.replace("s_item_", "item_")
            if "item_key" in tag:
                line_item = SLineItem()
            elif "sep" in line.tag:
                receipt.line_items.append(line_item)
                line_item = SLineItem()
            else:
                setattr(line_item, tag, line.text)    
    return receipt
