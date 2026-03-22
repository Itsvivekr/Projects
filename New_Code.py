import socket
import requests
import qrcode
import hashlib
import json
import os
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
# ================= SETTINGS =================
BOT_TOKEN = "8747540971:AAHmgfV2LesfnXNscPYvD7QMfQShZxFx1Yg"
CHAT_ID = "1169359211"

UDP_IP = "0.0.0.0"
UDP_PORT = 4210
PDF_FILE = "PH_Report.pdf"
QR_FILE = "PH_Report_QR.png"

# ================= UDP SETUP =================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP Broadcast on port", UDP_PORT)

# ================= FUNCTION TO CLASSIFY pH =================
def classify_ph(ph_value):
    ph_value = int(ph_value)
    if 900 <= ph_value <= 1300:
        status = "BASE"
        editable = "No"  # not editable
    elif 1400 <= ph_value <= 1900:
        status = "NORMAL"
        editable = "Yes"  # editable
    elif 2100 <= ph_value <= 2700:
        status = "ACID"
        editable = "No"  # not editable
    else:
        status = "OUTRANGE"
        editable = "No"
    return status, editable


# ================= BLOCKCHAIN FUNCTIONS =================

def calculate_hash(index, timestamp, data, previous_hash):
    block_string = f"{index}{timestamp}{data}{previous_hash}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def add_block(data):
    chain = load_blockchain()

    index = len(chain)
    timestamp = str(datetime.datetime.now())
    previous_hash = chain[-1]["hash"] if chain else "0"

    block_hash = calculate_hash(index, timestamp, data, previous_hash)

    block = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "hash": block_hash
    }

    chain.append(block)
    save_blockchain(chain)

    print("🔐 Block Added")
    print("Hash:", block_hash)

    return block_hash

def retrieve_block_by_hash(search_hash):
    chain = load_blockchain()

    for block in chain:
        if block["hash"] == search_hash:
            return block
    return None


# ================= MAIN LOOP =================
while True:
    data, addr = sock.recvfrom(1024)
    received_text = data.decode()
    print("Received:", received_text)

    try:
        ph_value_str, _ = received_text.split(",")
    except:
        ph_value_str = received_text.split(",")[0]

    status, editable = classify_ph(ph_value_str)

    # ================= ADD TO BLOCKCHAIN =================
    block_data = {
        "pH": ph_value_str,
        "status": status,
        "editable": editable,
        "type": organic
    }

    block_hash = add_block(block_data)

    # ================= RETRIEVE BLOCK =================
    retrieved_block = retrieve_block_by_hash(block_hash)

    # ================= CREATE PDF =================
    doc = SimpleDocTemplate(PDF_FILE)
    elements = []
    styles = getSampleStyleSheet()

    # Heading
    heading_style = styles["Heading1"].clone('heading_style')
    heading_style.alignment = TA_CENTER
    elements.append(Paragraph("IoT Organic pH Lab Report", heading_style))
    elements.append(Spacer(1, 0.3 * inch))


    # Data Table
    elements.append(Paragraph("PH Analysis", styles["Heading2"]))
    elements.append(Spacer(1, 0.25 * inch))
    table_data = [
        ["pH Value", "Status", "Editable"],
        [ph_value_str, status, editable]
    ]

    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])

    table = Table(table_data, colWidths=[1.5*inch]*3, hAlign='LEFT')
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.25 * inch))

    # Notes / Interpretation
    notes = (
        "- BASE (900-1300): Nutrient solution is alkaline. Not editable.\n"
        "- NORMAL (1400-1900): Ideal pH range. Editable.\n"
        "- ACID (2100-2700): Nutrient solution is acidic. Not editable.\n"
        "- OUTRANGE: Check sensor or solution. Not editable."
    )
    elements.append(Paragraph("Interpretation:", styles["Heading2"]))
    elements.append(Paragraph(notes, styles["Normal"]))

    elements.append(Spacer(1, 0.25 * inch))

    # Blockchain Hash
    elements.append(Paragraph("Blockchain Hash:", styles["Heading2"]))
    elements.append(Paragraph(block_hash, styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Retrieved Block Data
    if retrieved_block:
        elements.append(Paragraph("Retrieved Blockchain Record:", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        retrieved_data = [
            ["Index", str(retrieved_block["index"])],
            ["Timestamp", retrieved_block["timestamp"]],
            ["pH", retrieved_block["data"]["pH"]],
            ["Status", retrieved_block["data"]["status"]],
            ["Editable", retrieved_block["data"]["editable"]],
            ["Type", retrieved_block["data"]["type"]],
            ["Previous Hash", retrieved_block["previous_hash"]],
            ["Hash", retrieved_block["hash"]],
        ]

        retrieved_table = Table(retrieved_data, colWidths=[1.5*inch, 3*inch], hAlign='LEFT' )
        retrieved_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ]))

        elements.append(retrieved_table)


    disclaimer_style = styles["Normal"].clone('disclaimer_style')
    disclaimer_style.alignment = TA_CENTER
    disclaimer_style.fontSize = 8
    disclaimer_style.textColor = colors.red
    disclaimer_text = (
    "Please be advised that the tested sample shows abnormal pH levels and exhibits high chemical reactivity.<br/><br/>"
    "Due to its unstable chemical behavior, the substance may be unsafe for consumption.<br/><br/>"
    "<b>This product is NOT EDIBLE and should not be consumed under any circumstances.</b>"
    )

    # ... after notes section
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(elements)
    print("PDF Updated Successfully")

    # ================= SEND TO TELEGRAM =================
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    with open(PDF_FILE, "rb") as f:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})

    result = response.json()
    if result["ok"]:
        file_id = result["result"]["document"]["file_id"]

        # Get download link
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()
        file_path = file_info["result"]["file_path"]
        download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # ================= GENERATE QR =================
        qr = qrcode.make(download_link)
        qr.save(QR_FILE)
        print("QR Code Updated Successfully")
        print("Download Link:", download_link)
    else:
        print("Error sending PDF to Telegram:", result)

    print("----------------------------------")
