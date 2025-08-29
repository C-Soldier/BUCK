# To import the streamlit module to use streamlit
import streamlit as st
# To import the billtracker class
from billtracker import Bill_Type as bt
# To import the datetime module
import datetime
# To import the pandas module for table
import pandas as pd
# To import the base64 module for streamlit user interface
import base64
# To be able to split the pdf text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
# To import the buck file to send the bill data to the chatbot
import buck

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
            color: #008000 ;
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
            color: #e7ffe7;
            position: relative;
            z-index: 20;
        }

        /* General text */
        .stMarkdown, .stText {
            color: #76ca76;
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





#This checks to see if “bills” is in the session, this will allow it to store the data the user entered even after reruns.
if "bills" not in st.session_state:
    st.session_state.bills = []




#The form for entering bills using streamlit’s input functions
with st.form("bill_form"):
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


#The line of code to allow users to enter new bills, the button is below the rest of the code


def clear_inputs():
    st.session_state.input_bill_name = ""
    st.session_state.input_service_name = ""
    st.session_state.input_total_amount = ""
    st.session_state.input_amount_paid = ""


if submitted:
    try:
        # Convert user inputs into float values
        total_amount = float(total_amount_input.replace('$', '').replace(',', '').strip())
        amount_paid = float(amount_paid_input.replace('$', '').replace(',', '').strip())




 #The code that will calculate remaining amount
        amount_due = total_amount - amount_paid
        if amount_due < 0:
            st.warning("⚠️ Amount paid is greater than total bill. Adjusting to $0 due.")
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


#The button to add new bills
st.button("**Make New Bill**", on_click=clear_inputs)
# Display Summary
if st.session_state.bills:
    st.subheader("📊 Payment Overview")


    df = pd.DataFrame(st.session_state.bills)


 #The code that will calculate summary totals
    total_paid = df["Amount Paid"].sum()
    total_due = df["Amount Due"].sum()
    total_billed = df["Total Amount"].sum()


    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Paid So Far", f"${total_paid:,.2f}")
    col2.metric("🧾 Still Due", f"${total_due:,.2f}")
    col3.metric("📈 Total Billed", f"${total_billed:,.2f}")
    st.subheader("📋 Bill List")


#The column widths for the table, instead of a normal dataframe so we can add the delete button
    col_widths = [2, 2, 2, 2, 2, 2, 1]


#Gives the title for the rows
    header_cols = st.columns(col_widths)
    headers = ["Name", "Type", "Service", "Bill Date", "Amount Due", "Deadline", ""]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")


#This loop allows us to put a delete button on the side of each bill
    for idx, bill in enumerate(st.session_state.bills):
        row_cols = st.columns(col_widths)
        row_cols[0].write(bill["Name"])
        row_cols[1].write(bill["Type"])
        row_cols[2].write(bill["Service"])
        row_cols[3].write(str(bill["Bill Date"]))
        row_cols[4].write(f"${bill['Amount Due']:,.2f}")
        row_cols[5].write(str(bill["Deadline"]))

        #Deletes the bill data at the exact row next to the delete clicked
        if row_cols[6].button("🗑", key=f"delete_{idx}"):
            st.session_state.bills.pop(idx)
            st.rerun()


           




 #The line of code that will display the Deadline Notifications 
    st.subheader("⚠🚨 Upcoming Deadlines")
    today = datetime.date.today()
    deadline_limit = today + datetime.timedelta(days=3)


#The condition it has to follow to display the upcoming deadlines
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
#Aaron Greene’s Work ദ്ദി ˉ͈̀꒳ˉ͈́ )✧

    if st.button("**Send Bills To Buck**"):
        try:
            bill_data = df.to_string(index=False)
            # To split the excel text into chunks of data
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(bill_data)
            # To join the chunks into a single string
            text = "\n".join(chunks)
            st.session_state.chats.append({'role': 'user', 'content': text})
            # To call the buck.py file and send the data to the chatbot
            chat = buck.askGemini(text, st.session_state.chat_session)
            # Display the response from the chatbot about the image
            st.chat_message("assistant", avatar=st.session_state.buck_avatar).markdown(chat)
            # To store the chatbot responses in the session state
            st.session_state.chats.append({'role': 'assistant', 'content': chat}) 
            st.success("✅ Bills sent to Buck successfully!")
        except Exception as e:
            st.error(f"Error sending bills to Buck: {e}")






