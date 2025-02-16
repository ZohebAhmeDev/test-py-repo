import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
import random
import string
from datetime import datetime
import base64

def generate_pdf(waybills_data):
    pdf_path = "waybills.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_width, page_height = A4
    
    quadrant_width = page_width / 2
    quadrant_height = page_height / 2
    
    for i, data in enumerate(waybills_data[:4]):
        col = i % 2
        row = i // 2
        x = col * quadrant_width
        y = page_height - (row + 1) * quadrant_height
        
        c.rect(x, y, quadrant_width, quadrant_height)
        draw_waybill(c, x + 5*mm, y + 5*mm, 
                    quadrant_width - 10*mm, 
                    quadrant_height - 10*mm, 
                    data)
        
    c.save()
    return pdf_path

# def draw_waybill(c, x, y, width, height, data):
    # Logo handling
    try:
        c.drawImage('logo.jpeg', x, y + height - 15*mm, width=18*mm, height=18*mm)
    except:
        c.drawString(x, y + height - 15*mm, "[LOGO PLACEHOLDER]")
    
    # Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 45*mm, y + height - 10*mm, "WAYBILL")
    
    # Waybill Number
    waybill_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    c.setFont("Helvetica", 10)
    c.drawString(x, y + height - 25*mm, f"Waybill #: {waybill_num}")
    
    # Barcode
    barcode = code128.Code128(waybill_num, barHeight=10*mm, barWidth=0.8)
    barcode.drawOn(c, x, y + height - 40*mm)
    
    # Date/Time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(x, y + height - 45*mm, f"Generated: {current_time}")
    
    # Sender Info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 60*mm, "Sender:")
    c.setFont("Helvetica", 9)
    c.drawString(x, y + height - 65*mm, data['sender']['name'])
    c.drawString(x, y + height - 70*mm, data['sender']['address'])
    c.drawString(x, y + height - 75*mm, data['sender']['phone'])
    
    # Recipient Info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 85*mm, "Recipient:")
    c.setFont("Helvetica", 9)
    c.drawString(x, y + height - 90*mm, data['recipient']['name'])
    c.drawString(x, y + height - 95*mm, data['recipient']['address'])
    c.drawString(x, y + height - 100*mm, data['recipient']['phone'])
    
    # Package Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 110*mm, "Package Details:")
    c.setFont("Helvetica", 9)
    details = [
        f"Weight: {data['package']['weight']} kg",
        f"Dimensions: {data['package']['dimensions']}",
        f"Contents: {data['package']['contents']}"
    ]
    for i, detail in enumerate(details):
        c.drawString(x, y + height - (115 + i*5)*mm, detail)
def draw_waybill(c, x, y, width, height, data):
    # Logo handling
    try:
        c.drawImage('logo.jpeg', x, y + height - 15*mm, width=18*mm, height=18*mm)
    except:
        c.drawString(x, y + height - 15*mm, "[LOGO PLACEHOLDER]")
    # Line below logo
    c.line(x, y + height - 20*mm, x + width, y + height - 20*mm)
    # Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 45*mm, y + height - 10*mm, "PRIORITY MAIL")
    
    # Waybill Number
    waybill_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    c.setFont("Helvetica", 10)
    c.drawString(x, y + height - 25*mm, f"Waybill #: {waybill_num}")
    
    # Barcode
    barcode = code128.Code128(waybill_num, barHeight=10*mm, barWidth=0.8)
    barcode.drawOn(c, x, y + height - 40*mm)
    
    # Date/Time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(x, y + height - 45*mm, f"Generated: {current_time}")
    
    # Section separator lines
    c.setStrokeColorRGB(0, 0, 0)  # Black color
    c.setLineWidth(0.5*mm)        # Line thickness
    
    # Line below header
    c.line(x, y + height - 47*mm, x + width, y + height - 47*mm)
    
    # Sender Info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 60*mm, "Sender:")
    c.setFont("Helvetica", 9)
    c.drawString(x, y + height - 65*mm, data['sender']['name'])
    c.drawString(x, y + height - 70*mm, data['sender']['address'])
    
    # Line below sender
    c.line(x, y + height - 73*mm, x + width, y + height - 73*mm)
    
    # Recipient Info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 85*mm, "Recipient:")
    c.setFont("Helvetica", 9)
    c.drawString(x, y + height - 90*mm, data['recipient']['name'])
    c.drawString(x, y + height - 95*mm, data['recipient']['address'])
    
    # Line below recipient
    c.line(x, y + height - 104*mm, x + width, y + height - 104*mm)
    
    # Package Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y + height - 110*mm, "Package Details:")
    # Line above package details
    
    
    c.setFont("Helvetica", 9)
    details = [
        f"Weight: {data['package']['weight']} kg",
        f"Dimensions: {data['package']['dimensions']}",
        f"Contents: {data['package']['contents']}"
    ]
    for i, detail in enumerate(details):
        c.drawString(x, y + height - (115 + i*5)*mm, detail)
def main():
    st.title("Waybill Generator 📦")
    
    if 'waybills' not in st.session_state:
        st.session_state.waybills = []
    
    with st.form("waybill_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Sender Details")
            sender_name = st.text_input("Sender Name")
            sender_address = st.text_area("Sender Address")
            sender_phone = st.text_input("Sender Phone")
            
        with col2:
            st.header("Recipient Details")
            recipient_name = st.text_input("Recipient Name")
            recipient_address = st.text_area("Recipient Address")
            recipient_phone = st.text_input("Recipient Phone")
            
        st.header("Package Details")
        weight = st.number_input("Weight (kg)", min_value=0.1)
        dimensions = st.text_input("Dimensions (cm)", placeholder="LxWxH")
        contents = st.text_input("Contents")
        
        submitted = st.form_submit_button("Add Waybill")
        
        if submitted:
            waybill = {
                'sender': {
                    'name': sender_name,
                    'address': sender_address,
                    'phone': sender_phone
                },
                'recipient': {
                    'name': recipient_name,
                    'address': recipient_address,
                    'phone': recipient_phone
                },
                'package': {
                    'weight': str(weight),
                    'dimensions': dimensions,
                    'contents': contents
                }
            }
            st.session_state.waybills.append(waybill)
            st.success("Waybill added!")
    
    st.subheader(f"Waybills Queued: {len(st.session_state.waybills)}")
    
    if st.button("Generate PDF"):
        if len(st.session_state.waybills) == 0:
            st.warning("Add at least 1 waybill first!")
        else:
            pdf_path = generate_pdf(st.session_state.waybills)
            
            with open(pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                download_link = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="waybills.pdf">Download PDF</a>'
                st.markdown(download_link, unsafe_allow_html=True)
            
            st.session_state.waybills = []

if __name__ == "__main__":
    main()
