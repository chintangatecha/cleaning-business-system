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
from models.models import (Client, Cleaner, Job, Roster, Invoice, Payment,
    GSTType, PaymentMode, EmploymentType, MessageTemplate, MessageHistory)
from utils.messaging import MessageService
from datetime import datetime, timedelta

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
    
    menu = ["Dashboard", "Clients", "Team", "Roster", "Invoices", "Messaging"]
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
    elif choice == "Messaging":
        show_messaging()

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

def show_messaging():
    st.header("Messaging")
    
    # Initialize message service
    msg_service = MessageService()
    db = get_db()
    
    # Create tabs for different messaging functions
    tab1, tab2, tab3 = st.tabs(["Send Messages", "Message Templates", "Message History"])
    
    with tab1:
        # File uploader for CSV
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Verify required columns
                required_columns = ["Client Name", "Phone Number"]
                if not all(col in df.columns for col in required_columns):
                    st.error("CSV must contain columns: 'Client Name' and 'Phone Number'")
                else:
                    # Display trial account warning
                    st.warning("""
                    ⚠️ Important: You are using a Twilio trial account. You can only send messages to verified numbers.
                    Please verify your numbers at: https://www.twilio.com/user/account/phone-numbers/verified
                    Or upgrade your Twilio account to remove this restriction.
                    """)
                    
                    # Display the data
                    st.write("Preview of uploaded data:")
                    st.dataframe(df)
                    
                    # Template selection
                    templates = db.query(MessageTemplate).all()
                    template_names = ["Custom Message"] + [t.name for t in templates]
                    selected_template = st.selectbox("Select Message Template", template_names)
                    
                    if selected_template == "Custom Message":
                        message = st.text_area("Enter your message:", 
                            help="You can use {Client Name} as a placeholder that will be replaced with the actual client name")
                    else:
                        template = db.query(MessageTemplate).filter(MessageTemplate.name == selected_template).first()
                        message = template.content
                        
                        # Show preview with sample data
                        preview = message.replace("{Client Name}", "John Doe")
                        st.text_area("Message Preview (with sample data):", preview, disabled=True)
                        st.info("The actual message will use the client names from your CSV file.")
                    
                    # Scheduling options
                    schedule_msg = st.checkbox("Schedule Message")
                    scheduled_time = None
                    if schedule_msg:
                        scheduled_time = st.datetime_input(
                            "Schedule for",
                            value=datetime.now() + timedelta(hours=1),
                            min_value=datetime.now()
                        )
                    
                    # Send Message button
                    if st.button("Send Messages"):
                        if not message:
                            st.error("Please enter a message or select a template")
                        else:
                            # Prepare data and validate phone numbers
                            valid_entries = []
                            has_errors = False
                            
                            for index, row in df.iterrows():
                                try:
                                    phone = msg_service.format_phone_number(row["Phone Number"])
                                    valid_entries.append({
                                        "index": index,
                                        "client_name": row["Client Name"],
                                        "phone": phone
                                    })
                                except Exception as e:
                                    st.error(f"Invalid phone number for {row['Client Name']}: {str(e)}")
                                    has_errors = True
                            
                            if has_errors:
                                st.warning("Please fix the errors above and try again.")
                                return
                            
                            total_messages = len(valid_entries)
                            if total_messages == 0:
                                st.error("No valid entries found in the CSV file.")
                                return
                            
                            progress_bar = st.progress(0.0)
                            success_count = 0
                            
                            for i, entry in enumerate(valid_entries):
                                try:
                                    # Create message history record
                                    history = MessageHistory(
                                        client_name=entry["client_name"],
                                        phone_number=entry["phone"],
                                        message=message,
                                        scheduled_for=scheduled_time
                                    )
                                    
                                    if not scheduled_time:
                                        # Replace template variables
                                        personalized_message = message.replace("{Client Name}", entry["client_name"])
                                        
                                        # Send message immediately
                                        result = msg_service.send_message(entry["phone"], personalized_message)
                                        history.status = "success" if result["success"] else "failed"
                                        history.error = result.get("error")
                                        history.sent_at = datetime.utcnow() if result["success"] else None
                                        
                                        if result["success"]:
                                            success_count += 1
                                            st.success(f"Message sent to {entry['client_name']} ({entry['phone']})")
                                        else:
                                            st.error(f"Failed to send message to {entry['client_name']} ({entry['phone']}): {result.get('error')}")
                                    else:
                                        history.status = "scheduled"
                                        success_count += 1
                                    
                                    db.add(history)
                                    db.commit()
                                    
                                    # Update progress bar
                                    current_progress = float(i + 1) / float(total_messages)
                                    progress_bar.progress(current_progress)
                                except Exception as e:
                                    st.error(f"Error sending message to {entry['client_name']}: {str(e)}")
                                    continue
                            
                            # Show final status
                            if scheduled_time:
                                st.success(f"Successfully scheduled {success_count} out of {total_messages} messages for {scheduled_time}")
                            else:
                                st.success(f"Successfully sent {success_count} out of {total_messages} messages")
                            
                            if scheduled_time:
                                st.success(f"Messages scheduled for {scheduled_time}")
                            else:
                                st.success("Messages sent successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("Message Templates")
        
        # Add new template form
        with st.form("new_template"):
            template_name = st.text_input("Template Name")
            template_content = st.text_area("Template Content")
            
            if st.form_submit_button("Add Template"):
                if template_name and template_content:
                    template = MessageTemplate(name=template_name, content=template_content)
                    db.add(template)
                    db.commit()
                    st.success("Template added successfully!")
                else:
                    st.error("Please fill in all fields")
        
        # Display existing templates
        templates = db.query(MessageTemplate).all()
        if templates:
            for template in templates:
                with st.expander(f"Template: {template.name}"):
                    st.text_area("Content", template.content, disabled=True)
                    if st.button(f"Delete {template.name}"):
                        db.delete(template)
                        db.commit()
                        st.success("Template deleted!")
                        st.rerun()
    
    with tab3:
        st.subheader("Message History")
        
        # Display message history
        history = db.query(MessageHistory).order_by(MessageHistory.created_at.desc()).all()
        if history:
            history_data = []
            for h in history:
                history_data.append({
                    "Client": h.client_name,
                    "Phone": h.phone_number,
                    "Status": h.status,
                    "Scheduled For": h.scheduled_for,
                    "Sent At": h.sent_at,
                    "Error": h.error or ""
                })
            st.dataframe(pd.DataFrame(history_data))

if __name__ == "__main__":
    main()
