import streamlit as st
from billtracker import Bill_Type as bt
import datetime
import pandas as pd
import base64

# --- APP CUSTOMIZATION SECTION ---
# App titles
st.markdown("""
    <h1 style= 
    'text-align: center;'
    color: #90C383;
    ><strong><i>📜📌 Bill & Subscription Tracker</i></strong></h1>
            
    <style>
    position: sticky;
    top: 0;
    </style>
    """,
    unsafe_allow_html=True
    )


#Background
# Load and encode the image
image_path = "billtracker_wallpaper.jpeg"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Use st.markdown to set the background image via CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
        min-height: 100vh;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Injecting CSS for the theme - mostly green
st.markdown(
    """
    <style>
        /* Text Font - Sans-Serif */
        * {
            font-family: "Verdana", "Sans-Serif";
        }

        /* Use patterns over the gradient behind the text */
        .stApp::before, .stApp::after, {
            content: "";
            position: absolute;
            border-radius: 50%;
            background: #578C35; 
            pointer-events: auto;
            filter: drop-shadow(10px);
            z-index: 0;
            border-color: #FFFFFF;
        }

        /* Sidebar background - lighter than background */
        section[data-testid="stSidebar"] {
            border-right: 2px solid #8FC087;
            padding-top: 1rem;
        }

        /* --- BUTTONS --- */
        div.stButton > button {
            background-color: #191B18 ;
            color: #f0fff0 ;
            font-weight: bold;
            border-radius: 8px;
            border: 1px solid #FFFFFF ;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background-color: #4cb152;
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #76ca76;
            position: relative;
            z-index: 20;
        }

        /* General text */
        .stMarkdown, .stText {
            color: #e7ffe7;
            position: relative;
            z-index: 20;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Bill & Subscription Tracker",
    page_icon="📜📌",
    layout="centered"
)

# Session state to store bills between reruns
if "bills" not in st.session_state:
    st.session_state.bills = []


#Form for entering bills
with st.form("bill_form", clear_on_submit=True):
    st.subheader("➕ Add New Bill")
    bill_type = st.selectbox("Bill Type", ["Utility", "Subscription", "Loan", "Other"])
    bill_name = st.text_input("Bill Name (e.g., Internet, Netflix)",key="input_bill_name")
    service_name = st.text_input("Service Provider",key="input_service_name")


    total_amount_input = st.text_input("Total Amount of Bill (e.g., $100.00)",key="input_total_amount")
    amount_paid_input = st.text_input("Amount Paid (e.g., $25.00)",key="input_amount_paid")


    bill_date = st.date_input("Bill Date", value=datetime.date.today())
    deadline = st.date_input("Payment Deadline", value=datetime.date.today() + datetime.timedelta(days=7))
    bill_status = st.selectbox("Bill Status", ["Unpaid", "Paid", "Pending"])


    submitted = st.form_submit_button("➕Add Bill")

if submitted:
    try:
        # Convert user inputs into float values
        total_amount = float(total_amount_input.replace('$', '').replace(',', '').strip())
        amount_paid = float(amount_paid_input.replace('$', '').replace(',', '').strip())


        # Calculate remaining amount
        amount_due = total_amount - amount_paid
        if amount_due < 0:
            st.warning("⚠️ Amount paid is greater than total bill. Adjusting to $0 due.")
            st.toast('⚠️ Amount paid is greater than total bill')
            amount_due = 0.0


        # Create Bill_Type instance (you may want to extend the class to handle amount_paid too)
        new_bill = bt(
            bill_type=bill_type,
            bill_name=bill_name,
            service_name=service_name,
            amount=total_amount,
            bill_date=bill_date,
            bill_status=bill_status
        )


        # Store all relevant info
        bill_data = {
            "Type": new_bill.bill_type,
            "Name": new_bill.bill_type_name,
            "Service": new_bill.service_name,
            "Total Amount": new_bill.amount,
            "Amount Paid": amount_paid,
            "Amount Due": amount_due,
            "Bill Date": new_bill.bill_date,
            "Status": new_bill.bill_status,
            "Deadline": deadline
        }


        st.session_state.bills.append(bill_data)
        st.success("☑ Bill added successfully!")


    except ValueError:
        st.error(" Invalid amount format. Use currency like $100.00")

# Display Summary
if st.session_state.bills:
    st.subheader("📊 Payment Overview")

    df = pd.DataFrame(st.session_state.bills)

    # Calculate summary totals
    total_paid = df["Amount Paid"].sum()
    total_due = df["Amount Due"].sum()
    total_billed = df["Total Amount"].sum()

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Paid So Far", f"${total_paid:,.2f}")
    col2.metric("🧾 Still Due", f"${total_due:,.2f}")
    col3.metric("📈 Total Billed", f"${total_billed:,.2f}")
    st.subheader("📋 Bill List")

    # Define the column widths for the table
    col_widths = [2, 2, 2, 2, 2, 2, 1]

    # Render the header row
    header_cols = st.columns(col_widths)
    headers = ["Name", "Type", "Service", "Bill Date", "Amount Due", "Deadline"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    # Render each row with a delete button
    for idx, bill in enumerate(st.session_state.bills):
        row_cols = st.columns(col_widths)
        row_cols[0].write(bill["Name"])
        row_cols[1].write(bill["Type"])
        row_cols[2].write(bill["Service"])
        row_cols[3].write(str(bill["Bill Date"]))
        row_cols[4].write(f"${bill['Amount Due']:,.2f}")
        row_cols[5].write(str(bill["Deadline"]))
    
    
        if row_cols[6].button("🗑️", key=f"delete_{idx}"):
            st.session_state.bills.pop(idx)
            st.success("☑ Bill deleted successfully!")
            st.toast("☑ Bill deleted successfully!")
            st.rerun()

            


    #Deadline Notifications
    st.subheader("⚠🚨 Upcoming Deadlines")
    today = datetime.date.today()
    deadline_limit = today + datetime.timedelta(days=3)


    upcoming_df = df[
        (df["Deadline"] >= today) &
        (df["Deadline"] <= deadline_limit) &
        (df["Amount Due"] > 0)
    ]


    if not upcoming_df.empty:
        for i, row in upcoming_df.iterrows():
            st.warning(f"🔔 Payment for **{row['Name']}** is due on **{row['Deadline']}**. Amount Due: **${row['Amount Due']:,.2f}**")
    else:
        st.info("✅ No upcoming deadlines in the next 3 days.")

st.markdown(
    f"""
    <style>
    .bill_form{{
    background-color: #000000;
    border: 2px, #FFFFFF;
    border-radius: 4px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

