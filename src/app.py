import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Add the src directory to Python path
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from models.base import SessionLocal, engine
from models.models import Client, Cleaner, Job, Roster, Invoice, Payment, GSTType, PaymentMode, EmploymentType

st.set_page_config(
    page_title="Cleaning Business Management System",
    page_icon="🧹",
    layout="wide"
)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def main():
    st.title("Cleaning Business Management System")
    
    menu = ["Dashboard", "Clients", "Team", "Roster", "Invoices"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Dashboard":
        show_dashboard()
    elif choice == "Clients":
        show_clients()
    elif choice == "Team":
        show_team()
    elif choice == "Roster":
        show_roster()
    elif choice == "Invoices":
        show_invoices()

def show_dashboard():
    st.header("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Clients", "25")
    with col2:
        st.metric("Team Members", "10")
    with col3:
        st.metric("Weekly Jobs", "45")
    
    st.subheader("Upcoming Jobs")
    # Add upcoming jobs table here
    
    st.subheader("Recent Invoices")
    # Add recent invoices table here

def show_clients():
    st.header("Client Management")
    
    tab1, tab2 = st.tabs(["Client List", "Add New Client"])
    
    with tab1:
        db = get_db()
        clients = db.query(Client).all()
        if clients:
            client_data = []
            for client in clients:
                client_data.append({
                    "Name": client.name,
                    "Contact": client.contact,
                    "Frequency": client.frequency,
                    "GST Type": client.gst_type.value,
                    "Payment Mode": client.payment_mode.value
                })
            st.dataframe(pd.DataFrame(client_data))
    
    with tab2:
        with st.form("new_client_form"):
            name = st.text_input("Client Name")
            contact = st.text_input("Contact Number")
            address = st.text_area("Address")
            frequency = st.selectbox(
                "Cleaning Frequency",
                ["Weekly", "Fortnightly", "Monthly", "3-Monthly"]
            )
            gst_type = st.selectbox(
                "GST Type",
                [gt.value for gt in GSTType]
            )
            payment_mode = st.selectbox(
                "Payment Mode",
                [pm.value for pm in PaymentMode]
            )
            
            if st.form_submit_button("Add Client"):
                db = get_db()
                new_client = Client(
                    name=name,
                    contact=contact,
                    address=address,
                    frequency=frequency,
                    gst_type=GSTType(gst_type),
                    payment_mode=PaymentMode(payment_mode)
                )
                db.add(new_client)
                db.commit()
                st.success("Client added successfully!")

def show_team():
    st.header("Team Management")
    
    tab1, tab2 = st.tabs(["Team List", "Add Team Member"])
    
    with tab1:
        db = get_db()
        cleaners = db.query(Cleaner).all()
        if cleaners:
            cleaner_data = []
            for cleaner in cleaners:
                cleaner_data.append({
                    "Name": cleaner.name,
                    "Cost Rate": f"${cleaner.cost_rate:.2f}",
                    "Type": cleaner.employment_type.value
                })
            st.dataframe(pd.DataFrame(cleaner_data))
    
    with tab2:
        with st.form("new_team_member_form"):
            name = st.text_input("Name")
            cost_rate = st.number_input("Cost Rate ($/hour)", min_value=0.0)
            employment_type = st.selectbox(
                "Employment Type",
                [et.value for et in EmploymentType]
            )
            availability = st.multiselect(
                "Available Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            )
            
            if st.form_submit_button("Add Team Member"):
                db = get_db()
                new_cleaner = Cleaner(
                    name=name,
                    cost_rate=cost_rate,
                    employment_type=EmploymentType(employment_type),
                    availability=",".join(availability)
                )
                db.add(new_cleaner)
                db.commit()
                st.success("Team member added successfully!")

def show_roster():
    st.header("Roster Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Weekly Roster")
        # Add calendar view here
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Generate Next Week's Roster"):
            st.info("Generating roster...")
            # Add roster generation logic here

def show_invoices():
    st.header("Invoice Management")
    
    tab1, tab2 = st.tabs(["Invoice List", "Generate Invoice"])
    
    with tab1:
        db = get_db()
        invoices = db.query(Invoice).all()
        if invoices:
            invoice_data = []
            for invoice in invoices:
                invoice_data.append({
                    "Invoice #": invoice.id,
                    "Client": invoice.job.client.name,
                    "Amount": f"${invoice.amount:.2f}",
                    "GST": f"${invoice.gst:.2f}",
                    "Status": invoice.status
                })
            st.dataframe(pd.DataFrame(invoice_data))
    
    with tab2:
        st.info("Select a completed job to generate an invoice")
        # Add invoice generation form here

if __name__ == "__main__":
    main()
