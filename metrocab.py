import streamlit as st
import qrcode
from io import BytesIO
import uuid

# --------------------------
# QR GENERATION FUNCTION
# --------------------------
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


st.set_page_config(page_title="Metro Ticket Booking", page_icon="@")
st.title("Metro Ticket Booking System")

stations = ["Ameerpet", "Miyapur", "LB Nagar", "KPHB", "JNTU"]

# --------------------------
# INPUT FIELDS
# --------------------------
name = st.text_input("Name")

source = st.selectbox("From Station", stations)
destination = st.selectbox("To Station", stations)

no_tickets = st.number_input("Tickets", min_value=1, value=1)

st.write("Do you need a cab?")
cab_required = st.radio("", ["Yes", "No"], horizontal=True)

drop_location = ""
if cab_required == "Yes":
    drop_location = st.text_input("Enter Drop Location")

# --------------------------
# PRICE CALCULATION
# --------------------------
price_per_ticket = 30
total_amount = no_tickets * price_per_ticket
st.info(f"Total Amount : ₹{total_amount}")

# --------------------------
# BOOK BUTTON
# --------------------------
if st.button("Book"):
    if name.strip() == "":
        st.error("Please enter passenger name")
    elif source == destination:
        st.error("From and To stations cannot be same")
    elif cab_required == "Yes" and drop_location.strip() == "":
        st.error("Please enter drop location")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Cab Required: {cab_required}\n"
            f"Drop Location: {drop_location}\n"
            f"Total Amount: ₹{total_amount}"
        )

        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")

        st.success("Ticket Booked Successfully")

        st.subheader("Metro & Cab Details")
        st.write(f"Booking ID : {booking_id}")
        st.write(f"Passenger : {name}")
        st.write(f"From : {source}")
        st.write(f"To : {destination}")
        st.write(f"Tickets : {no_tickets}")
        st.write(f"Cab : {cab_required}")
        if cab_required == "Yes":
            st.write(f"Drop Location : {drop_location}")
        st.write(f"Amount Paid : ₹{total_amount}")

        st.image(buf.getvalue(), width=220)
